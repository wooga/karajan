#
# Copyright 2017 Wooga GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime, date


class ConfigHelper(dict):
    @staticmethod
    def __default_config():
        return {
            'context': {
                'defaults': {},
            },
            'targets': {
                'test_table': {
                    'start_date': datetime.now(),
                    'schema': 'test_schema',
                    'key_columns': ['key_column'],
                    'aggregated_columns': {
                        'test_aggregation': {
                            'test_column': {
                                'column_name': 'test_src_column',
                                'update_type': 'REPLACE',
                            },
                            'another_test_column': {
                                'column_name': 'another_test_src_column',
                                'update_type': 'MAX',
                            },
                        },
                        'another_aggregation': {
                            'another_aggregation_test_column': {
                                'column_name': 'another_aggregation_test_src_column',
                                'update_type': 'KEEP',
                            }
                        },
                    },
                },
                'another_table': {
                    'start_date': datetime.now(),
                    'schema': 'another_test_schema',
                    'key_columns': ['key_column'],
                    'aggregated_columns': {
                        'test_aggregation': {
                            'test_column': {
                                'column_name': 'another_table_test_src_column',
                                'update_type': 'MIN',
                            },
                        },
                    },
                },
            },
            'aggregations': {
                'test_aggregation': {
                    'query': "SELECT * FROM DUAL WHERE dt BETWEEN '{{ start_date }}' AND '{{ end_date }}'",
                    'time_key': 'test_time_key',
                },
                'another_aggregation': {
                    'query': 'SELECT everything FROM here',
                    'time_key': 'another_test_time_key',
                },
            },
        }

    def __init__(self, **kwargs):
        super(ConfigHelper, self).__init__(**kwargs)
        self.update(self.__default_config())

    def parameterize_context(self, items=None, with_targets=True):
        if items is None:
            items = {'item': {}, 'another_item': {}}
        self['context']['items'] = items
        self['context']['item_column'] = 'item_column'
        if with_targets:
            for tk, tv in self['targets'].iteritems():
                tv['items'] = '*'
        return self

    def parameterize_aggregation(self, aggregation_id='test_aggregation'):
        self['aggregations'][aggregation_id]['query'] = "SELECT * FROM {{ item }} WHERE dt BETWEEN '{{ start_date }}' AND '{{ end_date }}'"
        return self

    def with_parameter_columns(self):
        params = {
            'date': date(2017, 1, 1),
            'datetime': datetime(2017, 1, 1, 0, 0, 0),
            'number': 42,
            'bool': True,
        }
        if self['context'].get('items'):
            for item, p in self['context'].get('items').iteritems():
                p.update(params)
        else:
            self['context']['defaults'].update(params)
        for tc in self['targets'].values():
            parameter_columns = {}
            for k in params:
                parameter_columns["%s_col" % k] = k
            tc['parameter_columns'] = parameter_columns
        return self

    def with_timeseries(self, target_id='test_table'):
        self['targets'][target_id]['timeseries_key'] = 'timeseries_column'
        return self

    def with_offset(self, offset=1, aggregation_id='test_aggregation'):
        self['aggregations'][aggregation_id]['offset'] = offset
        return self

    def with_reruns(self, reruns=3, aggregation_id='test_aggregation'):
        self['aggregations'][aggregation_id]['reruns'] = reruns
        return self
