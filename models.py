import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

data = {
    "email_text": [
        "I need help with my bill payment.",
        "My account isn't accessible.",
        "Need technical support urgently!",
        "Can you assist with a change in my address?"
    ],
    "label": ["Billing Issues", "Account Management", "Technical Support", "Change"]
}

df = pd.DataFrame(data)

model = make_pipeline(
    CountVectorizer(),
    MultinomialNB()
)

model.fit(df["email_text"], df["label"])

def classify_email(text):
    return model.predict([text])[0]
