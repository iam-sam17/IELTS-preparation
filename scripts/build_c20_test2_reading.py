#!/usr/bin/env python3
"""
Compile Cambridge 20 Test 2 Reading with authentic OCR'd passages and full question structure.
"""

import json
import re

# Read OCR'd passages
def clean_passage(text, title):
    lines = [line.strip() for line in text.splitlines()]
    paragraphs = []
    curr = []
    for l in lines:
        if not l:
            if curr:
                paragraphs.append(" ".join(curr))
                curr = []
            continue
        # Filter out headers and footers
        l_lower = l.lower()
        if any(h in l_lower for h in ["reading passage", "authentic ielts", "@realexamielts", "you should spend about 20 minutes"]):
            continue
        if l == title or l.upper() == title.upper():
            continue
        curr.append(l)
    if curr:
        paragraphs.append(" ".join(curr))
    
    html = f"<h3>{title}</h3>"
    for p in paragraphs:
        if p:
            html += f"<p>{p}</p>"
    return html

import subprocess

# Run OCR on passages
p1_text = subprocess.run(['tesseract', '--tessdata-dir', 'scripts/tessdata', '-l', 'eng', '/tmp/p25.png', 'stdout'], capture_output=True, text=True).stdout + "\n" + subprocess.run(['tesseract', '--tessdata-dir', 'scripts/tessdata', '-l', 'eng', '/tmp/p26.png', 'stdout'], capture_output=True, text=True).stdout

p2_text = subprocess.run(['tesseract', '--tessdata-dir', 'scripts/tessdata', '-l', 'eng', '/tmp/p29.png', 'stdout'], capture_output=True, text=True).stdout + "\n" + subprocess.run(['tesseract', '--tessdata-dir', 'scripts/tessdata', '-l', 'eng', '/tmp/p30.png', 'stdout'], capture_output=True, text=True).stdout

p3_text = subprocess.run(['tesseract', '--tessdata-dir', 'scripts/tessdata', '-l', 'eng', '/tmp/p33.png', 'stdout'], capture_output=True, text=True).stdout + "\n" + subprocess.run(['tesseract', '--tessdata-dir', 'scripts/tessdata', '-l', 'eng', '/tmp/p34.png', 'stdout'], capture_output=True, text=True).stdout

html_p1 = clean_passage(p1_text, "Manatees")
html_p2 = clean_passage(p2_text, "Procrastination")
html_p3 = clean_passage(p3_text, "Invasion of the Robot Umpires")

