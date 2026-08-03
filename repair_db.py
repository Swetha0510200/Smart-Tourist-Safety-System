import sqlite3
import shutil
import os

SOURCE_DB = "tourist_safety.db"
BACKUP_DB = "tourist_safety_backup.db"
REPAIRED_DB = "tourist_safety_repaired.db"

if not os.path.exists(SOURCE_DB):
    print(f"❌ {SOURCE_DB} not found.")
    exit()

# Backup first
try:
    shutil.copy2(SOURCE_DB, BACKUP_DB)
    print("✅ Backup created:", BACKUP_DB)
except Exception as e:
    print("❌ Backup failed:", e)

try:
    src = sqlite3.connect(SOURCE_DB)
    dst = sqlite3.connect(REPAIRED_DB)

    src.backup(dst)

    src.close()
    dst.close()

    print("✅ Repair successful!")
    print("Repaired database:", REPAIRED_DB)

except Exception as e:
    print("❌ Database repair failed.")
    print("Error:", e)