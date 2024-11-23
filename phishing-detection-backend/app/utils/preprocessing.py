import re

def clean_text(text):
    """
    Preprocesses email text by removing unnecessary characters, URLs, and other irrelevant parts.
    """
    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove special characters and extra whitespaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Tokenize common phishing patterns
    text = re.sub(r'\bclick here\b', 'click_here', text)
    text = re.sub(r'\bverify your account\b', 'verify_account', text)
    text = re.sub(r'\blogin\b', 'login', text)
    text = re.sub(r'\bupdate\b', 'update', text)
    text = re.sub(r'\bbank\b', 'bank', text)
    text = re.sub(r'\bpassword\b', 'password', text)

    return text
