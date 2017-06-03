from util import *


def get_flag(ip, port, flag_id, token):
    base_url = 'http://' + ip + ':' + str(port) + '/'
    entry = get_entry(base_url, token, flag_id)
    return {'FLAG': entry['entry']}
