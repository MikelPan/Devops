#!/bin/bash
#
# docker-entrypoint for docker-solr

# Generate Data Config XML FIle
cat > /opt/solr/server/solr/gettingstarted/conf/data-config.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<dataConfig>
    <dataSource name="mydb" driver="com.mysql.jdbc.Driver" url="jdbc:mysql://${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE}" user="${MYSQL_USERNAME}" password="${MYSQL_PASSWORD}"/>
  <document>
      <entity name="resumeinfo_all" dataSource="mydb"
          query="select id, phone, username, email, jobs, degree, age from repository_resumeinfo" pk="id">
          <field name="id" column="id" />
          <field name="phone" column="phone" />
          <field name="username" column="username" />
          <field name="email" column="email" />
          <field name="jobs" column="jobs" />
          <field name="degree" column="degree" />
          <field name="age" column="age" />
      </entity>
        <entity name="resume_source_text" dataSource="mydb"
          query="select resumeinfo_id, repository_resumesourcetext.describe as c from repository_resumeinfo_raw_text LEFT OUTER JOIN repository_resumesourcetext ON resumeinfo_id = repository_resumesourcetext.id">
          <field name="id" column="resumeinfo_id" />
          <field name="raw_text" column="c" />
      </entity>
  </document>
</dataConfig>
EOF

set -e

if [[ "$VERBOSE" = "yes" ]]; then
    set -x
fi

if [[ -v SOLR_PORT ]] && ! grep -E -q '^[0-9]+$' <<<"${SOLR_PORT:-}"; then
  SOLR_PORT=8983
  export SOLR_PORT
fi

# when invoked with e.g.: docker run solr -help
if [ "${1:0:1}" = '-' ]; then
    set -- solr-foreground "$@"
fi

# execute command passed in as arguments.
# The Dockerfile has specified the PATH to include
# /opt/solr/bin (for Solr) and /opt/docker-solr/scripts (for our scripts
# like solr-foreground, solr-create, solr-precreate, solr-demo).
# Note: if you specify "solr", you'll typically want to add -f to run it in
# the foreground.
exec "$@"