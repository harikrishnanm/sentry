#!/bin/bash

mysqldump -u root -proot123 sentry > "/home/pi/sentry/sentry/backup/dbbackup-$(date +"%d-%m-%y %T")" 2> /home/pi/sentry/sentry/backup/dbbackup.log
