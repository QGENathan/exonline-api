Usage
Python

from exonline_sdk import ExOnlineClient
from exonline_sdk.models import AttachmentData

# Option 1: Env Vars (EXO_KEY defined)
client = ExOnlineClient(api_key="your_key_here")

# Option 2: Config
# Ensure EXO_KEY is set in your environment
from exonline_sdk.config import Config
config = Config.from_env()
client = ExOnlineClient(api_key=config.api_key)

# Get Data
projects = client.get_projects(account_id=123)