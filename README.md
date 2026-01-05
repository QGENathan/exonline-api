**Usage**
```Python

from exonline_api import ExOnlineClient
from exonline_api.models import AttachmentData

# Option 1: Env Vars (EXO_KEY defined)
client = ExOnlineClient(api_key="your_key_here")

# Option 2: Config
# Ensure EXO_KEY is set in your environment
from exonline_api.config import Config
config = Config.from_env()
client = ExOnlineClient(api_key=config.api_key)

# Get Projects
projects = client.get_projects(account_id=123)

# Get Equipment
EQ_IDS = [12345, 12346]
equipment = client.get_equipment(project_id=123, dossier_ids=EQ_IDS)

# Get Equipment Attachments (Documents / Assoc Eq.)
EqAttc = client.get_attachment_data(project_id=123, dossier_ids=EQ_IDS)

```
