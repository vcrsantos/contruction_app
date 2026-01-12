import shutil
from datetime import datetime
import os

DB_PATH = "contruction.db"
BACKUP_DIR = "backups"

def backup_db():
    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{BACKUP_DIR}/contruction_{timestamp}.db"

    shutil.copy(DB_PATH, backup_file)
