# Credit Recommendation Parquet Merger Service

## Table of Contents

- [Introduction](#introduction)
- [Working](#working)
- [Deployment](#deployment)
- [References](#references)

## Introduction

- #### Credit Recommendation Audit Workflow Diagram

![credit recommendation audit workflow](credit-recommendation-audit-workflow.png)

- This service is used to merge all the small files created by `credit-recommendation-parquet-service` for previous day and creates a single file
  containing all the record.
- It creates the aggregated file for each customer and saves it in following
  partition `/base_path/auditing/customer=scindo/year=2022/month=11/day=25/hour=25`
- Wherever the partition `hour=25` is present it means the merger service has aggregated all the record and saved in this partition.

## Working

- As this function doesn't expose any api endpoint, it cannot be triggered outside the aws cloud.
- This service is triggered based on below cron expression which can be found inside `function.yml` file.
    - [function.yml file](serverless/sls-configs/functions/functions.yml)

```
  events:
    - schedule: cron(0 2 ? * * *)
```

- All the partition column related data that this service requires can be found inside `providers/aws/<env>/env.yml` file
    - [dev env yml file link](serverless/sls-configs/providers/aws/dev/env.yml)

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