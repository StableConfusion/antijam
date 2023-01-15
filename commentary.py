import requests
from random import randint


class Commentator:
    def __init__(self):

        self.api_url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
        self.headers = {"Authorization": "Bearer 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"}
        self.prompt = "Two sport commentators are commenting a racing game.\n"
        self.turn = 0
        self.available_bad_comments = [
            "Oh my, what a traffic!",
            "That seems bad...",
            "Gotta go to work",
            "Make it quick!",
            "Whose sh*t code is that?"
        ]
        self.available_good_comments = [
            "So clean!",
            "Nice!",
            "Thx for no traffic!",
            "That one's much better",
            "Cracow traffic is fixed now"
        ]

    def query(self, payload):
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def speak(self):
        if self.turn == 0:
            self.prompt += "\nCommentator1: "
        else:
            self.prompt += "\nCommentator2: "
        output = self.query({"inputs": self.prompt})
        self.prompt = output[0]['generated_text']
        out_split = output[0]['generated_text'].split('\n')
        next_comment = self.get_next_comment(out_split)

        print('\n', next_comment)
        self.turn = not self.turn
        return next_comment

    def get_next_comment(self, output):
        comment = []
        i = len(output) - 1
        while i > 0:
            if self.turn == 0 and "Commentator1" in output[i]:
                break
            elif self.turn == 1 and "Commentator2" in output[i]:
                break
            comment.append(output[i])
            i -= 1

        comment.append(output[i])
        comment = comment[::-1]
        return ' '.join(comment)

    def cut_commentator(self, speech: str):
        speech_split = speech.split(' ')

        res = []
        i = len(speech_split) - 1
        while i > 0:
            if "Commentator" in speech_split[i]:
                break
            res.append(speech_split[i])
            i -= 1

        return ' '.join(res)

    def random_generated_comment(self, is_good):
        if is_good:
            return self.available_good_comments[randint(0, 4)]
        else:
            return self.available_bad_comments[randint(0, 4)]


if __name__ == '__main__':
    C = Commentator()
    C.speak()
    C.speak()
