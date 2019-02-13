# SudokuServerless
A serverless website with a sudoku theme

## Setup
Copying test puzzles to s3 bucket:
```
aws s3 cp puzzles/ s3://sudoku-unsolved-puzzles --recursive
```

