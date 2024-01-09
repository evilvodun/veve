class Response:
    @staticmethod
    def ok(data):
        return {'status': True, 'message': data}

    @staticmethod
    def error(data):
        return {'status': False, 'message': data}
