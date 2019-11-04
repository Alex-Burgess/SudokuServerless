# Sudokuless

## Introduction
A serverless website with a sudoku theme, based on [Build a Serverless Web App...](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/).

[AWS Amplify Framework](https://aws-amplify.github.io) is used to provide user authentication.

The web component is written in React.  Further inspiration is taken from [AWS Full Stack Template](https://github.com/awslabs/aws-full-stack-template).

## Architecture
The architecture in use is very similar to the diagrams in the [AWS Full Stack Template](https://github.com/awslabs/aws-full-stack-template).

![alt text](../master/diagrams/Sudokuless.png "API Services")

## Deployment
Split into following sections:
1. Web infrastructure
1. User authentication.
1. API Services
1. Pipeline - Covered in [CI/CD Pipeline](#cicd-pipeline)

### Web Infastructure
1. Create Web stack:
    ```
    aws cloudformation create-stack --stack-name Sudoku-Serverless-Test \
     --template-body file://main.yaml \
     --parameters ParameterKey=DefaultSSLCertificate,ParameterValue=true
    ```
1. Create SSL Certificate in ACM Console.
1. Update Stack With SSL Certificate ID:
    ```
    aws acm list-certificates --region us-east-1 --query 'CertificateSummaryList[?DomainName==`sudokuless.com`].CertificateArn' --output text

    aws cloudformation update-stack --stack-name Sudoku-Serverless-Main \
     --template-body file://main.yaml \
     --parameters ParameterKey=SSLCertificateId,ParameterValue=532933b8-20fc-....
    ```
1. Deploy React Application
    ```
    npm install
    REACT_APP_STAGE=test npm run build
    aws s3 sync build/ s3://test.sudokuless.com --delete
    ```

### User Authentication
Useful AWS documentation: [Adding Social Identity Providers to a User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html)

1. Create Auth stack (with termination protection):
    ```
    aws cloudformation create-stack --stack-name Sudoku-Serverless-Auth-Test \
     --template-body file://auth.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --enable-termination-protection
    ```
1. Configure UserPool:
    ```
    aws cognito-idp list-user-pools --max-results 10 --query 'UserPools[*].{Id:Id, Name:Name}'

    aws cognito-idp create-user-pool-domain --user-pool-id us-west-1_aaaaaaaaa  --domain sudokuless
    ```
1. Configuring social authentication with LoginWithAmazon.
  1. Create [Amazon](https://developer.amazon.com/login-with-amazon) developer account.
  1. Create Security Profile - [Steps](Adding Social Identity Providers to a User Pool)
  1. Update app ID, secret and scope in Identity providers.
1. Configuring social authentication with Google
  1. Create [Google](https://console.developers.google.com) developer account.
  1. Create OAuth client IDs - [Steps](Adding Social Identity Providers to a User Pool)
  1. Update app ID, secret and scope in Identity providers.
1. Configuring social authentication with Facebook
  1. Create [Facebook](https://developers.facebook.com/) developer account.
  1. Create App ID - [Steps](Adding Social Identity Providers to a User Pool)
  1. Update app ID, secret and scope in Identity providers.
1. Enable all Identity Providers in App Client Settings and select Allowed OAuth Flows and Scopes (console).

### API Services
1. Create Role for API Gateway to perform writes to CloudWatch Logs with.
  ```
  aws cloudformation create-stack --stack-name Sudoku-Serverless-Api-Role --template-body file://api-logging.yaml \
   --enable-termination-protection \
   --capabilities CAPABILITY_NAMED_IAM
  ```
1. Create Puzzle service - See (Puzzle)[services/PuzzleApi/README.md] for full details:
    ```
    sam build

    sam package \
        --output-template-file packaged.yaml \
        --s3-bucket sam-builds-puzzle

    sam deploy \
        --template-file packaged.yaml \
        --stack-name Service-Puzzle-Test \
        --capabilities CAPABILITY_NAMED_IAM
    ```
1. Add data to puzzle buckets:
    ```
    aws s3 cp data/example_puzzles/ s3://sudokuless-unsolved-prod --recursive
    aws s3 cp data/example_puzzle_solutions/ s3://sudokuless-solved-prod --recursive
    ```
1. Create Solve service - See (Solve)[services/SolveApi/README.md] for full details:
    ```
    sam build

    sam package \
        --output-template-file packaged.yaml \
        --s3-bucket sam-builds-solve

    sam deploy \
        --template-file packaged.yaml \
        --stack-name Service-Solve-test \
        --capabilities CAPABILITY_NAMED_IAM
    ```

## CI/CD Pipeline
A deployment pipeline is used to automate the build, packaging and deployment of the SAM serverless services.

*Notes:*
* The pipeline uses a github project as a source.  To configure the webhook, an oauth token is required, which is created as Personal Access Token in GitHub.  This is stored in the parameter store, with encryption.  Cloudformation only has limited support for using encrypted parameters, and as such there is no method provided to automatically retrieve this value from the parameter store.  To workaround this, using the CLI to input the value and ensuring that the parameter has `NoEcho: true` specified.

### Create Pipeline
1. Add github oauth key to parameter store, either by console or by cli:
    ```
    aws ssm put-parameter --name "/Sudoku/github" --value "123456abcde...." --type SecureString
    ```
1. Test retrieving the parameter
    ```
    aws ssm get-parameter --name "/Sudoku/github" --with-decryption
    ```
1. Add Postman Collection and Environment IDs to parameter store (See [Postman](#Postman) reference commands for retrieving IDs.):
    ```
    aws ssm put-parameter --name /Postman/Staging/CollectionId --type String --value "6596444-38afc6ee-????"
    aws ssm put-parameter --name /Postman/Staging/EnvironmentId --type String --value "6596444-ea7ff6c9-??????"
    aws ssm put-parameter --name /Postman/Prod/CollectionId --type String --value "6596444-38afc6ee-????"
    aws ssm put-parameter --name /Postman/Prod/EnvironmentId --type String --value "6596444-ea7ff6c9-??????"
    ```
1. Create the stack, using the cli to import the oauth token from the parameter store:
    ```
    aws cloudformation create-stack --stack-name Sudoku-Pipeline \
     --template-body file://pipeline.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameters ParameterKey=GitHubToken,ParameterValue=`aws ssm get-parameter --name "/Sudoku/github" --with-decryption --query 'Parameter.Value' --output text`
    ```

### Update the Pipeline Without Change Set
```
aws cloudformation update-stack --stack-name Sudoku-Pipeline \
 --template-body file://pipeline.yaml \
 --capabilities CAPABILITY_NAMED_IAM \
 --parameters ParameterKey=Staging,ParameterValue=true \
    ParameterKey=GitHubToken,ParameterValue=`aws ssm get-parameter --name "/Sudoku/github" --with-decryption --query 'Parameter.Value' --output text`
```

Or without staging:
```
aws cloudformation update-stack --stack-name Sudoku-Pipeline \
 --template-body file://pipeline.yaml \
 --capabilities CAPABILITY_NAMED_IAM \
 --parameters ParameterKey=GitHubToken,ParameterValue=`aws ssm get-parameter --name "/Sudoku/github" --with-decryption --query 'Parameter.Value' --output text`
```

### Update the Pipeline With Change Set
1. Create a change set:
    ```
    aws cloudformation create-change-set --change-set-name pipeline-updates \
     --stack-name Sudoku-Pipeline \
     --template-body file://pipeline.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameters ParameterKey=GitHubToken,ParameterValue=`aws ssm get-parameter --name "/Sudoku/github" --with-decryption --query 'Parameter.Value' --output text`
    ```
1. Check change set:
    ```
    aws cloudformation describe-change-set --change-set-name pipeline-updates \
     --stack-name Sudoku-Pipeline
    ```
1. Apply change set:
    ```
    aws cloudformation execute-change-set --change-set-name pipeline-updates \
     --stack-name Sudoku-Pipeline
     ```

## Testing
The philosophy on testing is taken from the [The Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html).

The testing includes the [Worlds hardest sudoku](https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html).

### Browser
*Note: This is currently done manually, but should be performed by a Selenium test in due course.*

Browser test list:
1. Log in / Log out with username and password
1. Log in / Log out with Amazon
1. Log in / Log out with Google
1. Log in / Log out with Facebook
1. Pages requiring authentication should not show, when not logged in.  Instead user is redirected to sign in.
1. Pages requiring authentication should show when logged in.  Home page should show user dash board when logged in.
1. Try page retrieves puzzle from API.
1. Try page, incorrect puzzle attempt.
1. Try page, correct puzzle attempt.
1. Solve page, valid puzzle attempt.
1. Solve page, invalid puzzle attempt.

### Integration Tests
Postman is used to test the service APIs.  AWS SAM can also be used to test Lambda functions and APIs locally.  

See [Postman](#Postman) reference commands for details of running the tests using Newman the CLI tool.

See the following for more information:
* (Puzzle)[services/PuzzleApi/README.md]
* (Solve)[services/SolveApi/README.md]

### Unit Tests
Pytest is used to performing unit tests of the python modules.  See the following for more information:
* (Puzzle)[services/PuzzleApi/README.md]
* (Solve)[services/SolveApi/README.md]

# Reference
### React
Before the first execution, it is necessary to install the node modules.
```
npm install
```
Run the react server locally:
```
REACT_APP_STAGE=test npm start
```

Build and Deploy to Staging:
```
REACT_APP_STAGE=staging npm run build
aws s3 sync build/ s3://staging.sudokuless.com --delete
```

Build and Deploy to Production:
```
REACT_APP_STAGE=prod npm run build
aws s3 sync build/ s3://sudokuless.com --delete
```

### Postman
Set a local environment variable for the Postman API key:
```
export POSTMAN=??????
```

To find your collection uid:
```
curl https://api.getpostman.com/collections?apikey=$POSTMAN
```

To find your environment uid:
```
curl https://api.getpostman.com/environments?apikey=$POSTMAN
```

Install Newman:
```
npm i newman -g;
```

Test a collection:
```
newman run https://api.getpostman.com/collections/<Collection UID>?apikey=$POSTMAN --environment https://api.getpostman.com/environments/<Environment UID>?apikey=$POSTMAN
```

### Create a new lambda/api service using SAM
```
sam init --runtime python3.6 --name tryNewPuzzle
```

### Tag a new git version
```
git tag -a v0.0.1 -m "Tag description..."
git push origin v0.0.1
```
