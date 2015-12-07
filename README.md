Kadup provides a command line interface to schedule and run rsync to backup local directories.

On Windows it utilizes Cygwin with rsync installed and uses schtaks command to schedule when rsync will run.
On Unix platforms (i.e. OS X and Linux) rsync needs to be installed and cron will be used for scheduling.

The format of the rsync command used is:
`$ rsync -azt --verbose --delete "<backup_dir>" "<destination_dir>"`

Kadup also has a some very limited cli capabilities.