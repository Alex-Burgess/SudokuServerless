import React, { Component } from "react";
import { PageHeader } from "react-bootstrap";
import LoaderButton from "../components/LoaderButton";
import { API } from "aws-amplify";
import "./Try.css";
import PuzzleDetails from "../components/PuzzleDetails";
import Puzzle from "../components/Puzzle";

export default class Try extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: true,
      startingPuzzle: [],
      puzzle: [],
      solution: [],
      completed: false,
      correct: false,
      id: null,
      level: null
    };
  }

  async componentDidMount() {
    if (!this.props.isAuthenticated) {
      return;
    }

    try {
      const responseObject = await this.try();
      this.setState({ level: responseObject.level });
      this.setState({ id: responseObject.id });

      var puzzle = [];
      var cellId = 0;
      for (const row of responseObject.puzzle_rows){
        for (const cell of row){
          puzzle[cellId] = cell;
          cellId = cellId + 1;
        }
      }

      this.setState({ puzzle: puzzle });
      const startingPuzzle = [...puzzle];
      this.setState({ startingPuzzle: startingPuzzle });
    } catch (e) {
      alert(e);
    }

    this.setState({ isLoading: false });
  }

  try() {
    console.log('Calling tryNewPuzzle API');
    return API.get("tryNewPuzzle", "/");
  }

  validateForm() {
    var emptyCellCount = 0;
    for (var cell of this.state.puzzle){
      if (cell === 0) {
        emptyCellCount = emptyCellCount + 1;
      }
    }

    if (emptyCellCount > 0) {
      return false;
    }

    return true;
  }

  solution() {
    return API.get("getNewPuzzleSolution", "/" + this.state.id);
  }

  updateDataFromAPI(solutionJson) {
    console.log('puzzle rows: ' + solutionJson.puzzle_rows);

    var puzzle = [];
    var cellId = 0;
    for (const row of solutionJson.puzzle_rows){
      for (const cell of row){
        puzzle[cellId] = cell;
        cellId = cellId + 1;
      }
    }

    return puzzle;
  }

  checkPuzzleCorrect(puzzle, solution){
    for (var i = 0; i < 81; i++) {
      if (parseInt(puzzle[i]) !== parseInt(solution[i])) {
        console.log("Attempt did not match the solution. Cell: " + i + " AttemptValue:" + puzzle[i] + " SolutionValue:" + solution[i]);
        return false;
      }
    }

    return true;
  }

  handleSubmit = async event => {
    event.preventDefault();
    this.setState({ isLoading: true });

    try {
      const solutionJson = await this.solution();
      const solution = this.updateDataFromAPI(solutionJson);
      this.setState({ solution: solution });

      var correct = this.checkPuzzleCorrect(this.state.puzzle, this.state.solution);
      this.setState({ correct: correct });
      this.setState({ completed: true });
    } catch (e) {
      console.log('Error returned from get Solution API call: ' + e.response.data.error);
      this.setState({ showError: true });
      this.setState({ errorMessage: e.response.data.error });
    }

    this.setState({ isLoading: false });
  }

  handleChange = event => {
    var puzzle = this.state.puzzle;
    puzzle[event.target.name] = event.target.value;

    this.setState({ puzzle: puzzle });
  }

  renderNewPuzzle() {
    return (
      <div className="try">
        <PageHeader>Try a puzzle</PageHeader>
        { this.state.id ? <PuzzleDetails id={this.state.id} level={this.state.level} /> : null }

        <div className="tryPuzzle">
          <form onSubmit={this.handleSubmit}>
            { this.state.id ? <Puzzle puzzle={this.state.puzzle} startingPuzzle={this.state.startingPuzzle} isLoading={this.state.isLoading} handleChange={this.handleChange} /> : null }
            <LoaderButton bsSize="lg" disabled={!this.validateForm()} type="submit"
              isLoading={this.props.isLoading} text="Finished" loadingText="Checking…"
            />
          </form>
        </div>
      </div>
    );
  }

  renderSolution() {
    return (
      <div className="try">
        <PageHeader>Try a puzzle</PageHeader>
        { this.state.id ? <PuzzleDetails id={this.state.id} level={this.state.level} /> : null }

        {!this.state.isLoading
          ? <div className="tryPuzzle">
              <Puzzle puzzle={this.state.puzzle} startingPuzzle={this.state.startingPuzzle} />
              {!this.state.correct
                ? <div>Not quite! The solution
                    <Puzzle puzzle={this.state.solution} startingPuzzle={this.state.startingPuzzle}/>
                  </div>
                : <div>Correct!</div>
              }
            </div>
          : <div>Oops there was an issue.</div>
          }
      </div>
    );
  }

  render() {
    return (
      <div>
        {this.state.completed ? this.renderSolution() : this.renderNewPuzzle()}
      </div>
    );
  }
}
