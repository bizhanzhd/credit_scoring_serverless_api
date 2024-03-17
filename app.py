import datetime
import json

from AuditLogger import AuditLogBuilder
from scindo_input_controller import Input_controller
from scindo_output_estimator import Default_estimator


def handler(event, context):
    # started audit log
    audit_log = AuditLogBuilder()
    start_date_time = datetime.datetime.now()
    audit_log.with_customer("scindo").with_request_id(context.aws_request_id).with_status('STARTED').with_start_date_time(start_date_time).build()

    controller = Input_controller()
    estimator = Default_estimator()

    received_body = event['body']

    if type(received_body) is str:
        body = json.loads(received_body)
    else:
        body = received_body

    # call the controller
    result = controller.run(body)
    if result["flag"] == True:
        completed_date_time = datetime.datetime.now()
        audit_log.with_status('FAILED').with_error_message(result["response"]).with_completed_date_time(
            completed_date_time).with_processing_time_in_milliseconds(
            (completed_date_time - start_date_time).total_seconds() * 1000).build()

        return {
            "statusCode": result['response_code'],
            'body': json.dumps({'err_message': result["response"]})
        }

    # Call the calculator
    try:
        estimate = estimator.run(data=body)
        print(estimate)
    except Exception as ex:
        print('error occurred while running estimator with error :: {}'.format(ex))
        completed_date_time = datetime.datetime.now()
        audit_log.with_status('FAILED').with_error_message(result["response"]).with_completed_date_time(
            completed_date_time).with_processing_time_in_milliseconds(
            (completed_date_time - start_date_time).total_seconds() * 1000).build()

        return {
            "statusCode": 500,
            'body': json.dumps({'err_message': "Internal error"})
        }
    
    else:
        print('returning the response')

    response = {
        "statusCode": result['response_code'],
        'body': json.dumps({'estimate': estimate})
    }

    # Completed audit logs
    completed_date_time = datetime.datetime.now()
    audit_log.with_status('COMPLETED').with_completed_date_time(completed_date_time).with_response(response).with_processing_time_in_milliseconds(
        (completed_date_time - start_date_time).total_seconds() * 1000).build()

    return response
