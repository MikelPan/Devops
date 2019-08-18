### 安装ansible
```shell
# 安装ansible
yum install -y ansible
pip install ansible_alicloud
pip install footmark 
pip install ansible_alicloud
export ALICLOUD_ACCESS_KEY="your_accesskey"
export ALICLOUD_SECRET_KEY="your_accesskey_secret"
```
### 使用ansible 创建阿里云资源
```shell
# 创建vpc
- name: Create a new AlibabaCloud VPC resource
    ali_vpc:
      alicloud_region: '{{ alicloud_region }}'
      cidr_block: '{{ vpc_cidr }}'
      vpc_name: '{{ vpc_name }}'
    when: not vpcs.vpcs
    register: vpc
# 创建交换机
- name: Create a new Alibaba Cloud VSwitch resource
    ali_vswitch:
      alicloud_region: '{{ alicloud_region }}'
      alicloud_zone: '{{ alicloud_zone }}'
      state: 'present'
      cidr_block: '{{ vswitch_cidr }}'
      vswitch_name: '{{ vswitch_name }}'
      description: '{{ vswitch_description }}'
      vpc_id: '{{vpcs.vpcs.0.id}}'
    register: vswitch
# 创建安全组
- name: Create a security group
    ali_security_group:
      alicloud_region: '{{ alicloud_region }}'
      state: 'present'
      name: '{{ group_name }}'
      description: '{{ group_description }}'
      vpc_id: '{{vpcs.vpcs.0.id}}'
      rules: '{{ group_inboundRules }}'
      rules_egress: '{{ group_outboundRules }}'
    register: group
# 创建ecs
- name: Create an ECS instance
    ali_instance:
      alicloud_region: '{{ alicloud_region }}'
      alicloud_zone: '{{ alicloud_zone }}'
      image_id: '{{ image }}'
      instance_type: '{{ type }}'
      instance_name: '{{ instance_name }}'
      description: '{{ description }}'
      host_name: '{{ host_name }}'
      key_name: '{{ key_name }}'
      vswitch_id: '{{vswitch.vswitch.id}}'
      security_groups: '{{group.group.id}}'
      count: '{{count}}'
      allocate_public_ip: '{{ allocate_public_ip }}'
      internet_charge_type: '{{ internet_charge_type }}'
      max_bandwidth_in: '{{ max_bandwidth_in }}'
      max_bandwidth_out: '{{ max_bandwidth_out }}'
      tags: '{{tags}}'
    register: ecs
  - name: output information of the vm
    debug:
      msg: "The created vm is {{ ecs }}."
```
### 使用动态资源创建
```shell
# 使用动态库
pip install ansible_alicloud_module_utils
pip show footmark
pip install footmark --upgrade
wget https://raw.githubusercontent.com/alibaba/ansible-provider/master/contrib/inventory/alicloud.py
chmod +x alicloud.py
wget https://raw.githubusercontent.com/alibaba/ansible-provider/master/contrib/inventory/alicloud.ini
alicloud_access_key = Abcd1234 
alicloud_secret_key = Abcd2345
export ALICLOUD_ACCESS_KEY = Abcd1234
export ALICLOUD_SECRET_KEY = Abcd2345
./alicloud.py --list
```