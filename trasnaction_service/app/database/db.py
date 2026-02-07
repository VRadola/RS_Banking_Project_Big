import boto3
from config import AWS_REGION, DDB_TRANSACTION_TABLE

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
db_client = boto3.client("dynamodb", region_name=AWS_REGION)

transaction_table = dynamodb.Table(DDB_TRANSACTION_TABLE)