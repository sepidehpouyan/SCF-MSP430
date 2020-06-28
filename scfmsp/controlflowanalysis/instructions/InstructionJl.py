from scfmsp.controlflowanalysis.StatusRegister import StatusRegister
from scfmsp.controlflowanalysis.instructions.AbstractInstructionBranching import AbstractInstructionBranching


class InstructionJl(AbstractInstructionBranching):
    name = 'jl'

    def get_execution_time(self):
        return self.clock

    def get_branching_condition_domain(self, ac):
        return ac.sra.get(StatusRegister.Negative) & ac.sra.get(StatusRegister.Overflow)