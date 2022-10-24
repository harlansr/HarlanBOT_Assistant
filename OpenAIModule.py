#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

import openai
import json


class OpenAI:
    def __init__(self, engine_key=0):
        self.engine_key = engine_key
        with open('secret_code.json', 'r') as f:
            data = json.load(f)
        self.OPENAI_API = data['key']['openai_api']
        self.OPENAI_ENGINE = data['list']['openai']["engine"][self.engine_key]

    def ask_ai(self, query):
        # return [self.OPENAI_API, self.OPENAI_ENGINE]
        openai.api_key = self.OPENAI_API

        response = openai.Completion.create(
            engine=self.OPENAI_ENGINE,
            prompt=query,
            temperature=0.1,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # return 'test';

        content = response.choices[0].text.split('.')
        # return response.choices[0].text
        if len(content) != 0:
            return self._chose_return(content)
        else:
            return None

    def _chose_return(self, content, index=0):
        if len(content) > index:
            if content[index] != '' and not content[index] is None:
                answer = content[index].splitlines()
                aaa = ""
                for ans in answer:
                    if ans != '' and not ans is None:
                        aaa += ans + ", "
                return aaa
            else:
                return self._chose_return(content, index + 1)
        else:
            return None


def main():
    answer = OpenAI().ask_ai("apakah kamu punya pacar sekarang atau tidak")
    print(answer)


if __name__ == "__main__":
    # print(test)
    main()