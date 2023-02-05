import base64
import hashlib
import json
import os
import re
import redis
import requests
from requests_oauthlib import OAuth2Session
from flask import Flask, render_template, redirect, request, session
import werkzeug

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.secret_key = os.urandom(50)

r = redis.from_url(app.config.get("REDIS_URL"))

app.register_error_handler(404, werkzeug.exceptions.NotFound)


def make_token():
    return OAuth2Session(app.config.get("CLIENT_ID"),
                         redirect_uri=app.config.get("REDIRECT_URI"),
                         scope=["tweet.read", "users.read", "follows.read",
                                "offline.access"])


def get_user_details(token):
    response = requests.request(
        "GET",
        "https://api.twitter.com/2/users/me",
        headers={
            "Authorization": "Bearer {}".format(token),
            "Content-Type": "application/json",
        },
        params={"user.fields": "id,username"}
    )

    return response.json()


def get_following(user_id, token):
    response = requests.request(
        "GET",
        f"https://api.twitter.com/2/users/{user_id}/following",
        headers={
            "Authorization": "Bearer {}".format(token),
            "Content-Type": "application/json",
        }
    )

    return response.json()


@app.route("/", methods=["GET"])
def index():
    app.logger.info(r)
    return render_template("index.html")


@app.route("/login")
def login():
    global twitter
    global code_verifier

    twitter = make_token()

    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")

    authorization_url, state = twitter.authorization_url(
        "https://twitter.com/i/oauth2/authorize",
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/oauth/callback", methods=["GET"])
def callback():
    code = request.args.get("code")

    token = twitter.fetch_token(
        token_url="https://api.twitter.com/2/oauth2/token",
        client_secret=app.config.get("CLIENT_SECRET"),
        code_verifier=code_verifier,
        code=code,
    )
    st_token = '"{}"'.format(token)
    j_token = json.loads(st_token)
    r.set("token", j_token)

    user_details = get_user_details(token["access_token"])
    following = get_following(user_details["data"]["id"],
                              token["access_token"])
    app.logger.info(following)
    return f"{user_details}"
