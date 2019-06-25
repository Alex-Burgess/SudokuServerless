# tryNewPuzzle

## Description
This API is called by a web page when a user requests to attempt a new puzzle.  When triggered, this service gets a new unsolved puzzle from an S3 bucket.

## Architecture
See project [README](../../README.md) for architecture diagram.

## Requirements

* AWS CLI already configured with Administrator permission
* [Python 3 installed](https://www.python.org/downloads/)
* Python dependencies, e.g. pytest, boto3, moto.
* [Docker installed](https://www.docker.com/community-edition)
* An S3 bucket with the unsolved puzzles

## Getting Started
### Build Bucket
Create an S3 bucket to store the SAM builds:
```
aws cloudformation create-stack --stack-name sam-builds-trynewpuzzle --template-body file://sam-builds-bucket.yaml
```

### Packaging and deployment
Package our Lambda function to S3:

```
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket sam-builds-trynewpuzzle
```

Create a Cloudformation Stack and deploy your SAM resources.

```
sam deploy \
    --template-file packaged.yaml \
    --stack-name Service-TryNewPuzzle \
    --capabilities CAPABILITY_NAMED_IAM
```

After deployment is complete you can run the following command to retrieve the API Gateway Endpoint URL:
```
aws cloudformation describe-stacks \
    --stack-name Service-TryNewPuzzle \
    --query 'Stacks[].Outputs[?OutputKey==`UnsolvedPuzzleFunctionApi`]' \
    --output table
```

## Deploying to Environments
Add input parameter to template??
Using gradual code deployments to production, with automated test execution and automated roll back in case of errors.  A good test, would be to deploy with the wrong bucket name, so that it fails and rolls back.

## Logging
Get logs for last 10 minutes:
```
sam logs -n UnsolvedPuzzleFunction
```

Tail logs, e.g. whilst executing function test:
```
sam logs -n UnsolvedPuzzleFunction --tail
```

See [SAM CLI Logging](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html) for more options.

## Testing
### Unit Testing
To execute `pytest` against our `tests` folder to run our initial unit tests:
```
python -m pytest tests/ -v
```

### Local Lambda Testing
Local testing allows you to see how the function will work once deployed, e.g. with memory allocation and timeouts.

1. Build:
    ```
    sam build
    ```
1. Generate test event:
    ```
    sam local generate-event apigateway aws-proxy > events/api_event.json
    ```
1. Invoke Function (Option 1):
    ```
    sam local invoke --event events/api_event.json
    ```
1. Invoke Function with Name (Option 2):
    ```
    sam local invoke UnsolvedPuzzleFunction --event events/api_event.json
    ```
1. Invoke Function with stdin event (Option 3):
    ```
    echo '{"message": "Hey, are you there?" }' | sam local invoke
    ```
1. Invoke function with environment variables (Option 4).  In this example, we can specify the UNSOLVED_BUCKET_NAME environment variable, e.g. for testing purposes:
    ```
    echo '{"message": "Hey, are you there?" }' | sam local invoke --env-vars prod_env.json
    ```

### Local API Testing
Local testing of the API, ensures that API and lambda function are correctly configured.
1. Start API
    ```
    sam local start-api
    ```
1. Use local endpoint in browser or with Postman: `http://localhost:3000/tryNewPuzzle`
1. (Optional) Just as with invoking functions, environment variables can also be specified for local api testing.
    ```
    sam local start-api --env-vars prod_env.json
    ```

## Cleanup
In order to delete our Serverless Application recently deployed you can use the following AWS CLI Command:

```
aws cloudformation delete-stack --stack-name Service-TryNewPuzzle
```

# Appendix
## SAM and AWS CLI commands

All commands used throughout this document

```
# Generate event.json via generate-event command
sam local generate-event apigateway aws-proxy > event.json

# Invoke function locally with event.json as an input
sam local invoke UnsolvedPuzzleFunction --event event.json

# Run API Gateway locally
sam local start-api

# Package Lambda function defined locally and upload to S3 as an artifact
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket sam-builds-trynewpuzzle

# Deploy SAM template as a CloudFormation stack
sam deploy \
    --template-file packaged.yaml \
    --stack-name Service-TryNewPuzzle \
    --capabilities CAPABILITY_IAM

# Describe Output section of CloudFormation stack previously created
aws cloudformation describe-stacks \
    --stack-name Service-TryNewPuzzle \
    --query 'Stacks[].Outputs[?OutputKey==`UnsolvedPuzzleFunctionApi`]' \
    --output table

# Tail Lambda function Logs using Logical name defined in SAM Template
sam logs -n UnsolvedPuzzleFunction --stack-name Service-TryNewPuzzle --tail

# Deploy the API Manually:
aws apigateway get-rest-apis --query 'items[?name==`Service-GetNewPuzzleSolution`].{name:name, ID:id}'

aws apigateway get-stages --rest-api-id <api-id> --query 'item[?stageName==`Prod`].{stageName:stageName, deploymentId:deploymentId}'

aws apigateway update-stage \
 --rest-api-id <api-id> \
 --stage-name Prod \
 --patch-operations op='replace',path='/deploymentId',value='<deployment-id>'
```
