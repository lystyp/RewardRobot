import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    print("port = " + str(os.environ.get('PORT', 5000)))
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
