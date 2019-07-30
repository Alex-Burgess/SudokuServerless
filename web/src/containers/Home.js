import React, { Component } from "react";
import { PageHeader, ListGroup } from "react-bootstrap";
import "./Home.css";
// import { API } from "aws-amplify";


export default class Home extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: true,
      notes: []
    };
  }

  async componentDidMount() {
    if (!this.props.isAuthenticated) {
      return;
    }

    // try {
    //   const notes = await this.notes();
    //   this.setState({ notes });
    // } catch (e) {
    //   alert(e);
    // }

    this.setState({ isLoading: false });
  }

  // notes() {
  //   return API.get("tryNewPuzzle", "/");
  // }

  renderNotesList(notes) {
    return null;
  }

  renderLander() {
    return (
      <div className="lander">
        {process.env.REACT_APP_STAGE !== "prod"
          ? <h1>Sudokuless - {process.env.REACT_APP_STAGE}</h1>
          : <h1>Sudokuless</h1>
        }
        <p>A Serverless demo application using AWS</p>
        <img src="/screenshot.png" className="img-fluid full-width" alt="Screenshot" />
      </div>
    );
  }

  renderNotes() {
    return (
      <div className="notes">
        <PageHeader>Your Puzzle Results</PageHeader>
        <p>Username: {this.props.user}</p>
        <p>Email: {this.props.email}</p>
        <ListGroup>
          {!this.state.isLoading && this.renderNotesList(this.state.notes)}
        </ListGroup>
      </div>
    );
  }

  render() {
    return (
      <div className="Home">
        {this.props.isAuthenticated ? this.renderNotes() : this.renderLander()}
      </div>
    );
  }
}
