# AI automation developer assignment
A repo to exhibit skills to create a ChatGPT powered summary generating and emailing application
Follow the following steps to launch the application (tested on UNIX based systems - not windows OS):
1. Clone the repo and go to its folder. 
2. Create a python environment:
  ```python -m venv env```
3. Acitvate the created environment:
  ```source activate ./env/bin/activate```
4. Install the requirements of this application:
  ```pip install -r ./requirements.txt```
5. **Update your system environment variables**. You can check [here](https://www3.ntu.edu.sg/home/ehchua/programming/howto/Environment_Variables.html) to figure out how to set environment variables. Following variables are needed by this applciation:
  1. OPENAI_API_KEY *api key from openai to enable usage of chatGPT*
  2. MAIL_SERVER  *DNS address of the mailing server that you would like to use to send email from. for Gmail it is ususally "smtp.gmail.com"*
  3. MAIL_PORT *Port at which the DNS server of the mailing server listens to. For Gmail it is usually 587*
  4. MAIL_USERNAME *The email address from which you will be sending emails e.g.* ********@gmail.com*
  5. MAIL_PASSWORD *Password that enables access to your mailing server. For Gmail this is the 16 digit "App password" especially created for third party applications*
6. Run the application by invoking the "main.py" file:
  ```python ./main.py```