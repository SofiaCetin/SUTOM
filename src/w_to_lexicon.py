import json

language = input().strip().lower()
file_to_w = f"{language}.json"
file_path = f"lang/{file_to_w}"
with open(file_path, 'r', encoding="utf-8") as json_f:
    data = json.load(json_f)

try:
    while True:

        word = input().strip()

        if len(word) < 6 or len(word) > 10:
            continue

        key = f"{len(word)}_letter_words"

        if word in data[key]:
            continue   
        else:
            data[key].append(word)

except EOFError:
    with open(file_path, 'w', encoding="utf-8") as json_f:
        json.dump(data, json_f, indent = 2, ensure_ascii=False)