from scfmsp.controlflowanalysis.instructions.AbstractInstructionTwoRegisters import AbstractInstructionTwoRegisters
from scfmsp.controlflowanalysis.ExecutionPoint import ExecutionPoint
from scfmsp.sidechannelverifier.SecurityLevel import SecurityLevel


class InstructionMov(AbstractInstructionTwoRegisters):
    name = 'mov'

    def get_successors(self):
        oplist = self.oplist.split()
        if(oplist[0][0] == '3' and oplist[0][1] == '0' and oplist[0][2] == '4' and oplist[0][3] == '1'): # ret
            if self.get_execution_point().has_caller():
                return [self.get_execution_point().caller]
            else:
                return []

        elif(oplist[0][0] == '3' and oplist[0][1] == '0' and oplist[0][2] == '4' and oplist[0][3] == '0'): # br
            hex_addr =  oplist[0][6] + oplist[0][7] + oplist[0][4] + oplist[0][5]
            br_target = int(hex_addr, 16)
            target = ExecutionPoint(self.function.name, br_target, self.function.caller)
            return [target,]
            
        else:
            return [self.get_execution_point().forward(self.length*2)]
    
    def get_execution_time(self):
        return self.clock

    def execute_judgment(self, ac):
        if(self.register_mode and self.dst_register_mode):
            ac.ra.set(self.arguments[1], ac.ra.get(self.arguments[0]) & ac.secenv.get(self.get_execution_point()))
        
        if(self.register_mode and self.dst_indexed_mode):
            if(ac.mem == SecurityLevel.LOW):
                ac.mem = ac.ra.get(self.arguments[0]) & ac.secenv.get(self.get_execution_point())

        if((self.indexed_mode or self.indirect_mode) and self.dst_register_mode):
            if(ac.ra.get(self.arguments[0]) == SecurityLevel.HIGH):
                ac.mem = ac.ra.get(self.arguments[0])
            ac.ra.set(self.arguments[1], ac.mem & ac.secenv.get(self.get_execution_point()))

        if((self.indexed_mode or self.indirect_mode) and self.dst_indexed_mode):
            ac.mem = ac.mem & ac.secenv.get(self.get_execution_point()) 

        if(self.immediate_mode and self.dst_register_mode):
            ac.ra.set(self.arguments[1], ac.secenv.get(self.get_execution_point()))

        if(self.immediate_mode and self.dst_indexed_mode):
            ac.mem = ac.secenv.get(self.get_execution_point())