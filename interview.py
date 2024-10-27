
from config import Config
import gpt

class Interview:
    def __init__(self, context: str):
        system_prompt = Config.get("system_prompt").format(context=context)

        self.context = context
        self.messages = [
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": system_prompt
                }
            ]
            },
        ]


    def ask(self, question: str) -> str:
        response = gpt.ask(self.messages, question)

        self.messages.append(
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": question
                }
            ]
            }
        )

        self.messages.append(
            {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": response
                }
            ]
            }
        )

        return response
