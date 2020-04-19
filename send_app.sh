#!/bin/bash

if [ $# -ne 3 ]
then
    echo "usage ./send_app.sh {user} {ipaddress} {dir}"
    exit -1
fi

scp -r ./instance \
    ./models \
    ./app.py \
    ./config.py \
    ./coordinator.py \
    ./README.md \
    ./requirements.txt \
    ./start.sh \
    ${1}@${2}:${3}
