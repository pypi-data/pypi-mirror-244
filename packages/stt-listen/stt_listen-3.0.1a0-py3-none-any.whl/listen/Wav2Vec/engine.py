import os
import glob
import io
import logging
import torch, torchaudio

import numpy as np
from transformers import AutoModelForCTC, Wav2Vec2ProcessorWithLM
from timeit import default_timer as timer
from deepmultilingualpunctuation import PunctuationModel

from listen.Wav2Vec import audio, utils

cuda_device = os.environ.get("ASR_GPU_ID", "0")
device = torch.device(f"cuda:{cuda_device}" if torch.cuda.is_available() else "cpu")

'''
Load the pre-trained model into the memory
@param models: Path or name of the Wav2Vec2.0 models with CTC to load.
@Retval
Returns a list [Model, Scorer, Model Load Time, Scorer Load Time]
'''
def load_model(model_id, ):
    logging.info(f"Loading {model_id}")
    model_load_start = timer()
    model = AutoModelForCTC.from_pretrained(model_id).to(device)
    model_load_end = timer() - model_load_start
    logging.debug("Loaded accoustic model in %0.3fs." % (model_load_end))

    scorer_load_start = timer()
    scorer = Wav2Vec2ProcessorWithLM.from_pretrained(model_id)
    scorer_load_end = timer() - scorer_load_start
    logging.debug('Loaded scorer (language model) in %0.3fs.' % (scorer_load_end))

    return [model, scorer, model_load_end, scorer_load_end]

'''
Resolve directory path for the models and fetch each of them.
@param dirName: Path to the directory containing pre-trained models
@Retval:
Returns the model dirName
'''
def resolve_models(dirName):
    return dirName

class Transcriber:

    def __init__(self, models_path):
        #abs_models_path = os.path.expanduser(models_path)
        model_id = resolve_models(models_path)
        self.model, self.scorer, _, _  = load_model(model_id)
        self.punct_model = PunctuationModel(model="oliverguhr/fullstop-punctuation-multilingual-sonar-base")
        self.sample_rate = self.scorer.feature_extractor.sampling_rate
    
    def punctuate(self, sentence: str):
        return self.punct_model.restore_punctuation(sentence).capitalize()

    def _transcribe(self, audio_bin):
        #Tokenize
        input_values = self.scorer(audio_bin, sampleing_rate=self.sample_rate, return_tensors="pt").input_values.to(device)
        #Take logits
        with torch.inference_mode():
            logits = self.model(input_values).logits
        #Take argmax
        #predicted_ids = torch.argmax(logits, dim=-1)
        #Get the words from predicted word ids
        transcription = self.scorer.batch_decode(logits.cpu().numpy()).text[0]
        #Output is all upper case
        return transcription.lower().capitalize()

    '''
    Run Inference on input audio
    @param audio: Input audio for running inference on
    @param fs: Sample rate of the input audio file
    @Retval:
    Returns a list [Inference, Inference Time]
    '''
    def transcribe(self, audio_bin, fs):
        inference_time = 0.0
        audio_length = len(audio_bin) * (1 / fs)

         

        # Run STT
        logging.debug('Running inference...')
        inference_start = timer()
        output = self._transcribe(audio_bin)
        inference_end = timer() - inference_start
        inference_time += inference_end
        logging.debug('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))
        if output:
            logging.debug('Punctuating sentence...')
            inference_start = timer()
            output = self.punctuate(output)
            inference_end = timer() - inference_start
            inference_time += inference_end
            logging.debug('Punctuation took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))
        logging.debug(f'Inference: {output}')
        
        return [output, inference_time]

    '''
    Takes audio_bin as input and returns the transcription
    @param audio_bin: Input audio for running inference on
    @Retval:
    Returns the transcription

    Audio is expected to be in the format of a 16-bit signed integer, i.e. 2 bytes per sample.
    '''
    def run(self, audio_bin: bytes):
        #audio_data = np.frombuffer(audio_bin, np.int16)
        audio_data = torch.frombuffer(audio_bin, dtype=torch.int16).to(dtype=torch.float32)
        # waveform, sample_rate = torchaudio.load(audio_data)
        return self.transcribe(audio_data, self.sample_rate)

class Response:  
    def __init__(self, text, time):
        self.text = text
        self.time = time

class Error:
    def __init__(self, message):
        self.message = message