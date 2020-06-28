from enum import Enum


class SecurityLevel(Enum):
    LOW = False
    HIGH = True

    def __le__(self, other):
        return not (self.value & (not other.value))

    def __and__(self, other):
        return SecurityLevel(self.value | other.value)
