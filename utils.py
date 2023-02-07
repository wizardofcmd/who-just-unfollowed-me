import base64
import requests
from requests_oauthlib import OAuth2Session


def get_oauth2_session(client_id, redirect_uri, scopes):
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)


def get_refresh_token(oauth2_session, config, refresh_token):
    basic_auth = base64.b64encode(
        str.encode(f'{config.get("CLIENT_ID")}:'
                   f'{config.get("CLIENT_SECRET")}'))
    basic_auth = \
        basic_auth.decode('ascii')

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': f'Basic {basic_auth}'
    }

    refreshed_token = oauth2_session.refresh_token(
        client_id=config.get("CLIENT_ID"),
        client_secret=config.get("CLIENT_SECRET"),
        token_url=config.get("TOKEN_URL"),
        headers=headers,
        refresh_token=refresh_token,
    )

    return refreshed_token


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


def get_followers(user_id, token):
    response = requests.request(
        "GET",
        f"https://api.twitter.com/2/users/{user_id}/followers",
        headers={
            "Authorization": "Bearer {}".format(token),
            "Content-Type": "application/json",
        }
    )

    return response.json()
