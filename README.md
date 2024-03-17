# Credit Recommendation Layers

## Table of Contents

- [Introduction](#introduction)
- [Working](#working)
- [Deployment](#deployment)
- [References](#references)

## Introduction

- This repository is creating a layer that has aws-wrangler dependency.
- Since aws wrangler dependency is used in multiple service, i.e. **credit-recommendation-parquet-service** and
  **credit-recommendation-parquet-merger-service** so instead of replicating the same code in multiple lambda functions, a layer is created and is
  used
  in multiple lambda function.

## Working

- users just need to import the output of this stack as shown below where this dependency is required.

```
  layers:
    - !ImportValue sls-credit-recommendation-layers-${opt:stage}-PythonHandlerLambdaLayerQualifiedArn
```

## Deployment

1. The dependency is zipped into `layers.zip` file as per aws documentation for creating python layer.
   Reference for creating a layer is attached in the reference section of this document.

2. Execute below command by going to the folder where `package.json` resides and then install below node dependencies from
   terminal.

```
npm install -g serverless serverless-offline serverless-prune-plugin serverless-plugin-existing-s3 serverless-latest-layer-version serverless-python-requirements serverless-deployment-bucket
```

- execute below command to install project dependencies

```
npm install
```

3. Execute below command inside terminal by going inside the directory having `serverless.yml`
   file to deploy the service in aws cloud.

```
sls deploy --verbose --stage=<environment-name>
```

> #### Serverless.com framework is used as an infrastructure tool to create and deploy the resources on aws cloud

> #### Note in order to execute the above command you should have aws cli installed on your machine and aws client_id and client_secret configured along with the aws region that you want to deploy the resources in.

## References

- [Serverless framework documentation](https://www.serverless.com/framework/docs)
- [Serverless layers](https://www.serverless.com/framework/docs/providers/aws/guide/layers)
- [Serverless resources deployment](https://www.serverless.com/framework/docs/providers/aws/guide/deploying)
- [Aws Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)