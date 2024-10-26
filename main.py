from interview import Interview
from config import Config
if __name__ == "__main__":
    

    interview_context = Config.get("interview_context")

    interview = Interview(interview_context) 

    question = "What programming languages are you most comfortable with, and which have you used for game development?"
    answer = interview.ask(question)
    print(answer)

