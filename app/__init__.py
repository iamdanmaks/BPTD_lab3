from flask import Flask


app = Flask(__name__)
app.config.update(
    SECRET_KEY='шифр'
)


from app import routes
