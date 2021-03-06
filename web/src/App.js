import React, { Component, Fragment } from "react";
import { Link, withRouter } from "react-router-dom";
import { Nav, Navbar, NavItem } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import "./App.css";
import Routes from "./Routes";
import { Auth, Hub } from "aws-amplify";
import { Helmet } from 'react-helmet';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isAuthenticated: false,
      isAuthenticating: true,
      email: null
    };
  }

  async componentDidMount() {
    Hub.listen("auth", ({ payload: { event, data } }) => {
          console.log("There was an event: " + event)
          switch (event) {
            case "signIn":
              console.log("User was signed in");
              this.setState({ user: data });
              this.userHasAuthenticated(true);
              this.getAttributes();
              break;
            case "signOut":
              console.log("User was sign out");
              this.setState({ user: null });
              break;
            default:
              console.log("Unexpected auth event: " + event);
              this.setState({ user: null });
              break;
          }
        });

    try {
      await Auth.currentSession();
      this.userHasAuthenticated(true);
      console.log("User was authenticated");
    }
    catch(e) {
      if (e !== 'No current user') {
        alert(e);
      }
    }

    if (this.state.isAuthenticated) {
      try {
        this.getAttributes();
      }
      catch(e) {
        if (e !== 'No current user') {
          alert(e);
        }
      }
    }

    this.setState({ isAuthenticating: false });
  }

  getAttributes = async () => {
    console.log("Getting email address");
    let user = await Auth.currentAuthenticatedUser();
    const { attributes } = user;
    console.log("User email: " + attributes['email']);
    this.setState({ email: attributes['email'] });
  }

  userHasAuthenticated = authenticated => {
    this.setState({ isAuthenticated: authenticated });
  }

  handleLogout = async event => {
    await Auth.signOut();

    this.userHasAuthenticated(false);

    this.props.history.push("/login");
  }

  render() {
    const childProps = {
      isAuthenticated: this.state.isAuthenticated,
      userHasAuthenticated: this.userHasAuthenticated,
      email: this.state.email
    };

    return (
      !this.state.isAuthenticating &&
      <div className="App container">
        <Helmet>
          {process.env.REACT_APP_STAGE !== "prod"
            ? <title>Sudokuless - {process.env.REACT_APP_STAGE}</title>
            : <title>Sudokuless</title>
          }
        </Helmet>
        <Navbar fluid collapseOnSelect>
          <Navbar.Header>
            <Navbar.Brand>
              <Link to="/">Sudokuless</Link>
            </Navbar.Brand>
            <Navbar.Toggle />
          </Navbar.Header>
          <Navbar.Collapse>
            <Nav pullRight>
              {this.state.isAuthenticated
                ? <Fragment>
                    <LinkContainer to="/try">
                      <NavItem>Try</NavItem>
                    </LinkContainer>
                    <LinkContainer to="/solve">
                      <NavItem>Solve</NavItem>
                    </LinkContainer>
                    <LinkContainer to="/settings">
                      <NavItem>Settings</NavItem>
                    </LinkContainer>
                    <NavItem onClick={this.handleLogout}>Logout</NavItem>
                  </Fragment>
                : <Fragment>
                    <LinkContainer to="/signup">
                      <NavItem>Signup</NavItem>
                    </LinkContainer>
                    <LinkContainer to="/login">
                      <NavItem>Login</NavItem>
                    </LinkContainer>
                  </Fragment>
                }
            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <Routes childProps={childProps} />
      </div>
    );
  }
}

export default withRouter(App);
