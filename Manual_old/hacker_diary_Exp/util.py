import requests
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, HMAC
from Crypto.Signature import PKCS1_v1_5
import base64
import json


def create_account(base_url, username, password):
    credentials = {
        'username': username,
        'password': password
    }
    # create account
    response = requests.post(base_url + 'register/', data=json.dumps(credentials),
                             headers={'Content-Type': 'application/json'})
    if response.status_code != requests.codes.created:
        response.raise_for_status()
    return response.json()


def login(base_url, username, password):
    credentials = {
        'username': username,
        'password': password
    }
    response = requests.post(base_url + 'login/', data=json.dumps(credentials),
                             headers={'Content-Type': 'application/json'})
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    return response.json()


def post_entry(base_url, jwt_token, entry):
    headers = {
        'Authorization': 'JWT ' + jwt_token,
        'Content-Type': 'application/json'
    }
    response = requests.post(base_url + 'entries/', headers=headers, data=json.dumps(entry))
    if response.status_code != requests.codes.created:
        response.raise_for_status()
    return response.json()


def get_public_key(base_url):
    response = requests.get(base_url + 'public_key/')
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    return response.json().get('public_key')


def verify_token(jwt_token, public_key, account):
    (header, body, signature) = jwt_token.split('.')
    header_decoded = json.loads(base64.b64decode(header).decode())
    if header_decoded['typ'] != 'JWT' or header_decoded['alg'] != 'RS256':
        raise Exception('JWT token has invalid type or algorithm!')

    body_decoded = json.loads(base64.b64decode(body).decode())
    if body_decoded['username'] != account['username']:
        raise Exception('JWT token payload has the wrong username!')

        #
        # key = RSA.importKey(public_key)
        # message = HMAC.new(public_key.encode(), (header + '.' + body).encode(), SHA256)
        # verifier = PKCS1_v1_5.new(key)
        # if not verifier.verify(message, signature):
        #     raise Exception('JWT token signature failed to match public key!')


def get_entry(base_url, jwt_token, entry_id):
    headers = {
        'Authorization': 'JWT ' + jwt_token
    }
    response = requests.get(base_url + 'entries/' + str(entry_id), headers=headers)
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    return response.json()


def get_all_entries(base_url, jwt_token):
    headers = {
        'Authorization': 'JWT ' + jwt_token
    }
    response = requests.get(base_url + 'entries/', headers=headers)
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    return response.json()
