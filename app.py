from flask import Flask, render_template, request
from groq import Groq
from flask_cors import CORS
from dotenv import load_dotenv
import os
app = Flask(__name__)
CORS(app)

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        user_story = request.form["user_story"]

        try:
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": f"Generate from 6 to 10 positive and negative effective test cases for: {user_story}"
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1
            )

            result = completion.choices[0].message.content

        except Exception as e:
            result = f"Error: {e}"

        return render_template("result.html", user_story=user_story, result=result)

    return render_template("index.html")

# ✅ تشغيل السيرفر
if __name__ == "__main__":
    app.run(debug=True)
