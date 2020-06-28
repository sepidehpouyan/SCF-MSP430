class RegionComputation:
   
    def __init__(self, program, region_then, region_else, nemesis_region_then, nemesis_region_else):
        self.program = program
        self.region_then = region_then
        self.region_else = region_else
        self.nemesis_region_then = nemesis_region_then
        self.nemesis_region_else = nemesis_region_else
        self.missing_then = []
        self.missing_else = []
        self.nemesis_missing_then = []
        self.nemesis_missing_else = []

    def start_computation(self, instruction):
        successors = instruction.get_successors_checked()
        self.missing_else.append(successors[0])
        self.missing_then.append(successors[1])
        self.nemesis_missing_else.append(successors[0])
        self.nemesis_missing_then.append(successors[1])

        junction1 = self.__compute(self.missing_then, self.nemesis_missing_then, self.region_then, self.nemesis_region_then, instruction)
        junction2 = self.__compute(self.missing_else, self.nemesis_missing_else, self.region_else, self.nemesis_region_else, instruction)

        return junction1 or junction2

    def __compute(self, missing, nemesis_missing, region, nemesis_region, instruction):
        junction = None
        while len(missing) > 0:
            first_eps = missing.pop(0)
            if first_eps != instruction.immediate_post_dominator and first_eps not in region:
                region.add(first_eps)
                missing.extend(self.program.get_instruction_at_execution_point(first_eps).get_successors_checked())
            elif first_eps == instruction.immediate_post_dominator:
                junction = first_eps

        while len(nemesis_missing) > 0:
            first_eps = nemesis_missing.pop(0)
            if first_eps != instruction.immediate_post_dominator and first_eps not in nemesis_region:
                nemesis_region.append(first_eps)
                successors = self.program.get_instruction_at_execution_point(first_eps).get_successors_checked()
                if len(successors) != 0:
                    nemesis_missing.append(successors[0])

        return junction
