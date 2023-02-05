import requests


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
