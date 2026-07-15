import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class IBMWatsonxClient:
    def __init__(self):
        self.api_key = os.getenv("IBM_API_KEY", "").strip()
        self.agent_url = os.getenv("AGENT_URL", "").strip().rstrip("/")
        self.agent_uid = os.getenv("AGENT_UID", "").strip()
        self._token = None
        self._token_expiry = 0.0
        self._session = requests.Session()

    def _get_token(self):
        if not self._token or time.time() >= self._token_expiry - 60:
            resp = requests.post(
                "https://iam.cloud.ibm.com/identity/token",
                data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": self.api_key},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30
            )
            resp.raise_for_status()
            token_data = resp.json()
            self._token = token_data["access_token"]
            self._token_expiry = time.time() + token_data.get("expires_in", 3600)
        return self._token

    def chat(self, messages: list[dict]) -> str:
        token = self._get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        endpoint = f"{self.agent_url}/v1/orchestrate/{self.agent_uid}/chat/completions"

        combined_prompt = "Here is our conversation history. Read it to understand the context, then answer my newest message.\n\n"
        for m in messages[:-1]: 
            role = "AI" if m["role"] == "assistant" else "Me"
            combined_prompt += f"[{role}]: {m['content']}\n"
            
        combined_prompt += f"\n[My Newest Message]: {messages[-1]['content']}\n"
        combined_prompt += "\nPlease reply directly to My Newest Message to continue our workflow."

        payload = {"messages": [{"role": "user", "content": combined_prompt}], "stream": False}
        resp = self._session.post(endpoint, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]