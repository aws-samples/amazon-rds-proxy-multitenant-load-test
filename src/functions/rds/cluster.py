from __future__ import print_function

import logging

import boto3
from crhelper import CfnResource

logger = logging.getLogger(__name__)
helper = CfnResource(
    json_logging=False, log_level="DEBUG", boto_level="CRITICAL", sleep_on_delete=120
)
rds = boto3.client("rds")


@helper.create
def create(event, context):
    logger.info("Got Create")
    properties = event.get("ResourceProperties", {})
    db_cluster_identifier = properties.get("DBClusterIdentifier")

    db_cluster_resource_id = _rds_describe_db_clusters(db_cluster_identifier)

    helper.Data.update({"DbClusterResourceId": db_cluster_resource_id})

    return helper.PhysicalResourceId


@helper.update
def update(event, context):
    logger.info("Got Update")


@helper.delete
def delete(event, context):
    logger.info("Got Delete")


def handler(event, context):
    helper(event, context)


def _rds_describe_db_clusters(db_cluster_identifier):
    response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_identifier)
    resource_id = response["DBClusters"][0]["DbClusterResourceId"]
    return resource_id
