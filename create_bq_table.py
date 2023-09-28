import logging
import os
from datetime import datetime
import google.cloud.logging
from google.cloud import bigquery


logging.basicConfig(
    format="[%(asctime)s][%(levelname)s] %(message)s", level=logging.INFO
)
logger = logging.getLogger()

logging_client = google.cloud.logging.Client()
logging_client.setup_logging()
logger.setLevel(logging.INFO)

bq_table = os.environ['BQ_TABLE']


def main(request):
    '''
    detele (existing) bq_table and crate new table
    e.g. schema for dataset policy
    '''
    client = bigquery.Client()
    client.delete_table(table=bq_table, not_found_ok=True)
    schema = [
        bigquery.SchemaField("user_by_email", "STRING", mode="Nullable"),
        bigquery.SchemaField("special_group", "STRING", mode="Nullable"),
        bigquery.SchemaField("role", "STRING", mode="Required"),
        bigquery.SchemaField("dataset_id", "STRING", mode="Required"),
        bigquery.SchemaField("date", "DATE", mode="Required")
    ]

    table = bigquery.Table(bq_table, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="date",
        expiration_ms=7776000000  # 90 days
        )

    client.create_table(table)
    logger.info(
        "Created table {}.{}.{}".format(
            table.project, table.dataset_id, table.table_id)
    )
    return 'OK', 200
