#!/usr/bin/env python3
"""
Complete, High-Precision Cambridge 16 Extractor for CD-IELTS Simulator.
Extracts all 4 tests (Listening, Reading, Writing) directly from digital text in
'Cambridge IELTS 16/Cambridge IELTS 16.pdf' using Gemini flash-lite and official answer keys.
"""

import os
import sys
import json
import re
import time
from pathlib import Path
import pymupdf
from google import genai
from google.genai import types

# Auto-load .env
env_file = Path(__file__).resolve().parent.parent / ".env"
if env_file.is_file():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))

API_KEY = os.getenv("GEMINI_API_KEY", "")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found in environment or .env!")
    sys.exit(1)

PDF_PATH = "Cambridge IELTS 16/Cambridge IELTS 16.pdf"
OUTPUT_DIR = "extracted_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

C16_CONFIG = {
    1: {
        "Listening": {
            "pages": list(range(11, 17)),
            "ans_page": 122,
            "audio_files": [
                "Test 1 Part 1[@cambridgematerials].mp3",
                "Test 1 Part 2[@cambridgematerials].mp3",
                "Test 1 Part 3[@cambridgematerials].mp3",
                "Test 1 Part 4[@cambridgematerials].mp3"
            ]
        },
        "Reading": {
            "pages": list(range(17, 30)),
            "ans_page": 123,
            "audio_files": []
        },
        "Writing": {
            "pages": [30, 31],
            "ans_page": None,
            "audio_files": []
        }
    },
    2: {
        "Listening": {
            "pages": list(range(33, 39)),
            "ans_page": 124,
            "audio_files": [
                "Test 2 Part 1[@cambridgematerials].mp3",
                "Test 2 Part 2[@cambridgematerials].mp3",
                "Test 2 Part 3[@cambridgematerials].mp3",
                "Test 2 Part 4[@cambridgematerials].mp3"
            ]
        },
        "Reading": {
            "pages": list(range(39, 53)),
            "ans_page": 125,
            "audio_files": []
        },
        "Writing": {
            "pages": [53, 54],
            "ans_page": None,
            "audio_files": []
        }
    },
    3: {
        "Listening": {
            "pages": list(range(56, 62)),
            "ans_page": 126,
            "audio_files": [
                "Test 3 Part 1[@cambridgematerials].mp3",
                "Test 3 Part 2[@cambridgematerials].mp3",
                "Test 3 Part 3[@cambridgematerials].mp3",
                "Test 3 Part 4[@cambridgematerials].mp3"
            ]
        },
        "Reading": {
            "pages": list(range(62, 74)),
            "ans_page": 127,
            "audio_files": []
        },
        "Writing": {
            "pages": [74, 75],
            "ans_page": None,
            "audio_files": []
        }
    },
    4: {
        "Listening": {
            "pages": list(range(77, 83)),
            "ans_page": 128,
            "audio_files": [
                "Test 4 Part 1[@cambridgematerials].mp3",
                "Test 4 Part 2[@cambridgematerials].mp3",
                "Test 4 Part 3[@cambridgematerials].mp3",
                "Test 4 Part 4[@cambridgematerials].mp3"
            ]
        },
        "Reading": {
            "pages": list(range(83, 96)),
            "ans_page": 129,
            "audio_files": []
        },
        "Writing": {
            "pages": [96, 97],
            "ans_page": None,
            "audio_files": []
        }
    }
}

SYSTEM_PROMPT = """You are an automated structural data formatting utility for educational testing simulators.
Your sole function is to format assessment practice tests into valid CD-IELTS JSON schema.
- All passages verbatim in HTML <p> and <h3> tags.
- All 40 questions (Reading/Listening) or 2 tasks (Writing), IDs 1-40.
- Blanks: <input type='text' data-qid='<id>' class='ielts-input' />
- Multiple choice / TFNG: proper input radio/checkbox elements.
- Official correct answer extracted into 'answer'. Never leave 'answer' empty for Listening/Reading.
"""

