import time
import torch
import msgpack
from drqa.model import DocReaderModel
from prepro import annotate, to_id, init
from train import BatchGen

cuda = torch.cuda.is_available()

if not cuda:
    raise Exception("CUDA not available!")

model_file = "models/best_model.pt"
checkpoint = torch.load(model_file)
print("---best_model.py loaded---")

state_dict = checkpoint['state_dict']

with open('SQuAD/meta.msgpack', 'rb') as f:
    meta = msgpack.load(f, encoding='utf8')
print("---meta.msgpack loaded---")
    
embedding = torch.Tensor(meta['embedding'])

opt = checkpoint['config']
opt['pretrained_words'] = True
opt['vocab_size'] = embedding.size(0)
opt['embedding_dim'] = embedding.size(1)
opt['pos_size'] = len(meta['vocab_tag'])
opt['ner_size'] = len(meta['vocab_ent'])
opt['cuda'] = cuda

BatchGen.pos_size = opt['pos_size']
BatchGen.ner_size = opt['ner_size']
model = DocReaderModel(opt, embedding, state_dict)
print("---DocReaderModel initialized---")

w2id = {w: i for i, w in enumerate(meta['vocab'])}
tag2id = {w: i for i, w in enumerate(meta['vocab_tag'])}
ent2id = {w: i for i, w in enumerate(meta['vocab_ent'])}
init()
print("---spacy nlp loaded---")


def predict(evidence, question):
    dummy_placeholder = 0

    annotated = annotate((dummy_placeholder, evidence, question), meta['wv_cased'])
    model_in = to_id(annotated, w2id, tag2id, ent2id)
    model_in = next(iter(BatchGen([model_in], batch_size=1, gpu=cuda, evaluation=True)))
    prediction = model.predict(model_in)[0]

    return prediction


# def main():
#     evidence_list = []
#     question_list = []

#     evidence_list.append("Super Bowl 50 was an American football game to determine the champion of the National Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion Denver Broncos defeated the National Football Conference (NFC) champion Carolina Panthers 24-10 to earn their third Super Bowl title. The game was played on February 7, 2016, at Levi's Stadium in the San Francisco Bay Area at Santa Clara, California.")
#     evidence_list.append("Beanie style with simple design. So cool to wear and make you different. It wears as peak cap and a fashion cap. It is good to match your clothes well during party and holiday, also makes you charming and fashion, leisure and fashion in public and streets. It suits all adults, for men or women. Matches well with your winter outfits so you stay warm all winter long.")
#     evidence_list.append("Question Answering (QA) is a computer science discipline within the fields of information retrieval and natural language processing (NLP), which is concerned with building systems that automatically answer questions posed by humans in a natural language.")

#     question_list.append("What day was the game played on?")
#     question_list.append("Is it for women?")
#     question_list.append("What is question answering?")

#     for i in range(len(evidence_list)):
#         try:
#             evidence = evidence_list[i]
#             question = question_list[i]
#             start_time = time.time()

#             annotated = annotate((dummy_placeholder, evidence, question), meta['wv_cased'])
#             model_in = to_id(annotated, w2id, tag2id, ent2id)
#             model_in = next(iter(BatchGen([model_in], batch_size=1, gpu=cuda, evaluation=True)))
#             prediction = model.predict(model_in)[0]

#             end_time = time.time()
#             print('Answer: {}'.format(prediction))
#             print('Time: {:.4f}s'.format(end_time - start_time))
#         except Exception as e:
#             print(e)

# if __name__ == "__main__":
#     main()