# Access layer
import json
import os
import random
import sys

import boto3
import mysql.connector

ENDPOINT = os.environ["endpoint"]
PORT = "3306"
REGION = os.environ["region"]
os.environ["LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN"] = "1"
user_name = "user"
database_name = "user_database"


def lambda_handler(event, context):

    random_ints = [random.randint(0, 999) for i in range(5)]
    where_clause = f"{random_ints[0], random_ints[1], random_ints[2], random_ints[3], random_ints[4]}"
    query = f"SELECT * FROM mytable WHERE ID IN {where_clause};"

    # tenant id
    tenant_id = event["queryStringParameters"]["tenant"]
    dbUser = user_name + tenant_id
    # dbUser = 'user100';

    # database
    database = database_name + tenant_id
    # database = 'user_database100';

    # Resource name
    resource_a = os.environ["cluster_endpoint_resource"]
    resource = resource_a + tenant_id
    # resource = 'arn:aws:rds-db:us-east-1:account-no:dbuser:*/user100';

    arn = os.environ["iam_arn"]

    session_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {"Effect": "Allow", "Action": "rds-db:connect", "Resource": resource}
        ],
    }

    # gets the credentials from .aws/credentials
    client_sts = boto3.client("sts")

    sts_response = client_sts.assume_role(
        RoleArn=arn, RoleSessionName="test", Policy=json.dumps(session_policy)
    )

    session = boto3.Session()
    client = boto3.client(
        "rds",
        aws_access_key_id=sts_response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=sts_response["Credentials"]["SecretAccessKey"],
        aws_session_token=sts_response["Credentials"]["SessionToken"],
    )

    token = client.generate_db_auth_token(
        DBHostname=ENDPOINT, Port=PORT, DBUsername=dbUser, Region=REGION
    )

    try:
        conn = mysql.connector.connect(
            host=ENDPOINT, user=dbUser, passwd=token, port=PORT, database=database
        )
        cur = conn.cursor()
        cur.execute(query)
        query_results = cur.fetchall()
        print(query_results)

    except Exception as e:
        print("Database connection failed due to {}".format(e))
        query_results = "Database connection failed due to {}".format(e)

    return {"statusCode": 200, "body": json.dumps(query_results)}
