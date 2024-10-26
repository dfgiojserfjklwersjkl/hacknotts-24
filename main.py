from interview import Interview
from config import Config
if __name__ == "__main__":
    

    interview_context = Config.get("interview_context")

    interview = Interview(interview_context) 

    question = "What is your name?"
    answer = interview.ask(question)
    print(answer)

