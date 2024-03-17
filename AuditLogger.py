from abc import ABCMeta, abstractmethod


class IBuilder(metaclass=ABCMeta):
    "Audit Logger Builder Interface"

    @staticmethod
    @abstractmethod
    def with_request_id(self, request_id):
        "aws request_id"

    @staticmethod
    @abstractmethod
    def with_response(self, response):
        "response"

    @staticmethod
    @abstractmethod
    def with_status(self, status):
        "status STARTED/SUCCESS/FAILED"

    @staticmethod
    @abstractmethod
    def with_customer(self, customer):
        "customer name"

    @staticmethod
    @abstractmethod
    def with_start_date_time(self, start_date_time):
        "start date time"

    @staticmethod
    @abstractmethod
    def with_completed_date_time(self, completed_date_time):
        "completed date time"

    @staticmethod
    @abstractmethod
    def with_error_message(self, error_message):
        "error message"

    @staticmethod
    @abstractmethod
    def with_processing_time_in_milliseconds(self, processing_time_in_milliseconds):
        "total processing time"

    @staticmethod
    @abstractmethod
    def build(self):
        "Return the audit logger object"


class AuditLogBuilder(IBuilder):
    "The Concrete Builder."

    def __init__(self):
        self.auditLog = AuditLog()

    def with_response(self, response):
        self.auditLog.response = response
        return self

    def with_request_id(self, request_id):
        self.auditLog.request_id = request_id
        return self

    def with_status(self, status):
        self.auditLog.status = status
        return self

    def with_start_date_time(self, start_date_time):
        self.auditLog.start_date_time = start_date_time
        return self

    def with_completed_date_time(self, completed_date_time):
        self.auditLog.completed_date_time = completed_date_time
        return self

    def with_error_message(self, error_message):
        self.auditLog.error_message = error_message
        return self

    def with_customer(self, customer):
        self.auditLog.customer = customer
        return self

    def with_processing_time_in_milliseconds(self, processing_time_in_milliseconds):
        self.auditLog.processing_time_in_milliseconds = processing_time_in_milliseconds
        return self

    def build(self):
        response = {'type': self.auditLog.logType, 'status': self.auditLog.status, 'request_id': self.auditLog.request_id}

        if self.auditLog.customer:
            response['customer'] = self.auditLog.customer
        if self.auditLog.response:
            response['response'] = str(self.auditLog.response)
        if self.auditLog.start_date_time:
            response['start_date_time'] = str(self.auditLog.start_date_time)
        if self.auditLog.completed_date_time:
            response['completed_date_time'] = str(self.auditLog.completed_date_time)
        if self.auditLog.error_message:
            response['error_message'] = self.auditLog.error_message
        if self.auditLog.processing_time_in_milliseconds:
            response['processing_time_in_milliseconds'] = self.auditLog.processing_time_in_milliseconds
        print(response)


class AuditLog():

    def __init__(self):
        self.logType = 'AUDITING'
        self.request_id = None
        self.status = None
        self.start_date_time = None
        self.completed_date_time = None
        self.error_message = None
        self.processing_time_in_milliseconds = None
        self.response = None
        self.customer = None
