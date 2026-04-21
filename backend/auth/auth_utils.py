import re

_GUID_REGEX = re.compile(
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
)


def get_authenticated_user_details(request_headers):
    user_object = {}

    ## Priority 1: Azure EasyAuth headers (injected by the Azure App Service auth layer)
    if "X-Ms-Client-Principal-Id" in request_headers.keys():
        raw_user_object = dict(request_headers.items())
        user_object['user_principal_id'] = raw_user_object.get('X-Ms-Client-Principal-Id')
        user_object['user_name'] = raw_user_object.get('X-Ms-Client-Principal-Name')
        user_object['auth_provider'] = raw_user_object.get('X-Ms-Client-Principal-Idp')
        user_object['auth_token'] = raw_user_object.get('X-Ms-Token-Aad-Id-Token')
        user_object['client_principal_b64'] = raw_user_object.get('X-Ms-Client-Principal')
        user_object['aad_id_token'] = raw_user_object.get('X-Ms-Token-Aad-Id-Token')

    ## Priority 2: URL user parameter passed by the frontend as X-User-Id header
    elif "X-User-Id" in request_headers.keys():
        url_user_id = request_headers.get("X-User-Id", "")
        if _GUID_REGEX.match(url_user_id):
            user_object['user_principal_id'] = url_user_id
            user_object['user_name'] = 'url-param-user'
            user_object['auth_provider'] = 'url_param'
            user_object['auth_token'] = None
            user_object['client_principal_b64'] = None
            user_object['aad_id_token'] = None
        else:
            ## Invalid GUID — fall through to the no-auth dev default
            from . import sample_user
            raw_user_object = sample_user.sample_user
            user_object['user_principal_id'] = raw_user_object.get('X-Ms-Client-Principal-Id')
            user_object['user_name'] = raw_user_object.get('X-Ms-Client-Principal-Name')
            user_object['auth_provider'] = raw_user_object.get('X-Ms-Client-Principal-Idp')
            user_object['auth_token'] = raw_user_object.get('X-Ms-Token-Aad-Id-Token')
            user_object['client_principal_b64'] = raw_user_object.get('X-Ms-Client-Principal')
            user_object['aad_id_token'] = raw_user_object.get('X-Ms-Token-Aad-Id-Token')

    ## Priority 3: No auth / development mode — use the sample user
    else:
        from . import sample_user
        raw_user_object = sample_user.sample_user
        user_object['user_principal_id'] = raw_user_object.get('X-Ms-Client-Principal-Id')
        user_object['user_name'] = raw_user_object.get('X-Ms-Client-Principal-Name')
        user_object['auth_provider'] = raw_user_object.get('X-Ms-Client-Principal-Idp')
        user_object['auth_token'] = raw_user_object.get('X-Ms-Token-Aad-Id-Token')
        user_object['client_principal_b64'] = raw_user_object.get('X-Ms-Client-Principal')
        user_object['aad_id_token'] = raw_user_object.get('X-Ms-Token-Aad-Id-Token')

    return user_object