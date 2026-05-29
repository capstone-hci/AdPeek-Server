import os
from dotenv import load_dotenv

load_dotenv()

USE_SIMULATE = os.getenv("USE_SIMULATE", "true").lower() == "true"
MUSE_SERIAL = os.getenv("MUSE_SERIAL", None)