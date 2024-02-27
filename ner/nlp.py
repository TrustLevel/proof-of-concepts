import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def rewrite_query(text):


    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"rewrite this query so its more suitable to Entity recognition\nquery: \"{text}\"return only the rewritten query.\nrewritten query:"},
    ],
    temperature=0
    )

    return response.choices[0].message.content