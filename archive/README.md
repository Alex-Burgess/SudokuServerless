# SudokuServerless
A serverless website with a sudoku theme

## Setup
Deploying sam application for remote testing:
```
$ sam package --output-template-file packaged.yaml --s3-bucket serverless-remote-builds
$ sam deploy --template-file packaged.yaml --stack-name cloud9-SudokuServerless --capabilities CAPABILITY_NAMED_IAM --region eu-west-1
```

Copying test puzzles to s3 bucket:
```
aws s3 cp test_puzzles/ s3://sudoku-unsolved-puzzles --recursive
```


Worlds hardest sudoku
https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html 