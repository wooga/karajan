from behave import *

from config import *


@given(u'a minimal config')
def step_impl(context):
    context.conf = min_config()


@given(u'the attribute {attr} for the {model} {id} is not set')
def step_impl(context, attr, model, id):
    conf = get_model_conf(context, model).get(id)
    conf.pop(attr, None)


@given(u'the {model} {id} has the following items')
def step_impl(context, model, id):
    conf = get_model_conf(context, model).get(id)
    conf['items'] = conf.get('items', [])
    for row in context.table:
        conf['items'].append({k: row[k] for k in row.headings})


@given(u'the column {id} is parameterized')
def step_impl(context, id):
    conf = get_column_conf(context).get(id)
    conf['query'] = conf.get('query').replace('key', '{{ key }}')


@given(u'the column {id} has a {dep_type} dependency')
def step_impl(context, id, dep_type):
    conf = get_column_conf(context).get(id)
    conf['dependencies'] = conf.get('dependencies', [])
    conf['dependencies'].append(min_dependency_config(dep_type))


@given(u'the table {id} has a timeseries key {timeseries_key}')
def step_impl(context, id, timeseries_key):
    conf = get_table_conf(context).get(id)
    conf['key_columns'] = conf.get('key_columns', {})
    conf['key_columns']['datum'] = 'DATE'
    conf['timeseries_key'] = timeseries_key