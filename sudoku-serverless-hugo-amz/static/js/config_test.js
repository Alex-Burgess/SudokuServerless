window._config = {
    cognito: {
        userPoolId: 'eu-west-1_RLIJMD2h8', // e.g. us-east-2_uXboG5pAb
        userPoolClientId: '46oae21o0mvse9kbdnngdslogh', // e.g. 25ddkmj4v6hfsfvruhpfi7n4hv
        appWebDomain: 'sudokuless-test.auth.eu-west-1.amazoncognito.com', // Exclude the "https://" part.
        redirectUriSignIn: 'http://localhost:1313/signin/',
        redirectUriSignOut: 'http://localhost:1313/',
        identityProvider: 'LoginWithAmazon',
        region: 'eu-west-1' // e.g. us-east-2
    },
    api: {
        requestNewPuzzleUrl: 'https://ej4xecnx14.execute-api.eu-west-1.amazonaws.com/staging/tryNewPuzzle/',
        getNewPuzzleSolutionUrl: 'https://pdkvj7254c.execute-api.eu-west-1.amazonaws.com/staging/getNewPuzzleSolution/',
        solvePuzzle: 'https://nrvt0b0zoc.execute-api.eu-west-1.amazonaws.com/staging/solvePuzzle/'
    }
};
