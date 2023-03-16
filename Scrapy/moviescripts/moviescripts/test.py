############################
# Load environment variables
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = f'{Path(__file__).resolve().parents[4]}' + '\private_env.env'
load_dotenv(dotenv_path=dotenv_path)
CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')

print(CONNECTION_STRING)