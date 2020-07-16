#!/bin/bash
# REPO=docker-reg.emotibot.com.cn:55688
#this is git test
WORK_PATH=$(dirname "$0")
source ${WORK_PATH}/build.sh 
REPO=hub.docker.com
CONTAINER=transmit-tags

export TAG=$(git rev-parse --short HEAD)
set -o allexport
source dev.env
set +o allexport

echo "[ -------- 1.   build and run        -------- ]"
echo "[ -------- 2.   pull image and run   -------- ]"
echo "[ -------- 3.   run module           -------- ]"
echo "[ -------- 4.   stop module          -------- ]"
echo "[ -------- 5.   save image           -------- ]"

if [ $# -eq 1 ]; then
    mode=$1
else
    read mode
fi

echo "mode:"$mode
CMD=""


if [ $mode == "1" ]; then
    echo "[ -------- 1.   build and run        -------- ]"
    build
    imagePull
    dockerComposeUp
elif [ $mode == "2" ]; then
    echo "[ -------- 2.   pull image and run   -------- ]"
    CMD=("imagePull" "dockerComposeUp")
elif [ $mode == "3" ]; then
	echo "[ -------- 3.   run module           -------- ]"
    read -p "Enter TAG: " INPUT_TAG
    echo "input TAG: $INPUT_TAG"
    export TAG=$INPUT_TAG
    CMD=("docker-compose up -d")
elif [ $mode == "4" ]; then
	echo "[ -------- 4.   stop module          -------- ]"
    CMD=("docker-compose down")
elif [ $mode == "5" ]; then
    echo "[ -------- 5.   save image           -------- ]"
    CMD=("saveImage")
fi

if [[ ${#CMD} > 0 ]]; then
    for val in "${CMD[@]}"; do
      echo $val && eval $val
    done
fi
