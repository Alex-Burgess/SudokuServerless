# SudokuServerless
A serverless website with a sudoku theme, based on [Build a Serverless Web App...](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/).

[Worlds hardest sudoku](https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html)

### Quick start
Create the website:
```
hugo new site sudoku-serverless-hugo
git init
```

Add a theme:
```
git submodule add git@github.com:Alex-Burgess/kube.git sudoku-serverless-hugo/themes/kube
```

Copy and Update the config:
```
cp themes/kube/exampleSite/config.toml .
```

Create main stack:
```
aws cloudformation create-stack --stack-name Sudoku-Serverless-Main --template-body file://main.yaml
```

Build and Copy website content:
```
hugo
aws s3 sync public/ s3://sudoku-serverless --delete
```

Update stack:
```
aws cloudformation update-stack --stack-name Sudoku-Serverless-Main --template-body file://main.yaml
```

Add data to sudoku unsolved puzzles bucket:
```
aws s3 cp data/example_puzzles/ s3://sudoku-unsolved-puzzles --recursive
aws s3 cp data/example_puzzle_solutions/ s3://sudoku-unsolved-puzzle-solutions --recursive
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
     
# Reference

### Create a new lambda/api service using SAM
```
sam init --runtime python3.6 --name tryNewPuzzle
```
