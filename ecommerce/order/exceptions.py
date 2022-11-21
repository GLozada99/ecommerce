from ecommerce.core.exceptions import BusinessException


class NoEmployeeAvailableException(BusinessException):
    def __init__(
            self,
            message: str = 'There is no employee available to take the '
                           'order, create new employees or remove some '
                           'mails from EMAILS_NOT_ALLOWED'):
        self.message = message
        super().__init__(self.message)
