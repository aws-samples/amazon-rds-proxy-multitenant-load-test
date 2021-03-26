SHELL := /bin/bash

.PHONY : help init deploy test clean delete
.DEFAULT: help

# ENV VAR
PYTHON_PATH ?= ./src/layers/python
NODEJS_PATH ?= ./src/layers/nodejs

# Check for .custom.mk file if exists
CUSTOM_FILE ?= .custom.mk
CUSTOM_EXAMPLE ?= .custom.mk.example
ifneq ("$(wildcard $(CUSTOM_FILE))","")
	include $(CUSTOM_FILE)
else ifneq ("$(wildcard $(CUSTOM_EXAMPLE))","")
	include $(CUSTOM_EXAMPLE)
else
$(error File `.custom.mk` doesnt exist, please create one.)
endif

help:
	@echo "init	generate project for local development"
	@echo "deploy	deploy solution from source"
	@echo "test	run pre-commit checks"
	@echo "clean	delete virtualenv and installed libraries"
	@echo "delete	delete deployed stacks"

# Install local dependencies and git hooks
init: venv
	make build

deploy: package
	@printf "\n--> Deploying %s template...\n" $(STACK_NAME)
	@aws cloudformation deploy \
	  --template-file ./cfn/packaged.template \
	  --stack-name $(STACK_NAME) \
	  --region $(AWS_REGION) \
	  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
	  --parameter-overrides \
	  	CreateLoadTest=$(LOAD_TEST) \
	  	AvailabilityZones=$(AWS_REGION)a,$(AWS_REGION)b \
	  	LambdaRuntimeEnv=$(LAMBDA_RUNTIME_ENV)

package: build
	@printf "\n--> Packaging and uploading templates to the %s S3 bucket ...\n" $(BUCKET_NAME)
	@aws cloudformation package \
  	--template-file ./cfn/main.template \
  	--s3-bucket $(BUCKET_NAME) \
  	--s3-prefix $(STACK_NAME) \
  	--output-template-file ./cfn/packaged.template \
  	--region $(AWS_REGION)

build:
	@pip install -r $(PYTHON_PATH)/requirements.txt --target $(PYTHON_PATH)/python --upgrade

	@cd $(NODEJS_PATH); \
		mkdir -p nodejs; \
		rm -rf node_modules nodejs/node_modules; \
		npm install --production; \
		mv node_modules nodejs/;

delete:
	@printf "\n--> Deleting %s stack...\n" $(STACK_NAME)
	@aws cloudformation delete-stack \
            --stack-name $(STACK_NAME)
	@printf "\n--> $(STACK_NAME) deletion has been submitted, check AWS CloudFormation Console for an update..."

# Package for cfn-publish CI
cfn-publish-package: build
	zip -r packaged.zip -@ < ci/include.lst

# virtualenv setup
venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt; pre-commit install;
	touch venv/bin/activate

test:
	pre-commit run --all-files

test-cfn-lint:
	cfn-lint cfn/*.template

test-cfn-nag:
	cfn_nag_scan --input-path cfn

version:
	@bumpversion --dry-run --list cfn/main.template | grep current_version | sed s/'^.*='//

# Cleanup local build
clean:
	rm -rf venv
	find . -iname "*.pyc" -delete
