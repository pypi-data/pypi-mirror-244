# -*- coding: utf-8 -*-
# @Time    : 2023/3/25 09:09 
# @Author  : xzr
# @File    : tasks.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :


from celery import shared_task

from .signals import create_partitions


@shared_task(ignore_result=True)
def create_partitions_task(*args, **kwargs):
    """
    创建分区表
    """
    create_partitions(partition_num=3)
