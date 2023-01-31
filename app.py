import requests
from flask import Flask, render_template, redirect, request, url_for
import tweepy
import werkzeug

app = Flask(__name__)
app.config.from_pyfile('settings.py')

app.register_error_handler(404, werkzeug.exceptions.NotFound)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    client_id = app.config.get("TWITTER_CLIENT_ID")
    client_secret = app.config.get("TWITTER_CLIENT_SECRET")
    
    auth = tweepy.OAuth2UserHandler(
        redirect_uri=redirect_uri, client_id=client_id, 
        client_secret=client_secret, 
        scope=["tweet.read users.read follows.read"]
    )
    return redirect(auth.get_authorization_url())


@app.route("/authorize", methods=["GET", "POST"])
def authorize():
    return "Authorized?"
