# -*- coding: utf-8 -*-
# @Time    : 2023/3/25 09:09 
# @Author  : xzr
# @File    : tasks.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :


from django.apps import apps
from django.db import ProgrammingError
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .architect.commands import partition
from .architect.exceptions import ImportProblemError


@receiver(post_migrate, sender=apps.get_app_config('framework'), dispatch_uid='framework_create_partitions_task')
def create_partitions(*args, **kwargs):
    """
    创建分区表
    """
    paths = {model.__module__ for model in apps.get_models()}
    for path in paths:
        try:
            partition.run(dict(module=path, create=True, partition_num=kwargs.get('partition_num', 3)))
        except ProgrammingError:
            # Possibly because models were just un-migrated or
            # fields have been changed that effect Architect
            print("Unable to apply partitions for module '{}'".format(path))
        except (ModuleNotFoundError, ImportProblemError) as e:
            pass
