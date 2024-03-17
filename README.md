# Credit Recommendation Shared Infra Resources

## Table of Contents

- [Introduction](#introduction)
- [Description](#description)
- [Deployment](#deployment)
- [References](#references)

## Introduction

- This repository is used to create infra related resources such as
    - *API Gateway*
    - *API Gateway Authorizer*
    - *API Gateway Key*
    - *API Gateway Usage Plan*
    - *S3 bucket*
    - *Cognito User Pool*
    - *Cognito App Client*
    - *AWS WAF*
    - *Custom Cloudformation Resources through Lambda function*
- All resources which are required in the future which will be shared among different lambda functions should be created through this repository

## Description

- Api gateway related resources files are listed below.
    - [API Gateway](serverless/configs/resources/api-gateway.yml)
    - [API Gateway Credit Recommendation API Key](serverless/configs/resources/api-gateway-api-key.yml)
    - [API Gateway Scindo API Key](serverless/configs/resources/scindo-api-gateway-api-key.yml)
    - [API Gateway authorizer](serverless/configs/resources/api-gateway-authorizer.yml)
    - [API Gateway waf](serverless/configs/resources/api-gateway-waf2.yml)
    - [API Gateway WAF IP Whitelist](serverless/configs/resources/waf-ipv4-whitelist.yml)
    - [API Gateway WAF Association](serverless/configs/resources/api-gateway-waf-association.yml)
- S3 Bucket resources
    - [S3 Bucket](serverless/configs/resources/auditing-s3-bucket.yml)
- Cognito resources
    - [Cognito user pool](serverless/configs/resources/cognito-user-pool.yml)
    - [Cognito user pool client](serverless/configs/resources/cognito-user-pool-client.yml)
- Custom Cloudformation resources
    - [API Key to SSM parameter Store](serverless/configs/resources/credit-recommendation-api-key-secret-ssm.yml)
        - This file contains a custom lambda function which fetches all the api keys and inserts it into `AWS System Manager` *parameter store*.
    - [Cognito secret to SSM parameter Store](serverless/configs/resources/credit-recommendation-user-client-secret-ssm.yml)
        - This file contains a lambda function which saves the customer's cognito credentials which is used to acquire the access_token

## Deployment

1. Execute below command by going to the folder where `package.json` resides and then install below node dependencies from
   terminal.

```
npm install -g serverless serverless-offline serverless-prune-plugin serverless-plugin-existing-s3 serverless-latest-layer-version serverless-python-requirements serverless-deployment-bucket
```

- execute below command to install project dependencies

```
npm install
```

2. Execute below command inside terminal by going inside the directory having `serverless.yml`
   file to deploy the service in aws cloud.

```
sls deploy --verbose --stage=<environment-name>
```

> #### Serverless.com framework is used as an infrastructure tool to create and deploy the resources on aws cloud

> #### Note in order to execute the above command you should have aws cli installed on your machine and aws client_id and client_secret configured along with the aws region that you want to deploy the resources in.

## References

- [Serverless framework documentation](https://www.serverless.com/framework/docs)
- [Serverless resources deployment](https://www.serverless.com/framework/docs/providers/aws/guide/deploying)
- [AWS Cloudformation lambda backed custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources-lambda.html)
- [AWS cloudformation resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html)