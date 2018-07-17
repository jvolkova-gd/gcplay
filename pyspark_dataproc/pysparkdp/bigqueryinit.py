""" Create BigQuery dataset and table if not exist"""
from os import getenv

from google.cloud import bigquery
from google.api_core.exceptions import Conflict

from pysparkdp.config import Config, logger

Config().init_connect()

bc = bigquery.Client()

# ds == dataset
# Dataset IDs must be alphanumeric (plus underscores)
# and must be at most 1024 characters long.
ds_id = "bigquery_python"
ds_ref = bc.dataset(ds_id)
ds = bigquery.Dataset(ds_ref)
try:
    ds = bc.create_dataset(ds)
except Conflict:
    logger.info("Dataset %s already exist", ds_id)
    ds = bc.get_dataset(ds_ref)


table_id = "lines"
table_ref = ds_ref.table(table_id)
table = bigquery.Table(table_ref)
table.description = "Lines from GS process"
table.schema = [
    bigquery.SchemaField('line', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('id', 'INTEGER', mode='REQUIRED')
]

table.partitioning_type = 'DAY'
# remove tables in 7 days, partition_expiration - for TTL
table.partition_expiration = 604800000

try:
    table = bc.create_table(table)
except Conflict:
    logger.info("Table %s  in dataset %s already exist", table_id, ds_id)
    table = bc.get_table(table_ref)

rows_to_insert_for_test = [
    ('first test line', 1), ('second test line', 2)
]

bc.create_rows(table, rows_to_insert_for_test)
