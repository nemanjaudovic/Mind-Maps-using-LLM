import requests

API_URL = "https://api-inference.huggingface.co/models/google-bert/bert-base-uncased"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def create_answers(prompt):
    output = query({
        "inputs":'[MASK]'+ prompt
    })
    answers=[0,0,0,0]
    for i in range(4):
        answers[i] = output[i]['token_str']
    return answers



