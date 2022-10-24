# pip install nltk
# pip install numpy
# pip install tflearn
# pip install tensorflow

import os.path
import json
import pickle
import random

import nltk
import numpy
import tensorflow
import tflearn
from nltk.stem.lancaster import LancasterStemmer

DIR_INTENTS = "files/intents.json"
DIR_PICKLE = "files/training_models/data.pickle"
DIR_MODEL = "files/training_models/model.tflearn"


class ChatBOT:
    def __init__(self, train=False, accuracy=0.9):
        self.accuracy = accuracy
        self.words = []
        self.labels = []
        self.docs_x = []
        self.docs_y = []
        self.training = []
        self.output = []
        self.model = None

        self.stemmer = LancasterStemmer()

        if os.path.isfile(DIR_INTENTS):
            with open(DIR_INTENTS) as file:
                self.data = json.load(file)

            if train:
                self.train()
            else:
                try:
                    self.load()
                except:
                    self.train()

    def load(self):
        with open(DIR_PICKLE, "rb") as f:
            self.words, self.labels, self.training, self.output = pickle.load(f)

        self._load_model()
        self.model.load(DIR_MODEL)


    def _load_model(self):
        tensorflow.compat.v1.reset_default_graph()

        net = tflearn.input_data(shape=[None, len(self.training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(self.output[0]), activation="softmax")
        net = tflearn.regression(net)

        self.model = tflearn.DNN(net)

    def train(self):
        for intent in self.data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                self.words.extend(wrds)
                self.docs_x.append(wrds)
                self.docs_y.append(intent["tag"])

            if intent["tag"] not in self.labels:
                self.labels.append(intent["tag"])

        self.words = [self.stemmer.stem(w.lower()) for w in self.words if w not in "?"]
        self.words = sorted(list(set(self.words)))

        self.labels = sorted(self.labels)

        out_empty = [0 for _ in range(len(self.labels))]

        for x, doc in enumerate(self.docs_x):
            bag = []

            wrds = [self.stemmer.stem(w) for w in doc]

            for w in self.words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[self.labels.index(self.docs_y[x])] = 1

            self.training.append(bag)
            self.output.append(output_row)

        self.training = numpy.array(self.training)
        self.output = numpy.array(self.output)

        if os.path.isfile(DIR_PICKLE):
            with open(DIR_PICKLE, "wb") as f:
                pickle.dump((self.words, self.labels, self.training, self.output), f)

        self._load_model()

        self.model.fit(self.training, self.output, n_epoch=1000, batch_size=8, show_metric=True)
        self.model.save(DIR_MODEL)

    def bag_of_words(self, s, words):
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [self.stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1

        return numpy.array(bag)

    def ask(self, message, need_accuracy=False):
        results = self.model.predict([self.bag_of_words(message, self.words)])[0]
        results_index = numpy.argmax(results)
        results_max = results[results_index]
        tag = self.labels[results_index]

        if results_max > self.accuracy:
            for tg in self.data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            if need_accuracy:
                return random.choice(responses), results_max
            else:
                return random.choice(responses)

        message_clean = self._clean_text(message)
        list_data = []
        list_data.append(self.data["intents_fix"])
        list_data.append(self.data["intents"])

        for anl in list_data:
            for an in anl:
                use_this = False
                ptrn = an['patterns']
                for ann in ptrn:
                    anc = self._clean_text(ann)
                    if anc == message_clean:
                        use_this = True

                if use_this:
                    responses = an['responses']
                    return random.choice(responses)


    def _clean_text(self, text):
        text = text.replace("!", "")
        text = text.replace("?", "")
        return text.lower()


    def run_loop(self):
        print("Start talking with the bot!")
        while True:
            inp = input("You: ")
            if inp.lower() == "quit":
                break

            results = self.model.predict([self.bag_of_words(inp, self.words)])[0]
            results_index = numpy.argmax(results)
            results_max = results[results_index]
            tag = self.labels[results_index]

            if results_max > self.accuracy:
                for tg in self.data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']

                print(random.choice(responses))
            else:
                print("I didn't get that, try again")


if __name__ == "__main__":
    ChatBOT(True)

