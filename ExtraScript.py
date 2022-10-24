from neuralintents import GenericAssistant
import os
import webbrowser
import sys

import speech_recognition
import ScreenAnalysis as sa
from SearchImageModul import SearchImage
import pyautogui

from OpenAIModule import OpenAI
from HarlanAI_Module import ChatBOT

cb = ChatBOT(train=False, accuracy=0.2)


class extraScript:
    def __init__(self, assistant, speaker, recognizer):
        self.assistant = assistant
        self.speaker = speaker
        self.recognizer = recognizer
        self.openAI = OpenAI()

    def train_now(self):
        self.assistant = GenericAssistant('intents.json')
        self.assistant.train_model()
        self.assistant.save_model('model/model')
        return self.assistant

    def open_app(self, app):
        if app == "notepad":
            os.startfile(
                'C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_10.2103.6.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe')
        elif app == "netflix":
            webbrowser.open(f"https://netflix.com")
        elif app == "hotstar":
            webbrowser.open(f"https://www.hotstar.com/id")
        elif app == "youtube":
            webbrowser.open(f"https://youtube.com")
        elif app == "discord":
            os.startfile(f"C:\\Users\\harla\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe")
        elif app == "calculator":
            os.startfile(
                f"C:\\Program Files\\WindowsApps\\Microsoft.WindowsCalculator_11.2110.4.0_x64__8wekyb3d8bbwe\\CalculatorApp.exe")


