from scfmsp.controlflowanalysis.StatusRegister import StatusRegister
from scfmsp.controlflowanalysis.instructions.AbstractInstructionBranching import AbstractInstructionBranching


class InstructionJn(AbstractInstructionBranching):
    name = 'jn'

    def get_execution_time(self):
        return 2

    def get_branching_condition_domain(self, ac):
        return ac.sra.get(StatusRegister.Negative)