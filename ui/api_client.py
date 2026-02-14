import requests
from typing import List, Dict, Any, Optional, Union

class ApiClient:
    """
    Client to interact with the HR Tech AI Backend API.
    """
    def __init__(self, base_url: Optional[str] = None):
        from app.core.config import API_URL
        self.base_url = base_url or API_URL


    def _handle_response(self, response: requests.Response) -> Any:
        """
        Standardized handling of API responses.
        
        Args:
            response: The requests.Response object.
            
        Returns:
            The parsed JSON content or specific status indicators.
            
        Raises:
            Exception with descriptive messages for HTTP errors or network issues.
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Try to return the error message from API if available
            try:
                error_detail = response.json()
                raise Exception(f"API Error: {error_detail}") from e
            except ValueError:
                raise Exception(f"HTTP Error: {e}") from e
        except Exception as e:
            raise Exception(f"Network Error: {e}") from e

    def health_check(self) -> Dict[str, str]:
        r = requests.get(f"{self.base_url}/")
        return self._handle_response(r)

    def search_candidates(self, query: str) -> List[Dict[str, Any]]:
        r = requests.get(f"{self.base_url}/search", params={"q": query})
        return self._handle_response(r)

    def get_all_candidates(self) -> List[Dict[str, Any]]:
        r = requests.get(f"{self.base_url}/candidates")
        return self._handle_response(r)

    def add_resume(self, payload: Dict[str, Any]) -> Dict[str, str]:
        r = requests.post(f"{self.base_url}/resume", json=payload)
        return self._handle_response(r)

    def upload_resumes(self, files: List[tuple]) -> List[Dict[str, Any]]:
        """
        Upload multiple resume files for processing.
        files is a list of tuples: ('files', (filename, content, type))
        """
        r = requests.post(f"{self.base_url}/upload_resumes", files=files)
        return self._handle_response(r)

    def update_candidate(self, candidate_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        r = requests.put(f"{self.base_url}/candidates/{candidate_id}", json=payload)
        return self._handle_response(r)

    def delete_candidate(self, candidate_id: str) -> Union[str, Dict[str, str]]:
        r = requests.delete(f"{self.base_url}/candidates/{candidate_id}")
        # Delete might return 204 No Content
        if r.status_code == 204:
            return "Deleted"
        return self._handle_response(r)

    def rag_query(self, query: str) -> Dict[str, str]:
        r = requests.get(f"{self.base_url}/rag", params={"q": query})
        return self._handle_response(r)

    def list_indexes(self) -> List[str]:
        r = requests.get(f"{self.base_url}/api/index/list")
        return self._handle_response(r)

    def create_index(self, name_index: str) -> Dict[str, Any]:
        r = requests.post(f"{self.base_url}/api/index/create", params={"name_index": name_index})
        return self._handle_response(r)

    def get_index_detail(self, name_index: str) -> Dict[str, Any]:
        r = requests.post(f"{self.base_url}/api/index/detail", params={"name_index": name_index})
        return self._handle_response(r)
