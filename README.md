# SudokuServerless
A serverless website with a sudoku theme, based on [Build a Serverless Web App...](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/).

[Worlds hardest sudoku](https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html)

### Quick start
1. Create the website:
    ```
    hugo new site sudoku-serverless-hugo
    git init
    ```
1. Add a theme:
    ```
    git submodule add git@github.com:Alex-Burgess/kube.git sudoku-serverless-hugo/themes/kube
    ```
1. Copy and Update the config:
    ```
    cp themes/kube/exampleSite/config.toml .
    ```
1. Create Web stack:
    ```
    aws cloudformation create-stack --stack-name Sudoku-Serverless-Main --template-body file://main.yaml \
     --parameters ParameterKey=Environment,ParameterValue=prod \
     ParameterKey=DefaultSSLCertificate,ParameterValue=true
    ```
1. Create SSL Certificate in ACM Console
1. Update Stack With SSL Certificate ID:
    ```
    aws acm list-certificates --region us-east-1 --query 'CertificateSummaryList[?DomainName==`sudokuless.com`].CertificateArn' --output text

    aws cloudformation update-stack --stack-name Sudoku-Serverless-Main --template-body file://main.yaml \
     --parameters ParameterKey=Environment,ParameterValue=prod \
     ParameterKey=SSLCertificateId,ParameterValue=532933b8-20fc-....
    ```
1. Create Auth stack (with termination protection):
    ```
    aws cloudformation create-stack --stack-name Sudoku-Serverless-Auth --template-body file://auth.yaml \
    --capabilities CAPABILITY_NAMED_IAM \
    --enable-termination-protection
    ```
1. Configure UserPool:
    ```
    aws cognito-idp list-user-pools --max-results 10 --query 'UserPools[*].{Id:Id, Name:Name}'

    aws cognito-idp create-user-pool-domain --user-pool-id us-west-1_aaaaaaaaa  --domain sudokuless
    ```
1. If configuring LoginWithAmazon see [Procedure](sudoku-serverless-hugo-amz/README.md)
1. Build and Copy website content:
    ```
    rm -Rf public/
    hugo
    aws s3 sync public/ s3://sudokuless.com --delete
    ```

*Create API Services*
1. Create Role for API Gateway to perform writes to CloudWatch Logs with.
  ```
  aws cloudformation create-stack --stack-name Sudoku-Serverless-Api-Role --template-body file://api-logging.yaml \
   --enable-termination-protection \
   --capabilities CAPABILITY_NAMED_IAM
  ```

Add data to puzzle buckets:
```
aws s3 cp data/example_puzzles/ s3://sudoku-unsolved-puzzles-prod --recursive
aws s3 cp data/example_puzzle_solutions/ s3://sudoku-unsolved-puzzle-solutions-prod --recursive
```

### React Commands
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


### Deployments
A deployment pipeline is used to automate the build, packaging and deployment of the SAM serverless services.

*Notes:*
* The pipeline uses a github project as a source.  To configure the webhook, an oauth token is required, which is created as Personal Access Token in GitHub.  This is stored in the parameter store, with encryption.  Cloudformation only has limited support for using encrypted parameters, and as such there is no method provided to automatically retrieve this value from the parameter store.  To workaround this, using the CLI to input the value and ensuring that the parameter has `NoEcho: true` specified.

#### Create Pipeline
1. Add github oauth key to parameter store, either by console or by cli:
    ```
    aws ssm put-parameter --name "/Sudoku/github" --value "123456abcde...." --type SecureString
    ```
1. Test retrieving the parameter
    ```
    aws ssm get-parameter --name "/Sudoku/github" --with-decryption
    ```
1. Create the stack, using the cli to import the oauth token from the parameter store:
    ```
    aws cloudformation create-stack --stack-name Sudoku-Pipeline \
     --template-body file://pipeline.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameters ParameterKey=GitHubToken,ParameterValue=`aws ssm get-parameter --name "/Sudoku/github" --with-decryption --query 'Parameter.Value' --output text`
    ```

#### Update the Pipeline
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

Alternatively, straight forward update:
```
aws cloudformation update-stack --stack-name Sudoku-Pipeline \
 --template-body file://pipeline.yaml \
 --capabilities CAPABILITY_NAMED_IAM \
 --parameters ParameterKey=GitHubToken,ParameterValue=`aws ssm get-parameter --name "/Sudoku/github" --with-decryption --query 'Parameter.Value' --output text`
```

### Staging Environment
The Pipeline above is just a POC for building, testing and deploying the serverless functions. There is no automated deployments for the content (such as demo'ed in devopsalex.com).  To deploy a staging web site:

1. Create stack:
    ```
    aws cloudformation create-stack --stack-name Sudoku-Serverless-Staging --template-body file://main.yaml \
     --parameters ParameterKey=Environment,ParameterValue=staging \
     ParameterKey=DefaultSSLCertificate,ParameterValue=true
    ```
1. Create SSL Certificate
1. Update Stack With SSL Certificate ID:
    ```
    aws acm list-certificates --region us-east-1 --query 'CertificateSummaryList[?DomainName==`staging.sudokuless.com`].CertificateArn' --output text

    aws cloudformation update-stack --stack-name Sudoku-Serverless-Staging --template-body file://main.yaml \
     --parameters ParameterKey=Environment,ParameterValue=staging \
     ParameterKey=SSLCertificateId,ParameterValue=6f7aac3b-4e50-....
    ```
1. Build and Copy website content:
    ```
    rm -Rf public/
    hugo --config config.staging.toml
    aws s3 sync public/ s3://staging.sudokuless.com --delete
    ```
1. Add data to sudoku unsolved puzzles bucket:
    ```
    aws s3 cp data/example_puzzles/ s3://sudoku-unsolved-puzzles-staging --recursive
    aws s3 cp data/example_puzzle_solutions/ s3://sudoku-unsolved-puzzle-solutions-staging --recursive
    ```
1. Create Auth stack (with termination protection):
    ```
    aws cloudformation create-stack --stack-name Sudoku-Serverless-Auth-Staging --template-body file://auth.yaml \
     --parameters ParameterKey=Environment,ParameterValue=staging \
     --capabilities CAPABILITY_NAMED_IAM \
     --enable-termination-protection
    ```
1. Configure UserPool:
    ```
    aws cognito-idp list-user-pools --max-results 10 --query 'UserPools[*].{Id:Id, Name:Name}'

    aws cognito-idp create-user-pool-domain --user-pool-id us-west-1_aaaaaaaaa  --domain sudokuless-staging
    ```
1. If configuring LoginWithAmazon see [Procedure](sudoku-serverless-hugo-amz/README.md)


# Reference

### Create a new lambda/api service using SAM
```
sam init --runtime python3.6 --name tryNewPuzzle
```

### Tag a new git version
```
git tag -a v0.0.1 -m "Tag description..."
git push origin v0.0.1
```