# Part 1 Questions (1-13)
questions_p1 = [
    {
        "id": 1,
        "type": "summary_completion",
        "instruction": "Complete the notes below. Choose ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "content": "Appearance: look similar to dugongs, but with a differently shaped <input type='text' data-qid='1' class='ielts-input' />",
        "answer": "tail"
    },
    {
        "id": 2,
        "type": "summary_completion",
        "instruction": "Complete the notes below. Choose ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "content": "Movement: have fewer neck bones than most mammals; need to use their <input type='text' data-qid='2' class='ielts-input' /> to help to turn their bodies around in order to look sideways",
        "answer": "flippers"
    },
    {
        "id": 3,
        "type": "summary_completion",
        "instruction": "Complete the notes below. Choose ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "content": "sense vibrations in the water by means of <input type='text' data-qid='3' class='ielts-input' /> on their skin",
        "answer": "hair"
    },
    {
        "id": 4,
        "type": "summary_completion",
        "instruction": "Complete the notes below. Choose ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "content": "Feeding: eat mainly aquatic vegetation, such as <input type='text' data-qid='4' class='ielts-input' />",
        "answer": "seagrasses"
    },
    {
        "id": 5,
        "type": "summary_completion",
        "instruction": "Complete the notes below. Choose ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "content": "grasp and pull up plants with their <input type='text' data-qid='5' class='ielts-input' />",
        "answer": "lips"
    },
    {
        "id": 6,
        "type": "summary_completion",
        "instruction": "Complete the notes below. Choose ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "content": "Breathing: come to the surface for air every 2-4 minutes when awake and every 15–20 while sleeping; may regulate the <input type='text' data-qid='6' class='ielts-input' /> of their bodies by using muscles of diaphragm to store air internally",
        "answer": "buoyancy"
    },
    {
        "id": 7,
        "type": "true_false_not_given",
        "instruction": "Do the following statements agree with the information given in Reading Passage 1?",
        "content": "7. West Indian manatees can be found in a variety of different aquatic habitats.<br><label><input type='radio' name='q7' value='TRUE'> TRUE</label><br><label><input type='radio' name='q7' value='FALSE'> FALSE</label><br><label><input type='radio' name='q7' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "TRUE"
    },
    {
        "id": 8,
        "type": "true_false_not_given",
        "instruction": "Do the following statements agree with the information given in Reading Passage 1?",
        "content": "8. The Florida manatee lives in warmer waters than the Antillean manatee.<br><label><input type='radio' name='q8' value='TRUE'> TRUE</label><br><label><input type='radio' name='q8' value='FALSE'> FALSE</label><br><label><input type='radio' name='q8' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "NOT GIVEN"
    },
    {
        "id": 9,
        "type": "true_false_not_given",
        "instruction": "Do the following statements agree with the information given in Reading Passage 1?",
        "content": "9. The African manatee’s range is limited to coastal waters between the West African countries of Mauritania and Angola.<br><label><input type='radio' name='q9' value='TRUE'> TRUE</label><br><label><input type='radio' name='q9' value='FALSE'> FALSE</label><br><label><input type='radio' name='q9' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "FALSE"
    },
    {
        "id": 10,
        "type": "true_false_not_given",
        "instruction": "Do the following statements agree with the information given in Reading Passage 1?",
        "content": "10. The extent of the loss of Amazonian manatees in the mid-twentieth century was only revealed many years later.<br><label><input type='radio' name='q10' value='TRUE'> TRUE</label><br><label><input type='radio' name='q10' value='FALSE'> FALSE</label><br><label><input type='radio' name='q10' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "NOT GIVEN"
    },
    {
        "id": 11,
        "type": "true_false_not_given",
        "instruction": "Do the following statements agree with the information given in Reading Passage 1?",
        "content": "11. It is predicted that West Indian manatee populations will fall in the coming decades.<br><label><input type='radio' name='q11' value='TRUE'> TRUE</label><br><label><input type='radio' name='q11' value='FALSE'> FALSE</label><br><label><input type='radio' name='q11' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "TRUE"
    },
    {
        "id": 12,
        "type": "true_false_not_given",
        "instruction": "Do the following statements agree with the information given in Reading Passage 1?",
        "content": "12. The risk to manatees from entanglement and plastic consumption increased significantly in the period 2009-2020.<br><label><input type='radio' name='q12' value='TRUE'> TRUE</label><br><label><input type='radio' name='q12' value='FALSE'> FALSE</label><br><label><input type='radio' name='q12' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "NOT GIVEN"
    },
    {
        "id": 13,
        "type": "true_false_not_given",
        "instruction": "Do the following statements agree with the information given in Reading Passage 1?",
        "content": "13. There is some legislation in place which aims to reduce the likelihood of boat strikes on manatees in Florida.<br><label><input type='radio' name='q13' value='TRUE'> TRUE</label><br><label><input type='radio' name='q13' value='FALSE'> FALSE</label><br><label><input type='radio' name='q13' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "TRUE"
    }
]

