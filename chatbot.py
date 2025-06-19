from flask import Flask, request, render_template, redirect, url_for, session
from file_picker import pick_file
from processor import process_file
from qa_engine import get_qa_chain
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

file_path = pick_file()
if not file_path:
    print("No file selected.")
    exit()

vectorstore = process_file(file_path)
qa_chain = get_qa_chain(vectorstore)


@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        user_input = request.form['message']
        session['chat_history'].append(('You', user_input))

        # If user asks to call or book appointment
        if 'call' in user_input.lower() or 'appointment' in user_input.lower():
            return redirect(url_for('form'))

        # Get bot response
        bot_response = qa_chain.run(user_input)
        session['chat_history'].append(('Bot', bot_response))
        session.modified = True

    return render_template('chat.html', chat_history=session['chat_history'])


@app.route('/form', methods=['GET', 'POST'])
def form():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        date = request.form['date']

        # Basic validations
        if not phone.isdigit() or len(phone) < 7:
            error = 'Invalid phone number.'
        elif '@' not in email or '.' not in email:
            error = 'Invalid email address.'
        else:
            session['chat_history'].append(('Bot', f"Appointment booked for {name} on {date}."))
            return redirect(url_for('chat'))

    return render_template('form.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
