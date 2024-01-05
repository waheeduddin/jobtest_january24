import json
import traceback
import os
from flask_cors import CORS, cross_origin


from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import logging
from config import Config
from .helpers import query_chatGPT, summary_prompt, action_item_table_prompt

config = Config()

app = Flask(__name__)

cors = CORS(app)

# Configure Flask-Mail settings
app.config['MAIL_SERVER'] = config.get_property("MAIL_SERVER")
app.config['MAIL_PORT'] = config.get_property("MAIL_PORT")  # Update with your SMTP port
app.config['MAIL_USERNAME'] = config.get_property("MAIL_USERNAME")  # Update with your email username
app.config['MAIL_PASSWORD'] = config.get_property("MAIL_PASSWORD")  # Update with your email password
app.config['MAIL_USE_TLS'] = config.get_property("MAIL_USE_TLS")
app.config['MAIL_USE_SSL'] = config.get_property("MAIL_USE_SSL")

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
            file.save("temp_text_file.txt")
            logging.info(f"File '{file.filename}' uploaded successfully.")

            # Read file contents
            with open("temp_text_file.txt", 'r') as f:
                file_contents = f.read()
            
            summary = query_chatGPT(prompt=summary_prompt,text_data=file_contents,openai_api_key=config.get_property("OPENAI_API_KEY"))
            action_item_table = query_chatGPT(prompt=action_item_table_prompt,text_data=file_contents,openai_api_key=config.get_property("OPENAI_API_KEY"))

            # # Send email
            try:
                msg = Message('Summary of the transcritpion', sender=config.get_property("MAIL_USERNAME"), recipients=[email])
                msg.body = summary
                mail.send(msg)
                logging.info(f"Email sent to {email} with summary.")
            except Exception as e:
                print("email failed")
                logging.error(f"Failed to send email to {email}. Error: {str(e)}")
            
            try:
                msg = Message('action item table of the transcription', sender=config.get_property("MAIL_USERNAME"), recipients=[email])
                msg.body = action_item_table
                mail.send(msg)
                logging.info(f"Email sent to {email} with action items.")
            except Exception as e:
                print("email failed")
                logging.error(f"Failed to send email to {email}. Error: {str(e)}")

            os.remove("temp_text_file.txt")
            return redirect(url_for('index'))

    return render_template('index.html')

