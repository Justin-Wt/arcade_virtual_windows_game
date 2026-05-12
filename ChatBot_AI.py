import requests
import json
import os

filename = "chatbot_memories.json"


def chat(parent, chat):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([{"name": parent, "data": []}], f)
    with open(filename, "r") as f:
        history = json.load(f)
    invalid = False

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": chat, "stream": False},
    )

    data = response.json()
    for item in history:
        if item["name"] == parent:
            item["data"].append({"content": chat})
            item["data"].append({"content": data["response"]})
            invalid = False
            print(history)
            print("found")
            break
        else:
            invalid = True
            print(history)
            print("not found")
    if invalid:
        history.append({"name": parent, "data": []})
        print(history)
        for item in history:
            if item["name"] == parent:
                item["data"].append({"content": chat})
                item["data"].append({"content": data["response"]})
                print(history)
    print(history)
    with open(filename, "w") as f:
        json.dump(history, f, indent=4)
    return data["response"]
