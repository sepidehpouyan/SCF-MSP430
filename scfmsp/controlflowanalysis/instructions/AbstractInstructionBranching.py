from scfmsp.sidechannelverifier.SecurityLevel import SecurityLevel
from scfmsp.sidechannelverifier.exceptions.BranchtimeDiffersException import BranchtimeDiffersException
from scfmsp.sidechannelverifier.exceptions.LoopOnHighConditionException import LoopOnHighConditionException
from scfmsp.sidechannelverifier.exceptions.NemisisOnHighConditionException import NemisisOnHighConditionException

from scfmsp.controlflowanalysis.RegionComputation import RegionComputation
from scfmsp.controlflowanalysis.instructions.AbstractInstructionControlFlow import AbstractInstructionControlFlow


class AbstractInstructionBranching(AbstractInstructionControlFlow):
    def __init__(self, function):
        super(AbstractInstructionBranching, self).__init__(function)
        self.regions_computed = False
        self.region_then = []
        self.region_else = []
        self.nemesis_region_then = []
        self.nemesis_region_else = []
        self.junction = None
        self.then_number = 0
        self.else_number = 0

    def get_successors(self):
        ret = super(AbstractInstructionBranching, self).get_successors()
        ret.append(self.get_branch_target())
        return ret

    def compute_regions(self):
        self.region_then = set()
        self.region_else = set()
        self.nemesis_region_then = []
        self.nemesis_region_else = []
        computation = RegionComputation(self.program, self.region_then, self.region_else, self.nemesis_region_then, self.nemesis_region_else)
        self.junction = computation.start_computation(self)

    def get_region_then(self):
        if not self.regions_computed:
            self.compute_regions()
            self.regions_computed = True
        
        return self.region_then

    def get_region_else(self):
        if not self.regions_computed:
            self.compute_regions()
            self.regions_computed = True
        
        return self.region_else

    def get_junction(self):
        if not self.regions_computed:
            self.compute_regions()
            self.regions_computed = True

        return self.junction

    def compare_region(self):
        for ep_then , ep_else in zip(self.nemesis_region_then, self.nemesis_region_else):
            instr_then = self.program.get_instruction_at_execution_point(ep_then)
            instr_else = self.program.get_instruction_at_execution_point(ep_else)
            if(instr_then.get_execution_time() != instr_else.get_execution_time()):
                return True
        return False

    def have_nemesis(self):
        nemesis = True
        if(len(self.nemesis_region_then) == len(self.nemesis_region_else)):
            nemesis = self.compare_region()
        return nemesis

    def is_loop(self):
        return self.immediate_dominator in self.get_region_else() or self.immediate_dominator in self.get_region_then()


    def get_branching_condition_domain(self, ac):
        pass

    def execute_judgment(self, ac):
        if (self.get_branching_condition_domain(ac) & ac.secenv.get(self.get_execution_point())) == SecurityLevel.LOW:
            return
      
        for ep in self.get_region_then():
            ac.secenv.set(ep, SecurityLevel.HIGH)
        for ep in self.get_region_else():
            ac.secenv.set(ep, SecurityLevel.HIGH)

        ac.stack = [SecurityLevel.HIGH for _ in range(len(ac.stack))]

        if self.is_loop():
            raise LoopOnHighConditionException()
        
        if self.have_nemesis():
            raise NemisisOnHighConditionException()

        if not self.is_loop():
            if not (self.get_branchtime_then() == self.get_branchtime_else()):
                raise BranchtimeDiffersException()