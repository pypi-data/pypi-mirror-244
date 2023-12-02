# -*- coding: utf-8 -*-
# @Time    : 2019-09-02 17:57
# @Author  : xzr
# @File    : celery_app
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 

from __future__ import absolute_import, unicode_literals

import os
import time

import ulid as ulid
from celery import Celery, Task

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.db.transaction import on_commit
from framework.utils import capture_exception


def commit_task(task_func):
    """
    发送任务时出错重试 3 次提交
    """
    replay_num = 3
    for i in range(replay_num):
        try:
            task_func()
            break
        except Exception as e:
            time.sleep(0.01)
            if i >= replay_num - 1:
                capture_exception()


class MyTask(Task):
    """等任务事务提交后再执行异步任务"""

    def apply_async(self, *args, **kwargs):  # 有些任务需要返回 task_result 所以就不全改了
        task_id = str(ulid.new())
        kwargs['task_id'] = task_id
        on_commit(lambda: commit_task(lambda: super(MyTask, self).apply_async(*args, **kwargs)))
        result = (kwargs.get('result_cls', None) or self.AsyncResult)(task_id)
        result.ignored = kwargs.get('ignored_result', False)
        return result


class MyCelery(Celery):
    task_cls = MyTask

    def send_task(self, *args, **kwargs):
        return super().send_task(*args, **kwargs)

    # def on_configure(self):
    #     client = raven.Client(settings.SENTRY_DSN)
    #     # register a custom filter to filter out duplicate logs
    #     register_logger_signal(client)
    #     # hook into the Celery error handle
    #     register_signal(client)


app = MyCelery('celery_app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    return self.request.id


# 设置任务路由 启动 celery 进程 用 -Q myadmin
# app.conf.task_routes = {'myadmin.tasks.*': {'queue': 'myadmin'}}
app.conf.task_routes = {}

celerybeat_schedule = {}

app.conf.update(
        CELERY_REDIS_MAX_CONNECTIONS=12,
        CELERY_POOL_LIMIT=13,
        CELERY_TASK_SERIALIZER='pickle',
        CELERY_RESULT_SERIALIZER='pickle',
        CELERY_ACCEPT_CONTENT=['json', 'pickle'],
        CELERY_ENABLE_UTC=False,
        CELERY_TIMEZONE='Asia/Shanghai',
        CELERY_TRANSPORT_OPTIONS={
                'max_connections': 40,
        },
        CELERYBEAT_SCHEDULE=celerybeat_schedule,
)
