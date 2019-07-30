import React from "react";
import "./Error.css";

class Error extends React.Component{
    render() {
        return (
            <div className="errorMessage">
                {this.props.errorMessage}
            </div>
        );
    }
};

export default Error
