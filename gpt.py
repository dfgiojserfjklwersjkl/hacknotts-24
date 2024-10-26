from openai import OpenAI


def ask(context: str, question: str) -> str:
    system_prompt = f"I want you to act as a {context} interview assistant,  I will give you some interview questions (as an  interviewer) and you need to answer them as an interviewee.
Your answer should be in the following style:
 <Answerstyle>Use clear, direct language and avoid complex terminology. Aim for a Flesch reading score of 80 or higher. Use the active voice. Avoid adverbs. Avoid buzzwords and instead use plain English. Use jargon where relevant. Avoid being salesy or overly enthusiastic and instead express calm confidence. </Answerstyle>"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": system_prompt
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": question
                }
            ]
            },
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
        )

    return response.choices[0].message.content or "Sorry, I don't know the answer to that question."

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    load_dotenv()
    client = OpenAI()

    res = ask("software engineer", "introduce yourself")
    print(res)