window._config = {
    cognito: {
        userPoolId: 'eu-west-1_hcA217WJn', // e.g. us-east-2_uXboG5pAb
        userPoolClientId: 'f0vbt18vn4jf8n5v6q3gbi1tb', // e.g. 25ddkmj4v6hfsfvruhpfi7n4hv
        appWebDomain: 'sudokuless2.auth.eu-west-1.amazoncognito.com', // Exclude the "https://" part.
  			redirectUriSignIn: 'https://sudokuless.com/signin/',
  			redirectUriSignOut: 'https://sudokuless.com/',
  			identityProvider: 'LoginWithAmazon',
        region: 'eu-west-1' // e.g. us-east-2
    },
    api: {
        requestNewPuzzleUrl: 'https://wdygge7sq9.execute-api.eu-west-1.amazonaws.com/prod/tryNewPuzzle/',
        getNewPuzzleSolutionUrl: 'https://2lzeuedz07.execute-api.eu-west-1.amazonaws.com/prod/getNewPuzzleSolution/',
        solvePuzzle: 'https://2qa0qpd1u4.execute-api.eu-west-1.amazonaws.com/prod/solvePuzzle/'
    }
};
