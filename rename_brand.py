
from pathlib import Path
import re
import shutil

# Project root = folder containing this script
ROOT = Path(__file__).resolve().parent

# Old and new application names
OLD_NAME = "Fit" + "Track"
NEW_NAME = "fitnesstrack"

# Folders that must not be modified
SKIP_DIRS = {
    ".venv",
    ".git",
    "__pycache__",
    "node_modules",
    ".fitnesstrack_rename_backup",
}

# Files containing private settings or binary data
SKIP_FILES = {
    ".env",
    ".env.example",
}

# Backup folder
BACKUP = ROOT / ".fitnesstrack_rename_backup"

pattern = re.compile(re.escape(OLD_NAME), re.IGNORECASE)

changed = 0
replacements = 0

for file in ROOT.rglob("*"):

    if not file.is_file():
        continue

    relative = file.relative_to(ROOT)

    if any(part in SKIP_DIRS for part in relative.parts):
        continue

    if file.name in SKIP_FILES:
        continue

    # Avoid editing this script itself
    if file.name == Path(__file__).name:
        continue

    try:
        original = file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue

    updated, count = pattern.subn(NEW_NAME, original)

    if count == 0:
        continue

    # Save original file before modification
    backup_file = BACKUP / relative
    backup_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file, backup_file)

    # Write updated content
    file.write_text(updated, encoding="utf-8")

    changed += 1
    replacements += count

    print(f"Updated: {relative} ({count} replacements)")

print("\n" + "=" * 45)
print("APPLICATION RENAMING COMPLETED")
print("=" * 45)
print(f"Files modified: {changed}")
print(f"Total replacements: {replacements}")
print(f"New application name: {NEW_NAME}")
print(f"Backups saved in: {BACKUP}")
