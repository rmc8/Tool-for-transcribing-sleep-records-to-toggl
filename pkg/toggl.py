from typing import Optional

import requests

from .exceptions import TogglPermissionException, TogglBadRequestException


class TogglAPI:
    def __init__(self, token):
        self.base_url: str = "https://api.track.toggl.com/api/v8"
        self.token: str = token
    
    def _request(self, path: str, method: str = "GET", payload: Optional[dict] = None) -> dict:
        url: str = f"{self.base_url}/{path}"
        res = requests.request(method=method, url=url,
                               auth=(self.token, "api_token"),
                               json=payload)
        if res.status_code == 403:
            raise TogglPermissionException
        elif res.status_code == 400:
            raise TogglBadRequestException
        return res.json()
    
    def create_time_entry(self, description: str, duration: int, start: str,
                          created_with: str = "Python", **kwargs) -> dict:
        # Required
        payload: dict = {
            "time_entry": {
                "description": description,
                "duration": duration,
                "start": start,
                "created_with": created_with,
            }
        }
        
        # Optional
        for key, val in kwargs.items():
            if val is not None:
                payload["time_entry"][key] = val
        
        # POST
        res: dict = self._request(path="time_entries", method="POST", payload=payload)
        return res
