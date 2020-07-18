httpSettings = {
    'content_header': {'Content-Type': 'application/json'}
}


def add_auth(headers, auth_token):
    headers['Authorization'] = 'Bearer ' + auth_token
    return headers
