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
|DBWriterClass|db.t3.small|The database instance class for the Proxy and No Proxy VPC Amazon Aurora Writer, for example db.m5.large.|
|DBReaderClass|db.r5.large|The database instance class for the Proxy and No Proxy VPC Amazon Aurora Replicas, for example db.m5.large.|
|PerformanceInsightsRetentionPeriod|7|The amount of time, in days, to retain Performance Insights data. Valid values range between 7 and 731 (2 years).|
|LambdaRuntimeEnv|Node.js|The runtime for Lambda access Function/Layer.|
|LocustAmiId|/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2|The latest Amazon Linux AMI from Systems Manager Parameter Store.|
|LocustInstanceType|c5.large|The Amazon EC2 instance type used in the Load Test cluster that runs Locust.|
|LocustVersion|latest|The Locust version to deploy.|
|LocustSecondaryInstanceCapacity|2|The number of secondary Amazon EC2s for the Load Test Cluster. Minimum value is 2.|
|ApiEndpointType|PRIVATE|The Amazon API Gateway endpoint type. Valid values are (EDGE, REGIONAL, PRIVATE).|
|CIDRRange|Requires input|The CIDR block of your IP address that you wil use to connect to the Locust Dashboard. This limits the CIDR range from which the Locust dashboard can be accessed.|
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

## Detailed Pricing
This sample is intended to be deployed only for as long as is strictly necessary, to avoid incurring additional costs. As soon as the load test is completed, the stack should be destroyed (see 'Clean up' above). Note that all pricing is estimated based on the us-east-1 region, and without the Free Tier.

Assuming a 150 request per second load test for 30 minutes, the price breakdown is estimated as follows:

|Service|Cost|Description|
|---------------|-------|-----------|
|Amazon Aurora MySQL| $0.43 |2x db.r5.large and 1x db.t3.small database instances running continuously, 150 RPS.|
|Amazon RDS Proxy| $0.02 |Based on 2 vCPUs of db.r5.large, running continuously.|
|Amazon EC2| $0.14 |3x c5.large instances running continuously.|
|Amazon CloudWatch| $0.01 |CloudWatch dashboard + 20 metrics.|
|AWS X-Ray| $0.07 |150 Traces Per Second, with a 5% sampling rate.|
|AWS Secrets Manager| $0.73 |200 secrets, and 75 API calls per second.|
|AWS Lambda| $1.22 |150 RPS, assuming 2000ms duration per request.|
|Amazon API Gateway| $0.93 |150RPS to the REST API type.|
|AWS Private Link| $0.01 |Interface VPC endpoint for API Gateway, 2AZs, 170GB in total processed per Month.|
|Data Transfer| $0.00 |170Gb transfer between AZs.|
|Total| $3.54 |Total.|

Assuming a 150 request per second load test for 4 hours, the price breakdown is estimated as follows:

|Service|Cost|Description|
|---------------|-------|-----------|
|Amazon Aurora MySQL| $3.40 |2x db.r5.large and 1x db.t3.small database instances running continuously, 150 RPS.|
|Amazon RDS Proxy| $0.12 |Based on 2 vCPUs of db.r5.large, running continuously.|
|Amazon EC2| $1.08 |3x c5.large instances running continuously.|
|Amazon CloudWatch| $0.07 |CloudWatch dashboard + 20 metrics.|
|AWS X-Ray| $0.56 |150 Traces Per Second, with a 5% sampling rate.|
|AWS Secrets Manager| $5.84 |200 secrets, and 75 API calls per second.|
|AWS Lambda| $9.75 |150 RPS, assuming 2000ms duration per request.|
|Amazon API Gateway| $7.43 |150RPS to the REST API type.|
|AWS Private Link| $0.09 |Interface VPC endpoint for API Gateway, 2AZs, 170GB in total processed per Month.|
|Data Transfer| $0.02 |170Gb transfer between AZs.|
|Total| $28.36 |Total.|

The above pricing examples (excluding the RDS Proxy cost) are based off of the AWS Pricing Calculator, and derived from the monthly cost taken [here](https://calculator.aws/#/estimate?id=1e41c1d61a96024f80f7b88b53554df6e47bdfae).

Assuming the resources are deployed for a month, without a load test (all of the resources are running, except Locust), the price breakdown is estimated as follows:

|Service|Cost|Description|
|---------------|-------|-----------|
|Amazon Aurora MySQL| $455.45 |2x db.r5.large and 1x db.t3.small database instances running continuously.|
|Amazon RDS Proxy| $21.60 |Based on 2 vCPUs of db.r5.large, running continuously.|
|Amazon EC2| $195.15 |3x c5.large instances running continuously.|
|Amazon CloudWatch| $12.00 |CloudWatch dashboard + 20 metrics.|
|AWS Secrets Manager| $80.00 |200 secrets.|
|AWS Private Link| $14.60 |Interface VPC endpoint for API Gateway, 2AZs.|
|Total| $778.80 |Total.|

The above pricing example (excluding the RDS Proxy cost) is based off of the AWS Pricing Calculator, and derived from the monthly cost taken [here](https://calculator.aws/#/estimate?id=fbd9e04fe2058108614023cbd93c99dd17aaf6b7).

## Contributing

Contributions are more than welcome. Please read the [code of conduct](CODE_OF_CONDUCT.md) and the [contributing guidelines](CONTRIBUTING.md).

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
