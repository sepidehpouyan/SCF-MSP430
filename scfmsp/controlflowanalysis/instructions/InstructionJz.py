from scfmsp.controlflowanalysis.StatusRegister import StatusRegister
from scfmsp.controlflowanalysis.instructions.AbstractInstructionBranching import AbstractInstructionBranching


class InstructionJz(AbstractInstructionBranching):
    name = 'jz'

    def get_execution_time(self):
        return 2

    def get_branching_condition_domain(self, ac):
        return ac.sra.get(StatusRegister.ZERO)