# Part 2 Questions (14-26)
questions_p2 = [
    {
        "id": 14,
        "type": "matching_headings",
        "instruction": "Reading Passage 2 has six paragraphs, A-F. Which paragraph contains the following information? Write the correct letter, A-F.",
        "content": "14. mention of false assumptions about why people procrastinate<br><input type='text' data-qid='14' class='ielts-input' placeholder='A-F' />",
        "answer": "B"
    },
    {
        "id": 15,
        "type": "matching_headings",
        "instruction": "Reading Passage 2 has six paragraphs, A-F. Which paragraph contains the following information? Write the correct letter, A-F.",
        "content": "15. reference to the realisation that others also procrastinate<br><input type='text' data-qid='15' class='ielts-input' placeholder='A-F' />",
        "answer": "F"
    },
    {
        "id": 16,
        "type": "matching_headings",
        "instruction": "Reading Passage 2 has six paragraphs, A-F. Which paragraph contains the following information? Write the correct letter, A-F.",
        "content": "16. neurological evidence of a link between procrastination and emotion<br><input type='text' data-qid='16' class='ielts-input' placeholder='A-F' />",
        "answer": "B"
    },
    {
        "id": 17,
        "type": "summary_completion",
        "instruction": "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        "content": "Many people think that procrastination is the result of <input type='text' data-qid='17' class='ielts-input' />. Others believe it to be the result of an inability to organise time efficiently.",
        "answer": "laziness"
    },
    {
        "id": 18,
        "type": "summary_completion",
        "instruction": "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        "content": "But scientific studies suggest that procrastination is actually due to poor mood management. The tasks we are most likely to put off are those that could damage our self-esteem or cause us to feel <input type='text' data-qid='18' class='ielts-input' /> when we think about them.",
        "answer": "anxious"
    },
    {
        "id": 19,
        "type": "summary_completion",
        "instruction": "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        "content": "Research comparing chronic procrastinators with other people even found differences in the brain regions associated with regulating emotions and identifying <input type='text' data-qid='19' class='ielts-input' />.",
        "answer": "threats"
    },
    {
        "id": 20,
        "type": "summary_completion",
        "instruction": "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        "content": "Emotionally loaded and difficult tasks often cause us to procrastinate. Getting ready to take <input type='text' data-qid='20' class='ielts-input' /> might be a typical example of one such task.",
        "answer": "exams"
    },
    {
        "id": 21,
        "type": "summary_completion",
        "instruction": "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        "content": "People who are likely to procrastinate tend to be either <input type='text' data-qid='21' class='ielts-input' /> or those with low self-esteem.",
        "answer": "perfectionists"
    },
    {
        "id": 22,
        "type": "summary_completion",
        "instruction": "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        "content": "Procrastination is only a short-term measure for managing emotions. It’s often followed by a feeling of <input type='text' data-qid='22' class='ielts-input' />, which worsens our mood and leads to more procrastination.",
        "answer": "guilt"
    },
    {
        "id": 23,
        "type": "multiple_choice",
        "instruction": "Choose TWO letters, A-E. Which TWO comparisons between employees who often procrastinate and those who do not are mentioned in the text?",
        "content": "<label><input type='checkbox' name='q23' value='A'> A. Their salaries are lower.</label><br><label><input type='checkbox' name='q23' value='B'> B. The quality of their work is inferior.</label><br><label><input type='checkbox' name='q23' value='C'> C. They don’t keep their jobs for as long.</label><br><label><input type='checkbox' name='q23' value='D'> D. They don’t enjoy their working lives as much.</label><br><label><input type='checkbox' name='q23' value='E'> E. They have poorer relationships with colleagues.</label>",
        "answer": "A"
    },
    {
        "id": 24,
        "type": "multiple_choice",
        "instruction": "Choose TWO letters, A-E. (Second choice for questions 23 and 24)",
        "content": "<label><input type='checkbox' name='q24' value='A'> A. Their salaries are lower.</label><br><label><input type='checkbox' name='q24' value='B'> B. The quality of their work is inferior.</label><br><label><input type='checkbox' name='q24' value='C'> C. They don’t keep their jobs for as long.</label><br><label><input type='checkbox' name='q24' value='D'> D. They don’t enjoy their working lives as much.</label><br><label><input type='checkbox' name='q24' value='E'> E. They have poorer relationships with colleagues.</label>",
        "answer": "C"
    },
    {
        "id": 25,
        "type": "multiple_choice",
        "instruction": "Choose TWO letters, A-E. Which TWO recommendations for getting out of a cycle of procrastination does the writer give?",
        "content": "<label><input type='checkbox' name='q25' value='A'> A. not judging ourselves harshly</label><br><label><input type='checkbox' name='q25' value='B'> B. setting ourselves manageable aims</label><br><label><input type='checkbox' name='q25' value='C'> C. rewarding ourselves for tasks achieved</label><br><label><input type='checkbox' name='q25' value='D'> D. prioritising tasks according to their importance</label><br><label><input type='checkbox' name='q25' value='E'> E. avoiding things that stop us concentrating on our tasks</label>",
        "answer": "A"
    },
    {
        "id": 26,
        "type": "multiple_choice",
        "instruction": "Choose TWO letters, A-E. (Second choice for questions 25 and 26)",
        "content": "<label><input type='checkbox' name='q26' value='A'> A. not judging ourselves harshly</label><br><label><input type='checkbox' name='q26' value='B'> B. setting ourselves manageable aims</label><br><label><input type='checkbox' name='q26' value='C'> C. rewarding ourselves for tasks achieved</label><br><label><input type='checkbox' name='q26' value='D'> D. prioritising tasks according to their importance</label><br><label><input type='checkbox' name='q26' value='E'> E. avoiding things that stop us concentrating on our tasks</label>",
        "answer": "E"
    }
]

