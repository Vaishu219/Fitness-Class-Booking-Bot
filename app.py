from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

classes = {
    "yoga": ["7 AM", "6 PM"],
    "zumba": ["8 AM", "7 PM"],
    "cardio": ["6 AM", "5 PM"]
}

selected_class = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global selected_class
    user_msg = request.json["message"].lower()

    if "hi" in user_msg or "hello" in user_msg:
        return jsonify(reply="Hello! Available classes: Yoga, Zumba, Cardio")

    if user_msg in classes:
        selected_class = user_msg
        times = ", ".join(classes[user_msg])
        return jsonify(reply=f"{user_msg.capitalize()} available at {times}. Choose a time.")

    if selected_class != "" and ("am" in user_msg or "pm" in user_msg):
        return jsonify(reply=f"✅ Your {selected_class.capitalize()} class at {user_msg} is booked!")

    return jsonify(reply="Please select a class: Yoga, Zumba, or Cardio")

if __name__ == "__main__":
    app.run(debug=True)