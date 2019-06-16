#!/bin/bash
#gluster volume create redis-pv1 replica 3 transport tcp node1:/opt/redisdata/pv1 node2:/opt/redisdata/pv1 node3:/opt/redisdata/pv1 force
#gluster volume start redis-pv1
gluster volume create redis-pv2 replica 3 transport tcp node1:/opt/redisdata/pv2 node2:/opt/redisdata/pv2 node3:/opt/redisdata/pv2 force
gluster volume start redis-pv2
gluster volume create redis-pv3 replica 3 transport tcp node1:/opt/redisdata/pv3 node2:/opt/redisdata/pv3 node3:/opt/redisdata/pv3 force
gluster volume start redis-pv3
gluster volume create redis-pv4 replica 3 transport tcp node1:/opt/redisdata/pv4 node2:/opt/redisdata/pv4 node3:/opt/redisdata/pv4 force
gluster volume start redis-pv4
gluster volume create redis-pv5 replica 3 transport tcp node1:/opt/redisdata/pv5 node2:/opt/redisdata/pv5 node3:/opt/redisdata/pv5 force
gluster volume start redis-pv5
gluster volume create redis-pv6 replica 3 transport tcp node1:/opt/redisdata/pv6 node2:/opt/redisdata/pv6 node3:/opt/redisdata/pv6 force
gluster volume start redis-pv6
