import json

file = 'docs/extracted_data/c21_test2_reading.json'
with open(file, 'r') as f:
    data = json.load(f)

changed = False
for part in data.get('parts', []):
    for q in part.get('questions', []):
        if q.get('type') == 'matching_headings':
            content = q.get('content', '')
            if '<input' not in content:
                # Add the input box at the end of the text
                q['content'] = content + f" <input type='text' data-qid='{q['id']}' class='ielts-input' style='width:50px; text-transform:uppercase;' />"
                changed = True
                print(f"Patched Q{q['id']}")

if changed:
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)
    print("Saved changes.")
