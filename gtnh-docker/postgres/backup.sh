# vars
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="../backups/gtoverseer_backup_${TIMESTAMP}.sql"

# create backup dir
mkdir -p "../backups"
# pgdump for backup
pg_dump -d postgres > $BACKUP_FILE