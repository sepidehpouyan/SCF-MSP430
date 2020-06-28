from scfmsp.controlflowanalysis.AbstractInstruction import AbstractInstruction
from scfmsp.controlflowanalysis.StatusRegister import StatusRegister


class InstructionRrc(AbstractInstruction):
    name = 'rrc'

    def get_execution_time(self):
        oplist = self.oplist.split()
        if(self.register_mode):
            return 1

        if(self.indexed_mode):
            if(oplist[0][1] == '3'): # constant generator -----------------
                return 1
            else:
                return 4

        if(self.indirect_mode or self.immediate_mode):
            if(oplist[0][1] == '2' or oplist[0][1] == '3'):
                return 1
            else:
                return 3

    def execute_judgment(self, ac):
        if(self.register_mode):
            domain = ac.ra.get(self.arguments[0]) & ac.secenv.get(self.get_execution_point()) & ac.sra.get(StatusRegister.CARRY)
            ac.ra.set(self.arguments[0], domain)
        
        else:
            domain = ac.mem & ac.secenv.get(self.get_execution_point()) & ac.sra.get(StatusRegister.CARRY)
            ac.mem = domain
            
        ac.sra.set(StatusRegister.CARRY, domain)
        ac.sra.set(StatusRegister.ZERO, domain)
        ac.sra.set(StatusRegister.Negative, domain)
        ac.sra.set(StatusRegister.Overflow, domain)