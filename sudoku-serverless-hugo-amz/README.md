# Deploy LoginWithAmazon POC Notes

1. Update UserPool Configuration
    ```
    aws cognito-idp create-identity-provider --cli-input-json file://identity-provider-config.json

    aws cognito-idp update-user-pool-client --user-pool-id eu-west-1_hcA217WJn --client-id f0vbt18vn4jf8n5v6q3gbi1tb \
       --supported-identity-providers LoginWithAmazon \
       --callback-urls '["https://sudokuless.com/signin/"]' \
       --logout-urls '["https://sudokuless.com"]' \
       --allowed-o-auth-scopes '["email","openid","profile","aws.cognito.signin.user.admin"]' \
       --allowed-o-auth-flows '["implicit"]'
    ```
1. Clean Public folder
    ```
    rm -Rf public
    ```
1. Build Hugo Project
    ```
    hugo
    ```
1. Update signin page js scripts
    ```
    vi public/signin/index.html

    Replace line 59 with:
    <script type="text/javascript" src="/js/aws-cognito-sdk.min.js"></script><script type="text/javascript" src="/js/amazon-cognito-auth.js"></script><script type="text/javascript" src="/js/config.js"></script><script type="text/javascript" src="/js/cognito-auth-amz.js"></script>
    ```
1. Sync content
    ```
    aws s3 sync public/ s3://sudokuless --delete
    ```
1. Clear CloudFront Cache


# Issues
1. Found that amazon-cognito-identity.min.js and amazon-cognito-auth.js did not play nicely together and caused issues with using the sdks.
1. Worked around this, by only having amazon-cognito-auth.js in the signin page, but this meant that functionality to redirect users to dashboard page if logged in didn't work, if they went to the signin page.
1. Found the use of libraries/sdks in this way made for quite hacky code implementation.
