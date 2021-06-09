import json
import logging
import os
import random

import boto3
import mysql.connector
from crhelper import CfnResource

logger = logging.getLogger(__name__)
helper = CfnResource(
    json_logging=False, log_level="DEBUG", boto_level="CRITICAL", sleep_on_delete=120
)

try:
    secretsmanager = boto3.client("secretsmanager")
    rds = boto3.client("rds")

    ENDPOINT = os.environ["ENDPOINT"]
    PORT = "3306"
    USR = os.environ["USER"]
    NUMBER_OF_USERS = os.environ["USERS_TO_CREATE"]
    NUMBER_OF_ROWS = os.environ["NUMBER_OF_ROWS"]
    REGION = os.environ["REGION"]
    DBNAME = os.environ["DATABASE"]
    os.environ["LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN"] = "1"
    secret_arn = os.environ["SECRETARN"]
except Exception as e:
    helper.init_failure(e)


@helper.create
def create(event, context):
    logger.info("Got Create")

    secret_value = json.loads(
        secretsmanager.get_secret_value(SecretId=secret_arn)["SecretString"]
    )
    password = secret_value["password"]

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
            query1 = f"CREATE USER {dbusername} IDENTIFIED WITH AWSAuthenticationPlugin as 'RDS';"
            query2 = f"CREATE DATABASE {dbname};"
            query3 = f"GRANT CREATE VIEW, SHOW VIEW, SELECT, INSERT, UPDATE ON {dbname}.* TO {dbusername};"
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
        cur.execute("COMMIT;")
        print("Success")

    except Exception as e:
        error_statement = "Database connection failed due to {}".format(e)
        print(error_statement)
        raise Exception(error_statement)

    return helper.PhysicalResourceId


@helper.update
def update(event, context):
    logger.info("Got Update")


@helper.delete
def delete(event, context):
    logger.info("Got Delete")


def handler(event, context):
    helper(event, context)
