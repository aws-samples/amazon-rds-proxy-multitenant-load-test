import json
import logging
import os
import random
import secrets
import string

import boto3
import mysql.connector
from crhelper import CfnResource

logger = logging.getLogger(__name__)
helper = CfnResource(
    json_logging=False, log_level="DEBUG", boto_level="CRITICAL", sleep_on_delete=120
)
secretsmanager = boto3.client("secretsmanager")
rds = boto3.client("rds")

ENDPOINT = os.environ["ENDPOINT"]
PORT = "3306"
USR = os.environ["USER"]
NUMBER_OF_USERS = os.environ["USERS_TO_CREATE"]
NUMBER_OF_ROWS = os.environ["NUMBER_OF_ROWS"]
REGION = os.environ["REGION"]
DBNAME = os.environ["DATABASE"]
PROXY_NAME = os.environ["PROXY_NAME"]
os.environ["LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN"] = "1"
secret_arn = os.environ["SECRETARN"]

alphabet = string.ascii_letters + string.digits
passwords = [
    "".join(secrets.choice(alphabet) for n in range(32))
    for i in range(int(NUMBER_OF_USERS))
]

secret_tags = [
    {"Key": "Project", "Value": "Proxy"},
]


@helper.create
def create(event, context):
    logger.info("Got Create")

    secret_value = json.loads(
        secretsmanager.get_secret_value(SecretId=secret_arn)["SecretString"]
    )
    password = secret_value["password"]
    proxy_auth = []

    num_rows = int(NUMBER_OF_ROWS)

    try:
        conn = mysql.connector.connect(
            host=ENDPOINT, user=USR, passwd=password, port=PORT, database=DBNAME
        )
        cur = conn.cursor()
        cur.execute("START TRANSACTION;")
        for i in range(int(NUMBER_OF_USERS)):
            dbusername = "user" + str(i)
            dbname = "user_database" + str(i)
            query1 = f"CREATE USER {dbusername} IDENTIFIED BY '{passwords[i]}';"
            query2 = f"CREATE DATABASE {dbname};"
            query3 = f"GRANT ALL PRIVILEGES ON {dbname}.* TO {dbusername};"
            query4 = f"USE {dbname}"
            query5 = f"CREATE TABLE mytable (ID INT AUTO_INCREMENT PRIMARY KEY, Column_A VARCHAR(10), Column_B VARCHAR(10), Column_C VARCHAR(10), Column_D VARCHAR(10), Column_E VARCHAR(10));"
            insert_query = [
                f"INSERT INTO mytable (Column_A,Column_B,Column_C,Column_D,Column_E) VALUES ({random.randint(1, 1000000)},{random.randint(1, 1000000)},{random.randint(1, 1000000)},{random.randint(1, 1000000)},{random.randint(1, 1000000)});"
                for i in range(num_rows)
            ]
            for query in [query1, query2, query3, query4, query5]:
                cur.execute(query)
            for insert in insert_query:
                cur.execute(insert)

            secret_name = (
                "Amazon_rds_proxy_multitenant_load_test/Proxy_secret_for_user" + str(i)
            )
            secret_description = (
                "Proxy secret created, for use with RDS Proxy and Aurora MySQL, for user"
                + str(i)
            )
            secret_string = {
                "username": f"user{str(i)}",
                "password": f"{passwords[i]}",
                "engine": "mysql",
                "port": 3306,
                "dbname": f"{dbname}",
                "dbClusterIdentifier": "proxy",
            }
            response = secretsmanager.create_secret(
                Name=secret_name,
                Description=secret_description,
                SecretString=json.dumps(secret_string),
                Tags=secret_tags,
            )

            proxy_auth.append(
                {
                    "SecretArn": response["ARN"],
                    "IAMAuth": "REQUIRED",
                }
            )

        cur.execute("COMMIT;")

        rds.modify_db_proxy(DBProxyName=PROXY_NAME, Auth=proxy_auth)

        print("Success")

    except Exception as e:
        print("Connection failed due to {}".format(e))

    return helper.PhysicalResourceId


@helper.update
def update(event, context):
    logger.info("Got Update")


@helper.delete
def delete(event, context):
    logger.info("Got Delete")
    _delete_secret()


def handler(event, context):
    helper(event, context)


def _delete_secret():
    for num in range(int(NUMBER_OF_USERS)):
        secret_name = (
            f"Amazon_rds_proxy_multitenant_load_test/Proxy_secret_for_user{num}"
        )
        secretsmanager.delete_secret(
            SecretId=secret_name, ForceDeleteWithoutRecovery=True
        )
