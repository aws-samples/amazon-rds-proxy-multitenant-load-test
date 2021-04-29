## Amazon RDS Proxy MySQL Multi-Tenant Load Test

[![Publish Version](https://github.com/aws-samples/amazon-rds-proxy-multitenant-load-test/workflows/Publish%20Version/badge.svg)](https://github.com/aws-samples/amazon-rds-proxy-multitenant-load-test/actions)
[![Unit Tests](https://github.com/aws-samples/amazon-rds-proxy-multitenant-load-test/workflows/Unit%20Tests/badge.svg)](https://github.com/aws-samples/amazon-rds-proxy-multitenant-load-test/actions)

#### Database migration from a simulated on-premises MS SQL Server to an Amazon RDS instance in AWS Cloud

An AWS CloudFormation template that builds and load tests two multi-tenant Amazon Aurora MySQL clusters, one with and one without Amazon RDS Proxy. This is repository that is referenced in the accompanying blog post: Build and load test a multi-tenant SaaS database proxy solution with Amazon RDS Proxy.

An overview of the architecture is below:

![Architecture](docs/Architecture.png)

### Usage

#### Prerequisites

To deploy the solution, you will require an AWS account. If you don’t already have an AWS account,
create one at <https://aws.amazon.com> by following the on-screen instructions.
Your access to the AWS account must have IAM permissions to launch AWS CloudFormation templates that create IAM roles.

#### Deployment

The application is deployed as an [AWS CloudFormation](https://aws.amazon.com/cloudformation) template.

> **Note**
You are responsible for the cost of the AWS services used while running this sample deployment. There is no additional
>cost for using this sample. For full details, see the pricing pages for each AWS service you will be using in this sample. Prices are subject to change.

1. Deploy the latest CloudFormation template by following the link below for your preferred AWS region:

|Region|Launch Template|
|------|---------------|
|**US East (N. Virginia)** (us-east-1) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-us-east-1/rds-proxy-load-test/latest/main.template)|
|**US East (Ohio)** (us-east-2) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-us-west-2/rds-proxy-load-test/latest/main.template)|
|**US West (N. California)** (us-west-1) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-eu-west-1/rds-proxy-load-test/latest/main.template)|
|**US West (Oregon)** (us-west-2) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-eu-west-2/rds-proxy-load-test/latest/main.template)|
|**Asia Pacific (Mumbai)** (ap-south-1) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-eu-central-1/rds-proxy-load-test/latest/main.template)|
|**Asia Pacific (Seoul)** (ap-northeast-2) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-ap-southeast-2/rds-proxy-load-test/latest/main.template)|
|**Asia Pacific (Singapore)** (ap-southeast-1) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-ap-southeast-2/rds-proxy-load-test/latest/main.template)|
|**Asia Pacific (Sydney)** (ap-southeast-2) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-ap-southeast-2/rds-proxy-load-test/latest/main.template)|
|**Asia Pacific (Tokyo)** (ap-northeast-1) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-ap-southeast-2/rds-proxy-load-test/latest/main.template)|
|**Canada (Central)** (ca-central-1) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-ap-southeast-2/rds-proxy-load-test/latest/main.template)|
|**Europe (Frankfurt)** (eu-central-1) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-ap-southeast-2/rds-proxy-load-test/latest/main.template)|
|**Europe (Ireland)** (eu-west-1) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-ap-southeast-2/rds-proxy-load-test/latest/main.template)|
|**Europe (London)** (eu-west-2) | [![Deploy to AWS](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=rds-proxy-load-test&templateURL=https://s3.amazonaws.com/solution-builders-ap-southeast-2/rds-proxy-load-test/latest/main.template)|

2. If prompted, login using your AWS account credentials.
1. You should see a screen titled "*Create Stack*" at the "*Specify template*" step. The fields specifying the CloudFormation
template are pre-populated. Click the *Next* button at the bottom of the page.
1. On the "*Specify stack details*" screen you may customize the following parameters of the CloudFormation stack:

|Parameter label|Default|Description|
|---------------|-------|-----------|
|CreateLoadTest|true|If True, this creates a Load Test VPC and an accompanying No Proxy VPC, in order to run a load test and compare metrics between Proxy and No Proxy.|
|AvailabilityZones|Requires input|The list of Availability Zones to use for the subnets in the VPC. Select two Availability Zones from the list.|
|DBInstanceClass|db.r5.large|The database instance class for the Proxy and No Proxy VPC Amazon Aurora instances, for example db.m5.large.|
|PerformanceInsightsRetentionPeriod|7|The amount of time, in days, to retain Performance Insights data. Valid values range between 7 and 731 (2 years).|
|LambdaRuntimeEnv|Node.js|The runtime for Lambda access Function/Layer.|
|LocustAmiId|/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2|The latest Amazon Linux AMI from Systems Manager Parameter Store.|
|LocustInstanceType|c5.large|The Amazon EC2 instance type used in the Load Test cluster that runs Locust.|
|LocustVersion|latest|The Locust version to deploy.|
|LocustSecondaryInstanceCapacity|2|The number of secondary Amazon EC2s for the Load Test Cluster. Minimum value is 2.|
|ApiEndpointType|PRIVATE|The Amazon API Gateway endpoint type. Valid values are (EDGE, REGIONAL, PRIVATE).|
|OnPremIp|0.0.0.0/0|The CIDR block of an on-premise IP address. This limits the CIDR range from which the Locust dashboard can be accessed.|
|Environment|DEV|The type of environment to tag your infrastructure with. You can specify DEV (development), TEST (test), or PROD (production).|
|EnableFlowLogs|false|Optional CloudWatch Logs group to send VPC flow logs to. Flow Logs incur additional cost. Set to "false" to disable.|

   When completed, click *Next*
1. [Configure stack options](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-add-tags.html) if desired, then click *Next*.
1. On the review you screen, you must check the boxes for:
   * "*I acknowledge that AWS CloudFormation might create IAM resources*"
   * "*I acknowledge that AWS CloudFormation might create IAM resources with custom names*"
   * "*I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND*"

   These are required to allow CloudFormation to create a Role to allow access to resources needed by the stack and name the resources in a dynamic way.
1. Click *Create Stack*
1. Wait for the CloudFormation stack to launch. This will take around 30 minutes. Completion is indicated when the "Stack status" is "*CREATE_COMPLETE*".
   * You can monitor the stack creation progress in the "Events" tab.
1. Note the *EC2SQLServerEip* and *RDSSQLEndpoint* displayed in the *Outputs* tab of the main stack. This can be used to access the EC2 host and RDS instance.

If you are familiar with Locust, you can also modify the Locust file as written in the CloudFormation template. For more information, please refer to [here](https://docs.locust.io/en/stable/writing-a-locustfile.html) for how to write a Locustfile.

## Local Development
See [Local Development](docs/LOCAL_DEVELOPMENT.md) guide to get a copy of the project up and running on your local machine for development and testing purposes.

### Clean up

To remove the stack:

1. Open the AWS CloudFormation Console
1. Click the *aws-multitenant-rds-proxy* project, right-click and select "*Delete Stack*"
1. Your stack will take some time to be deleted. You can track its progress in the "Events" tab.
1. When it is done, the status will change from "DELETE_IN_PROGRESS" to "DELETE_COMPLETE". It will then disappear from the list.

## Contributing

Contributions are more than welcome. Please read the [code of conduct](CODE_OF_CONDUCT.md) and the [contributing guidelines](CONTRIBUTING.md).

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
