import json

def update_part(filename, part_idx, passage_append, q_indices_to_clean):
    with open(filename, 'r') as f:
        data = json.load(f)
        
    part = data['parts'][part_idx]
    
    # Check if we already patched this to avoid duplicates
    if '<table' in part.get('passage', '') and 'id="patched"' in part.get('passage', ''):
        return
        
    part['passage'] = part.get('passage', '') + "<br>" + passage_append
    
    # Deduplicate and clean questions
    new_questions = []
    seen = set()
    for i, q in enumerate(part['questions']):
        if q['id'] not in seen:
            seen.add(q['id'])
            if i in q_indices_to_clean:
                q['content'] = f"Question {q['id']}"
                # Remove table artifacts from instruction if any
                q['instruction'] = q.get('instruction', '').replace('Complete the table below. ', '')
            new_questions.append(q)
            
    part['questions'] = new_questions
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


html_c18_t2 = """
<table id="patched" border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
    <thead>
        <tr>
            <th>Location</th>
            <th>Job title</th>
            <th>Responsibilities include</th>
            <th>Pay and conditions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><input type='text' data-qid='6' class='ielts-input' style='width:100px;' /> Street</td>
            <td>Breakfast supervisor</td>
            <td>Checking portions, etc. are correct</td>
            <td>Starting salary £9.75 per hour</td>
        </tr>
        <tr>
            <td>City Road</td>
            <td>Breakfast supervisor</td>
            <td>Making sure <input type='text' data-qid='7' class='ielts-input' style='width:100px;' /> is clean</td>
            <td>Start work at 5.30 a.m.</td>
        </tr>
        <tr>
            <td>City Road</td>
            <td>Breakfast supervisor</td>
            <td>Making sure equipment is clean</td>
            <td>Starting salary £<input type='text' data-qid='8' class='ielts-input' style='width:60px;' /> per hour</td>
        </tr>
        <tr>
            <td><input type='text' data-qid='9' class='ielts-input' style='width:100px;' /></td>
            <td>Junior chef</td>
            <td>Supporting senior chefs</td>
            <td>Annual salary £23,000</td>
        </tr>
        <tr>
            <td>City Road</td>
            <td>Junior chef</td>
            <td>Maintaining stock and organising <input type='text' data-qid='10' class='ielts-input' style='width:100px;' /> once a month</td>
            <td>No work on a Sunday</td>
        </tr>
    </tbody>
</table>
"""

html_c19_t2 = """
<table id="patched" border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
    <thead>
        <tr>
            <th>Time</th>
            <th>Activity</th>
            <th>Notes</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>5 minutes</td>
            <td>tuning guitars</td>
            <td>using an app or by <input type='text' data-qid='7' class='ielts-input' style='width:100px;' /></td>
        </tr>
        <tr>
            <td>10 minutes</td>
            <td>strumming chords using our thumbs</td>
            <td>keeping time while the teacher is <input type='text' data-qid='8' class='ielts-input' style='width:100px;' /></td>
        </tr>
        <tr>
            <td>15 minutes</td>
            <td>playing songs</td>
            <td>often listening to a <input type='text' data-qid='9' class='ielts-input' style='width:100px;' /> of a song</td>
        </tr>
        <tr>
            <td>10 minutes</td>
            <td>playing single notes and simple tunes</td>
            <td>playing together, then <input type='text' data-qid='10' class='ielts-input' style='width:100px;' /></td>
        </tr>
    </tbody>
</table>
"""

html_c19_t3 = """
<table id="patched" border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
    <thead>
        <tr>
            <th>Place</th>
            <th>Item</th>
            <th>Other ideas</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Fish market</td>
            <td>a dozen prawns</td>
            <td>a handful of <input type='text' data-qid='7' class='ielts-input' style='width:100px;' /> (type of seaweed)</td>
        </tr>
        <tr>
            <td>Organic shop</td>
            <td>beans</td>
            <td>a <input type='text' data-qid='8' class='ielts-input' style='width:100px;' /> for dessert</td>
        </tr>
        <tr>
            <td>Organic shop</td>
            <td>spices</td>
            <td><input type='text' data-qid='9' class='ielts-input' style='width:100px;' /></td>
        </tr>
        <tr>
            <td>Bakery</td>
            <td>a brown loaf</td>
            <td>a <input type='text' data-qid='10' class='ielts-input' style='width:100px;' /> tart</td>
        </tr>
    </tbody>
</table>
"""

update_part('docs/extracted_data/c18_test2_listening.json', 0, html_c18_t2, list(range(5, 10)))
update_part('docs/extracted_data/c19_test2_listening.json', 0, html_c19_t2, list(range(6, 10)))
update_part('docs/extracted_data/c19_test3_listening.json', 0, html_c19_t3, list(range(6, 10)))

print("Patched C18 T2, C19 T2, C19 T3.")
