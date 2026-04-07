import re
import logging

GUID_REGEX = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    re.IGNORECASE
)

DEFAULT_USER_ID = '00000000-0000-0000-0000-000000000000'


def get_authenticated_user_details(request_headers):
    user_object = {}

    ## Check for external user ID passed from Dynamics via frontend header.
    ## If present and a valid GUID, use it; otherwise fall back to the default user.
    external_user_id = request_headers.get('X-External-User-Id', '').strip()
    if external_user_id and GUID_REGEX.match(external_user_id):
        resolved_id = external_user_id
        logging.debug(f"[ExternalUser] Valid user ID received: {resolved_id}")
    else:
        resolved_id = DEFAULT_USER_ID
        if external_user_id:
            logging.warning(f"[ExternalUser] Invalid GUID received, defaulting to zero user: {external_user_id}")
        else:
            logging.debug("[ExternalUser] No user ID in request, defaulting to zero user")

    user_object['user_principal_id'] = resolved_id
    user_object['user_name'] = resolved_id
    user_object['auth_provider'] = 'external'
    user_object['auth_token'] = None
    user_object['client_principal_b64'] = None
    user_object['aad_id_token'] = None

    return user_object