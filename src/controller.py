import json
import traceback
from flask_cors import CORS, cross_origin


from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import logging
from config import Config
from .helpers import create_summary

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
            file.save(file.filename)
            logging.info(f"File '{file.filename}' uploaded successfully.")

            # Read file contents
            with open(file.filename, 'r') as f:
                file_contents = f.read()
            
            print(create_summary(file_contents,openai_api_key=config.get_property("OPENAI_API_KEY")))
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
