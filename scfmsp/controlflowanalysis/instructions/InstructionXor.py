from scfmsp.controlflowanalysis.instructions.AbstractInstructionTwoRegisters import AbstractInstructionTwoRegisters
from scfmsp.sidechannelverifier.SecurityLevel import SecurityLevel


class InstructionXor(AbstractInstructionTwoRegisters):
    name = 'xor'

    def get_execution_time(self):
        return self.clock

    def execute_judgment(self, ac):
        super(InstructionXor, self).execute_judgment(ac)
        self._execute_judgment_carry(ac)
        self._execute_judgment_zero(ac)
        self._execute_judgment_negative(ac)
        self._execute_judgment_overflow(ac)