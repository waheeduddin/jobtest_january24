from src import app, config
import os

if __name__ == "__main__":
    if config.check_config():
        app.run(host = '0.0.0.0', port=os.getenv("PORT",default=8080), debug = False)
    else:
        print("CLOSING THE APPLICATION!")