def extract_module(client, doc, test_num, module_name, cfg):
    out_file = os.path.join(OUTPUT_DIR, f"c16_test{test_num}_{module_name.lower()}.json")
    print(f"\n=======================================================")
    print(f"Extracting Cambridge 16 Test {test_num} {module_name}...")
    print(f"=======================================================")
    
    pages = cfg["pages"]
    ans_page = cfg["ans_page"]
    audio_files = cfg["audio_files"]
    
    content_text = "\n--- PAGE BREAK ---\n".join([doc[p - 1].get_text() for p in pages])
    ans_text = doc[ans_page - 1].get_text() if ans_page else "Writing task - no short answers."
    
    prompt = f"""{SYSTEM_PROMPT}

Format Cambridge 16 Test {test_num} {module_name} into CD-IELTS JSON schema.
Module: {module_name}
Associated audio files: {json.dumps(audio_files)}

Content:
{content_text}

Answer Key / Explanations:
{ans_text}

Return valid JSON:
{{
  "book": 16,
  "test": {test_num},
  "module": "{module_name}",
  "title": "Cambridge 16 {module_name} Test {test_num}",
  "parts": [
    {{
      "part_number": 1,
      "title": "Part/Passage Title",
      "audio_file": "relative_audio_or_empty_str",
      "passage": "<h3>Title</h3><p>Full passage text...</p>",
      "questions": [
        {{
          "id": 1,
          "type": "fill_in_the_blank|multiple_choice|true_false_not_given|yes_no_not_given|matching_headings|summary_completion",
          "instruction": "...",
          "content": "HTML question content",
          "answer": "Official answer"
        }}
      ]
    }}
  ]
}}
"""

    if os.path.exists(out_file):
        try:
            with open(out_file, "r", encoding="utf-8") as fp:
                existing = json.load(fp)
            tot_q = sum(len(p.get("questions", [])) for p in existing.get("parts", []))
            target_min = 2 if module_name == "Writing" else 40
            if tot_q >= target_min:
                print(f"  Skipping {out_file} (already extracted with {tot_q} questions).")
                return True
        except Exception:
            pass

    models = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.5-flash"]
    for m in models:
        for attempt in range(3):
            try:
                print(f"  Attempting with {m} (attempt {attempt+1})...")
                resp = client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                text = resp.text or ""
                cleaned = re.sub(r"^```json\s*", "", text.strip())
                cleaned = re.sub(r"\s*```$", "", cleaned.strip())
                data = json.loads(cleaned)
                
                data["book"] = 16
                data["test"] = test_num
                data["module"] = module_name
                data["title"] = f"Cambridge 16 {module_name} Test {test_num}"
                
                # Ensure audio files are assigned to parts if Listening
                if module_name == "Listening" and "parts" in data:
                    for idx, part in enumerate(data["parts"]):
                        if idx < len(audio_files):
                            part["audio_file"] = audio_files[idx]
                
                with open(out_file, "w", encoding="utf-8") as fp:
                    json.dump(data, fp, indent=2, ensure_ascii=False)
                    
                total_q = sum(len(p.get("questions", [])) for p in data.get("parts", []))
                print(f"  SUCCESS! Saved {out_file} with {len(data.get('parts', []))} part(s) and {total_q} questions.")
                return True
            except Exception as e:
                err_str = str(e)
                print(f"  Error with {m}: {err_str[:150]}")
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    print("  Rate limit encountered. Sleeping 20 seconds...")
                    time.sleep(20)
                else:
                    time.sleep(5)
    return False

def main():
    print("Starting Cambridge 16 Complete Extraction Suite...")
    doc = pymupdf.open(PDF_PATH)
    client = genai.Client(api_key=API_KEY)
    
    success_count = 0
    total_count = 0
    
    for t in [1, 2, 3, 4]:
        for mod in ["Listening", "Reading", "Writing"]:
            total_count += 1
            cfg = C16_CONFIG[t][mod]
            ok = extract_module(client, doc, t, mod, cfg)
            if ok:
                success_count += 1
            time.sleep(6) # safe RPM delay
            
    print(f"\n=======================================================")
    print(f"FINISHED! Successfully extracted {success_count}/{total_count} modules for Cambridge 16.")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
