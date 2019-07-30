# Puzzle

## Description
This service provides 2 methods for the Puzzle API.
1. A simple get request returns a random unsolved puzzle
1. A get request with the ID of a puzzle returns the solved version of the puzzle

## Architecture
See project [README](../../README.md) for architecture diagram.

## Requirements

* AWS CLI already configured with Administrator permission
* [Python 3 installed](https://www.python.org/downloads/)
* Python dependencies, e.g. pytest, boto3, moto.
* [Docker installed](https://www.docker.com/community-edition)

## Deployment
1. Create an S3 bucket to store the SAM builds:
    ```
    aws cloudformation create-stack --stack-name sam-builds-puzzle --template-body file://sam-builds-bucket.yaml
    ```
1. Create a new build of the code:
    ```
    sam build
    ```
1. Test:
    ```
    sam local invoke UnsolvedFunction --event events/puzzle_api_unsolved_event.json --env-vars env_vars/test_env.json
    sam local invoke SolvedFunction --event events/puzzle_api_solved_event.json --env-vars env_vars/test_env.json
    ```
1. Package our Lambda function to S3:
    ```
    sam package \
        --output-template-file packaged.yaml \
        --s3-bucket sam-builds-puzzle
    ```
1.Create a Cloudformation Stack and deploy your SAM resources.
    ```
    sam deploy \
        --template-file packaged.yaml \
        --stack-name Service-Puzzle-Test \
        --capabilities CAPABILITY_NAMED_IAM
    ```
1. After deployment is complete you can run the following command to retrieve the API Gateway Endpoint URL:
    ```
    aws cloudformation describe-stacks \
        --stack-name Service-Puzzle-Test \
        --query 'Stacks[].Outputs[?OutputKey==`ApiUrl`]' \
        --output table
    ```
1. Add data to puzzle buckets:
    ```
    aws s3 cp data/example_puzzles/ s3://sudokuless-unsolved-test --recursive
    aws s3 cp data/example_puzzle_solutions/ s3://sudokuless-solved-test --recursive
    ```

## Testing
### Unit Testing
Python version 3.6 is used with the lambda, so a matching local python environment is also used:
```
pyenv local 3.6.8
```

To execute `pytest` against our `tests` folder to run our initial unit tests:
```
pytest
```

Test a specific file, class or test:
```
File: pytest tests/test_solved.py
Class: pytest tests/test_unsolved.py::TestEnvironmentVariable
Unit Test: pytest tests/test_unsolved.py::TestEnvironmentVariable::test_get_bucket_name
```

### Local Lambda Testing
Local testing allows you to see how the function will work once deployed, e.g. with memory allocation and timeouts.  Sample events have already been generated, see the command reference below for an example of generating a new one.

1. Build:
    ```
    sam build
    ```
1. Invoke a Function:
    ```
    sam local invoke UnsolvedFunction --event events/puzzle_api_unsolved_event.json --env-vars env_vars/test_env.json
    sam local invoke SolvedFunction --event events/puzzle_api_solved_event.json --env-vars env_vars/test_env.json
    ```

### Local API Testing
Local testing of the API, ensures that API and lambda function are correctly configured.
1. Start API
    ```
    sam local start-api
    ```
1. Use local endpoint in browser or with Postman: `http://localhost:3000/puzzle`
1. (Optional) Just as with invoking functions, environment variables can also be specified for local api testing.
    ```
    sam local start-api --env-vars test_env.json
    ```

## Logging
Get logs for last 10 minutes:
```
sam logs -n UnsolvedFunction --stack-name Service-Puzzle-Test
```

Tail logs, e.g. whilst executing function test:
```
sam logs -n UnsolvedFunction --stack-name Service-Puzzle-Test --tail
```

See [SAM CLI Logging](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html) for more options.

## Cleanup
In order to delete our Serverless Application recently deployed you can use the following AWS CLI Command:

```
aws cloudformation delete-stack --stack-name Service-Puzzle-Test
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
