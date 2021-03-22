# Local Development

This section details how to run the solution locally and deploy your code changes from the command line.

### Pre-Requisites

The following dependencies must be installed:
- Python >=3.8 and pip
- virtualenv
- nodejs
- ruby >=2.6 and gem
- [cfn-nag](https://github.com/stelligent/cfn_nag)

### Build local development environment

Once you have installed pre-requisites, you must run the following command to create a `virtualenv` and install all dependencies before commencing development.

1. Create a S3 bucket
   ```shell
   BUCKET_NAME="your-s3-bucket-name"
   AWS_REGION="aws-region(e.g. us-east-1)"
   aws s3 mb s3://${BUCKET_NAME} --region $AWS_REGION
   ```
1. Create a `.custom.mk` file and populate it with your own values
   ```shell
   cp .custom.mk.example .custom.mk
   ```
1. Initialize the local environment
   ```shell
   make init
   ```
1. Activate `virtualenv` environment.
   ```shell
   source venv/bin/activate
   ```

### Deploy the stack

To deploy the solution manually from the source to your AWS account, run the following:

```shell
make deploy
```

This will deploy the nested stacks using the AWS CLI profile of the current shell. By default, this will be the profile `default`.

### Delete the resources created via CloudFormation

Below command will delete deployed stacks.

```shell
make delete
```

### Test changes

The following command will run `pre-commit` tests. This should be run before every new commit.

```shell
make test
```

### Clean the virtual environment

This command will delete the virtual environment and all installed packages install via `make init`

```shell
make clean
```
