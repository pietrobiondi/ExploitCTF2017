from Crypto import Random
import binascii
from util import *


def set_flag(ip, port, flag):
    base_url = 'http://' + ip + ':' + str(port) + '/'
    username = (binascii.hexlify(Random.get_random_bytes(10))).decode()
    password = (binascii.hexlify(Random.get_random_bytes(10))).decode()

    account = create_account(base_url, username, password)
    entry_request = {
        'entry': flag,
        'title': 'flag'
    }

    # login
    jwt = login(base_url, username, password)
    jwt_token = jwt['token']

    # verify token
    public_key = get_public_key(base_url)
    verify_token(jwt_token, public_key, account)
    entry = post_entry(base_url, jwt_token, entry_request)

    # return entryid
    return {
        'FLAG_ID': entry['id'],
        'TOKEN': jwt_token
    }


