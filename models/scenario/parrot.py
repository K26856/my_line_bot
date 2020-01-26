class Parrot :
    def __init__(self) :
        pass

    def response(self, params):
        """
        """
        response_message = '{}ってなに？'.format(params.message)
        return response_message

