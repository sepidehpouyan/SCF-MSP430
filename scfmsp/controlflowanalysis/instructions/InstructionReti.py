from scfmsp.controlflowanalysis.AbstractInstruction import AbstractInstruction


class InstructionReti(AbstractInstruction):
    name = 'reti'

    def get_execution_time(self):
        return 5

    def get_successors(self):
        if self.get_execution_point().has_caller():
            return [self.get_execution_point().caller]
        else:
            return []

    def execute_judgment(self, ac):
        pass