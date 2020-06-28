from scfmsp.controlflowanalysis.instructions.AbstractInstructionControlFlow import AbstractInstructionControlFlow


class InstructionJmp(AbstractInstructionControlFlow):
    name = 'jmp'

    def get_execution_time(self):
        return 2

    def get_successors(self):
        return [self.get_branch_target()]

    def execute_judgment(self, ac):
        pass