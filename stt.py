
import os
import re
import sys

import pyaudio
from dotenv import load_dotenv
from google.cloud import speech
from inputimeout import inputimeout
from inputimeout.inputimeout import TimeoutOccurred

from config import Config
from stream import ResumableMicrophoneStream

load_dotenv()

# Audio recording parameters
SAMPLE_RATE = Config.get("input")["sample_rate"] or 44100
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"


def listen_print_loop(responses, stream) -> str:
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.

    Arg:
        responses: The responses returned from the API.
        stream: The audio stream to be processed.
    """
    sentences = [""]

    for response in responses:

        if not response.results:
            continue

        result = response.results[0]

        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        result_seconds = 0
        result_micros = 0

        if result.result_end_time.seconds:
            result_seconds = result.result_end_time.seconds

        if result.result_end_time.microseconds:
            result_micros = result.result_end_time.microseconds

        stream.result_end_time = int(
            (result_seconds * 1000) + (result_micros / 1000))

        corrected_time = stream.corrected_time()

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.

        if result.is_final:
            sys.stdout.write(transcript + "\n")

            sentences[-1] = transcript
            sentences.append("")

            stream.is_final_end_time = stream.result_end_time
            stream.last_transcript_was_final = True

        else:
            sys.stdout.write(transcript + "\r")
            sentences[-1] = transcript
            stream.last_transcript_was_final = False

        try:
            inputimeout(prompt='', timeout=0.1)
            return ''.join(sentences)

        except TimeoutOccurred as e:
            pass

    return ""


def main(language: str, device_index: int) -> str:
    """start bidirectional streaming from microphone input to speech API"""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code=language,
        max_alternatives=1,
        profanity_filter=False,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    mic_manager = ResumableMicrophoneStream(
        SAMPLE_RATE, CHUNK_SIZE, device_index)
    print(mic_manager.chunk_size)
    sys.stdout.write(YELLOW)
    sys.stdout.write('\nListening, say "Quit" or "Exit" to stop.\n\n')
    sys.stdout.write("End (ms)       Transcript Results/Status\n")
    sys.stdout.write("=====================================================\n")

    transcript_output = ''

    with mic_manager as stream:
        while not stream.closed:
            sys.stdout.write(YELLOW)
            sys.stdout.write(
                "\n" + str("NEW REQUEST\n")
            )

            stream.audio_input = []
            audio_generator = stream.generator()

            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            transcript_output = listen_print_loop(responses, stream)

            print(transcript_output)

            return transcript_output

        else:
            return ""


if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-api-key.json'

    pya = pyaudio.PyAudio()
    info = pya.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    device_index = None
    print("Available devices:\n")
    for i in range(pya.get_device_count()):
        devinfo = pya.get_device_info_by_index(i)
        if devinfo['name'] == 'pulse':
            device_index = i
            break
    lang = "en-US"
    if device_index is None:
        print("No matching device found")
        exit()
    main(lang, device_index)
