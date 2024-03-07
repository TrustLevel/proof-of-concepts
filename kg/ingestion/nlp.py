import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_article_content(article_title, scraped_text):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"identify and extract the actual news article content from the following scraped webpage text, removing any boilerplate or non-article content:\n{scraped_text}\Take into account the the article title '{article_title}', so any related content likely belongs to the article content. Also be aware that the article might contian irrelevant information (ads) in between, so content might be spread out. Return only the actual article content. Actual article content:"},
    ],
    temperature=0
    )

    return response.choices[0].message.content