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
      var $inputs = $('#tryForm :input');

      var attemptValues = [];
      var i = 0;
      var empty = 0;
      $inputs.each(function() {
        attemptValues.push($(this).val());

        if ($(this).val() == 0) {
          empty = empty + 1;
        }
      });

      if (empty > 0){
          alert("Puzzle is not complete. Number of cells to complete " + empty);
          return;
      } else {
        console.log("Completed puzzle data: " + attemptValues);

        var solutionJson = getPuzzleSolution();
        checkPuzzleCorrect(attemptValues,solutionJson);
      }
    }

    function getPuzzleSolution(){
      // Retrive the puzzle using api call
      // var solution_puzzle_rows = result.puzzle_rows;

      var solution_puzzle_rows = [
        [5,8,1,9,6,4,7,2,3],
        [7,2,4,5,1,3,6,9,8],
        [3,6,9,7,8,2,4,1,5],
        [4,1,9,2,5,7,8,6,9],
        [2,9,6,3,4,8,1,5,7],
        [8,5,7,1,9,6,2,3,4],
        [1,4,2,8,3,9,5,7,6],
        [9,7,8,6,2,5,3,4,1],
        [6,3,5,4,7,1,9,8,2]
      ];

      return solution_puzzle_rows;
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
      // for (i = 0; i < 9; i++) {
        if (attemptValues[i] != solutionValues[i]) {
          console.log("Attempt did not match the solution. AttemptValue:" + attemptValues[i] + " SolutionValue:" + solutionValues[i]);
          $('#finished-button').hide();
          $('#failed').show();

          displaySolution(solutionJson);
          return;
        }
      }


      $('#finished-button').hide();
      $('#correct').show();
    }

    function displaySolution(solutionValues){
      var table_body ='<table>';
      for (const row of solutionValues){
        table_body += '<tr>'
        for (const cell of row){
          table_body += '<td><input type="text" value="' + cell + '" readonly></td>';
        }
        table_body += '</tr>'
      }
      table_body+='</table>';
      $('#puzzle-solution').html(table_body);
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
