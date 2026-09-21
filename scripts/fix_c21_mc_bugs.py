import json
import glob
import re

c21_files = sorted(glob.glob('docs/extracted_data/c21_*.json'))

for file in c21_files:
    changed = False
    with open(file, 'r') as f:
        data = json.load(f)
        
    for part in data.get('parts', []):
        for q in part.get('questions', []):
            if q.get('type') == 'multiple_choice':
                content = q.get('content', '')
                if '<input' not in content:
                    # Append an input text box at the end
                    q['content'] = content + f"<br><br><input type='text' data-qid='{q['id']}' class='ielts-input' placeholder='Type letter(s)' style='width:100px; text-transform:uppercase;' />"
                    changed = True
                    print(f"Patched {file} Q{q['id']}")
                    
    if changed:
        with open(file, 'w') as f:
            json.dump(data, f, indent=2)

print("Patching complete.")
