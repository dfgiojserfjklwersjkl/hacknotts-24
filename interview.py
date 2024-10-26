
import gpt

class Interview:
    def __init__(self, context: str):
        self.context = context


    def ask(self, question: str) -> str:
        return gpt.ask(self.context, question)