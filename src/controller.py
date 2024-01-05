import json
import traceback
# from src.main import smart_prompts, rag_chat_stream, template
from flask_cors import CORS, cross_origin
# from flask import Blueprint, request, Response


from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import logging
import os

# from .helper_functions import call_qa_backend , call_word_count_backend, call_login_token_backend, get_templateStructure, get_template_word_count

import openai

openai.api_key = os.getenv("OPENAI_API_KEY",default=None)

app = Flask(__name__)

cors = CORS(app)
            
@app.route('/chat_stream',methods=['POST','OPTIONS'])
@cross_origin()
def streaming_chat_endpoint():
    pass

@app.route('/template',methods=['POST'])
@cross_origin()
def templates_endpoint():
    pass



# Configure Flask-Mail settings
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Update with your SMTP server
app.config['MAIL_PORT'] = 587  # Update with your SMTP port
app.config['MAIL_USERNAME'] = 'your_username@example.com'  # Update with your email username
app.config['MAIL_PASSWORD'] = 'your_password'  # Update with your email password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Configure logger
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        file = request.files['file']

        if email and file:
            # Save uploaded file
            file.save(file.filename)
            logging.info(f"File '{file.filename}' uploaded successfully.")

            # Read file contents
            with open(file.filename, 'r') as f:
                file_contents = f.read()

            print(file_contents)
            # # Send email
            # try:
            #     msg = Message('File Contents', sender='your_email@example.com', recipients=[email])
            #     msg.body = file_contents
            #     mail.send(msg)
            #     logging.info(f"Email sent to {email} with file contents.")
            # except Exception as e:
            #     logging.error(f"Failed to send email to {email}. Error: {str(e)}")

            return redirect(url_for('index'))

    return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
