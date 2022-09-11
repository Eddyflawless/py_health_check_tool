import os
import configparser

def getConfiguations():
    config = {}
    # aws configuration
    config['region_name'] = os.environ.get('AWS_REGION')
    config['aws_access_key_id'] = os.environ.get('AWS_ACCESS_KEY_ID')
    config['aws_secret_access_key'] = os.environ.get('AWS_SECRET_ACCESS_KEY')
    #SES
    config['email_source'] = os.environ.get('EMAIL_SOURCE')
    config['email_to_address'] = os.environ.get('EMAIL_TO_ADDRESS')
    # monitor parameters
    config['wait_seconds'] = os.environ.get('WAIT_SECONDS', 20)
    config['wait_factor'] = os.environ.get('WAIT_FACTOR', 1)
    
    return config

def getHostList():
    config = configparser.ConfigParser()
    config.read('hosts.ini')
    return config
    