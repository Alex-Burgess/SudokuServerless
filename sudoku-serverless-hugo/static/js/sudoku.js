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

        $('#finished').show();
    }

    $(function onDocReady() {
        if (/try/.test(window.location.href)) {
          requestNewPuzzle();
        }

        $('#finished').click(function() {
            var $inputs = $('#tryForm :input');

            var values = {};
            var i = 0;
            var empty = 0;
            $inputs.each(function() {
              i = i + 1;
              values[i] = $(this).val();
              if ($(this).val() == 0) {
                empty = empty + 1;
              }
            });

            if (empty > 0){
                alert("Puzzle is not complete. Number of cells to complete " + empty);
                return;
            }

            console.log("Completed puzzle data: " + JSON.stringify(values))

            alert("Puzzle Completed!");
        });

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
