from datetime import datetime, date, timedelta

import airflow.bin.cli as cli
from airflow import settings
from airflow.models import DagBag
from dateutil.parser import parse as parsedate

from karajan.exceptions import KarajanException
from karajan.model import KarajanDAG


def run(args):
    # load DAGs and find KarajanDAGs
    dags = get_dags(args)

    run_id = "karajan_run_{}".format(datetime.now())
    start_date = args.start_date if args.start_date else yesterday()
    end_date = args.end_date if args.end_date else yesterday()

    conf = {
        'start_date': start_date,
        'end_date': end_date,
    }

    # create DAG runs
    for dag in dags.values():
        cli.api_client.trigger_dag(dag_id=dag.dag_id,
                                   run_id=run_id,
                                   conf=conf,
                                   execution_date=end_date)


def yesterday():
    return datetime.combine(date.today(), datetime.min.time()) - timedelta(days=1)


def get_dags(args):
    dagbag = DagBag(cli.process_subdir(args.subdir))
    dags = {id: dag for id, dag in dagbag.dags.iteritems() if isinstance(dag, KarajanDAG)}
    # check weither we want selected KarajanDAGs or all of them
    if hasattr(args, 'karajan_id'):
        dags = {id: dag for id, dag in dags.iteritems() if dag.karajan_id == args.karajan_id}
        if not dags:
            raise KarajanException('no DAGs with karajan_id {} found.'.format(args.karajan_id))
        return dags
    return dags


class KarajanCLIFactory(cli.CLIFactory):
    args = {
        'karajan_id': cli.Arg(("karajan_id",), "The id of the Karajan setup"),
        'subdir': cli.Arg(
            ("-sd", "--subdir"),
            "File location or directory from which to look for the dag",
            default=settings.DAGS_FOLDER),
        'start_date': cli.Arg(
            ("-s", "--start_date"), "Override start_date YYYY-MM-DD",
            type=parsedate),
        'end_date': cli.Arg(
            ("-e", "--end_date"), "Override end_date YYYY-MM-DD",
            type=parsedate),
    }

    subparsers = (
        {
            'func': run,
            'help': "Trigger aggregations for a Karajan setup",
            'args': ('karajan_id', 'subdir', 'start_date', 'end_date'),
        },
    )
    subparsers_dict = {sp['func'].__name__: sp for sp in subparsers}