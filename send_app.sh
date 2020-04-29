#!/bin/bash

if [ $# -ne 3 ]
then
    echo "usage ./send_app.sh {user} {ipaddress} {dir}"
    exit -1
fi

for i in `find . -name "__pycache__"`
do
    rm -rf $i
done

scp -r ./instance \
    ./models \
    ./app.py \
    ./config.py \
    ./coordinator.py \
    ./README.md \
    ./requirements.txt \
    ./start.sh \
    ${1}@${2}:${3}
