import json
import glob

def get_select_html(qid, qtype):
    if qtype == 'true_false_not_given':
        options = ["TRUE", "FALSE", "NOT GIVEN"]
    else:
        options = ["YES", "NO", "NOT GIVEN"]
        
    html = f" <select data-qid='{qid}' class='ielts-input' style='margin-left: 10px;'>"
    html += "<option value=''></option>"
    for opt in options:
        html += f"<option value='{opt}'>{opt}</option>"
    html += "</select>"
    return html

def fix_tfng():
    c21_files = sorted(glob.glob('docs/extracted_data/c21_*.json'))
    
    for file in c21_files:
        changed = False
        with open(file, 'r') as f:
            data = json.load(f)
            
        for part in data.get('parts', []):
            for q in part.get('questions', []):
                t = q.get('type', '')
                if t in ['true_false_not_given', 'yes_no_not_given']:
                    content = q.get('content', '')
                    if '<select' not in content and '<input' not in content:
                        q['content'] = content + get_select_html(q['id'], t)
                        changed = True
                        print(f"Patched {file} Q{q['id']}")
                        
        if changed:
            with open(file, 'w') as f:
                json.dump(data, f, indent=2)

if __name__ == '__main__':
    fix_tfng()
    print("TFNG Patching complete.")
