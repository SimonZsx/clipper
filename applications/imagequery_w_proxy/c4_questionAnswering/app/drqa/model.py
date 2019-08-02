# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
import random
import torch
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import logging

from torch.autograd import Variable
from .utils import AverageMeter
from .rnn_reader import RnnDocReader

# Modification:
#   - X change the logger name
#   - X save & load "state_dict"s of optimizer and loss meter. Official doc: https://pytorch.org/tutorials/beginner/saving_loading_models.html
#   - save all random seeds
#   - change the dimension of inputs (for POS and NER features)
#   - remove "reset parameters" and use a gradient hook for gradient masking
# Origin: https://github.com/facebookresearch/ParlAI/tree/master/parlai/agents/drqa

logger = logging.getLogger(__name__)
# About logger and __name__: https://realpython.com/python-logging/#the-logging-module
# Logger class, which are instantiated using the module-level function logging.getLogger(name). 
# Multiple calls to getLogger() with the same name will return a reference to the same Logger object, 
# which saves us from passing the logger objects.

# “It is recommended that we use module-level loggers by passing __name__ as the name parameter to getLogger() 
# to create a logger object as the name of the logger itself would tell us from where the events are being logged. 
# __name__ is a special built-in variable in Python which evaluates to the name of the current module.”

class DocReaderModel(object):
    """High level model that handles intializing the underlying network
    architecture, saving, updating examples, and predicting examples.
    """

    def __init__(self, opt, embedding=None, state_dict=None):
        # Book-keeping.
        # YY: For continue with paused training

        # print("{}: opt = {}".format(self.__class__.__name__, opt))
        # Output:
        # {'question_merge': 'self_attn', 'use_qemb': True, 'ner': True, 'epochs': 40, 'pretrained_words': True, 
        # 'learning_rate': 0.1, 'optimizer': 'adamax', 'embedding_dim': 300, 'rnn_padding': False, 
        # 'grad_clipping': 10, 'doc_layers': 3, 'momentum': 0, 'batch_size': 32, 'max_len': 15, 
        # 'dropout_rnn_output': True, 'cuda': True, 'pos': True, 'dropout_rnn': 0.4, 'concat_rnn_layers': True,
        # 'pos_size': 50, 'save_last_only': False, 'reduce_lr': 0.0, 'hidden_size': 128, 'seed': 1013, 
        # 'model_dir': '/home/ubuntu/DrQA/models', 'weight_decay': 0, 'tune_partial': 1000, 
        # 'vocab_size': 91187, 'data_file': 'SQuAD/data.msgpack', 'question_layers': 3, 'resume': '', 
        # 'num_features': 4, 'fix_embeddings': False, 'ner_size': 19, 'save_dawn_logs': False, 'dropout_emb': 0.4, 
        # 'log_per_updates': 3, 'resume_options': False, 'rnn_type': 'lstm'}

        self.opt = opt
        self.device = torch.cuda.current_device() if opt['cuda'] else torch.device('cpu')
        self.updates = state_dict['updates'] if state_dict else 0

        self.train_loss = AverageMeter()
        # This training loss is only used for displaying real time training
        # progress. The evidence is that: when initializing the optimizer, 
        # the parameter passed in is not the train_loss, but the paramters.
        # The actual loss, used for backward propogation and call backward()
        # during each iteration is called *loss*. 
        # from the network. 

        if state_dict:
            self.train_loss.load(state_dict['loss'])

        # Building network.
        self.network = RnnDocReader(opt, embedding=embedding)
        if state_dict:
            new_state = set(self.network.state_dict().keys())
            for k in list(state_dict['network'].keys()):
                if k not in new_state:
                    del state_dict['network'][k]
            self.network.load_state_dict(state_dict['network'])
        self.network.to(self.device)

        # Building optimizer.
        self.opt_state_dict = state_dict['optimizer'] if state_dict else None
        self.build_optimizer()

    def build_optimizer(self):
        parameters = [p for p in self.network.parameters() if p.requires_grad]
        if self.opt['optimizer'] == 'sgd':
            self.optimizer = optim.SGD(parameters, self.opt['learning_rate'],
                                       momentum=self.opt['momentum'],
                                       weight_decay=self.opt['weight_decay'])
        elif self.opt['optimizer'] == 'adamax':
            self.optimizer = optim.Adamax(parameters,
                                          weight_decay=self.opt['weight_decay'])
        else:
            raise RuntimeError('Unsupported optimizer: %s' % self.opt['optimizer'])

        if self.opt_state_dict:
            self.optimizer.load_state_dict(self.opt_state_dict)

    def update(self, ex):
        """Forward a batch of examples; step the optimizer to update weights."""

        # Switch to Train mode
        self.network.train() 

        # Transfer to GPU 
        # YY: Reason for difference from the original source code
        # 1. The code here adds 2 more features: POS and NER. 
        # Thus the dimension changes. 
        # 2. We are predicting the starting and ending point 
        # in the paragraph, thus we have 2 outputs: target_start and target_end.
        # Args:
        # target_s: target starting index
        # target_e: target ending index
        # score_s: predicted starting index
        # score_e: predicted ending index
        #
        # Can use size of *ex* to replace hard-coded value
        inputs = [e.to(self.device) for e in ex[:7]] 
        # from 0 to 6, the *slice operation* is left-inclusive interval
        target_s = ex[7].to(self.device)
        target_e = ex[8].to(self.device)

        # Run forward
        score_s, score_e = self.network(*inputs)

        # Compute loss and accuracies
        loss = F.nll_loss(score_s, target_s) + F.nll_loss(score_e, target_e)
        self.train_loss.update(loss.item())

        # Clear gradients and run backward
        self.optimizer.zero_grad()
        loss.backward()

        # Clip gradients
        torch.nn.utils.clip_grad_norm_(self.network.parameters(), self.opt['grad_clipping'])

        # Update parameters
        self.optimizer.step()
        self.updates += 1

    def predict(self, ex):
        # Switch to evaluation mode
        self.network.eval() 

        # Transfer to GPU
        if self.opt['cuda']:
            inputs = [Variable(e.cuda()) for e in ex[:7]]
        else:
            inputs = [Variable(e) for e in ex[:7]]

        # Run forward
        with torch.no_grad():
            score_s, score_e = self.network(*inputs)

        # Transfer to CPU/normal tensors for numpy ops
        score_s = score_s.data.cpu()
        score_e = score_e.data.cpu()

        # Get argmax text spans
        text = ex[-2]
        spans = ex[-1]
        predictions = []
        max_len = self.opt['max_len'] or score_s.size(1)

        # print("{}: score_s = {}".format(self.__class__.__name__, score_s))

        for i in range(score_s.size(0)):
            scores = torch.ger(score_s[i], score_e[i])
            # https://pytorch.org/docs/stable/torch.html?highlight=torch%20ger#torch.ger
            # torch.ger(vec1, vec2, out=None) -> Tensor
            # Outer product of vec1 and vec2. If vec1 is a vector of size n and vec2 is a vector of size m, 
            # then out must be a matrix of size (n×m)

            scores.triu_().tril_(max_len - 1)
            # triu_(k=0) -> Tensor: In-place version of triu()
            # Returns the upper triangular part of a matrix (2-D tensor) or batch of matrices input, 
            # the other elements of the result tensor out are set to 0.
            # The upper triangular part of the matrix is defined as the elements on and above the diagonal.
            # https://pytorch.org/docs/stable/tensors.html
            # https://pytorch.org/docs/stable/torch.html#torch.tril
            scores = scores.numpy()
            s_idx, e_idx = np.unravel_index(np.argmax(scores), scores.shape)
            s_offset, e_offset = spans[i][s_idx][0], spans[i][e_idx][1]
            predictions.append(text[i][s_offset:e_offset])

        # print("{}: predictions = {}".format(self.__class__.__name__, predictions))
        return predictions

    def save(self, filename, epoch, scores):
        em, f1, best_eval = scores
        params = {
            'state_dict': {
                'network': self.network.state_dict(),
                'optimizer': self.optimizer.state_dict(),
                'updates': self.updates,
                'loss': self.train_loss.state_dict()
            },
            'config': self.opt,
            'epoch': epoch,
            'em': em,
            'f1': f1,
            'best_eval': best_eval,
            'random_state': random.getstate(),
            'torch_state': torch.random.get_rng_state(),
            'torch_cuda_state': torch.cuda.get_rng_state()
        }
        try:
            torch.save(params, filename)
            print('model saved to {}'.format(filename))
        except BaseException:
            logger.warning('[ WARN: Saving failed... continuing anyway. ]')
