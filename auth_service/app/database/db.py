import boto3
from ..config import DDB_USERS_TABLE, AWS_REGION

dynamodb = boto3.resource("dynamodb", region_name = AWS_REGION)
users_table = dynamodb.Table(DDB_USERS_TABLE)