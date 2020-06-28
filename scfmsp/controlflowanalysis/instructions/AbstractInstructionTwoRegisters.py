from scfmsp.controlflowanalysis.AbstractInstruction import AbstractInstruction
from scfmsp.controlflowanalysis.StatusRegister import StatusRegister


class AbstractInstructionTwoRegisters(AbstractInstruction):       
    
    def execute_judgment(self, ac):
        rd = self.arguments[1]
        domain = self._get_register_domain(ac)
        if(self.dst_register_mode):
            ac.ra.set(rd, domain)
        else:
            ac.mem = domain

    def _get_register_domain(self, ac):
        
        oplist = self.oplist.split()

        rd = self.arguments[1] # destination
        rr = self.arguments[0] # source

        if(self.register_mode and self.dst_register_mode):
            return ac.ra.get(rd) & ac.ra.get(rr) & ac.secenv.get(self.get_execution_point())

        if(self.register_mode and self.dst_indexed_mode):
            return ac.mem & ac.ra.get(rr) & ac.secenv.get(self.get_execution_point())

        if((self.indexed_mode or self.indirect_mode) and self.dst_register_mode):
            if(oplist[0][3] == '3' or oplist[0][3] == '2'):
                return ac.ra.get(rd) & ac.secenv.get(self.get_execution_point())
            else:
                return ac.ra.get(rd) & ac.mem & ac.secenv.get(self.get_execution_point())

        if((self.indexed_mode or self.indirect_mode) and self.dst_indexed_mode):
           return ac.mem & ac.secenv.get(self.get_execution_point())

        if(self.immediate_mode and self.dst_register_mode):
            if (oplist[0][1] == '0'):
                return ac.ra.get(rd) & ac.secenv.get(self.get_execution_point())  
            else:
                return ac.mem & ac.ra.get(rd) & ac.secenv.get(self.get_execution_point()) 
 
        if(self.immediate_mode and self.dst_indexed_mode):
            return ac.mem & ac.secenv.get(self.get_execution_point())
            

    def _execute_judgment_carry(self, ac):
        domain = self._get_register_domain(ac)
        ac.sra.set(StatusRegister.CARRY, domain)

    def _execute_judgment_zero(self, ac):
        domain = self._get_register_domain(ac)
        ac.sra.set(StatusRegister.ZERO, domain)

    def _execute_judgment_negative(self, ac):
        domain = self._get_register_domain(ac)
        ac.sra.set(StatusRegister.Negative, domain)

    def _execute_judgment_overflow(self, ac):
        domain = self._get_register_domain(ac)
        ac.sra.set(StatusRegister.Overflow, domain)
    
    def _execute_judgment_carry_influence(self, ac):
        rd = self.arguments[1]
        if(self.dst_register_mode):
            ac.ra.set(rd, ac.ra.get(rd) & ac.sra.get(StatusRegister.CARRY) & ac.secenv.get(self.get_execution_point()))
        else:
            ac.mem = ac.mem & ac.sra.get(StatusRegister.CARRY) & ac.secenv.get(self.get_execution_point())
