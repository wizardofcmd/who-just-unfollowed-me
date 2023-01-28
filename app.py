from flask import abort, Flask, render_template
import werkzeug

app = Flask(__name__)

app.register_error_handler(404, werkzeug.exceptions.NotFound)

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")