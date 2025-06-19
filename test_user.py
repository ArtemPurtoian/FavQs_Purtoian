import requests
import pytest


# constants to use throughout the tests
AUTH_TOKEN = "Token token=6b6d9294961815b760fa4f8427d71b4d"
BASE_URL = "https://favqs.com/api"


"""
fixture that creates a user using AUTH_TOKEN, request payload
and returns user credentials
"""
@pytest.fixture(scope="session")
def create_user():
    url_create_user = f"{BASE_URL}/users"

    headers = {
        "Authorization": f"{AUTH_TOKEN}"
    }

    login = "useruser16" # to be changed before running pytest
    email = "useruser16@gmail.com" # to be changed before running pytest
    password = "userpassword"

    payload = {
        "user": {
            "login": login,
            "email": email,
            "password": password
        }
    }

    # sending a POST request
    response_create = requests.post(url_create_user, json=payload,
                                    headers=headers)
    # json object from the response
    response_json_create = response_create.json()

    print(f"\nPOST response ({response_create.status_code}):\n",
          response_json_create)

    """
    getting the user token and login from the POST response and
    assigning it to the variables
    """
    user_token = response_create.json()["User-Token"]
    user_login_created = response_create.json()["login"]

    return {
        "user_token": user_token,
        "user_login": user_login_created,
        "email": payload["user"]["email"]
    }

# creating and getting a user
def test_get_user(create_user):
    user_token = create_user["user_token"]
    user_login = create_user["user_login"]
    url_get_user = f"{BASE_URL}/users/{user_login}"

    headers_user = {
        "Authorization": f"{AUTH_TOKEN}",
        "User-Token": f"{user_token}"
    }

    # sending a GET request after creating the user
    response_get = requests.get(url_get_user, headers=headers_user)
    response_json_get = response_get.json()

    print(f"GET response ({response_get.status_code}):\n", response_json_get)

    # getting login and email from the json object
    user_get_login = response_json_get["login"]
    user_get_email = response_json_get["account_details"]["email"]

    # checking login and email after creation
    assert user_get_login == user_login
    assert user_get_email == create_user["email"]

# updating a user
def test_update_user(create_user):
    user_token = create_user["user_token"]
    user_login = create_user["user_login"]
    user_email = create_user["email"]
    url = f"{BASE_URL}/users/{user_login}"

    headers = {
        "Authorization": f"{AUTH_TOKEN}",
        "User-Token": f"{user_token}"
    }

    # pattern for updating login and email
    updated_login = user_login + "_updated"
    updated_email = "updated_" + user_email

    payload = {
        "user": {
            "login": f"{updated_login}",
            "email": f"{updated_email}"
        }
    }

    # sending a PUT request to update the user
    response_put = requests.put(url, json=payload, headers=headers)
    response_json_put = response_put.json()

    print(f"PUT response ({response_put.status_code}):\n", response_json_put)

    url_updated_user = f"{BASE_URL}/users/{updated_login}"
    response_get = requests.get(url_updated_user, headers=headers)
    response_json_get = response_get.json()

    print(f"GET response ({response_get.status_code}):\n", response_json_get)

    # getting login and email from the json object
    user_get_login = response_json_get["login"]
    user_get_email = response_json_get["account_details"]["email"]

    # checking login and email are updated
    assert user_get_login == updated_login
    assert user_get_email == updated_email
