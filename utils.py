import re

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def mask_pii(text):
    # Example: Replace email addresses
    text = re.sub(r'\b[\w.-]+?@\w+?\.\w+\b', '[EMAIL]', text)
    return text
