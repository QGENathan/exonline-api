# config.py
import os
from dataclasses import dataclass

@dataclass
class Config:
    api_key: str
    base_url: str = "https://cloud.ex-online.com/TagBrowser/api/v2/Puppy"

    @classmethod
    def from_env(cls) -> "Config":
        """Loads configuration from environment variables."""
        api_key = os.getenv("EXO_KEY")
        if not api_key:
            raise ValueError("EXO_KEY environment variable is not set.")
        
        return cls(
            api_key=api_key,
            base_url=os.getenv("EXO_BASE_URL", cls.base_url)
        )