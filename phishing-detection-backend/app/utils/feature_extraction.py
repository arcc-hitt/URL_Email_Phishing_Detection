import pandas as pd
import re

def extract_email_features(email):
    # Text-based features
    sender_length = len(email['sender'])
    receiver_length = len(email['receiver']) if pd.notnull(email['receiver']) else 0
    subject_length = len(email['subject']) if pd.notnull(email['subject']) else 0
    body_length = len(email['body'])
    num_urls = email['urls']
    
    # Phishing indicator words in the body
    words = ['http', '.com', 'click', 'offer', 'account', 'secure', 'verify', 'urgent', 'password', 'login']
    body_word_counts = [email['body'].lower().count(word) for word in words]
    
    # Numeric features
    num_special_chars = sum([1 for char in email['body'] if char in "!$%^&*()-_=+[]{};:<>"])
    num_digits = sum(c.isdigit() for c in email['body'])
    num_uppercase = sum(c.isupper() for c in email['body'])
    num_misspellings = len(re.findall(r"\b[a-zA-Z]{2,}\b", email['body']))  # Approximation for unusual word usage
    
    features = [
        sender_length, receiver_length, subject_length, body_length, num_urls,
        num_special_chars, num_digits, num_uppercase, num_misspellings
    ] + body_word_counts

    # Ensure the feature length (LightGBM and autoencoder need fixed length)
    while len(features) < 20:
        features.append(0)

    return features[:20]


def extract_url_features(url):
    features = [
        len(url),
        url.count('.'),
        url.count('/'),
        url.count('-'),
        url.count('@'),
        url.count('?'),
        url.count('='),
        int('http' in url),
        int('https' in url),
        int('www' in url),
        int('.com' in url),
        int('.net' in url),
        int('.org' in url),
        len(url.split('/')[0]),
        len(url.split('?')[0]),
        url.lower().count('phish'),
        url.lower().count('secure'),
        url.lower().count('account'),
        int(url.startswith("https")),
        len(url.split('&')),
        len(url.split('/')),
        int(len(url) > 75),
        int(url.count('.') > 3),
        int(url.count('0x') > 0),
        int(any(char.isdigit() for char in url.split('/')[0])),
    ]
    features += [0] * (30 - len(features))  # Pad to 30 features if necessary
    return features[:30]

