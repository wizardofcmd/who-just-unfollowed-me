from flask import Flask, render_template
import werkzeug

app = Flask(__name__)
app.config.from_pyfile('settings.py')

app.register_error_handler(404, werkzeug.exceptions.NotFound)


@app.route("/", methods=["GET"])
def index():
    app.logger.info(f"{app.config}")
    return render_template("index.html")