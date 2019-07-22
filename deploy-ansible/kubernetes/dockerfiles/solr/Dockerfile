FROM ubuntu:16.04
ARG TOMCAT_TAR=apache-tomcat-9.0.8.tar.gz
ARG SOLR_TAR=solr-7.3.1.tgz

RUN apt update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:openjdk-r/ppa && \
    apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y vim curl wget dnsutils net-tools inetutils-ping && \
    rm -rf /var/cache/apt/archives/*

ENV TZ=Asia/Shanghai \
    JRE_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre/ \
    JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/

RUN wget http://mirrors.shu.edu.cn/apache/lucene/solr/7.3.1/$SOLR_TAR -P /opt/ && tar zxf /opt/$SOLR_TAR -C /
RUN wget http://mirrors.shu.edu.cn/apache/tomcat/tomcat-9/v9.0.8/bin/$TOMCAT_TAR -P /opt/ && tar zxf /opt/$TOMCAT_TAR -C / && \
    mkdir /apache-tomcat-9.0.8/webapps/solr

RUN cp -r /solr-7.3.1/server/solr-webapp/webapp/* /apache-tomcat-9.0.8/webapps/solr/
RUN cp -r /solr-7.3.1/server/lib/ext/* /apache-tomcat-9.0.8/webapps/solr/WEB-INF/lib/
RUN cp -r /solr-7.3.1/server/lib/metrics*.* /apache-tomcat-9.0.8/webapps/solr/WEB-INF/lib/
RUN cp -r /solr-7.3.1/dist/solr-dataimporthandler-* /apache-tomcat-9.0.8/webapps/solr/WEB-INF/lib/

RUN mkdir -p /apache-tomcat-9.0.8/solrhome
RUN cp -r /solr-7.3.1/server/solr/* /apache-tomcat-9.0.8/solrhome/
RUN mkdir -p /apache-tomcat-9.0.8/webapps/solr/WEB-INF/classes && \
    cp /solr-7.3.1/example/resources/log4j.properties /apache-tomcat-9.0.8/webapps/solr/WEB-INF/classes/

COPY web.xml /apache-tomcat-9.0.8/webapps/solr/WEB-INF/web.xml

CMD /apache-tomcat-9.0.8/bin/startup.sh && tailf /apache-tomcat-9.0.8/logs/catalina.out