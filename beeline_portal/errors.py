class BaseBeelinePBXException(Exception):
    def __init__(self, response: dict):
        self.error_code = response.get('errorCode', 500)
        self.description = response.get('description', 'Server error')
        super(BaseBeelinePBXException, self).__init__(response)


class BeelinePBXException(BaseBeelinePBXException):
    pass
