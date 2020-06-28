from scfmsp.sidechannelverifier.SecurityLevel import SecurityLevel
from scfmsp.sidechannelverifier.SecurityLevelAssignment import SecurityLevelAssignment

class AssignmentCollection:
    def __init__(self, secenv, stack, ra, sra, mem):
        self.secenv = secenv
        self.stack = stack
        self.ra = ra
        self.sra = sra
        self.mem = mem

    def getKey(self, arg):
        key = arg
        return key

    def is_modified(self):
        return self.secenv.is_modified() | self.ra.is_modified() | self.sra.is_modified() #| self.mem.is_modified()

    def reset(self):
        self.secenv.reset()
        self.ra.reset()
        self.sra.reset()
        #self.mem.reset()

    def __and__(self, other):
        secenv = self.secenv & other.secenv
        ra = self.ra & other.ra
        sra = self.sra & other.sra
        mem = self.mem & other.mem

        # Handle stack
        stack = []
        min_len = min(len(self.stack), len(other.stack))
        for i in range(0, min_len):
            stack.append(self.stack[i] & other.stack[i])
        if len(self.stack) == min_len:
            stack.extend(other.stack[min_len:])
        else:
            stack.extend(self.stack[min_len:])

        return AssignmentCollection(secenv, stack, ra, sra, mem)

    def __le__(self, other):
        
        return \
            (self.ra <= other.ra) &\
            (self.sra <= other.sra) &\
            (self.mem <= other.mem)

    @staticmethod
    def bottom():
        
        return AssignmentCollection(
            SecurityLevelAssignment.bottom(),
            [],
            SecurityLevelAssignment.bottom(),
            SecurityLevelAssignment.bottom(),
            SecurityLevel.LOW
        )

    @staticmethod
    def top():
    
        return AssignmentCollection(
            SecurityLevelAssignment.top(),
            [],
            SecurityLevelAssignment.top(),
            SecurityLevelAssignment.top(),
            SecurityLevel.HIGH
        )
