def get_access_token(response):
    return response.json()['accessToken']


def get_resource_id(response):
    return response.headers['resource_id']
