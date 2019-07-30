from __future__ import absolute_import, division, print_function

import numpy as np
import shlex
import subprocess
import sys
import wave
import os

from deepspeech import Model, printVersions
from timeit import default_timer as timer

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

# Define the sample rate for audio
SAMPLE_RATE = 16000
BEAM_WIDTH = 500
LM_ALPHA = 0.75
LM_BETA = 1.85

# Model related constants
# Number of MFCC features to use
N_FEATURES = 26
# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9


def convert_samplerate(audio_path):
    sox_cmd = "sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - ".format(quote(audio_path), SAMPLE_RATE)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use {}hz files or install it: {}'.format(SAMPLE_RATE, e.strerror))
        # sudo apt-get install sox

    return SAMPLE_RATE, np.frombuffer(output, np.int16)


def load_model( model_dir="../models/",
                model="output_graph.pb", 
                alphabet="alphabet.txt", 
                lm="lm.binary", 
                trie="trie"):
    model = model_dir + model
    alphabet = model_dir + alphabet
    lm = model_dir + lm
    trie = model_dir + trie

    global ds

    print('Loading model from file {}'.format(model), file=sys.stderr)
    model_load_start = timer()
    ds = Model(model, N_FEATURES, N_CONTEXT, alphabet, BEAM_WIDTH)
    model_load_end = timer() - model_load_start
    print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)

    if lm and trie:
        print('Loading language model from files {} {}'.format(lm, trie), file=sys.stderr)
        lm_load_start = timer()
        ds.enableDecoderWithLM(alphabet, lm, trie, LM_ALPHA, LM_BETA)
        lm_load_end = timer() - lm_load_start
        print('Loaded language model in {:.3}s.'.format(lm_load_end), file=sys.stderr)


def infer(audio):
    # read audio
    fin = wave.open(audio, 'rb')
    fs = fin.getframerate()
    if fs != SAMPLE_RATE:
        print('Warning: original sample rate ({}) is different than {}hz. Resampling might cause bad recognition.'.format(fs, SAMPLE_RATE), file=sys.stderr)
        fs, audio = convert_samplerate(audio)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1/SAMPLE_RATE)
    fin.close()

    # run infer
    print('Running inference.')
    inference_start = timer()
    result = ds.stt(audio, fs)
    print(result)
    inference_end = timer() - inference_start
    print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)
    return result


def predict(audio):
    res = infer(audio)
    return res


# the DeepSpeech Model
ds = None
load_model()

def main():
    for i in range(3):
        predict("../dataset3/recordings/" + str(i) + ".wav")
    

if __name__ == '__main__':
    main()
