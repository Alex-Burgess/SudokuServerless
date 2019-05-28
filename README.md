# SudokuServerless
A serverless website with a sudoku theme, based on [Build a Serverless Web App...](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/).


### Quick start
Create the website:
```
hugo new site sudoku-serverless-hugo
git init
git submodule add git@github.com:Alex-Burgess/kube.git themes/kube
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



# Reference
To do.
