# EXO API

import requests
from typing import Optional, List
from .exceptions import APIError, AuthenticationError
from .models import Project, EqItem, AttachmentData, APIResponse

class ExOnlineClient:
    def __init__(self, api_key: str, base_url: str = "https://cloud.ex-online.com/TagBrowser/api/v2/Puppy"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key or unauthorized access.") from http_err
            else:
                raise APIError(f"HTTP error occurred: {http_err}") from http_err
    
    def get_attachment_data(self, project_id: int, dossier_ids: List[int], date_from: str = "2010-01-01", date_to: str = None) -> List[AttachmentData]:
        """
            Fetches Documents and Associated Equipment for given dossier IDs within a project.
        """
        params = {
            "project": project_id,
            "eq": ",".join(map(str, dossier_ids))
        }

        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        
        response_json = self._request("GET", "ListEqAttc", params=params)
        response = APIResponse.from_dict(response_json, AttachmentData)
        if response.err != 0:
            raise APIError(f"API returned error {response.err}: {response.message}")

        return response.data
    
    def get_projects(self, account_id: int, pg: int = 1, pgSize:int = 100) -> List[Project]:
        """Fetches a list of projects for the specified account ID."""
        params = {
            "account_id": account_id,
            "pg": pg,
            "pgSize": pgSize
        }

        response_json = self._request("GET", "ListProjects", params=params)
        response = APIResponse.from_dict(response_json, Project)
        if response.err != 0:
            raise APIError(f"API returned error {response.err}: {response.message}")

        return response.data
    
    def get_equipment(self, project_id: int, dossier_ids: List[int], date_from: str = "2010-01-01", date_to: str = None, pg: int = 1, pgSize: int = 1000) -> List[EqItem]:
        """
        Fetches detailed equipment properties for specific IDs.
        """
        params = {
            "project": project_id,
            "eq": ",".join(map(str, dossier_ids)),
            "pg": pg,
            "pgSize": pgSize
        }
        if date_from: params["date_from"] = date_from
        if date_to: params["date_to"] = date_to

        raw_json = self._request("GET", "ListEq", params=params)

        response = APIResponse.from_dict(raw_json, EqItem)

        if response.err != 0:
            raise APIError(f"API Error {response.err}: {response.message}")

        return response.data