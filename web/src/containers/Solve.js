import React, { Component } from "react";
import { PageHeader } from "react-bootstrap";
import { API } from "aws-amplify";
import "./Solve.css";
import LoaderButton from "../components/LoaderButton";
import Error from "../components/Error";
import Puzzle from "../components/Puzzle";

export default class Try extends Component {
  constructor(props) {
    super(props);

    var puzzle = [];
    for (var c = 0; c < 81; c++) {
        puzzle[c] = 0;
    }

    var startingPuzzle = [];
    for (var x = 0; x < 81; x++) {
        startingPuzzle[x] = 0;
    }

    this.state = {
      isLoading: true,
      startingPuzzle: startingPuzzle,
      puzzle: puzzle,
      solution: [],
      solutionStatus: false,
      showError: false
    };
  }

  async componentDidMount() {
    if (!this.props.isAuthenticated) {
      return;
    }

    this.setState({ isLoading: false });
  }

  validateForm() {
    var emptyCellCount = 0;
    for (var cell of this.state.puzzle){
      if (cell === 0) {
        emptyCellCount = emptyCellCount + 1;
      }
    }

    if (emptyCellCount > 65) {
      return false;
    }

    return true;
  }

  updateDataForAPI() {
    var requestPuzzle = {
      puzzle_rows : []
    }

    let row = [];
    var cellNumber = 0;

    for (var cell of this.state.puzzle){
        row.push(parseInt(cell));
        cellNumber = cellNumber + 1;

        if (cellNumber === 9) {
          requestPuzzle["puzzle_rows"].push(row);
          row = [];
          cellNumber = 0;
        }
    }

    return requestPuzzle;
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

  solve(requestPuzzle) {
    return API.post("solve", "/", {
      body: requestPuzzle
    });
  }

  handleChange = event => {
    var puzzle = this.state.puzzle;
    puzzle[event.target.name] = event.target.value;

    this.setState({ puzzle: puzzle });
  }

  handleSubmit = async event => {
    event.preventDefault();
    this.setState({ isLoading: true });

    try {
      const puzzleJson = this.updateDataForAPI();
      const solutionJson = await this.solve(puzzleJson);
      const solution = this.updateDataFromAPI(solutionJson);
      this.setState({ solution: solution });
      this.setState({ solutionStatus: true });
    } catch (e) {
      console.log('Error returned from solve API call: ' + e.response.data.error);
      this.setState({ showError: true });
      this.setState({ errorMessage: e.response.data.error });
    }

    this.setState({ isLoading: false });
  }

  renderPuzzle() {
    return (
      <div className="solve">
        <PageHeader>Solve a puzzle</PageHeader>
        { this.state.showError ? <Error errorMessage={this.state.errorMessage}/> : null }
        <div className="solvePuzzle">
          <form onSubmit={this.handleSubmit} onChange={this.handleChange}>
            {!this.state.isLoading ? <Puzzle puzzle={this.state.puzzle} startingPuzzle={this.state.startingPuzzle} handleChange={this.handleChange} /> : null }
            <LoaderButton bsSize="lg" disabled={!this.validateForm()} type="submit"
              isLoading={this.state.isLoading} text="Solve" loadingText="Solving…"
            />
          </form>
        </div>
      </div>
    );
  }

  renderSolution() {
    return (
      <div className="solve">
        <PageHeader>Solve a puzzle</PageHeader>
        <div className="solvePuzzle">
          Solution
          {!this.state.isLoading ? <Puzzle puzzle={this.state.solution} startingPuzzle={this.state.startingPuzzle} handleChange={this.handleChange} /> : null }
        </div>
      </div>
    );
  }

  render() {
    return (
      <div>
        {this.state.solutionStatus ? this.renderSolution() : this.renderPuzzle()}
      </div>
    );
  }
}
