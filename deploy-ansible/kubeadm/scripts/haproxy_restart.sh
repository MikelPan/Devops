#!/bin/bash
docker container stop my-haproxy
docker container rm my-haproxy
docker run -d --name my-haproxy \
-v /etc/haproxy:/usr/local/etc/haproxy:ro \
-p 8443:8443 \
-p 1080:1080 \
--restart always \
haproxy:1.7.11-alpine
