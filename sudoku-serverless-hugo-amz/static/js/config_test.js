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
        requestNewPuzzleUrl: 'https://hsjqb93qkh.execute-api.eu-west-1.amazonaws.com/test/tryNewPuzzle/',
        getNewPuzzleSolutionUrl: 'https://fh690lofdi.execute-api.eu-west-1.amazonaws.com/test/getNewPuzzleSolution/',
        solvePuzzle: 'https://vpt95x5u8b.execute-api.eu-west-1.amazonaws.com/test/solvePuzzle/'
    }
};
