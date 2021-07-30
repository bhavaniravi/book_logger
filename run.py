from application.app import app, db

from flask import json
from werkzeug.exceptions import HTTPException
import traceback

@app.route("/")
def home():
    try:
        return "Hello, World!"
    except AttributeError as e:
        return {"exception": traceback.format_exc()}, 500

if __name__ == "__main__":
    app.run(debug=True)