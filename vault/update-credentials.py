#!/usr/bin/env python
import json
import base64
import os

import redis


if __name__ == '__main__':
    log_file = '/var/log/app.log'

    print('Looking for root token in: %s' % log_file)

    tokens = []
    with open(log_file) as log:
        for line in log:
            if line.startswith('Root Token'):
                tokens.append(line.strip())

    token = tokens[-1].split(' ')[-1]

    print('Found root token: %s' % token)
    print('Saving token in redis')

    relationships = json.loads(base64.b64decode(os.environ["PLATFORM_RELATIONSHIPS"]))
    r = redis.StrictRedis(host=relationships['redis'][0]['host'], port=relationships['redis'][0]['port'], db=0)
    if r.set('token', token):
        print('Token saved in redis as `token`')
    else:
        print('Error saving in redis')
