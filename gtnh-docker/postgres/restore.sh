# check if arg was passed
if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/backup/file.sql"
    exit 1
fi
BACKUP_FILE="$1"

# break if file doesnt exist
if [! -f "$BACKUP_FILE" ]; then
    echo "File not found: $BACKUP_FILE"
    exit 1
fi

# restore the backup
psql -U "${POSTGRES_USER}" -d "postgres" < "$BACKUP_FILE"