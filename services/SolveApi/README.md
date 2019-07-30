# Solve

## Description
This API is called by a user submits a finished sudoku puzzle.  The service retrieves the puzzle solution from an s3 bucket which is used to compare against the users solution attempt.

## Architecture
See project [README](../../README.md) for architecture diagram.

## Requirements

* AWS CLI already configured with Administrator permission
* [Python 3 installed](https://www.python.org/downloads/)
* Python dependencies, e.g. pytest, boto3, moto.
* [Docker installed](https://www.docker.com/community-edition)

## Getting Started
### Build Bucket
Create an S3 bucket to store the SAM builds:
```
aws cloudformation create-stack --stack-name sam-builds-solve --template-body file://sam-builds-bucket.yaml
```

sam local invoke Function --event events/solve_api_event.json

sam build

### Packaging and deployment
Package our Lambda function to S3:

```
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket sam-builds-solve
```

Create a Cloudformation Stack and deploy your SAM resources.

```
sam deploy \
    --template-file packaged.yaml \
    --stack-name Service-Solve-test \
    --capabilities CAPABILITY_NAMED_IAM
```

After deployment is complete you can run the following command to retrieve the API Gateway Endpoint URL:
```
aws cloudformation describe-stacks \
    --stack-name Service-Solve-test \
    --query 'Stacks[].Outputs[?OutputKey==`ApiUrl`]' \
    --output table
```

## Logging
Get logs for last 10 minutes:
```
sam logs -n Function
```

Tail logs, e.g. whilst executing function test:
```
sam logs -n Function --tail
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
1. Invoke Function (Option 1):
    ```
    sam local invoke --event events/api_solve_puzzle_event.json
    ```
1. Invoke Function with Name (Option 2):
    ```
    sam local invoke Function --event events/api_solve_puzzle_event.json
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
1. Use local endpoint in browser or with Postman: `http://localhost:3000/getNewPuzzleSolution/1.json`
1. (Optional) Just as with invoking functions, environment variables can also be specified for local api testing.
    ```
    sam local start-api --env-vars prod_env.json
    ```

## Cleanup
In order to delete our Serverless Application recently deployed you can use the following AWS CLI Command:

```
aws cloudformation delete-stack --stack-name Service-Solve-test
```

# Appendix
### Deploying with overrides:
```
aws cloudformation create-stack --template-body file://packaged.yaml  \
 --stack-name RandomStack \
 --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
 --parameters ParameterKey=UnsolvedBucketPrefix,ParameterValue=test-unsolved-puzzles
```

### Generate test event:
```
sam local generate-event apigateway aws-proxy > events/api_event.json
```

### API Gateway Manual Deployment
```
aws apigateway get-rest-apis --query 'items[?name==`puzzle-test`].{name:name, ID:id}'

aws apigateway get-stages --rest-api-id <api-id> --query 'item[?stageName==`prod`].{stageName:stageName, deploymentId:deploymentId}'

aws apigateway update-stage \
 --rest-api-id <api-id> \
 --stage-name Prod \
 --patch-operations op='replace',path='/deploymentId',value='<deployment-id>'
```
