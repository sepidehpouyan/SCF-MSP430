from scfmsp.controlflowanalysis.StackPointer import StackPointer
from scfmsp.controlflowanalysis.AbstractInstruction import AbstractInstruction


class InstructionPush(AbstractInstruction):
    name = 'push'

    def get_execution_time(self):
        oplist = self.oplist.split()
        if(self.register_mode):
            return 3

        if(self.indexed_mode):
            if(oplist[0][1] == '3'): # constant generator -----------------
                return 3
            else:
                return 5

        if(self.indirect_mode):
            if(oplist[0][1] == '2' or oplist[0][1] == '3'):
                return 3
            else:
                return 4

        if(self.immediate_mode):
           if (oplist[0][1] == '0'):
               return 4
           else:
               if(oplist[0][1] == '2' or oplist[0][1] == '3'):
                   return 3
               else:
                   return 5

    def execute_judgment(self, ac):
        if(self.register_mode):
            ac.stack.append(ac.ra.get(self.arguments[0]) & ac.secenv.get(self.get_execution_point()))

        if(self.indexed_mode or self.indirect_mode):
            ac.stack.append(ac.mem & ac.secenv.get(self.get_execution_point()))
            
        if(self.immediate_mode):
            if (self.oplist[0][1] == '0'):
                ac.stack.append(ac.secenv.get(self.get_execution_point()))
            else:
                ac.stack.append(ac.mem & ac.secenv.get(self.get_execution_point()))

        sp_domain = ac.ra.get(StackPointer.SP)& ac.secenv.get(self.get_execution_point())
        ac.ra.set(StackPointer.SP, sp_domain)