class Response:
    @staticmethod
    def ok(data):
        return {'status': 'success', 'message': data}

    @staticmethod
    def error(data):
        return {'status': 'error', 'message': data}
