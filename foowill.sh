#!/bin/bash
  set -e
  LOGFILE=/var/log/gunicorn/foowill.log
  LOGDIR=$(dirname $LOGFILE)
  NUM_WORKERS=3
  # user/group to run as
  USER=edu
  GROUP=edu
  cd /mnt/xuflus/virtualenvs/foowill
  source bin/activate
  test -d $LOGDIR || mkdir -p $LOGDIR

  cd /mnt/xuflus/Webs/foowill
  exec /mnt/xuflus/virtualenvs/foowill/bin/gunicorn_django -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE

