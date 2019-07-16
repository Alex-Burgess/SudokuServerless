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
        var id = result.id;
        var level = result.level;
        var puzzle_rows = result.puzzle_rows;
        console.log('ID: ', id);
        console.log('Level: ', level);
        console.log('Puzzle Rows: ', puzzle_rows);

        $('#puzzle-id').val(id);
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
      var puzzleId = $('#puzzle-id').val()
      console.log('Puzzle ID: ', puzzleId);

      var validateResult = validateFinishedPuzzle(inputs);
      empty = validateResult.empty;
      attemptValues = validateResult.attemptValues;

      if (empty > 0){
        alert("Puzzle is not complete. Number of cells to complete " + empty);
        return
      }

      $.ajax({
          method: 'GET',
          url: _config.api.getNewPuzzleSolutionUrl + puzzleId,
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

      return {
        attemptValues: attemptValues,
        empty: empty
      };
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

    function emptyPuzzle(){
      var table_body ='<table>';

      for (i = 0; i < 9; i++) {
        table_body += '<tr>'
        for (j = 0; j < 9; j++) {
          table_body += '<td><input pattern="[0-9]*" type="text" size="1" width="100%" maxlength="1"></td>';
        }
        table_body += '</tr>'
      }
      table_body+='</table>';
      $('#puzzle').html(table_body);
    }

    function solvePuzzle(){
      var inputs = $('#solveForm :input');

      var validateResult = validateFinishedPuzzle(inputs);
      empty = validateResult.empty;
      if (empty > 65) {
        alert("This doesn't look like a valid puzzle.  The smallest solvable puzzles have at least 17 squares.");
        return;
      }

      puzzleJson = createPuzzleJson(inputs);

      $.ajax({
          method: 'POST',
          url: _config.api.solvePuzzle,
          headers: {
              Authorization: authToken,
          },
          data: puzzleJson,
          contentType: 'application/json',
          success: completeSolvePuzzle,
          error: function ajaxError(jqXHR, textStatus, errorThrown) {
              console.error('Error requesting puzzle solution: ', textStatus, ', Details: ', errorThrown);
              console.error('Response: ', jqXHR.responseText);
              alert('An error occured when requesting your puzzle solution:\n' + jqXHR.responseText);
          }
      });
    }

    function createPuzzleJson(inputs){
      var puzzleData = {
          puzzle_rows : []
      };

      var puzzleRows = [];
      for (row = 0; row < 9; row++) {
        var puzzleRow = [];
        for (col = 0; col < 9; col++) {
          cell = (row * 9) + col;
          if (inputs[cell].value) {
            val = Number(inputs[cell].value)
            puzzleRow.push(val);
          } else {
            puzzleRow.push(0);
          }
        }
        puzzleData.puzzle_rows.push(puzzleRow);
      }

      console.log("puzzleData stringify: " + JSON.stringify(puzzleData));

      return JSON.stringify(puzzleData);
    }

    function completeSolvePuzzle(result) {
        console.log('Response received from solvePuzzle API: ', result);

        solutionPuzzleJson = result.puzzle_rows;

        var table_body ='<table>';
        for (const row of solutionPuzzleJson){
          table_body += '<tr>'
          for (const cell of row){
            table_body += '<td><input type="text" value="' + cell + '" readonly></td>';
          }
          table_body += '</tr>'
        }
        table_body+='</table>';

        $('#puzzle-solved').html(table_body);
    }

    $(function onDocReady() {
        if (/try/.test(window.location.href)) {
          requestNewPuzzle();
        }

        if (/solve/.test(window.location.href)) {
          emptyPuzzle();
        }

        $('#finished').click(puzzleFinished);

        $('#solve').click(solvePuzzle);

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

                  var emailVal;
                  for (const attr of result){
                    console.log('Attribute: ' + attr + ' Value: ' + attr.getValue());
                    if ( attr.Name === "email" ){
                      console.log('Assigning email value: ' + attr.getValue());
                      emailVal = attr.getValue();
                    }
                  }

                  $('.welcomeMessage').text('Hi ' + emailVal + '!');
              });
          }

        });
    });

}(jQuery));
