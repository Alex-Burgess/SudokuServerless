/*global Sudoku _config AmazonCognitoIdentity AWSCognito*/

var Sudoku = window.Sudoku || {};

(function scopeWrapper($) {
    var dashboardUrl = '/user/';

    if (!(_config.cognito.userPoolId &&
          _config.cognito.userPoolClientId &&
          _config.cognito.region)) {
        $('#noCognitoMessage').show();
        return;
    }

     /*
      *  Event Handlers
      */

    $(function onDocReady() {
        var auth = initCognitoSDK();
        $('#AmazonLogin').click(function(){
          amazonLogin(auth)
        });

        $('#signOut').click(function(){
          auth.signOut();
        });

        console.log('Parsing Web response')
        var curUrl = window.location.href;
    		auth.parseCognitoWebResponse(curUrl);
    });

    // Perform user operations.
  	function amazonLogin(auth) {
  			auth.getSession();
  	}

  	// Operations when signed in.
    function showSignedIn(session) {
      console.log('getting session');

      console.log('Redirecting to user page')
      window.location.href = dashboardUrl;

  	}

    // Initialize a cognito auth object.
  	function initCognitoSDK() {
      console.log('Initing cognito sdk');
  		var authData = {
  			ClientId : _config.cognito.userPoolClientId, // Your client id here
  			AppWebDomain : _config.cognito.appWebDomain, // Exclude the "https://" part.
  			TokenScopesArray : [], // like ['openid','email','phone']...
  			RedirectUriSignIn : _config.cognito.redirectUriSignIn,
  			RedirectUriSignOut : _config.cognito.redirectUriSignOut,
  			IdentityProvider : _config.cognito.identityProvider,
        UserPoolId : _config.cognito.userPoolId,
        AdvancedSecurityDataCollectionFlag : false
  		};
  		var auth = new AmazonCognitoIdentity.CognitoAuth(authData);
  		// You can also set state parameter
  		// auth.setState(<state parameter>);
  		auth.userhandler = {
  			onSuccess: function(result) {
  				alert("Sign in success");
  				showSignedIn(result);
  			},
  			onFailure: function(err) {
  				alert("Error!" + err);
  			}
  		};
  		// The default response_type is "token", uncomment the next line will make it be "code".
  		// auth.useCodeGrantFlow();
  		return auth;
  	}

}(jQuery));
