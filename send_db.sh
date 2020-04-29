#!/bin/bash

if [ $# -ne 3 ]
then
    echo "usage ./send_app.sh {user} {ipaddress} {dir}"
    exit -1
fi

scp -r ./db/markov.sqlite3 \
     ./db/*.sql \
    ${1}@${2}:${3}/db/
