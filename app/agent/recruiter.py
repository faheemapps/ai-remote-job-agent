import re
EMAIL = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PHONE = r"(?:\+?\d[\d\s().-]{7,}\d)"

def extract_contacts(text):
    return {
        "emails": list(dict.fromkeys(re.findall(EMAIL, text or "")))[:5],
        "phones": list(dict.fromkeys(re.findall(PHONE, text or "")))[:5],
    }
