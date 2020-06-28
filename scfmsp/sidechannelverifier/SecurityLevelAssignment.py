from scfmsp.sidechannelverifier.SecurityLevel import SecurityLevel


class SecurityLevelAssignment:
    
    def __init__(self, default=SecurityLevel.LOW):
        self.default = default
        self.modified = False
        self.map = {}
        
    def get(self, key):
        return self.map.get(key, self.default)

    def set(self, key, val):
        if self.get(key) != val:
            self.modified = True
            self.map.update({
                key: val,
            })

    def is_modified(self):
        return self.modified

    def reset(self): 
        self.modified = False

    def __le__(self, other):
        if not (self.default <= other.default):
            return False

        for key in self.map.keys():
            if not (self.get(key) <= other.get(key)):
                return False
        return True

    def __and__(self, other):
        ret = SecurityLevelAssignment(self.default & other.default)

        for key in self.map.keys():
            ret.set(key, self.get(key) & other.get(key))
        for key in other.map.keys():
            ret.set(key, self.get(key) & other.get(key))

        return ret

    @staticmethod
    def bottom():
        return SecurityLevelAssignment(SecurityLevel.LOW)

    @staticmethod
    def top():
        return SecurityLevelAssignment(SecurityLevel.HIGH)
