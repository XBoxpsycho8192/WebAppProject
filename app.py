from flask import Flask
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

# This file is what actually starts and runs the web app.
if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
