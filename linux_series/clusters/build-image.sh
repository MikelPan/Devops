#!/bin/bash
MODULE=$1
PROJECT="spring_boot"
REGISTRY="harbor.plyx.site:8100/${PROJECT}/${MODULE}"
TIME=`data +"%Y%%m%d%H%M%S"`
TAGE=`docker logs -1 --pretty=format:"%h"`
IMAGE_NAME=${REGISTRY}:${TIME}_${TAGE}
mvn -U -pl ${MODULE} -am clean package
cd ${MODULE}
docker build -t ${IMAGE_NAME} .
cd -
docker push ${IMAGE_NMAE}