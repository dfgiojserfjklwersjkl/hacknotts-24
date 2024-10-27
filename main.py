import os

import pyaudio

import stt
from config import Config
from interview import Interview

if __name__ == "__main__":

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-api-key.json'

    interview_context = Config.get("interview_context")

    interview = Interview(interview_context)

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

    while True:
        question = stt.main(lang, device_index)

        answer = interview.ask(question)
        print(f"{question}\n\nAns:\n {answer}\n======")

        input("Press Enter to for the next question...")
