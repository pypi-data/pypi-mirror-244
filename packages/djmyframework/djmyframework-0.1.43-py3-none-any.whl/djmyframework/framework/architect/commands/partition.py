"""
Partition command implementation.
"""
from ..databases.bases import BasePartition
from ..exceptions import ImportProblemError

arguments = [
        {('-m', '--module')          : {
                'dest'    : 'module',
                'required': True,
                'help'    : 'path to the module with models to be partitioned'
        }, ('-c', '--create')        : {
                'dest'    : 'create',
                'required': False,
                'default' : True,
                'action'  : 'store_true',
                'help'    : '是否创建分区'
        }, ('-pn', '--partition_num'): {
                'dest'    : 'partition_num',
                'required': False,
                'default' : 1,
                'type'    : 'int',
                'help'    : '预先创建的分区数, 日期 range 类适用'
        }}
]


def run(args):
    """
    Prepares models from specified module for partitioning.

    :param dictionary args: (required). Dictionary of command arguments.
    """
    names = []
    module = args['module'][:-3] if args['module'].endswith('.py') else args['module']

    try:
        module_clss = filter(lambda obj: isinstance(obj, type), __import__(module, fromlist=module).__dict__.values())
    except ImportError as e:
        raise ImportProblemError(str(e))

    for cls in module_clss:
        if hasattr(cls, 'architect') and hasattr(cls.architect, 'partition'):
            partition: BasePartition = cls.architect.partition.get_partition()
            if not partition.exists():
                partition.prepare()
            if args.get('create'):
                partition.create(partition_num=args.get('partition_num', 1))
            names.append(cls.__name__)

    if not names:
        return 'unable to find any partitionable models in a module: {0}'.format(module)
    else:
        return 'successfully (re)configured the database for the following models: {0}'.format(', '.join(names))
