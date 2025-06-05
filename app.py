from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=incoming_msg,
            max_tokens=150,
            temperature=0.7,
        )
        answer = response.choices[0].text.strip()
        msg.body(answer)
    else:
        msg.body("Désolé, je n'ai pas compris.")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
