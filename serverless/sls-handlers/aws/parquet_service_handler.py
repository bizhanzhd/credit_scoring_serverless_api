import json
import logging
import traceback

import awswrangler as wr
import pandas as pd

pd.options.mode.chained_assignment = None


def handle(event, context):
    try:
        print('request received')
        parquet_obj = ParquetAPI(event, context)
        print('calling process')
        response = parquet_obj.process()
        print(f'returning response ${response}')
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
            'body': json.dumps(response)
        }
    except Exception as e:
        logging.info('Closing lambda function')
        logging.error(e)
        return {
            'statusCode': 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,code,code_verfier,applicationid",
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Credentials": False,
                "Access-Control-Allow-Origin": "*",
                "X-Requested-With": "*"
            },
            'body': json.dumps('Error calling Parquet API')
        }


class ParquetAPI:
    def __init__(self, event, context):
        self.body = Utils.parse_json(event['body'])
        self.data = Utils.parse_json(self.body['data'])
        self.config = Utils.parse_json(self.body['config'])

    def process(self):
        try:
            print('inside process method of the service')
            df_metrics_list = []

            print("converting record into dataframe")
            for record in self.data:
                parsed_record = Utils.parse_json(record)
                from_dict = pd.DataFrame(parsed_record, index=[0])
                df_metrics_list.append(from_dict)

            print("merging all the dataframe")
            df_metrics = pd.concat(df_metrics_list)

            # setting the date format
            date_columns = self.config['date_columns']
            for element in range(len(date_columns)):
                if date_columns[element] in df_metrics.columns:
                    df_metrics[date_columns[element]] = pd.to_datetime(df_metrics[date_columns[element]], format="%Y-%m-%d %H:%M:%S")
                else:
                    print('columns "{}" not present in data frame.'.format(date_columns[element]))
            df_metrics = df_metrics.convert_dtypes()

            columns_ = self.config['partition_columns']
            columns_data = self.config['partition_data']
            for element in range(len(columns_)):
                df_metrics[columns_[element]] = columns_data[element]

            file_path = f"{self.config['auditing_bucket_path']}/{self.config['auditing_path']}"
            print(f"saving the converted record into parquet format in bucket ${file_path}")
            return Wrangler(df_metrics, file_path, self.config['auditing_database'],
                            self.config['auditing_table_name'], self.config['partition_columns']).write_parquet()
        except Exception as e:
            print("'error 00::'", traceback.print_exc(), e)
            raise e


class Utils:
    def parse_json(element):
        try:
            return json.loads(element)
        except Exception as e:
            return element


class Wrangler:
    def __init__(self, df, path, db_name, table_name, partition_cols):
        self.df = df
        self.path = path
        self.db_name = db_name
        self.table_name = table_name
        self.partition_cols = partition_cols

    def write_parquet(self):
        response = wr.s3.to_parquet(df=self.df, path=self.path, dataset=True, mode="append", database=self.db_name, table=self.table_name,
                                    partition_cols=self.partition_cols)
        print("parquet file saved successfully.")
        return response
