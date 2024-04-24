import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b-it"
headers = {"Authorization": f"Bearer {os.getenv("HUGGINGFACE_API_KEY")}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
# bias_score: 0.2
output = query({
	"inputs": """Determine how biased the input text is. The bias score is in the range [0.0,1.0] where 0.0 means not biased and 1.0 means the text is biased. Let’s think step by step how to come to the bias score.
Text: House Speaker Mike Johnson is facing down yet another pivotal week of his speakership as he confronts both the threat of an ouster and mounting pressure to decide whether he will finally move ahead on aid to Ukraine, which he’s been pledging to pursue for months.

Throughout the two-week Easter recess, Rep. Marjorie Taylor Greene has kept up her attacks against Johnson as she continues to warn the speaker against pursuing any Ukraine aid package. But Johnson has also been working behind the scenes in an effort to thread the needle and find a package that could pass.

The issue for Johnson remains that any aid to Ukraine will need a large number of Democratic votes. Creating legislation that could attract enough Democratic support to get Ukraine across the finish line and included funding for Israel could be difficult, especially in the wake of an Israeli strike that killed World Central Kitchen aid workers last week. Following the strike, more Democrats have signaled they are open to attaching conditions to aid for Israel, a dynamic that could complicate future efforts to approve Israel aid through Congress.
bias_score:""",
})
print(output)