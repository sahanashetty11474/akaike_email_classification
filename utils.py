import re
import spacy

nlp = spacy.load("en_core_web_sm")

patterns = {
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "phone_number": re.compile(r"\b\d{10}\b"),
    "dob": re.compile(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"),
    "aadhar_num": re.compile(r"\b\d{12}\b"),
    "credit_debit_no": re.compile(r"\b\d{16}\b"),
    "cvv_no": re.compile(r"\b\d{3}\b"),
    "expiry_no": re.compile(r"\b(0[1-9]|1[0-2])\/\d{2,4}\b"),
}

def mask_pii(text):
    masked_text = text
    entities = []

    replacements = []

    for entity_type, pattern in patterns.items():
        for match in pattern.finditer(masked_text):
            start, end = match.span()
            entity_val = match.group()
            placeholder = f"[{entity_type}]"
            replacements.append((start, end, placeholder, entity_type, entity_val))

    doc = nlp(masked_text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            start, end = ent.start_char, ent.end_char
            entity_val = ent.text
            placeholder = "[full_name]"
            replacements.append((start, end, placeholder, "full_name", entity_val))

    replacements.sort(key=lambda x: x[0], reverse=True)

    for start, end, placeholder, entity_type, entity_val in replacements:
        masked_text = masked_text[:start] + placeholder + masked_text[end:]
        entities.insert(0, {
            "position": [start, start + len(placeholder)],
            "classification": entity_type,
            "entity": entity_val
        })

    return masked_text, entities
