from openai import OpenAI


def ask(context: str, question: str) -> str:
    system_prompt = f"You are in a {context} interview. You have to answer the following question"
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