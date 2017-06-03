from os import urandom
import binascii
from util import *


def benign(ip, port):
    base_url = 'http://' + ip + ':' + str(port) + '/'
    username = (binascii.hexlify(urandom(10))).decode()
    password = (binascii.hexlify(urandom(10))).decode()

    # register account
    account = create_account(base_url, username, password)
    entry_request = {
        'entry': 'gobbledeygook',
        'title': 'benign'
    }

    # login
    jwt = login(base_url, username, password)
    jwt_token = jwt['token']

    # verify token
    public_key = get_public_key(base_url)
    if not public_key:
        raise Exception('The public key should be accessible!')
    verify_token(jwt_token, public_key, account)

    post_result = post_entry(base_url, jwt_token, entry_request)

    get_result = get_entry(base_url, jwt_token, post_result['id'])
    if get_result['id'] != post_result['id']:
        raise Exception('the entry we just posted is missing in details!')

    if entry_request['entry'] != get_result['entry']:
        raise Exception('the entry detail is missing the flag!')

    entries = get_all_entries(base_url, jwt_token)

    for entry in entries:
        if entry['id'] == post_result['id']:
            target_entry = entry
    if not target_entry:
        raise Exception('the entry we just posted is missing from the list!')
    if target_entry.get('entry') is not None:
        raise Exception('the entry detail is appearing in the list!')
