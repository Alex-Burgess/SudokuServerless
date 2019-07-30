import React from "react";

class PuzzleDetails extends React.Component{
    render() {
        return (
            <div id="puzzle-level">
              <h4>
                {"Puzzle Id: " + this.props.id}
              </h4>
              <h4>
                {"Puzzle Level: " + this.props.level}
              </h4>
            </div>
        );
    }
};

export default PuzzleDetails
