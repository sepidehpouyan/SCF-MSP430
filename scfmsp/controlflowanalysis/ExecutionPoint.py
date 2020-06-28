class ExecutionPoint:
    def __init__(self, function, address, caller=None):
        self.function = function
        self.address = address
        self.caller = caller

        self.addr = 0

        self.__hash_cache = None

    def __unicode__(self):
        return '(%s, %s, %s)' % (self.function, hex(self.address), self.caller)

    def __repr__(self):
        return self.__unicode__()

    def __hash__(self):
        if self.__hash_cache is None:
            to_hash = (self.function, self.address, self.caller)
            self.__hash_cache = hash(to_hash)
        return self.__hash_cache

    def __eq__(self, other):
        return other is not None and self.address == other.address and self.__hash__() == other.__hash__()

    def __add__(self, other):
        return ExecutionPoint(self.function, self.address + other, self.caller) 

    def has_caller(self):
        return self.caller is not None

    def forward(self, count):
        return  self + count
