import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DefaultConfig:

    # Azure AD Configuration
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")

    
    # Application Configuration
    # SECRET_KEY = os.getenv("SECRET_KEY", "test@1234")
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "b5cfc8526e1dbd2de4501c1e64a9b44fd630b4f952e64b8ed6995e1859fa56b9"
    )
    
