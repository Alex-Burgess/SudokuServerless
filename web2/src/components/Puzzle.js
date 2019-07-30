import React from "react";
import "./Puzzle.css";

class Puzzle extends React.Component{
    createPuzzle(puzzle, startingPuzzle) {
      let rows = [];
      let row = [];
      var r = 0;
      var cellId = 0;
      var rowId = 0;

      for (var c = 0; c < 81; c++) {
        var cell = puzzle[c];
        var startingCellValue = startingPuzzle[c];

        if (cell === 0) {
          row.push(<td key={cellId}><input name={cellId} value={undefined} onChange={this.props.handleChange} pattern="[0-9]*" type="text" size="1" width="100%" maxLength="1" /></td>);
        } else if (startingCellValue !== 0) {
          row.push(<td key={cellId}><input name={cellId} value={cell} type="text" readOnly /></td>);
        } else {
          row.push(<td key={cellId}><input name={cellId} value={cell} onChange={this.props.handleChange} pattern="[0-9]*" type="text" size="1" width="100%" maxLength="1" /></td>);
        }

        cellId = cellId + 1;
        r = r + 1;

        if (r === 9) {
          rows.push(<tr key={rowId}>{row}</tr>)
          rowId = rowId + 1;
          row = [];
          r = 0;
        }
      }

      return (
        <div className="puzzle" id="puzzle">
          <table id="puzzle" className="puzzle">
           <tbody>
             {rows}
           </tbody>
         </table>
        </div>
      )
    }

    render() {
        return (
            <div>
              {this.createPuzzle(this.props.puzzle, this.props.startingPuzzle)}
            </div>
        );
    }
};

export default Puzzle
