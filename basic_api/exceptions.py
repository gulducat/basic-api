class BasicAPIException(Exception):
    pass


class NoAdapterError(BasicAPIException):
    pass


class NoMethodError(BasicAPIException):
    pass