class CommandScript:
    def __init__(self, speaker, recognizer):
        self.speaker = speaker
        self.recognizer = recognizer
        self.todo_list = []

    def answer(self, text):
        if (text != None):
            self.speaker.say(text)
            self.speaker.runAndWait()

    def _ask_confirm(self):
        done = False
        while not done:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    item = self.recognizer.recognize_google(audio)
                    item = item.lower()

                    if item == "yes":
                        return True
                    else:
                        return False
            except speech_recognition.UnknownValueError():
                self.recognizer = speech_recognition.Recognizer()
                self.speaker.say("I did not understand you! Please try again!")

    def _extra_query(self, try_again=True):
        query = ""
        done = False
        while not done:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)
                    item = self.recognizer.recognize_google(audio)
                    item = item.lower()
                    query = item
                    done = True
            # except speech_recognition.UnknownValueError():
            except:
                if try_again:
                    self.recognizer = speech_recognition.Recognizer()
                    self.speaker.say("I did not understand you! Please try again!")
                    self.speaker.runAndWait()
                else:
                    pass
        return query

    def create_note(self):
        self.speaker.say("What do you want to write into your note?")
        self.speaker.runAndWait()

        done = False

        while not done:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    note = self.recognizer.recognize_google(audio)
                    note = note.lower()

                    self.speaker.say("Choose a filename!")
                    self.speaker.runAndWait()

                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    filename = self.recognizer.recognize_google(audio)
                    filename = filename.lower()

                with open(f"{filename}.txt", 'w') as f:
                    f.write(note)
                    done = True
                    self.speaker.say("I Successfully created the note {filename}")
                    self.speaker.runAndWait()
            except speech_recognition.UnknownValueError:
                self.recognizer = speech_recognition.Recognizer()
                self.speaker.say("I did not understand you! Please try again!")
                self.speaker.runAndWait()

    def add_todo(self):
        recognizer = self.recognizer
        self.speaker.say("What do you want to add?")
        self.speaker.runAndWait()

        done = False

        while not done:
            try:
                with speech_recognition.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    item = recognizer.recognize_google(audio)
                    item = item.lower()

                    self.todo_list.append(item)
                    done = True

                    self.speaker.say(f"I add {item} to the to do list!")
                    self.speaker.runAndWait()

            except speech_recognition.UnknownValueError():
                recognizer = speech_recognition.Recognizer()
                self.speaker.say("I did not understand you! Please try again!")
                self.speaker.runAndWait()

    def show_todos(self):
        if len(self.todo_list) == 0:
            self.speaker.say("Your to do list is empty")
            self.speaker.runAndWait()
        else:
            self.speaker.say("The items on your to do list are the following")
            for item in self.todo_list:
                self.speaker.say(item)
            self.speaker.runAndWait()

    def quit(self):
        self.speaker.say("Ok Bye")
        self.speaker.runAndWait()
        sys.exit(0)

    def restart_script(self):
        self.speaker.say("Trying to restart program")
        self.speaker.runAndWait()
        os.system("python Main.py")

    def pc_shutdown(self):
        print("-- shutdown --")
        self.speaker.say("Are you sure want to shutdown this PC?")
        self.speaker.runAndWait()

        if (self._ask_confirm()):
            self.speaker.say("Ok, See you leter?")
            os.system("shutdown /s /t 2")
        else:
            self.speaker.say("Shutdown has been canceled")
            print("--- shutdown has been cancel ---")

    def pc_restart(self):
        global recognizer
        self.speaker.say("Are you sure want to restart this PC?")
        self.speaker.runAndWait()
        if (self._ask_confirm()):
            os.system("shutdown /r /t 1")
        else:
            self.speaker.say("Restart has been canceled?")
            print("--- restart has been cancel ---")

    def find_face(self):
        sAnalysis = sa.ScreenAnalysis()
        faceFind = sAnalysis.checkFace()
        if faceFind:
            self.speaker.say("Face founded")
        else:
            self.speaker.say("Face not found")
        self.speaker.runAndWait()

    def ss_face(self):
        sAnalysis = sa.ScreenAnalysis(showAuto=False, search=False)
        faceFind = sAnalysis.checkFace()
        if not faceFind:
            self.speaker.say("Face not found")

        self.speaker.runAndWait()

    def search_web(self, app, query=None):
        if query is None:
            self.speaker.say("What do you want to search?")
            self.speaker.runAndWait()
            query = self._extra_query()

        if app == "youtube":
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        elif app == "google":
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif app == "netflix":
            webbrowser.open(f"https://www.netflix.com/search?q={query}")
        elif app == "hotstar":
            webbrowser.open(f"https://www.hotstar.com/id/search?q={query}")
        elif app == "google_image":
            app = 'Google Image'
            webbrowser.open(f"https://www.google.com/search?q={query}&tbm=isch")
        elif app == "google_image_show_random":
            app = 'Google Image'
            success = SearchImage().searchImages_show_random(query)
            if not success:
                self.speaker.say("I am sorry, something wrong")
                self.speaker.runAndWait()
                return False

        self.speaker.say(f"Searching of {query} on {app}")
        self.speaker.runAndWait()

    def open_manual(self, query=None):
        if query is None:
            self.speaker.say("What do you want to open?")
            self.speaker.runAndWait()
            query = self._extra_query()
        pyautogui.press("win")
        pyautogui.write(query)
        pyautogui.press("enter")

        # self.speaker.say(f"Open of {query}")
        # self.speaker.runAndWait()

    def ask_openai(self):
        self.speaker.say("Connect to AI Server")
        print("-------------------------------")
        print("Connect to AI Server")
        print("-------------------------------")
        self.speaker.runAndWait()
        self._ask_openai()

    def _ask_openai(self):
        stop_word = ["stop", "cancel", "stop AI server"]
        query = self._extra_query(try_again=False)
        if query in stop_word:
            print("-------------------------------")
            print("Disconnect to AI Server")
            print("-------------------------------")
            self.speaker.say("Stop connect to AI Server")
            self.speaker.runAndWait()
            return False
        else:
            print(f"You said: " + query)
            # answer = cb.ask(query)
            # if answer is None:
            answer = OpenAI().ask_ai(query)
            if not answer is None:
                print(f"AI said: " + answer)
                self.speaker.say(answer.replace("\n", " "))
            else:
                print("AI said: { empty }")
                self.speaker.say("AI don't have answer")
            self.speaker.runAndWait()
            self._ask_openai()


def main():
    assistant = GenericAssistant('intents.json')
    extraScript(assistant, None, None).train_now()


if __name__ == "__main__":
    main()
