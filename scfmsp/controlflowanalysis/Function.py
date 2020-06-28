from scfmsp.controlflowanalysis.InstructionFactory import InstructionFactory

class Function:
    def __init__(self, name, program, file, caller=None):
        self.name = name
        self.program = program
        self.caller = caller

        self.file = file

        self.instructions = {}
        self.first_instruction = None

    def add_instruction(self, instruction):
        if self.first_instruction is None:
            self.first_instruction = instruction

        self.instructions.update({
            instruction.get_execution_point(): instruction
        })

    def get_for_caller(self, caller):
        caller_func = Function(self.name, self.program, self.file, caller)
        for instr in self.instructions.values():
            caller_func.add_instruction(InstructionFactory.copy_instruction(instr, caller_func))
        first_instr_copy = InstructionFactory.copy_instruction(self.first_instruction, caller_func)
        caller_func.add_instruction(first_instr_copy)
        caller_func.first_instruction = first_instr_copy
        
        return caller_func