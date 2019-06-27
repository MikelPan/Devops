#！/usr/bin/env python
# _*_ coding: utf-8 _*_
# 开发团队：云飞国际
# 开发人员： 93792
# 开发时间： 2019/6/2 16:18
# 文件名称： ansible_message.py
# 开发工具： PyCharm

import os,sys,json,shutil,re
import ansible.constants as C
C.HOST_KEY_CHECKING = False
from ansible.plugins.callback import CallbackBase
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import  DataLoader
from ansible.vars.manager import  VariableManager
from ansible.inventory.manager import  InventoryManager
from ansible.playbook import Play
from ansible.executor.task_queue_manager import  TaskQueueManager
from ansible import context

class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


def ansible_command():
    # 获取主机组信息
    BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source = os.path.join(BaseDir,'/etc/ansible/hosts')

    # 实例化loader对象
    loader = DataLoader()
    results_callback = ResultCallback()
    myinven = InventoryManager(loader=loader, sources=[source,])   # 实例化inventory对象

    varmanager = VariableManager(loader=loader, inventory=myinven)  # 实例化VariableManager对象
    context.CLIARGS = ImmutableDict(connection='smart', module_path='/root/.ansible/plugins/modules', forks=10, become=None,
                                    become_method=None, become_user=None, check=False, diff=False)


    # 执行对象和模块
    play_data = dict(
        name="Ansible adhoc example",
        hosts='all',
        gather_facts='no',
        tasks=[
            dict(action=dict(module='setup', args=""),register='shell_out'),
            dict(action=dict(module='debug', args=dict(msg="{{  shell_out }}"))),
         ],
    )

    play = Play().load(data=play_data,loader=loader,variable_manager=varmanager)
    passwords = {}

    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=myinven,
            variable_manager=varmanager,
            loader=loader,
            passwords=passwords,
            stdout_callback=results_callback,
            # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
        )
        result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
    finally:
        # we always need to cleanup child procs and the structres we use to communicate with them
        if tqm is  not None:
            list = []
            dict2 = {}
            dict2.update(tqm.__dict__)
            list.append(dict2)
            dict3 = dict2['hostvars']
            list_1 = []
            for v in dict3:
                ip = v
                list_1.append(ip)
            for j in list_1:
                dict4 = dict3[j]['ansible_facts']
                for k in dict4:
                    print(k)
                    if k == 'hostname':
                        print(dict4['hostname'])
                    elif k == 'fqdn':
                        print(dict4['fqdn'])
                    elif k == 'uptime_seconds':
                        print(dict4['uptime_seconds'])
                    elif k == 'domain':
                        print(dict4['domain'])
                    elif k == 'memtotal_mb':
                        print(str(dict4['memtotal_mb']/1024)+'M')
                    elif k == 'default_ipv4':
                        print(dict4['default_ipv4']['address'])



show_list = [('fqdn', u'主机名'),
             ('domain', u'域名'),
             ('uptime', u'运行时间'),
             ('kernelrelease', u'内核版本'),
             ('ip', u'IP'),
             ('mac', u'MAC'),
             ]


def data(result):
    if result:
        for line in result:

            if re.findall('=>', line):
                key, value = line.split('=>', 1)
                result_dict[key.strip()] = value.strip()
        for f_k, f_s in show_list:
            if f_k in result_dict:
                print(f_s, ":", result_dict[f_k])

if __name__ == '__main__':
    result_dict = {}
    result = ansible_command()
    data(result)

