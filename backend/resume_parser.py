import json
import pandas as pd
from docx import Document

    
def extract_all_text(doc_path):
    doc = Document(doc_path)
    all_text = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            all_text.append(text)

    return {"all_text": all_text}


def save_to_files(data, json_path):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)


data = extract_all_text("../data/resume.docx")
save_to_files(data, "../data/resume.json")
