#!/usr/bin/env python3
"""
Generate authentic Cambridge IELTS 20 Writing modules (Tests 1 to 4).
"""

import json
import os

OUTPUT_DIR = "extracted_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

WRITING_TESTS = {
    1: {
        "task1": {
            "title": "Writing Task 1",
            "prompt": "<p>You should spend about 20 minutes on this task.</p><p><strong>The tables below show changes in the total population of New York City and the breakdown between Manhattan and the outer four boroughs (Brooklyn, Bronx, Queens, and Staten Island) between 1800 and 2000.</strong></p><p>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</p><p>Write at least 150 words.</p>"
        },
        "task2": {
            "title": "Writing Task 2",
            "prompt": "<p>You should spend about 40 minutes on this task.</p><p>Write about the following topic:</p><blockquote style=\"border: 1px solid #000; padding: 15px; margin: 15px 0;\"><p><strong>Access to clean water is a basic human right. Therefore, every home should have a water supply that is provided free of charge.</strong></p><p><strong>Do you agree or disagree?</strong></p></blockquote><p>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p><p>Write at least 250 words.</p>"
        }
    },
    2: {
        "task1": {
            "title": "Writing Task 1",
            "prompt": "<p>You should spend about 20 minutes on this task.</p><p><strong>The maps below show changes to a farm site from 1950 to the present day.</strong></p><p>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</p><p>Write at least 150 words.</p>"
        },
        "task2": {
            "title": "Writing Task 2",
            "prompt": "<p>You should spend about 40 minutes on this task.</p><p>Write about the following topic:</p><blockquote style=\"border: 1px solid #000; padding: 15px; margin: 15px 0;\"><p><strong>Some people think that school children should have long holidays, while others believe that shorter holidays throughout the year are better.</strong></p><p><strong>Discuss both views and give your opinion.</strong></p></blockquote><p>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p><p>Write at least 250 words.</p>"
        }
    },
    3: {
        "task1": {
            "title": "Writing Task 1",
            "prompt": "<p>You should spend about 20 minutes on this task.</p><p><strong>The plans below show the layout of Little Chalfont Public Library in 2010 and following its refurbishment in 2024.</strong></p><p>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</p><p>Write at least 150 words.</p>"
        },
        "task2": {
            "title": "Writing Task 2",
            "prompt": "<p>You should spend about 40 minutes on this task.</p><p>Write about the following topic:</p><blockquote style=\"border: 1px solid #000; padding: 15px; margin: 15px 0;\"><p><strong>In many countries today, people are choosing to buy goods from large supermarket chains rather than local independent shops.</strong></p><p><strong>What are the reasons for this? Do you think this is a positive or negative development?</strong></p></blockquote><p>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p><p>Write at least 250 words.</p>"
        }
    },
    4: {
        "task1": {
            "title": "Writing Task 1",
            "prompt": "<p>You should spend about 20 minutes on this task.</p><p><strong>The diagram below illustrates the process by which fabric is manufactured from bamboo.</strong></p><p>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</p><p>Write at least 150 words.</p>"
        },
        "task2": {
            "title": "Writing Task 2",
            "prompt": "<p>You should spend about 40 minutes on this task.</p><p>Write about the following topic:</p><blockquote style=\"border: 1px solid #000; padding: 15px; margin: 15px 0;\"><p><strong>The increasing popularity of global fashion trends has led to people around the world wearing similar clothes. Some believe this damages local cultural traditions, while others think it is a positive sign of unity.</strong></p><p><strong>Discuss both views and give your opinion.</strong></p></blockquote><p>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</p><p>Write at least 250 words.</p>"
        }
    }
}

for t, data in WRITING_TESTS.items():
    doc = {
        "book": 20,
        "test": t,
        "module": "Writing",
        "title": f"Cambridge 20 Writing Test {t}",
        "parts": [
            {
                "part_number": 1,
                "title": data["task1"]["title"],
                "audio_file": "",
                "passage": data["task1"]["prompt"],
                "questions": [
                    {
                        "id": 1,
                        "type": "fill_in_the_blank",
                        "instruction": "Summarise the information by selecting and reporting the main features. Write at least 150 words.",
                        "content": "<textarea data-qid='1' class='ielts-textarea' rows='15' placeholder='Type your Task 1 response here...'></textarea>",
                        "answer": "Model answer not applicable for writing tasks."
                    }
                ]
            },
            {
                "part_number": 2,
                "title": data["task2"]["title"],
                "audio_file": "",
                "passage": data["task2"]["prompt"],
                "questions": [
                    {
                        "id": 2,
                        "type": "fill_in_the_blank",
                        "instruction": "Discuss the topic in depth. Write at least 250 words.",
                        "content": "<textarea data-qid='2' class='ielts-textarea' rows='20' placeholder='Type your Task 2 response here...'></textarea>",
                        "answer": "Model answer not applicable for writing tasks."
                    }
                ]
            }
        ]
    }
    
    out_file = os.path.join(OUTPUT_DIR, f"c20_test{t}_writing.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    print(f"Generated {out_file} with Task 1 & Task 2 prompts.")

print("All Cambridge 20 Writing tests generated successfully!")
