# rancher-backup-mongo

This container permit to backup all Mongo databases linked to this container (if no credential setting) on Rancher.

In fact, this container begin to make a dump of all Mongo databases linked to it, and then use duplicity to make external backup like FTP or Amazon S3.

## Backup options
The following options permit to set the backup policy :
- `CRON_SCHEDULE`: When you should start backup (incremental if full is not needed). For example, to start backup each day set `0 0 0 * * *`
- `TARGET_BACKEND`: This is the target URL to externalize the backup. For example, to use FTP as external backup set `ftp://login@my-ftp.com` and add environment variable `FTP_PASSWORD`. For Amazon S3, set `s3://host[:port]/bucket_name[/prefix]`. Read the ducplicity man for [all supported backend](http://duplicity.nongnu.org/duplicity.1.html#sect7). There are no default value.
- `TARGET_PATH`: The path were store backup on local and remote. The default value is `/backup/postgres`.
- `BK_FULL_FREQ`: The frequency when you should make a full backup. For example, if you should make a full backup each 7 days, set `7D`. The default value is `7D`.
- `BK_KEEP_FULL`: How many full backup you should to keep. For example, to keep 3 full backup set `3`. The default value is `3`.
- `BK_KEEP_FULL_CHAIN`: The number of intermediate incremental backup you should keep with the full backup. For example, if you should keep only the incremental backend after the last full backup set `1`. The default value is set to `1`.
- `VOLUME_SIZE`: The volume size to store the backup (in MB). The default value is `25`.
