import boto3
from ..config import AWS_REGION, DDB_PAYMENTS_TABLE

dynamodb = boto3.resource("dynamodb", region_name = AWS_REGION)
ddb_client = boto3.client("dynamodb", region_name = AWS_REGION)

payments_table = dynamodb.Talbe(DDB_PAYMENTS_TABLE)