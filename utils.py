import json
import requests
from requests_oauthlib import OAuth2Session


def get_oauth2_session(client_id, redirect_uri, scopes):
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)


def get_refresh_token(redis_obj, oauth2_session, config):
    t = redis_obj.get("token")

    refreshed_token = oauth2_session.refresh_token(
        client_id=config.get("CLIENT_ID"),
        client_secret=config.get("CLIENT_SECRET"),
        token_url=config.get("TOKEN_URL"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        params={"grant-type": "refresh_token"},
        refresh_token=t,
    )

    st_refreshed_token = '"{}"'.format(refreshed_token)
    j_refreshed_token = json.loads(st_refreshed_token)
    redis_obj.set("refresh_token", j_refreshed_token)

    return j_refreshed_token


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
