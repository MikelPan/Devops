### 使用travis ci构建
新建一个项目用来做CICD流程演示 CICD_DEMO https://github.com/gitplyx/CICD_DEMO.git
#### 配置travis 仓库
登录网站激活 仓库 https://travis-ci.org  并配置变量
DOCKER_USERNAME
DOCKER_PASSWORD
#### 注册dockerhub账号
https://cloud.docker.com/
#### 在项目根目录新建一个 Dockerfile 文件
```shell
FROM alpine
RUN echo "Hello World"
```
#### 新建 Travis CI 配置文件 .travis.yml 文件
```shell
language: bash
dist: xenial
services:
  - docker
install: php vendor/vendors.php
before_script:
  # 登录到 docker hub
  - echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
script:
  # 这里编写测试代码的命令
  - echo "test code"
after_success:
  # 当代码测试通过后执行的命令
  - docker build -t dockerplyx/alpine .
  - docker push dockerplyx/alpine
notifications:
  slack:
    rooms:
      - <account>:<token> # deployment
      - <account>:<token> # dev
      - secure: "sdfusdhfsdofguhdfgubdsifgudfbgs3453durghssecurestringidsuag34522irueg="  #加密
    template:
      - "%{repository_slug} (%{commit}) : %{message}"
      - "Build details: %{build_url}"
    webhooks:
      urls:
        - http://hooks.mydomain.com/travisci
        - http://hooks.mydomain.com/events
    on_success: change # default: always
    on_failure: always # default: always
    on_start:   change # default: never
    on_cancel:  always # default: always
    on_error:   always # default: always
    on_success: always
    on_failure: always
  email:
    recipients:
      - plyx_46204@126.com
    on_success: always
    on_failure: always
before_deploy: "echo 'ready?'"
deploy:
  provider: codedeploy
  access_key_id: "YOUR AWS ACCESS KEY"
  secret_access_key: "YOUR AWS SECRET KEY"
  bucket: "S3 Bucket"
  key: latest/MyApp.zip
  bundle_type: zip
  application: MyApp
  deployment_group: MyDeploymentGroup
  on:
    branch: production
after_deploy:
  - ./after_deploy_1.sh
  - ./after_deploy_2.sh
```

