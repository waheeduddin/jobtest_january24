from src import app
import os

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=os.getenv("PORT",default=8080), debug = False)
