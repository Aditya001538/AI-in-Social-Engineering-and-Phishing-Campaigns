from flask import Flask, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load and prepare data
data = pd.read_csv("phishing_emails.csv")
X = data["text"]
y = data["label"]

vectorizer = TfidfVectorizer(stop_words="english")
X_vec = vectorizer.fit_transform(X)

model = MultinomialNB()
model.fit(X_vec, y)

# Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def detect():
    if request.method == "POST":
        email_text = request.form["email"]
        email_vec = vectorizer.transform([email_text])
        result = model.predict(email_vec)[0]
        label = "Phishing Email" if result == 1 else "Legitimate Email"
        return f"<h2>Result: {label}</h2><br><a href='/'>Try Again</a>"
    
    return '''
        <form method="post">
            <textarea name="email" rows="10" cols="50" placeholder="Paste email text here..."></textarea><br>
            <input type="submit" value="Check Email">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
