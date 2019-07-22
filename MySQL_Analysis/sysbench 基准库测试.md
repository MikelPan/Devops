### sysbench 基准库测试
#### 一、sysbench安装
```shell
	# 二进制安装
	curl -s https://packagecloud.io/install/repositories/akopytov/sysbench/script.rpm.sh | sudo bash
	sudo yum -y install sysbench
	# 源代码安装
	yum -y install make automake libtool pkgconfig libaio-devel
	yum -y install mariadb-devel openssl-devel
	yum -y install postgresql-devel
	./autogen.sh
	./configure
	make -j 
	make install
	# 安装
	yum install automake gcc gcc-c++ libtool mysql-devel
	git clone https://github.com/akopytov/sysbench.git
	./autogen.sh
	./configure
	make && make install
```
#### 二、基本命令用法
```shell
	[root@www ~]# sysbench --help
	Usage:
	  sysbench [options]... [testname] [command]

	Commands implemented by most tests: prepare run cleanup help

	General options:
	  --threads=N                     number of threads to use [1]
	  --events=N                      limit for total number of events [0]
	  --time=N                        limit for total execution time in seconds [10]
	  --forced-shutdown=STRING        number of seconds to wait after the --time limit before forcing shutdown, or 'off' to disable [off]
	  --thread-stack-size=SIZE        size of stack per thread [64K]
	  --rate=N                        average transactions rate. 0 for unlimited rate [0]
	  --report-interval=N             periodically report intermediate statistics with a specified interval in seconds. 0 disables intermediate reports [0]
	  --report-checkpoints=[LIST,...] dump full statistics and reset all counters at specified points in time. The argument is a list of comma-separated values representing the amount of time in seconds elapsed from start of test when report checkpoint(s) must be performed. Report checkpoints are off by default. []
	  --debug[=on|off]                print more debugging info [off]
	  --validate[=on|off]             perform validation checks where possible [off]
	  --help[=on|off]                 print help and exit [off]
	  --version[=on|off]              print version and exit [off]
	  --config-file=FILENAME          File containing command line options
	  --tx-rate=N                     deprecated alias for --rate [0]
	  --max-requests=N                deprecated alias for --events [0]
	  --max-time=N                    deprecated alias for --time [0]
	  --num-threads=N                 deprecated alias for --threads [1]

	Pseudo-Random Numbers Generator options:
	  --rand-type=STRING random numbers distribution {uniform,gaussian,special,pareto} [special]
	  --rand-spec-iter=N number of iterations used for numbers generation [12]
	  --rand-spec-pct=N  percentage of values to be treated as 'special' (for special distribution) [1]
	  --rand-spec-res=N  percentage of 'special' values to use (for special distribution) [75]
	  --rand-seed=N      seed for random number generator. When 0, the current time is used as a RNG seed. [0]
	  --rand-pareto-h=N  parameter h for pareto distribution [0.2]

	Log options:
	  --verbosity=N verbosity level {5 - debug, 0 - only critical messages} [3]

	  --percentile=N       percentile to calculate in latency statistics (1-100). Use the special value of 0 to disable percentile calculations [95]
	  --histogram[=on|off] print latency histogram in report [off]

	General database options:

	  --db-driver=STRING  specifies database driver to use ('help' to get list of available drivers) [mysql]
	  --db-ps-mode=STRING prepared statements usage mode {auto, disable} [auto]
	  --db-debug[=on|off] print database-specific debug information [off]


	Compiled-in database drivers:
	  mysql - MySQL driver
	  pgsql - PostgreSQL driver

	mysql options:
	  --mysql-host=[LIST,...]          MySQL server host [localhost]
	  --mysql-port=[LIST,...]          MySQL server port [3306]
	  --mysql-socket=[LIST,...]        MySQL socket
	  --mysql-user=STRING              MySQL user [sbtest]
	  --mysql-password=STRING          MySQL password []
	  --mysql-db=STRING                MySQL database name [sbtest]
	  --mysql-ssl[=on|off]             use SSL connections, if available in the client library [off]
	  --mysql-ssl-cipher=STRING        use specific cipher for SSL connections []
	  --mysql-compression[=on|off]     use compression, if available in the client library [off]
	  --mysql-debug[=on|off]           trace all client library calls [off]
	  --mysql-ignore-errors=[LIST,...] list of errors to ignore, or "all" [1213,1020,1205]
	  --mysql-dry-run[=on|off]         Dry run, pretend that all MySQL client API calls are successful without executing them [off]

	pgsql options:
	  --pgsql-host=STRING     PostgreSQL server host [localhost]
	  --pgsql-port=N          PostgreSQL server port [5432]
	  --pgsql-user=STRING     PostgreSQL user [sbtest]
	  --pgsql-password=STRING PostgreSQL password []
	  --pgsql-db=STRING       PostgreSQL database name [sbtest]

	Compiled-in tests:
	  fileio - File I/O test
	  cpu - CPU performance test
	  memory - Memory functions speed test
	  threads - Threads subsystem performance test
	  mutex - Mutex performance test

	See 'sysbench <testname> help' for a list of options for each test.
```
#### 三、CPU性能测试
```shell
	sysbench --test=cpu --cpu-max-prime=20000 run
	cpu测试主要是进行素数的加法运算，在上面的例子中，指定了最大的素数为20000，自己可以根据机器cpu的性能来适当调整数值
```
#### 四、线程测试
```shell
	sysbench --test=threads --num-threads=64 --thread-yields=100 --thread-locks=2 run
```
#### 五、磁盘IO测试
```shell
	sysbench --test=fileio --num-threads=16 --file-total-size=3G --file-test-mode=rndrw prepare
	sysbench --test=fileio --num-threads=16 --file-total-size=3G --file-test-mode=rndrw run
	sysbench --test=fileio --num-threads=16 --file-total-size=3G --file-test-mode=rndrw cleanup
```
#### 六、内存测试
```shell
	sysbench --test=memory --memory-block-size=8k --memory-total-size=4G run 
```
#### 七、OLTP测试
```shell
	sysbench --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-passwd=root --test=/root/sysbench/sysbench/tests/db/oltp.lua --litp_tables_count=10 --oltp-table-size=1000000 --rand-init=on prepare
	--test=test/db/oltp.lua   调用oltp.lua脚本模拟测试
	--oltp_tables_count=10    生成10个测试表
	--oltp_table_size=100000  每个测试表填充数据量为100000
	--rand-init=on            表示每个测试表都是用随机数来填充的
	# 真实场景下测试
	sysbench --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root \
	--mysql-password=root --test=/root/sysbench/sysbench/tests/db/oltp.lua --oltp_tables_count=10 \
	--oltp-table-size=10000000 --num-threads=8 --oltp-read-only=off \
	--report-interval=10 --rand-type=uniform --max-time=3600 \
	 --max-requests=0 --percentile=99 run >> /tmp/sysbench_oltpX_8.log
	 –num-threads=8 表示发起 8个并发连接
	–oltp-read-only=off 表示不要进行只读测试，也就是会采用读写混合模式测试
	–report-interval=10 表示每10秒输出一次测试进度报告
	–rand-type=uniform 表示随机类型为固定模式，其他几个可选随机模式：uniform(固定),gaussian(高斯),special(特定的),pareto(帕累托)
	–max-time=120 表示最大执行时长为 120秒
	–max-requests=0 表示总请求数为 0，因为上面已经定义了总执行时长，所以总请求数可以设定为 0；也可以只设定总请求数，不设定最大执行时长
	–percentile=99 表示设定采样比例，默认是 95%，即丢弃1%的长请求，在剩余的99%里取最大值
	# 只读测试
	./bin/sysbench --test=./share/tests/db/oltp.lua \
	--mysql-host=10.0.201.36 --mysql-port=8066 --mysql-user=ecuser --mysql-password=ecuser \
	--mysql-db=dbtest1a --oltp-tables-count=10 --oltp-table-size=500000 \
	--report-interval=10 --oltp-dist-type=uniform --rand-init=on --max-requests=0 \
	--oltp-test-mode=nontrx --oltp-nontrx-mode=select \
	--oltp-read-only=on --oltp-skip-trx=on \
	--max-time=120 --num-threads=12 \
	[prepare|run|cleanup]
	mysql-db=dbtest1a：测试使用的目标数据库，这个库名要事先创建
	--oltp-tables-count=10：产生表的数量
	--oltp-table-size=500000：每个表产生的记录行数
	--oltp-dist-type=uniform：指定随机取样类型，可选值有 uniform(均匀分布), Gaussian(高斯分布), special(空间分布)。默认是special
	--oltp-read-only=off：表示不止产生只读SQL，也就是使用oltp.lua时会采用读写混合模式。默认 off，如果设置为on，则不会产生update,delete,insert的sql。
	--oltp-test-mode=nontrx：执行模式，这里是非事务式的。可选值有simple,complex,nontrx。默认是complex
	simple：简单查询，SELECT c FROM sbtest WHERE id=N
	complex (advanced transactional)：事务模式在开始和结束事务之前加上begin和commit， 一个事务里可以有多个语句，如点查询、范围查询、排序查询、更新、删除、插入等，并且为了不破坏测试表的数据，该模式下一条记录删除后会在同一个事务里添加一条相同的记录。
	nontrx (non-transactional)：与simple相似，但是可以进行update/insert等操作，所以如果做连续的对比压测，你可能需要重新cleanup,prepare。
	--oltp-skip-trx=[on|off]：省略begin/commit语句。默认是off
	--rand-init=on：是否随机初始化数据，如果不随机化那么初始好的数据每行内容除了主键不同外其他完全相同
	--num-threads=12： 并发线程数，可以理解为模拟的客户端并发连接数
	--report-interval=10：表示每10s输出一次测试进度报告
	--max-requests=0：压力测试产生请求的总数，如果以下面的max-time来记，这个值设为0
	--max-time=120：压力测试的持续时间，这里是2分钟。
	注意，针对不同的选项取值就会有不同的子选项。比如oltp-dist-type=special，就有比如oltp-dist-pct=1、oltp-dist-res=50两个子选项，代表有50%的查询落在1%的行（即热点数据）上，另外50%均匀的(sample uniformly)落在另外99%的记录行上。
	再比如oltp-test-mode=nontrx时, 就可以有oltp-nontrx-mode，可选值有select（默认）, update_key, update_nokey, insert, delete，代表非事务式模式下使用的测试sql类型。
	以上代表的是一个只读的例子，可以把num-threads依次递增（16,36,72,128,256,512），或者调整my.cnf参数，比较效果。另外需要注意的是，大部分mysql中间件对事务的处理，默认都是把sql发到主库执行，所以只读测试需要加上oltp-skip-trx=on来跳过测试中的显式事务。
    # 混合读写
    ./bin/sysbench --test=./share/tests/db/oltp.lua --mysql-host=10.0.201.36 --mysql-port=8066 --mysql-user=ecuser --mysql-password=ecuser --mysql-db=dbtest1a --oltp-tables-count=10 --oltp-table-size=500000 --report-interval=10 --rand-init=on --max-requests=0 --oltp-test-mode=nontrx --oltp-nontrx-mode=select --oltp-read-only=off --max-time=120 --num-threads=128 [prepare|run|cleanup]
    # 只更新
    ./bin/sysbench --test=./share/tests/db/update_index.lua \
	--mysql-host=10.0.201.36 --mysql-port=8066 --mysql-user=ecuser --mysql-password=ecuser \
	--mysql-db=dbtest1a --oltp-tables-count=10 --oltp-table-size=500000 \
	--report-interval=10 --rand-init=on --max-requests=0 \
	--oltp-read-only=off --max-time=120 --num-threads=128 \
	[ prepare | run | cleanup ]
	# 测试结果分析
	sysbench 0.5:  multi-threaded system evaluation benchmark

	Running the test with following options:
	Number of threads: 8
	Report intermediate results every 10 second(s)
	Random number generator seed is 0 and will be ignored

	Threads started!
	-- 每10秒钟报告一次测试结果，tps、每秒读、每秒写、99%以上的响应时长统计
	[  10s] threads: 8, tps: 1111.51, reads/s: 15568.42, writes/s: 4446.13, response time: 9.95ms (99%)
	[  20s] threads: 8, tps: 1121.90, reads/s: 15709.62, writes/s: 4487.80, response time: 9.78ms (99%)
	[  30s] threads: 8, tps: 1120.00, reads/s: 15679.10, writes/s: 4480.20, response time: 9.84ms (99%)
	[  40s] threads: 8, tps: 1114.20, reads/s: 15599.39, writes/s: 4456.30, response time: 9.90ms (99%)
	[  50s] threads: 8, tps: 1114.00, reads/s: 15593.60, writes/s: 4456.70, response time: 9.84ms (99%)
	[  60s] threads: 8, tps: 1119.30, reads/s: 15671.60, writes/s: 4476.50, response time: 9.99ms (99%)
	OLTP test statistics:
	    queries performed:
	        read:                            938224    -- 读总数
	        write:                           268064    -- 写总数
	        other:                           134032    -- 其他操作总数(SELECT、INSERT、UPDATE、DELETE之外的操作，例如COMMIT等)
	        total:                           1340320    -- 全部总数
	    transactions:                        67016  (1116.83 per sec.)    -- 总事务数(每秒事务数)
	    deadlocks:                           0      (0.00 per sec.)    -- 发生死锁总数
	    read/write requests:                 1206288 (20103.01 per sec.)    -- 读写总数(每秒读写次数)
	    other operations:                    134032 (2233.67 per sec.)    -- 其他操作总数(每秒其他操作次数)

	General statistics:    -- 一些统计结果
	    total time:                          60.0053s    -- 总耗时
	    total number of events:              67016    -- 共发生多少事务数
	    total time taken by event execution: 479.8171s    -- 所有事务耗时相加(不考虑并行因素)
	    response time:    -- 响应时长统计
	         min:                                  4.27ms    -- 最小耗时
	         avg:                                  7.16ms    -- 平均耗时
	         max:                                 13.80ms    -- 最长耗时
	         approx.  99 percentile:               9.88ms    -- 超过99%平均耗时

	Threads fairness:
	    events (avg/stddev):           8377.0000/44.33
	    execution time (avg/stddev):   59.9771/0.00
```	  
