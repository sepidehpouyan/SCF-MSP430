from scfmsp.controlflowanalysis.instructions.AbstractInstructionTwoRegisters import AbstractInstructionTwoRegisters


class InstructionBic(AbstractInstructionTwoRegisters):
    name = 'bic'

    def get_execution_time(self):
        return self.clock

    def execute_judgment(self, ac):
        super(InstructionBic, self).execute_judgment(ac)