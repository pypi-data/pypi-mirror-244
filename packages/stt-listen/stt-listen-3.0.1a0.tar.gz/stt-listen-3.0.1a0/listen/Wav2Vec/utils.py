import os
import re
# import json
import toml
import logging
import threading
import requests

from pathlib import Path
# from urllib import request
from time import sleep
# from typing import List, Optional, Dict

from listen import CONFIG_PATH, I18N

logging.basicConfig(level=logging.INFO)

# custom exception hook
def custom_hook(args):
    # report the failure
    logging.error(f'Thread failed: {args.exc_value}')

# set the exception hook
threading.excepthook = custom_hook

def get_config_or_default():
    # Check if conf exist

    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as cfg:
            CONFIG = toml.loads(cfg.read())
    else:        
        CONFIG = {
            'service': {
                'host': '0.0.0.0',
                'port': '5063',
                'n_proc': 2
            },
            'stt': {
                'is_allowed': False
            }
        }
        if not os.path.isdir(os.path.dirname(CONFIG_PATH)):
            os.makedirs(os.path.dirname(CONFIG_PATH))
        with open(CONFIG_PATH, 'w') as f:
            f.write(toml.dumps(CONFIG))
    
    return CONFIG

def is_allowed_to_listen(conf=get_config_or_default()):
    _stt_conf = conf.get('stt', False)
    if _stt_conf:
        return _stt_conf.get('is_allowed', False)
    return False

def get_best_model(lang):
    # Define the hub API endpoint URL
    url = "https://huggingface.co/api/models"

    # Define the request parameters
    params = {
        "search": "wav2vec2",
        "filter": lang,
        "sort": "downloads",
        # "full": "full",
    }

    # Send the request and get the response
    response = requests.get(url, params=params)

    # Check the response status
    if response.status_code == 200:
        # Convert the response to JSON
        data = response.json()

        # Extract the list of models
        models = data
        # Check if the list is empty
        if not models:
            # Display an error message
            logging.warning(f"No models found for language {lang}")
            return None
        else:
            # Filter the models that have performance metrics
            models_with_metrics = [model for model in models]
            # Check if the list is empty
            if not models_with_metrics:
                # Fallback on likes
                logging.warning(f"No models where found for language {lang}.")
                logging.info(f"Using likes as criteria")
                # Sort the list of models in descending order of likes and select the first element
                models = sorted(models, key=lambda x: x["likes"], reverse=True)
                best_model = models[0]
            else:
                # Use the performance metrics as criteria
                logging.info(f"Using models self-reported WER and CER as criteria")
                # Define a function that calculates the score of a model from its metrics
                def get_score(model):
                    model_id = model.get('modelId')
                    response = requests.get(f"{url}/{model_id}")
                    data = response.json()

                    mi = data.get('model-index')
                    if mi:
                        # Extract the results of the model
                        wer = cer = 1
                        for _mi in mi:
                            if _mi != "error":
                                results = _mi.get('results', [])
                                for r in results:
                                    metrics = r.get('metrics', [])
                                    # Extract the WER and CER of the model, if they exist, otherwise use a default value
                                    for _m in metrics:
                                        # print(_m)
                                        t, v = _m.get('type'), _m.get('value') if type(_m.get('value')) == float else 1
                                        if t == 'wer':
                                            # print(f'WER: {v}')
                                            wer = v if wer >= 1 else float((wer+v)/2)
                                        if t == 'cer':
                                            # print(f'CER: {v}')
                                            cer = v if cer >= 1 else float((cer+v)/2)
                        # Calculate the score of the model as the inverse of the product of WER and CER
                        print(f"{model_id}: {wer=} {cer=}")
                        score = 1 / (wer * cer)
                        sleep(0.5)
                        return score
                    else:
                        return 1

                # Sort the list of models in descending order of score and select the first element
                logging.info("Computing models scores based on reported mertrics...")
                models_with_metrics = sorted(models_with_metrics, key=get_score, reverse=True)
                best_model = models_with_metrics[0]

            # Return the name of the best model found
            logging.info(f"Using {best_model.get('modelId', '')} ({best_model.get('likes', 'N/A')} ♥️ ).")
            return best_model["modelId"]
    else:
        # Display an error message
        logging.warning(f"Request has failed with code {response.status_code}")
        return None

def get_loc_model_path(language=None):
    """
    Get localised model path.
    Returns the path or name to the Wav2Vec2 model of the choosen language.
    [Default] language: System language
    """
    return os.environ.get('ASR_MODEL_ID') or get_best_model(language or I18N)

def get_available_cpu_count():
    """Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program
    See this https://stackoverflow.com/a/1006301/13561390"""

    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        m = re.search(r"(?m)^Cpus_allowed:\s*(.*)$", open("/proc/self/status").read())
        if m:
            res = bin(int(m.group(1).replace(",", ""), 16)).count("1")
            if res > 0:
                return res
    except IOError:
        pass

    # Python 2.6+
    try:
        import multiprocessing

        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # https://github.com/giampaolo/psutil
    try:
        import psutil

        return psutil.cpu_count()  # psutil.NUM_CPUS on old versions
    except (ImportError, AttributeError):
        pass

    # POSIX
    try:
        res = int(os.sysconf("SC_NPROCESSORS_ONLN"))

        if res > 0:
            return res
    except (AttributeError, ValueError):
        pass

    # Windows
    try:
        res = int(os.environ["NUMBER_OF_PROCESSORS"])

        if res > 0:
            return res
    except (KeyError, ValueError):
        pass

    # jython
    try:
        from java.lang import Runtime

        runtime = Runtime.getRuntime()
        res = runtime.availableProcessors()
        if res > 0:
            return res
    except ImportError:
        pass

    # BSD
    try:
        sysctl = subprocess.Popen(["sysctl", "-n", "hw.ncpu"], stdout=subprocess.PIPE)
        scStdout = sysctl.communicate()[0]
        res = int(scStdout)

        if res > 0:
            return res
    except (OSError, ValueError):
        pass

    # Linux
    try:
        res = open("/proc/cpuinfo").read().count("processor\t:")

        if res > 0:
            return res
    except IOError:
        pass

    # Solaris
    try:
        pseudoDevices = os.listdir("/devices/pseudo/")
        res = 0
        for pd in pseudoDevices:
            if re.match(r"^cpuid@[0-9]+$", pd):
                res += 1

        if res > 0:
            return res
    except OSError:
        pass

    # Other UNIXes (heuristic)
    try:
        try:
            dmesg = open("/var/run/dmesg.boot").read()
        except IOError:
            dmesgProcess = subprocess.Popen(["dmesg"], stdout=subprocess.PIPE)
            dmesg = dmesgProcess.communicate()[0]

        res = 0
        while "\ncpu" + str(res) + ":" in dmesg:
            res += 1

        if res > 0:
            return res
    except OSError:
        pass

    raise Exception("Can not determine number of CPUs on this system")

