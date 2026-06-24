import time
import jwt
import httpx
from typing import Optional
from app.core.config import settings

class GitHubAppClient:
    def __init__(self):
        self.app_id = settings.GITHUB_APP_ID
        self.private_key = settings.GITHUB_APP_PRIVATE_KEY
        self.base_url = "https://api.github.com"

    def _generate_jwt(self) -> str:
        if not self.private_key or not self.app_id:
            raise ValueError("GITHUB_APP_ID or GITHUB_APP_PRIVATE_KEY is missing")
            
        now = int(time.time())
        payload = {
            "iat": now - 60,
            "exp": now + (10 * 60),
            "iss": self.app_id
        }
        
        # Ensure private key is properly formatted (newlines)
        key = self.private_key.replace("\\n", "\n")
        encoded_jwt = jwt.encode(payload, key, algorithm="RS256")
        return encoded_jwt

    def get_installation_token(self, installation_id: int) -> str:
        jwt_token = self._generate_jwt()
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/app/installations/{installation_id}/access_tokens",
                headers=headers
            )
            response.raise_for_status()
            return response.json()["token"]

    def get_client_for_installation(self, installation_id: int) -> httpx.Client:
        token = self.get_installation_token(installation_id)
        return httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
        )