# Part 3 Questions (27-40)
questions_p3 = [
    {
        "id": 27,
        "type": "yes_no_not_given",
        "instruction": "Do the following statements agree with the claims of the writer in Reading Passage 3?",
        "content": "27. When DeJesus first used ABS, he shared decision-making about strikes with it.<br><label><input type='radio' name='q27' value='YES'> YES</label><br><label><input type='radio' name='q27' value='NO'> NO</label><br><label><input type='radio' name='q27' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "NO"
    },
    {
        "id": 28,
        "type": "yes_no_not_given",
        "instruction": "Do the following statements agree with the claims of the writer in Reading Passage 3?",
        "content": "28. MLB considered it necessary to amend the size of the strike zone when criticisms were received from players.<br><label><input type='radio' name='q28' value='YES'> YES</label><br><label><input type='radio' name='q28' value='NO'> NO</label><br><label><input type='radio' name='q28' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "YES"
    },
    {
        "id": 29,
        "type": "yes_no_not_given",
        "instruction": "Do the following statements agree with the claims of the writer in Reading Passage 3?",
        "content": "29. MLB is keen to justify the money spent on improving the accuracy of ABS's calculations.<br><label><input type='radio' name='q29' value='YES'> YES</label><br><label><input type='radio' name='q29' value='NO'> NO</label><br><label><input type='radio' name='q29' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "NOT GIVEN"
    },
    {
        "id": 30,
        "type": "yes_no_not_given",
        "instruction": "Do the following statements agree with the claims of the writer in Reading Passage 3?",
        "content": "30. The hundred-mile-an-hour fastball led to a more exciting style of play.<br><label><input type='radio' name='q30' value='YES'> YES</label><br><label><input type='radio' name='q30' value='NO'> NO</label><br><label><input type='radio' name='q30' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "NO"
    },
    {
        "id": 31,
        "type": "yes_no_not_given",
        "instruction": "Do the following statements agree with the claims of the writer in Reading Passage 3?",
        "content": "31. The differing proposals for alterations to the baseball bat led to fierce debate on Sword's team.<br><label><input type='radio' name='q31' value='YES'> YES</label><br><label><input type='radio' name='q31' value='NO'> NO</label><br><label><input type='radio' name='q31' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "NOT GIVEN"
    },
    {
        "id": 32,
        "type": "yes_no_not_given",
        "instruction": "Do the following statements agree with the claims of the writer in Reading Passage 3?",
        "content": "32. ABS makes changes to the shape of the strike zone feasible.<br><label><input type='radio' name='q32' value='YES'> YES</label><br><label><input type='radio' name='q32' value='NO'> NO</label><br><label><input type='radio' name='q32' value='NOT GIVEN'> NOT GIVEN</label>",
        "answer": "YES"
    },
    {
        "id": 33,
        "type": "summary_completion",
        "instruction": "Complete the summary using the list of phrases, A-H, below. Write the correct letter, A-H.",
        "content": "Even after ABS was developed, MLB still wanted human umpires to shout out decisions as they had in their <input type='text' data-qid='33' class='ielts-input' placeholder='A-H' />.<br><small>A. pitch boundary | B. numerous disputes | C. team tactics | D. subjective assessment | E. widespread approval | F. former roles | G. total silence | H. perceived area</small>",
        "answer": "F"
    },
    {
        "id": 34,
        "type": "summary_completion",
        "instruction": "Complete the summary using the list of phrases, A-H, below. Write the correct letter, A-H.",
        "content": "The umpire's job had, at one time, required a <input type='text' data-qid='34' class='ielts-input' placeholder='A-H' /> about whether a ball was a strike.",
        "answer": "D"
    },
    {
        "id": 35,
        "type": "summary_completion",
        "instruction": "Complete the summary using the list of phrases, A-H, below. Write the correct letter, A-H.",
        "content": "A ball is considered a strike when the batter does not hit it and it crosses through a <input type='text' data-qid='35' class='ielts-input' placeholder='A-H' /> extending approximately from the batter's knee to his chest.",
        "answer": "H"
    },
    {
        "id": 36,
        "type": "summary_completion",
        "instruction": "Complete the summary using the list of phrases, A-H, below. Write the correct letter, A-H.",
        "content": "In the past, <input type='text' data-qid='36' class='ielts-input' placeholder='A-H' /> over strike calls were not uncommon, but today everyone accepts the complete ban on pushing or shoving the umpire.",
        "answer": "B"
    },
    {
        "id": 37,
        "type": "summary_completion",
        "instruction": "Complete the summary using the list of phrases, A-H, below. Write the correct letter, A-H.",
        "content": "One difference, however, is that during the first game DeJesus used ABS, strike calls were met with <input type='text' data-qid='37' class='ielts-input' placeholder='A-H' />.",
        "answer": "G"
    },
    {
        "id": 38,
        "type": "multiple_choice",
        "instruction": "Choose the correct letter, A, B, C or D.",
        "content": "What does the writer suggest about ABS in the fifth paragraph?<br><label><input type='radio' name='q38' value='A'> A. It is bound to make key decisions that are wrong.</label><br><label><input type='radio' name='q38' value='B'> B. It may reduce some of the appeal of the game.</label><br><label><input type='radio' name='q38' value='C'> C. It will lead to the disappearance of human umpires.</label><br><label><input type='radio' name='q38' value='D'> D. It may increase calls for the rules of baseball to be changed.</label>",
        "answer": "B"
    },
    {
        "id": 39,
        "type": "multiple_choice",
        "instruction": "Choose the correct letter, A, B, C or D.",
        "content": "Morgan Sword says that the introduction of ABS<br><label><input type='radio' name='q39' value='A'> A. was regarded as an experiment without a guaranteed outcome.</label><br><label><input type='radio' name='q39' value='B'> B. was intended to keep up with developments in other sports.</label><br><label><input type='radio' name='q39' value='C'> C. was a response to changing attitudes about the role of sport.</label><br><label><input type='radio' name='q39' value='D'> D. was an attempt to ensure baseball retained a young audience.</label>",
        "answer": "A"
    },
    {
        "id": 40,
        "type": "multiple_choice",
        "instruction": "Choose the correct letter, A, B, C or D.",
        "content": "Why does the writer include the views of Noë and Russo?<br><label><input type='radio' name='q40' value='A'> A. to show that attitudes to technology vary widely</label><br><label><input type='radio' name='q40' value='B'> B. to argue that people have unrealistic expectations of sport</label><br><label><input type='radio' name='q40' value='C'> C. to indicate that accuracy is not the same thing as enjoyment</label><br><label><input type='radio' name='q40' value='D'> D. to suggest that the number of baseball fans needs to increase</label>",
        "answer": "C"
    }
]

c20_t2_reading = {
    "book": 20,
    "test": 2,
    "module": "Reading",
    "title": "Cambridge 20 Reading Test 2",
    "parts": [
        {
            "part_number": 1,
            "title": "Manatees",
            "audio_file": "",
            "passage": html_p1,
            "questions": questions_p1
        },
        {
            "part_number": 2,
            "title": "Procrastination",
            "audio_file": "",
            "passage": html_p2,
            "questions": questions_p2
        },
        {
            "part_number": 3,
            "title": "Invasion of the Robot Umpires",
            "audio_file": "",
            "passage": html_p3,
            "questions": questions_p3
        }
    ]
}

out_path = "extracted_data/c20_test2_reading.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(c20_t2_reading, f, indent=2, ensure_ascii=False)

total_q = sum(len(p['questions']) for p in c20_t2_reading['parts'])
print(f"Successfully compiled {out_path} with {total_q} questions!")
for idx, p in enumerate(c20_t2_reading['parts']):
    print(f"  Part {idx+1}: {p['title']} | Passage length: {len(p['passage'])} chars | Questions: {len(p['questions'])}")
