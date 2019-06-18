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
          url: _config.api.requestNewPuzzleUrl,
          headers: {
              Authorization: authToken,
          },
          contentType: 'application/json',
          success: completeRequestNewPuzzle,
          error: function ajaxError(jqXHR, textStatus, errorThrown) {
              console.error('Error requesting puzzle: ', textStatus, ', Details: ', errorThrown);
              console.error('Response: ', jqXHR.responseText);
              alert('An error occured when requesting your puzzle:\n' + jqXHR.responseText);
          }
      });
    }

    function completeRequestNewPuzzle(result) {
        console.log('Response received from API: ', result);
        var level = result.level;
        var puzzle_rows = result.puzzle_rows;
        console.log('Level: ', level);
        console.log('Puzzle Rows: ', puzzle_rows);

        $('#puzzle-level').text('Level: ' + level);

        var table_body ='<table>';
        for (const row of puzzle_rows){
          table_body += '<tr>'
          for (const cell of row){
            if (cell == 0) {
              table_body += '<td><input pattern="[0-9]*" type="text" size="1" width="100%" maxlength="1" ></td>';
            } else {
              table_body += '<td><input type="text" value="' + cell + '" readonly></td>';
            }
          }
          table_body += '</tr>'
        }
        table_body+='</table>';
        $('#puzzle').html(table_body);

        $('#finished-button').show();
    }

    function puzzleFinished(){
      var inputs = $('#tryForm :input');

      var attemptValues = validateFinishedPuzzle(inputs);

      $.ajax({
          method: 'GET',
          url: _config.api.getNewPuzzleSolutionUrl + '1',
          headers: {
              Authorization: authToken,
          },
          contentType: 'application/json',
          success: function(response){
            completeGetNewPuzzleSolution(response, attemptValues);
          },
          error: function ajaxError(jqXHR, textStatus, errorThrown) {
              console.error('Error requesting puzzle solution: ', textStatus, ', Details: ', errorThrown);
              console.error('Response: ', jqXHR.responseText);
              alert('An error occured when requesting your puzzle solution:\n' + jqXHR.responseText);
          }
      });
    }

    function validateFinishedPuzzle(inputs){
      var attemptValues = [];
      var i = 0;
      var empty = 0;
      inputs.each(function() {
        attemptValues.push($(this).val());

        if ($(this).val() == 0) {
          empty = empty + 1;
        }
      });

      return attemptValues
    }

    function completeGetNewPuzzleSolution(result, attemptValues) {
        console.log('Response received from getNewPuzzleSolution API: ', result);
        console.log("Completed puzzle data: " + attemptValues);

        solutionPuzzleJson = result.puzzle_rows;

        var puzzleCorrect = checkPuzzleCorrect(attemptValues,solutionPuzzleJson);

        if (puzzleCorrect == true) {
          $('#finished-button').hide();
          $('#correct').show();
        } else {
          var table_body ='<table>';
          for (const row of solutionPuzzleJson){
            table_body += '<tr>'
            for (const cell of row){
              table_body += '<td><input type="text" value="' + cell + '" readonly></td>';
            }
            table_body += '</tr>'
          }
          table_body+='</table>';

          $('#finished-button').hide();
          $('#failed').show();
          $('#puzzle-solution').html(table_body);
        }
    }

    function checkPuzzleCorrect(attemptValues,solutionJson){
      var solutionValues = [];

      for (const row of solutionJson){
        for (const cell of row){
          solutionValues.push(cell);
        }
      }

      var i;
      for (i = 0; i < 81; i++) {
        if (attemptValues[i] != solutionValues[i]) {
          console.log("Attempt did not match the solution. AttemptValue:" + attemptValues[i] + " SolutionValue:" + solutionValues[i]);
          return false;
        }
      }

      return true;
    }

    $(function onDocReady() {
        if (/try/.test(window.location.href)) {
          requestNewPuzzle();
        }

        $('#finished').click(puzzleFinished);

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
