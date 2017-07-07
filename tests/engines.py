from datetime import datetime, date
from unittest import TestCase

from nose.tools import assert_equal
from parameterized import parameterized

from karajan.engines import ExasolEngine


class TestExasolEngine(TestCase):
    class Stub(object):
        def __init__(self, **kwargs):
            for k,v in kwargs.iteritems():
                setattr(self, k,v)

        def setattr(self, attr, value):
            setattr(self, attr, value)

    def setUp(self):
        self.engine = ExasolEngine()

    def test_param_column_op_w_item(self):
        context = TestExasolEngine.Stub(
            item_column='item_column'
        )
        target = TestExasolEngine.Stub(
            name='test_table',
            schema='test_schema',
            parameter_columns={
                'date_col': 'date',
                'datetime_col': 'datetime',
                'number_col': 'number',
                'bool_col': 'bool',
            },
            context=context
        )
        task_id = 'merge_parameter_columns'
        params = {
            'item': 'g9',
            'date': date(2017, 1, 1),
            'datetime': datetime(2017, 1, 1, 0, 0, 0),
            'number': 42,
            'bool': True,
        }
        op = self.engine.param_column_op(task_id, None, target, params, 'g9')
        expected = [
            "UPDATE test_schema.test_table SET datetime_col = '2017-01-01 00:00:00' WHERE (datetime_col IS NULL OR datetime_col != '2017-01-01 00:00:00') AND item_column = 'g9'",
            "UPDATE test_schema.test_table SET number_col = 42 WHERE (number_col IS NULL OR number_col != 42) AND item_column = 'g9'",
            "UPDATE test_schema.test_table SET bool_col = True WHERE (bool_col IS NULL OR bool_col != True) AND item_column = 'g9'",
            "UPDATE test_schema.test_table SET date_col = '2017-01-01' WHERE (date_col IS NULL OR date_col != '2017-01-01') AND item_column = 'g9'",
        ]
        assert_equal(expected, op.sql)

    def test_param_column_op_wo_item(self):
        context = TestExasolEngine.Stub(
            item_column='item_column'
        )
        target = TestExasolEngine.Stub(
            name='test_table',
            schema='test_schema',
            parameter_columns={
                'date_col': 'date',
                'datetime_col': 'datetime',
                'number_col': 'number',
                'bool_col': 'bool',
            },
            context=context
        )
        task_id = 'merge_parameter_columns'
        params = {
            'date': date(2017, 1, 1),
            'datetime': datetime(2017, 1, 1, 0, 0, 0),
            'number': 42,
            'bool': True,
        }
        op = self.engine.param_column_op(task_id, None, target, params, '')
        expected = [
            "UPDATE test_schema.test_table SET datetime_col = '2017-01-01 00:00:00' WHERE (datetime_col IS NULL OR datetime_col != '2017-01-01 00:00:00')",
            "UPDATE test_schema.test_table SET number_col = 42 WHERE (number_col IS NULL OR number_col != 42)",
            "UPDATE test_schema.test_table SET bool_col = True WHERE (bool_col IS NULL OR bool_col != True)",
            "UPDATE test_schema.test_table SET date_col = '2017-01-01' WHERE (date_col IS NULL OR date_col != '2017-01-01')",
        ]
        assert_equal(expected, op.sql)
