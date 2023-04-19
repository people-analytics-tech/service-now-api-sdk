from people_analytics_itsm_sdk.exceptions import ITSMException


class QueryTypeError(ITSMException):
    pass


class QueryMissingField(ITSMException):
    pass


class QueryEmpty(ITSMException):
    pass


class QueryExpressionError(ITSMException):
    pass


class QueryMultipleExpressions(ITSMException):
    pass


class RecordFilterException(ITSMException):
    pass


class RecordRetriesException(ITSMException):
    pass


class ManagerRetriveException(ITSMException):
    pass


class ManagerCreateException(ITSMException):
    pass


class ManagerDeleteException(ITSMException):
    pass


class ManagerFullUpdateException(ITSMException):
    pass


class ManagerUpdateException(ITSMException):
    pass


class ProducerSubmitException(ITSMException):
    pass
