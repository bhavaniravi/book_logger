from application.app import app

# Import your models here
from application.models import User

@app.route("/")
def home():
    return {"Status": "Success"}, 200 

# Write your API endpoints here