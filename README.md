# Credit Recommendation Parquet Service

## Table of Contents

- [Introduction](#introduction)
- [Working](#working)
- [Process to generate access token](#generate-access-token)
- [Deployment](#deployment)
- [References](#references)

## Introduction

- #### Credit Recommendation Audit Workflow Diagram

![credit recommendation audit workflow](credit-recommendation-audit-workflow.png)

- This service is created with the goal of centralizing the conversion of json data into parquet data.
- The caller service just have to send the data, which is an array of a json object and config(containing the location and partition data).
- This service automatically groups the data based on customers' name and saves it into specified s3 bucket.
- While saving the data, it also updates the Athena data catalog so that the latest data are available for querying.

## Generate-access-token

### Please follow below steps to generate access token

1. Create a new request in **Postman** and change the http method type to `POST`
2. Insert `https://dev-auth.virtualb.cloud/oauth2/token` in the url section
3. Go to **body** and select `x-www-form-urlencoded`
4. Insert below keys and values in the body
    - *key* : `grant_type`, *value* : `client_credentials`
    - *key* : `scope`, *value* : `prob/write`
5. Insert below key and value in header
    - *key* : `Authorization`, *value* : `Basic Base64Encode(client_id:client_secret)`
        - **Note**: <br />
          you have to get the client_id and client_secret, and then you have to perform base64encode on *<client_id>:<client_secret>*
6. And finally send the request

## Working

- In order to call the service, the user/client has to send the request at `https://<env>.api.virtualb.cloud/parquet` endpoint with `POST` httpMethod.
- Since this service is protected by cognito authorizer, the user/client has to obtain the access_token as explained [here](#generate-access-token)
- The `access_token` obtained from above step needs to go as part of `Authorization` header as
  bearer token.
    - `Authorization` : `Bearer <access_token>`
- user/client also need to provide `x-api-key` as part of the header.
- As part of the body user needs to send the data in a below format

```
{                                                             
  "data": [[json object],[json object]],
  "config": {
     "auditing_bucket_path": "<replace_bucket_name>",
     "auditing_database": "<replace_athena_database_name>",
     "auditing_table_name": "<replace_athena_table_name>,
     "auditing_path": "<replace_bucket_auditing_prefix_name>,
     "partition_columns": [<list_of_partitons_columns>], // eg. ["customer","year","month","day","hour"]
     "partition_data": [value of partiton patitions colums data], // eg ["scindo","2022","11","25","13"]
     "date_columns": [<list_of_date_columns>] //eg ['creationDate']
   }
}
```

- After hitting the endpoint, if the above data are valid, then this endpoint will return the below response.

```
{
  "paths": [
    "s3://bucket_name/auditing/customer=scindo/year=2022/month=11/day=25/hour=13/c84559a7128948e8b0fe528d88193ce8.snappy.parquet"
  ],
  "partitions_values": {
    "s3://bucket_name/auditing/customer=scindo/year=2022/month=11/day=25/hour=13/": [
      "scindo",
      "2022",
      "11",
      "25",
      "13"
    ]
  }
}
```

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
- [Serverless functions](https://www.serverless.com/framework/docs/providers/aws/guide/functions)
- [Serverless resources deployment](https://www.serverless.com/framework/docs/providers/aws/guide/deploying)
- [Cognito Oauth2 client credential flow](https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html)
- [AWS Supported Ouath2 flows](https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-user-pool-oauth-2-0-grants/)
- [Generate access token](https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html)
