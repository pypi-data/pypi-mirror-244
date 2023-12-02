import json
import websockets # not websocket!!!
from listen.Wav2Vec.utils import get_config_or_default

HOST, PORT = "0.0.0.0", "5063"
CONFIG = get_config_or_default()

if CONFIG.get('service'):
    HOST = CONFIG['service'].get('host', None)
    PORT = CONFIG['service'].get('port', None)

async def stt(audio_bin: bytes, host=HOST, port=PORT):
    async with websockets.connect(f"ws://{host}:{port}/api/v2/transcribe") as ws:
        try:
            await ws.send(audio_bin)
            response = await ws.recv()
            r = json.loads(json.loads(response)) # double json.loads to convert from string to dict
            # This is a wierd behavior. It should be investigated and fixed.
            if r.get('message'):
                return r.get('message')
            elif r.get('text'):
                return r.get('text')
        except Exception as e:
            raise e
        finally:
            await ws.close()