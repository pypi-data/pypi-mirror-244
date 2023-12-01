RESPONSE_NOT_RECEIVED_ERROR = 'Response was not received.'
CONFIGURATION_ISSUES_ERROR_MESSAGE = 'Service is not able to serve requests ' \
                                     'due to configuration issues'
TIMEOUT_ERROR_MESSAGE = 'Target service failed to respond'
SYNC_HEADER = 'sync'
APPLICATION_JSON = 'application/json'
RABBIT_DEFAULT_RESPONSE_TIMEOUT = 30

ADD_CONSUMPTION = 'ADD_CONSUMPTION'
GET_CONSUMPTION = 'GET_CONSUMPTION'
DELETE_CONSUMPTION = 'DELETE_CONSUMPTION'

ADD_ADJUSTMENT = 'ADD_ADJUSTMENT'
GET_ADJUSTMENT = 'GET_ADJUSTMENT'
DELETE_ADJUSTMENT = 'DELETE_ADJUSTMENT'

ADD_CONSUMPTION_DETAILS = 'ADD_CONSUMPTION_DETAILS'
GET_CONSUMPTION_DETAILS = 'GET_CONSUMPTION_DETAILS'
DELETE_CONSUMPTION_DETAILS = 'DELETE_CONSUMPTION_DETAILS'

CHECK_TENANT_STATUS = 'CHECK_TENANT_STATUS'
GET_TOTAL_BILLING_REPORT = 'GET_TOTAL_BILLING_REPORT'

PLAIN_CONTENT_TYPE = 'text/plain'
SUCCESS_STATUS = 'SUCCESS'
ERROR_STATUS = 'FAILED'
RESULTS = 'results'
DATA = 'data'


class Queues:
    DEFAULT_MAESTRO_REQUEST_QUEUE = 'DEFAULT_MAESTRO_REQUEST_QUEUE'
    DEFAULT_MAESTRO_RESPONSE_QUEUE = 'DEFAULT_MAESTRO_RESPONSE_QUEUE'

    DEFAULT_ADMIN_REQUEST_QUEUE = 'DEFAULT_ADMIN_REQUEST_QUEUE'
    DEFAULT_ADMIN_RESPONSE_QUEUE = 'DEFAULT_ADMIN_RESPONSE_QUEUE'

    DEFAULT_KPI_REQUEST_QUEUE = 'DEFAULT_KPI_REQUEST_QUEUE'
    DEFAULT_KPI_RESPONSE_QUEUE = 'DEFAULT_KPI_RESPONSE_QUEUE'


class BillingApiActions:
    DESCRIBE_BILLING_MONTH = 'DESCRIBE_BILLING_MONTH'
    DESCRIBE_CURRENCY = 'DESCRIBE_CURRENCY'
    GET_TOP_ACCOUNTS_REPORT = 'GET_TOP_ACCOUNTS_REPORT'
    GET_PRICING_POLICY = 'GET_PRICING_POLICY'
    SEND_PAAS_BILLING_REPORTS = 'SEND_PAAS_BILLING_REPORTS'
    ADD_COST_CENTER = 'ADD_COST_CENTER'
    BILLING_HEALTH_CHECK = 'BILLING_HEALTH_CHECK'
    SEND_COMMAND_EXECUTION_RESULT_REPORT = \
        'SEND_COMMAND_EXECUTION_RESULT_REPORT'
    UPDATE_PRICING_POLICY = 'UPDATE_PRICING_POLICY'
    CHECK_PRICING_POLICY = 'CHECK_PRICING_POLICY'
    CHANGE_TIME_UNIT_TO_PER_SECOND = 'CHANGE_TIME_UNIT_TO_PER_SECOND'
    ARCHIVE_BIG_QUERY = 'ARCHIVE_BIG_QUERY'
    BILLING_HEALTH_CHECK_V2 = 'BILLING_HEALTH_CHECK_V2'
    BILLING_CONFIGURE = 'BILLING_CONFIGURE'


class StatusCodes:
    BAD_REQUEST_400 = 400


class SdkCloud:
    AWS = 'AWS'
    GCP = 'GCP'
    AZURE = 'AZURE'
    GOOGLE = 'GOOGLE'
    OPEN_STACK = 'OPEN_STACK'
