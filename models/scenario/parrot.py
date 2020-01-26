class Parrot :
    def __init__(self) :
        pass

    def response(self, params):
        """
        """
        print(self.__class__)
        print(params.__class__)
        print(params.keys())
        response_message = '{}ってなに？'.format(params['message'])
        return response_message

