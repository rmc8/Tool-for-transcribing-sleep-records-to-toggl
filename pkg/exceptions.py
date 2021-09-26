class TogglPermissionException(Exception):
    msg: str = "Access to ToggleAPI has been denied, please make sure your Token is correct"


class TogglBadRequestException(Exception):
    msg: str = "There is an error in the request to the API"
