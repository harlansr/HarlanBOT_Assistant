#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from email import message
from email.mime import audio
from tkinter.tix import NoteBook
from typing import Mapping
from unittest import case
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import os
import webbrowser
import ExtraScript as es


NAME = "stela"
recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)


def train_model():
    eScript.train_now()
    assistant = GenericAssistant('intents.json', intent_methods=mappings, model_name=NAME)
    assistant.load_model('model/model')


cScript = es.CommandScript(speaker, recognizer)

mappings = {
    "ask_openai": cScript.ask_openai,
    "ss_face": cScript.ss_face,
    "find_face": cScript.find_face,
    "train_model": train_model,
    "create_note": cScript.create_note,
    "add_todo": cScript.add_todo,
    "show_todos": cScript.show_todos,
    "pc_shutdown": cScript.pc_shutdown,
    "pc_restart": cScript.pc_restart,
    "restart_script": cScript.restart_script,
    "exit": cScript.quit
}

assistant = GenericAssistant('intents.json', intent_methods=mappings, model_name=NAME)

eScript = es.extraScript(assistant, speaker, recognizer)

# eScript.train_now()
if not os.path.isdir('./model'):
    train_model()
assistant.load_model('model/model')

print("-------------------------------")
print("Ready to serve!")
print("-------------------------------")

##########################################################################################

speaker.say("Ready to serve")
speaker.runAndWait()

##########################################################################################

# for voice in voices:
#     print(f"voice: {voice}")
#
# speaker.say("Test percobaan suara, apakah bisa berbahasa indonesia")
# speaker.runAndWait()

##########################################################################################


def run():
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            message = recognizer.recognize_google(audio)
            message = message.lower()

        print(f"You said: {message}")
        split_message = message.split(" about ")
        respon = assistant.request(split_message[0])
        if respon:
            answer = None
            if len(split_message) > 1:
                answer = split_message[1]
            if respon.startswith("open:"):
                query = respon[len("open:"):]
                eScript.open_app(query)
            elif respon.startswith("search:"):
                query = respon[len("search:"):]
                cScript.search_web(query, answer)
            else:
                cScript.answer(respon)
        # else:
        #     if message.startswith("pleace open "):
        #         cScript.open_manual(message[len("pleace open "):])

    except speech_recognition.UnknownValueError:
        pass


while True:
    run()

# -------------------------------------------------------------
# NoteBook
# install :
# * pip install speechrecognition
# * pip install pyttsx3
# * pip install neuralintents

# How to install pyaudio in windows
# pip install pipwin
# pipwin install pyaudio

# Keyy
# https://win32com.goermezer.de/microsoft/windows/controlling-applications-via-sendkeys.html
# https://github.com/asweigart/pyautogui