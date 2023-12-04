class Trusteeship:
    __clients = []
    __methodName = None

    def register(self, client):
        if isinstance(client,list):
            self.__clients += client
        else:
            self.__clients.append(client)

    def __execute(self, *args, **kwargs):
         for logger in self.__clients:
            method = getattr(logger, self.__methodName, None)
            if method:
                method(*args, **kwargs)

    def __getattr__(self, attr):
        self.__methodName = attr
        return self.__execute

trusteeship = Trusteeship()