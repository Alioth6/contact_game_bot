from os import environ as env


class Config:
    TOKEN = env['TOKEN']

    WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0'

    MODEL_FILE_NAME = 'ft_freqprune_100K_20K_pq_300.bin'
    NOUNS_FILE_NAME = 'freq_nouns.txt'

    if env['APP_CONFIG'] == 'local':
        WEBHOOK_HOST = env['WEBHOOK_HOST']

        DATA_PATH = 'data/'

    elif env['APP_CONFIG'] == 'heroku':
        WEBHOOK_HOST = 'https://intense-cove-71886.herokuapp.com'
        WEBHOOK_PORT = env['AWS_ACCESS_KEY_ID']

        DATA_PATH = ''.join([
            's3://',
            env['AWS_ACCESS_KEY_ID'],
            ":",
            env['AWS_SECRET_ACCESS_KEY'],
            '@',
            env['S3_BUCKET_NAME'],
            '/'
        ])
