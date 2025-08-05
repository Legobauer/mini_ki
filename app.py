from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def simple_bot_reply(question):
    q = question.lower()

    match = re.search(r'(\d+[\s]*[\+\-\*/][\s]*\d+)', q)
    if match:
        try:
            return f"{eval(match.group(1))}"
        except:
            return "Sorry, das konnte ich nicht berechnen."

    if re.match(r'^[\d\s\+\-\*/\(\)\.]+$', q):
        try:
            return f"{eval(q)}"
        except:
            return "Sorry, das konnte ich nicht berechnen."

    if "hallo" in q or "hi" in q or "hey" in q or "moin" in q:
        return "Hey! Schön dich zu sehen 😊"
    elif "wie geht" in q:
        return "Mir geht's blendend – ich bin ja aus Code! 🖥️ Und dir?"
    elif "zeit" in q or "uhr" in q or "spät" in q:
        return f"Aktuelle Uhrzeit ⌚: {datetime.now().strftime('%H:%M:%S')}"
    elif "name" in q or "heiß" in q:
        return f"Du heißt übrigens: {session.get('username', 'Gast')}"
    elif "auch" in q:
        return "Freut mich zu hören! 😊 Gibt es was worüber du mit mir reden möchtest?"
    elif "was" in q:
        return "Was ist mir egal, ich bin hier um zu helfen! 😊"

    return "Ich bin noch am Lernen – stell mir einfache Fragen oder rechne mit mir!"

@app.route('/')
def index():
    username = session.get('username')
    history = session.get('history', [])
    return render_template('index.html', username=username, history=history)

@app.route('/set_name', methods=['POST'])
def set_name():
    session['username'] = request.form['username']
    session['history'] = []
    return redirect('/')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    answer = simple_bot_reply(question)

    history = session.get('history', [])
    history.append({'role': 'user', 'content': question})
    history.append({'role': 'bot', 'content': answer})
    session['history'] = history

    return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)

