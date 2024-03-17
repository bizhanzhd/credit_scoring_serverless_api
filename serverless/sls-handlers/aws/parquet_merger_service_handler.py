import datetime
import json
import os

import awswrangler as wr
import boto3

METRICS_BASE_PATH = os.environ["AUDITING_PATH"].strip()
BUCKET_NAME = os.environ["AUDITING_BUCKET"].strip()
WORKLOAD_METRICS_DATABASE = os.environ["AUDITING_DATABASE"].strip()
WORKLOAD_METRICS_TABLE_NAME = os.environ["AUDITING_TABLE_NAME"].strip()
BACK_DAYS = os.environ["BACK_DAYS"]


def handle(event, context):
    try:
        print("metrics base path::", METRICS_BASE_PATH)
        print("BUCKET NAME::", BUCKET_NAME)
        s3_client = boto3.client("s3")
        mydate = datetime.datetime.now()
        yesterday_date = mydate.date() - datetime.timedelta(days=int(BACK_DAYS))
        year = yesterday_date.year
        yesterday_year = f'year={year}'
        month = yesterday_date.month
        yesterday_month = f'month={month}'
        day = yesterday_date.day
        yesterday = f'day={day}'
        bucket = boto3.resource('s3').Bucket(BUCKET_NAME)
        result = bucket.meta.client.list_objects(Bucket=bucket.name, Prefix=f'{METRICS_BASE_PATH}/', Delimiter='/')


        if result.get('CommonPrefixes') is not None and len(result.get('CommonPrefixes')) > 0:
            # fetching the list of customer from s3 bucket
            for item in result.get('CommonPrefixes'):
                customer = item.get('Prefix').split('=')[1][:-1]
                customer_partition = f"customer={customer}"

                print(f"fetching the list of files for customer :: {customer}")
                response = s3_client.list_objects_v2(Bucket=BUCKET_NAME,
                                                     Prefix=f"{METRICS_BASE_PATH}/{customer_partition}/{yesterday_year}/{yesterday_month}/{yesterday}")
                files = response.get("Contents")
                file_list = []
                delete_list = []
                if files is not None:
                    for element in files:
                        if not element['Key'].__contains__('hour=25'):
                            file_name = f"s3://{BUCKET_NAME}/{element['Key']}"
                            file_list.append(file_name)
                            file_key = {'Key': element['Key']}
                            delete_list.append(file_key)
                    # print('delete list::', delete_list)
                    if len(file_list) > 0:
                        dfs = wr.s3.read_parquet(path=file_list)
                        # print(dfs)
                        dfs.convert_dtypes()
                        dfs['customer'] = customer
                        dfs['year'] = year
                        dfs['month'] = month
                        dfs['day'] = day
                        dfs['hour'] = 25
                        file_path = f"s3://{BUCKET_NAME}/{METRICS_BASE_PATH}"
                        print(f"writing merged parquet file for customer :: {customer}")
                        update_response = wr.s3.to_parquet(df=dfs, path=file_path, dataset=True, mode="append", database=WORKLOAD_METRICS_DATABASE,
                                                           table=WORKLOAD_METRICS_TABLE_NAME,
                                                           partition_cols=["customer", "year", "month", "day", "hour"])
                        print(f"deleting individual hourly parquet file for customer :: {customer}")
                        delete_response = s3_client.delete_objects(Bucket=BUCKET_NAME, Delete={"Objects": delete_list})
                    else:
                        print(f'No Data Available for customer :: {customer}')
                else:
                    print(f"No Data Available for customer :: {customer}")
        else:
            print(f"no customer available. skipping the merging activity")
        return {
            'statusCode': 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,code,code_verfier,applicationid",
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Credentials": False,
                "Access-Control-Allow-Origin": "*",
                "X-Requested-With": "*"
            },
            'body': json.dumps('Workload Metrics Merger Executed Successfully ')
        }
    except Exception as e:
        raise e
