/*global Sudoku _config*/

var Sudoku = window.Sudoku || {};
Sudoku.map = Sudoku.map || {};

var homePageUrl = '/';
var dashboardUrl = '/user/';

(function rideScopeWrapper($) {
    var authToken;
    Sudoku.authToken.then(function setAuthToken(token) {
        if (token) {
            authToken = token;

            if ((/signin/.test(window.location.href)) || (/register/.test(window.location.href)) || (/verify/.test(window.location.href)) || (window.location.pathname == "/") ) {
              window.location.href = dashboardUrl;
            }
        } else {
          if (!((/signin/.test(window.location.href)) || (/register/.test(window.location.href)) || (/verify/.test(window.location.href)) || (window.location.pathname == "/") )) {
            window.location.href = homePageUrl;
          }
        }
    }).catch(function handleTokenError(error) {
        alert(error);
        window.location.href = homePageUrl;
    });

    function requestNewPuzzle(){
      $.ajax({
          method: 'GET',
          // url: _config.api.invokeUrl + '/tryNewPuzzle',
          url: _config.api.invokeUrl,
          headers: {
              Authorization: authToken,
          },
          contentType: 'application/json',
          success: completeRequest,
          error: function ajaxError(jqXHR, textStatus, errorThrown) {
              console.error('Error requesting puzzle: ', textStatus, ', Details: ', errorThrown);
              console.error('Response: ', jqXHR.responseText);
              alert('An error occured when requesting your puzzle:\n' + jqXHR.responseText);
          }
      });
    }

    function completeRequest(result) {
        console.log('Response received from API: ', result);
        var level = result.level;
        var puzzle_rows = result.puzzle_rows;
        console.log('Level: ', level);
        console.log('Puzzle Rows: ', puzzle_rows);

        $('#level').append(level);
        $('#puzzle-section').show();
        for (const row of puzzle_rows){
          $('#puzzle').append($('<tr><td>' + row + '</td></tr>'));
        }
        // $('#puzzle').append($('<tr><td>1</td><td>2</td><td>3</td></tr>'));
    }

    // Register click handler for #request button
    $(function onDocReady() {
        $('#request').click(requestNewPuzzle);
        $('#signOut').click(function() {
            Sudoku.signOut();
            alert("You have been signed out.");
            window.location = homePageUrl;
        });

        Sudoku.authToken.then(function printWelcome(token) {
          var data = {
              UserPoolId: _config.cognito.userPoolId,
              ClientId: _config.cognito.userPoolClientId
          };

          var userPool = new AmazonCognitoIdentity.CognitoUserPool(data);
          var cognitoUser = userPool.getCurrentUser();

          if (cognitoUser != null) {
              cognitoUser.getSession(function(err, session) {
                  if (err) {
                     alert(err);
                      return;
                  }
                  console.log('session validity: ' + session.isValid());
              });

              cognitoUser.getUserAttributes(function(err, result) {
                  if (err) {
                      alert(err);
                      return;
                  }

                  $('.welcomeMessage').text('Hi ' + result[2].getValue() + '!');
              });
          }

        });
    });

}(jQuery));
