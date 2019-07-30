const test = {
  apiGateway: {
    REGION: "eu-west-1",
    TRY: "https://hsjqb93qkh.execute-api.eu-west-1.amazonaws.com/test/tryNewPuzzle",
    SOLVE: "https://vpt95x5u8b.execute-api.eu-west-1.amazonaws.com/test/solvePuzzle",
    SOLUTION: "https://fh690lofdi.execute-api.eu-west-1.amazonaws.com/test/getNewPuzzleSolution"
  },
  cognito: {
    REGION: "eu-west-1",
    USER_POOL_ID: "eu-west-1_RLIJMD2h8",
    APP_CLIENT_ID: "46oae21o0mvse9kbdnngdslogh",
    IDENTITY_POOL_ID: "eu-west-1:e0366b7b-1c01-46c3-b960-8a1e1a0fdab2",
    DOMAIN: "sudokuless-test.auth.eu-west-1.amazoncognito.com",
    SCOPE: ['email', 'profile', 'aws.cognito.signin.user.admin', 'openid'],
    REDIRECTSIGNIN: "http://localhost:3000/",
    REDIRECTSIGNOUT: "http://localhost:3000/",
    RESPONSETYPE: 'code',
  }
};

const staging = {
  apiGateway: {
    REGION: "eu-west-1",
    TRY: "https://ej4xecnx14.execute-api.eu-west-1.amazonaws.com/staging/tryNewPuzzle",
    SOLVE: "https://nrvt0b0zoc.execute-api.eu-west-1.amazonaws.com/staging/solvePuzzle",
    SOLUTION: "https://pdkvj7254c.execute-api.eu-west-1.amazonaws.com/staging/getNewPuzzleSolution"
  },
  cognito: {
    REGION: "eu-west-1",
    USER_POOL_ID: "eu-west-1_2eF2vZyKX",
    APP_CLIENT_ID: "rp869po59eb66kflg5p25jgj7",
    IDENTITY_POOL_ID: "eu-west-1:eb235942-9722-4625-a6e4-1c1c8906bb8c",
    DOMAIN: "sudokuless-staging.auth.eu-west-1.amazoncognito.com",
    SCOPE: ['email', 'profile', 'aws.cognito.signin.user.admin', 'openid'],
    REDIRECTSIGNIN: "https://staging.sudokuless.com/",
    REDIRECTSIGNOUT: "https://staging.sudokuless.com/",
    RESPONSETYPE: 'code',
  }
};

const prod = {
  apiGateway: {
    REGION: "eu-west-1",
    TRY: "https://wdygge7sq9.execute-api.eu-west-1.amazonaws.com/prod/tryNewPuzzle",
    SOLVE: "https://2qa0qpd1u4.execute-api.eu-west-1.amazonaws.com/prod/solvePuzzle",
    SOLUTION: "https://2lzeuedz07.execute-api.eu-west-1.amazonaws.com/prod/getNewPuzzleSolution"
  },
  cognito: {
    REGION: "eu-west-1",
    USER_POOL_ID: "eu-west-1_hcA217WJn",
    APP_CLIENT_ID: "f0vbt18vn4jf8n5v6q3gbi1tb",
    IDENTITY_POOL_ID: "eu-west-1:30a99420-7a33-42e7-9224-83ae42c51e85",
    DOMAIN: "sudokuless.auth.eu-west-1.amazoncognito.com",
    SCOPE: ['email', 'profile', 'aws.cognito.signin.user.admin', 'openid'],
    REDIRECTSIGNIN: "https://sudokuless.com/",
    REDIRECTSIGNOUT: "https://sudokuless.com/",
    RESPONSETYPE: 'code',
  }
};

const environment = process.env.REACT_APP_STAGE;
console.log("Environment: " + environment);
var config;
switch (environment) {
  case "prod":
    console.log("Config: prod");
    config = prod;
    break;
  case "staging":
  console.log("Config: staging");
  config = staging;
    break;
  default:
    console.log("Config: test");
    config = test;
    break;
}

export default {
  // Add common config values here
  ...config
};
