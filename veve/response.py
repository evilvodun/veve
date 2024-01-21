class Response:
    @staticmethod
    def ok(data) -> dict:
        return {'status': 'success', 'message': data}

    @staticmethod
    def error(data) -> dict:
        return {'status': 'error', 'message': data}
