from interview import Interview

if __name__ == "__main__":
    interview = Interview("This is a context")
    question = "What is the capital of France?"
    answer = interview.ask(question)
    print(answer)

