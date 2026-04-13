import re


UUID_REGEX = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def _get_header_value(request_headers, header_name):
    if hasattr(request_headers, "get"):
        value = request_headers.get(header_name)
        if value is not None:
            return value

    for key, value in request_headers.items():
        if key.lower() == header_name.lower():
            return value

    return None


def _is_valid_uuid(value):
    return isinstance(value, str) and UUID_REGEX.match(value) is not None


def get_authenticated_user_details(request_headers):
    user_object = {}
    external_user_id = _get_header_value(request_headers, "X-External-User-Id")
    principal_id_header = _get_header_value(request_headers, "X-Ms-Client-Principal-Id")

    ## check the headers for the Principal-Id (the guid of the signed in user)
    if principal_id_header is None:
        ## if it's not, assume we're in development mode and return a default user
        from . import sample_user
        raw_user_object = sample_user.sample_user
    else:
        ## if it is, get the user details from the EasyAuth headers
        raw_user_object = dict(request_headers.items())

    resolved_user_id = (
        external_user_id
        if _is_valid_uuid(external_user_id)
        else _get_header_value(raw_user_object, 'X-Ms-Client-Principal-Id')
    )

    user_object['user_principal_id'] = resolved_user_id
    user_object['user_name'] = _get_header_value(raw_user_object, 'X-Ms-Client-Principal-Name')
    user_object['auth_provider'] = _get_header_value(raw_user_object, 'X-Ms-Client-Principal-Idp')
    user_object['auth_token'] = _get_header_value(raw_user_object, 'X-Ms-Token-Aad-Id-Token')
    user_object['client_principal_b64'] = _get_header_value(raw_user_object, 'X-Ms-Client-Principal')
    user_object['aad_id_token'] = _get_header_value(raw_user_object, 'X-Ms-Token-Aad-Id-Token')

    return user_object