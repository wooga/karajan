from datetime import datetime


def get_conf(context):
    if 'conf' not in context:
        context.conf = {
            'tables': {},
            'columns': {},
        }
    return context.conf


def get_model_conf(context, model):
    conf = get_conf(context)
    return conf.get('%ss' % model)


def get_column_conf(context):
    return get_model_conf(context, 'column')


def get_table_conf(context):
    return get_model_conf(context, 'table')


def min_config():
    return {
        'tables': {
            "test": {
                'start_date': datetime.now(),
                'schema': 'test',
                'key_columns': {
                    'key_column': 'VARCHAR(100)',
                },
                'aggregated_columns': {
                    'test': 'test',
                }
            }
        },
        'columns': {
            'test': {
                'query': "SELECT 'key' AS key_column, 'val' AS val FROM DUAL",
                'column_type': 'VARCHAR(100)',
            }
        },
    }


def min_dependency_config(dep_type):
    conf = {
        'tracking': {'schema': 'test', 'table': 'test'},
        'delta': {'delta': 0}
    }[dep_type]
    conf['type'] = dep_type
    return conf