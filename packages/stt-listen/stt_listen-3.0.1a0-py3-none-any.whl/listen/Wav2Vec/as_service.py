# import torch
import json

from time import perf_counter

from fastapi import FastAPI, WebSocket, Response as FastAPIResponse

from listen.Wav2Vec.engine import Transcriber, Response, Error
from listen.Wav2Vec import utils
from listen.exception import NotAllowedToListenError

# torch.set_num_threads(1)

# Check if conf exist
CONFIG = utils.get_config_or_default()

is_allowed_to_listen = utils.is_allowed_to_listen(CONFIG)

if not is_allowed_to_listen:
    raise NotAllowedToListenError(utils.CONFIG_PATH)

# Load app configs and initialize a model
models_path = utils.get_loc_model_path()

print("Loading transcription model...")
transcriber = Transcriber(models_path=models_path)

print("Starting server...")
# create the FastAPI app
app = FastAPI()

@app.get("/")
async def healthcheck():
    return FastAPIResponse(content="Welcome to listen.sock: Transcription as a Service!", status_code=200)

@app.websocket("/api/v2/transcribe")
async def transcribe(websocket: WebSocket):
    print(f"Received WebSocket request at /api/v2/transcribe")
    # accept the websocket connection
    await websocket.accept()
    try:
        # receive audio data from the client as binary
        audio_data = await websocket.receive_bytes()
        
        inference_start = perf_counter()
        text, _ = transcriber.run(audio_data)
        inference_end = perf_counter() - inference_start

        print(f"Completed WebSocket request at /api/v2/transcribe in {inference_end} seconds")
        # send the transcription as json to the client
        await websocket.send_json(json.dumps(Response(text, inference_end).__dict__))
    except Exception as e:
        # raise e
        # send an error message if something goes wrong
        await websocket.send_json(json.dumps(Error(str(e)).__dict__))
    finally:
        # close the websocket connection
        await websocket.close()