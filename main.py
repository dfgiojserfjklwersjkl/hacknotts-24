from interview import Interview
from config import Config
if __name__ == "__main__":
    

    interview_context = Config.get("interview_context")

    interview = Interview(interview_context) 

    question = "What programming languages are you most comfortable with, and which have you used for game development?"
    answer = interview.ask(question)
    print(answer)

    question = "Can you describe your experience with game engines like Unity or Minecraft’s own engine? What projects have you worked on using these tools?"
    answer = interview.ask(question)
    print(answer)

    question = "Can you describe your experience with game engines like Unity or Minecraft’s own engine? What projects have you worked on using these tools?"
    answer = interview.ask(question)
    print(answer)

    question = "What game mechanics do you think are essential for engaging gameplay? Can you provide an example from a game you enjoy?"
    answer = interview.ask(question)
    print(answer)
    
