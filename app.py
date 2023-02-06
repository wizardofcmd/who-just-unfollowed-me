import base64
import hashlib
import json
import os
import re
import redis
from requests_oauthlib import OAuth2Session
from flask import Flask, render_template, redirect, request, session
import werkzeug
from utils import get_oauth2_session, get_refresh_token, get_user_details

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.secret_key = os.urandom(50)

r = redis.from_url(app.config.get("REDIS_URL"))

app.register_error_handler(404, werkzeug.exceptions.NotFound)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    global twitter
    global code_verifier

    twitter = get_oauth2_session(app.config.get("CLIENT_ID"),
                                 app.config.get("REDIRECT_URI"),
                                 ["tweet.read", "users.read", "follows.read",
                                  "offline.access"])

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
        token_url=app.config.get("TOKEN_URL"),
        client_secret=app.config.get("CLIENT_SECRET"),
        code_verifier=code_verifier,
        code=code,
    )

    r.set("token", token["access_token"])
    user_details = get_user_details(token["access_token"])

    basic_auth = base64.b64encode(
        str.encode(f'{app.config.get("CLIENT_ID")}:'
                   f'{app.config.get("CLIENT_SECRET")}'))
    basic_auth = \
        basic_auth.decode('ascii')

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': f'Basic {basic_auth}'
    }

    tokens = {"token": token}
    t = tokens["token"]
    refreshed_token = twitter.refresh_token(
        client_id=app.config.get("CLIENT_ID"),
        client_secret=app.config.get("CLIENT_SECRET"),
        token_url=app.config.get("TOKEN_URL"),
        refresh_token=t["refresh_token"],
        headers=headers
    )

    tokens.update({"new_token": refreshed_token})
    # refresh_token = get_refresh_token(r, twitter, app.config)

    return f"User:\t{user_details}\nOAuth Token:\t{token['access_token']}" \
           f"\nRefreshed token:\t{tokens['new_token']}"
