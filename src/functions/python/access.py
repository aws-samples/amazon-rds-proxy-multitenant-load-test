# Access layer
import json
import os
import random
import sys
import urllib.request

import boto3
import pymysql.cursors

ENDPOINT = os.environ["ENDPOINT"]
PORT = 3306
REGION = os.environ["REGION"]
ACCOUNT_ID = os.environ["ACCOUNT_ID"]
CLUSTER_ENDPOINT_RESOURCE = os.environ["CLUSTER_ENDPOINT_RESOURCE"]
SSL_CERTIFICATE_URL = os.environ["SSL_CERTIFICATE_URL"]
os.environ["LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN"] = "1"
user_name = "user"
database_name = "user_database"

urllib.request.urlretrieve(SSL_CERTIFICATE_URL, "/tmp/SSLCA.pem")


def lambda_handler(event, context):

    random_ints = [random.randint(0, 999) for i in range(5)]
    where_clause = f"{random_ints[0], random_ints[1], random_ints[2], random_ints[3], random_ints[4]}"
    query = f"SELECT * FROM mytable WHERE ID IN {where_clause};"

    # tenant id
    tenant_id = event["queryStringParameters"]["tenant"]
    dbUser = user_name + tenant_id
    # dbUser = 'user100'

    # database
    database = database_name + tenant_id
    # database = 'user_database100'

    # Resource name
    resource = CLUSTER_ENDPOINT_RESOURCE + tenant_id
    # resource = f"arn:aws:rds-db:{REGION}:{ACCOUNT_ID}:dbuser:*/user100"

    arn = os.environ["IAM_ARN"]

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
        conn = pymysql.connect(
            host=ENDPOINT,
            user=dbUser,
            password=token,
            port=PORT,
            database=database,
            cursorclass=pymysql.cursors.DictCursor,
            ssl_ca="/tmp/SSLCA.pem",
            ssl_verify_cert=True,
        )
        cur = conn.cursor()
        cur.execute(query)
        query_results = cur.fetchall()
        print(query_results)
        cur.close()

        return {"statusCode": 200, "body": json.dumps(query_results)}

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": "Internal Server Error"}
