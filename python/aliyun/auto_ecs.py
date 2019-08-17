#!/usr/bin/env python
# coding=utf-8
import json
import time
import traceback
from multiprocessing.pool import ThreadPool

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from aliyunsdkecs.request.v20140526.RenewInstanceRequest import RenewInstanceRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest


RUNNING_STATUS = 'Running'
CHECK_INTERVAL = 2
CHECK_TIMEOUT = 60


class InvalidInstanceId(Exception):
    pass


class AliyunRenewInstancesExample(object):

    def __init__(self):
        self.access_id = '<ACCESS_KEY_ID>'
        self.access_secret = '<ACCESS_SECRET>'
        # 实例所属的地域ID
        self.region_id = 'cn-shenzhen'
        # 指定的需要续费的实例 ID
        self.instance_ids = ['i-wz9bxddqvgcj7grwibd2']
        # 预付费续费时长
        self.period = 1
        # 续费时长单位，取值：Week/Month
        self.period_unit = 'Month'
        
        self.instance_charge_type = 'PrePaid'
        # "ecs.api.generator.renew_expire_time"
        self.expired_start_time = 'ExpiredStartTime'
        self.expired_end_time = 'ExpiredEndTime'
        # "ecs.api.generator.renew_page_size"
        self.page_size = 100

        self.client = AcsClient(self.access_id, self.access_secret, self.region_id)
        self.pool = ThreadPool(100)

    def run(self):
        try:
            self.renew_instances()
        except ClientException as e:
            print('Fail. Something with your connection with Aliyun go incorrect.'
                  ' Code: {code}, Message: {msg}'
                  .format(code=e.error_code, msg=e.message))
        except ServerException as e:
            print('Fail. Business error.'
                  ' Code: {code}, Message: {msg}'
                  .format(code=e.error_code, msg=e.message))
        except InvalidInstanceId as e:
            print(e)
        except Exception:
            print('Unhandled error')
            print(traceback.format_exc())

    def renew_instances(self):
        """
        批量续费实例，若需查询需要续费的实例，可查看 get_renew_instances 方法
        :return:
        """
        # self.instance_ids = self.get_renew_instances()
        instances = self.describe_instances()
        # 更新实例过期时间
        original_expired_time = {}
        for instance in instances:
            original_expired_time[instance['InstanceId']] = instance['ExpiredTime']
        # 通过多线程的方式进行批量续费
        self.pool.map(self.renew_instance, self.instance_ids)
        self.pool.close()
        self.pool.join()
        # 检查续费是否成功
        self._check_instances_expired_time(original_expired_time)

    def renew_instance(self, instance_id):
        """
        续费单个实例
        :param instance_id: 实例ID
        :return:
        """
        request = RenewInstanceRequest()
        request.set_InstanceId(instance_id)
        request.set_Period(self.period)
        request.set_PeriodUnit(self.period_unit)
        # 发送请求
        self.client.do_action_with_exception(request)
        
    def get_renew_instance_ids(self):
        """
        获取需要续费的实例ID
        :param instance_id: 实例ID列表
        :return:
        """
        start_time_utc = '2018-10-21T16:00Z'
        end_time_utc = '2018-12-01T16:00Z'
        page_num = 1
        total_count = 1
        instance_ids = []
        while len(instance_ids) < total_count:
            request = DescribeInstancesRequest()
            request.set_Filter3Key(self.expired_start_time)
            request.set_Filter3Value(start_time_utc)
            request.set_Filter4Key(self.expired_end_time)
            request.set_Filter4Value(end_time_utc)
            request.set_InstanceChargeType(self.instance_charge_type)
            request.set_PageSize(self.page_size)
            request.set_PageNumber(page_num)
            body = self.client.do_action_with_exception(request)
            data = json.loads(body)

            if not data['TotalCount']:
                return instance_ids

            ids = [str(instance['InstanceId']) for instance in data['Instances']['Instance']]
            instance_ids.extend(ids)
            total_count = data['TotalCount']
            page_num += 1
        print('Success. Instances which should be renewed include: {}'.format(', '.join(instance_ids)))
        return instance_ids

    def describe_instances(self):
        """
        获取实例信息
        :return: 实例信息列表
        """ 
        offset = 0
        total_count = len(self.instance_ids)
        instances = []
        while offset < total_count:
            ids = self.instance_ids[offset:min(offset+self.page_size, total_count)]
            request = DescribeInstancesRequest()
            request.set_PageSize(self.page_size)
            request.set_InstanceChargeType(self.instance_charge_type)
            request.set_InstanceIds(ids)
            body = self.client.do_action_with_exception(request)
            data = json.loads(body)
            ins = data['Instances']['Instance']
            ret_instance_ids = [instance['InstanceId'] for instance in ins]
            invalid_instance_ids = set(ids) - set(ret_instance_ids)
            if invalid_instance_ids:
                raise InvalidInstanceId('Fail. Invalid InstanceIds: {}'
                                        .format(', '.join(invalid_instance_ids)))
            instances.extend(ins)
            offset += self.page_size
        return instances

    def _check_instances_expired_time(self, original_expired_time):
        """
        每2秒中检查一次实例的到期时间，超时时间设为1分钟
        :param original_expired_time: 记录实例ID和原始过期时间的映射关系的字典.
        :return:
        """        
        start = time.time()
        while True:
            all_completed = True
            uncompleted_instance_ids = []
            instances = self.describe_instances()
            for instance in instances:
                if instance['ExpiredTime'] == original_expired_time[instance['InstanceId']]:
                    uncompleted_instance_ids.append(instance['InstanceId'])
                    all_completed = False

            if all_completed:
                print('Instances renew successfully')
                break

            if time.time() - start > CHECK_TIMEOUT:
                print('Check instance expired time timeout. '
                      'Following instances still not renewed successfully: {}'
                      .format(', '.join(uncompleted_instance_ids)))
                break

            time.sleep(CHECK_INTERVAL)
        return all_completed


if __name__ == '__main__':
    AliyunRenewInstancesExample().run()