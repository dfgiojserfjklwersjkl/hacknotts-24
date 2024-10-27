import os
import queue
import re
import sys
import time

import pyaudio
from dotenv import load_dotenv
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech as cloud_speech_types
from inputimeout import TimeoutOccurred, inputimeout

from config import Config
from stream import ResumableMicrophoneStream

load_dotenv()

STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = Config.get("input")["sample_rate"] or 44100
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"


def get_current_time() -> int:
    return int(round(time.time() * 1000))


def listen(
    stream_file: str,
) -> cloud_speech_types.StreamingRecognizeResponse:
    # Instantiates a client
    client = SpeechClient()

    # use microphone
    mic_manager = ResumableMicrophoneStream(
        rate=SAMPLE_RATE,
        chunk_size=CHUNK_SIZE,
        device_index=device_index,
    )

    with mic_manager as stream:
        while not stream.closed:

            stream.audio_input = []
            audio_generator = stream.generator()

            audio_requests = (
                cloud_speech_types.StreamingRecognizeRequest(audio=audio) for audio in audio_generator
            )

            recognition_config = cloud_speech_types.RecognitionConfig(
                auto_decoding_config=cloud_speech_types.AutoDetectDecodingConfig(),
                language_codes=["en-US"],
                model="long",
            )
            streaming_config = cloud_speech_types.StreamingRecognitionConfig(
                config=recognition_config
            )
            config_request = cloud_speech_types.StreamingRecognizeRequest(
                recognizer=f"projects/nineyrold/locations/global/recognizers/_",
                streaming_config=streaming_config,
            )

            def requests(config: cloud_speech_types.RecognitionConfig, audio: list):
                yield config
                yield from audio

            # Transcribes the audio into text
            responses_iterator = client.streaming_recognize(
                requests=requests(config_request, audio_requests)
            )
            responses = []
            for response in responses_iterator:
                responses.append(response)
                for result in response.results:
                    print(f"Transcript: {result.alternatives[0].transcript}")

            return responses


if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-api-key.json'
    pya = pyaudio.PyAudio()
    device_index = next((i for i in range(pya.get_device_count())
                        if pya.get_device_info_by_index(i)['name'] == 'pulse'), None)
    if device_index is None:
        print("No matching device found")
        exit()
