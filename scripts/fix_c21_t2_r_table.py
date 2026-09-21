import json

def fix_c21_t2_r_table():
    path = 'docs/extracted_data/c21_test2_reading.json'
    with open(path, 'r') as f:
        data = json.load(f)
        
    part = data['parts'][0]
    
    html = """
<div class='notes-completion'>
    <table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr>
                <th colspan="3" style="text-align: center; font-size: 1.2em; background-color: #f5f5f5;">Research into sleep and dreaming</th>
            </tr>
            <tr>
                <th></th>
                <th>Research findings</th>
                <th>Comment</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Humans</td>
                <td><ul><li>humans experience REM sleep and non-REM sleep</li><li>in REM sleep, the eyes and muscles move</li></ul></td>
                <td></td>
            </tr>
            <tr>
                <td><strong>1</strong> <input type="text" data-qid="1" class="ielts-input" style="width:100px;"></td>
                <td><ul><li>similar brain patterns were observed when active and sleeping</li></ul></td>
                <td>indicative of dreaming</td>
            </tr>
            <tr>
                <td>Pigeons</td>
                <td><ul><li>when sleeping, pigeons displayed activity in parts of the brain that deal with <strong>2</strong> <input type="text" data-qid="2" class="ielts-input" style="width:100px;"> input</li></ul></td>
                <td>may have been dreaming of flying</td>
            </tr>
            <tr>
                <td>Whales and dolphins</td>
                <td><ul><li>still have <strong>3</strong> <input type="text" data-qid="3" class="ielts-input" style="width:100px;"> their brain awake when they sleep</li><li>don't experience REM sleep, as this could affect their sensitivity to <strong>4</strong> <input type="text" data-qid="4" class="ielts-input" style="width:100px;"></li></ul></td>
                <td>their dreams are probably not very <strong>5</strong> <input type="text" data-qid="5" class="ielts-input" style="width:100px;"></td>
            </tr>
        </tbody>
    </table>
</div>
"""

    part['questions'][0]['content'] = html
    for i in range(1, 5):
        part['questions'][i]['content'] = ''
        
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    fix_c21_t2_r_table()
    print("Fixed C21 T2 R P1 table.")
