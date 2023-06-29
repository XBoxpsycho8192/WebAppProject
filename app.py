from flask import Flask
from models import db, DB_NAME
from views import views


app = Flask(__name__)
app.secret_key = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.register_blueprint(views, url_prefix="/")



@app.before_request
def create_tables():
    db.create_all()


# This file is what actually starts and runs the web app.
if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
