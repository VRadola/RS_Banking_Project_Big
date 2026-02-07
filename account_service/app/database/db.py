import boto3
from config import AWS_REGION, DDB_ACCOUNTS_TABLE, DDB_CARDS_TABLE

dynamodb = boto3.resource("dynamo_db", region_name=AWS_REGION)
db_client = boto3.client("dynamo_db", region_name=AWS_REGION)

accounts_table = dynamodb.Table(DDB_ACCOUNTS_TABLE)
cards_table = dynamodb.Table(DDB_CARDS_TABLE)