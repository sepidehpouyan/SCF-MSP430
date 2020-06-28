from scfmsp.controlflowanalysis.instructions.AbstractInstructionTwoRegisters import AbstractInstructionTwoRegisters


class InstructionBis(AbstractInstructionTwoRegisters):
    name = 'bis'

    def get_execution_time(self):
        return self.clock

    def execute_judgment(self, ac):
        super(InstructionBis, self).execute_judgment(ac)