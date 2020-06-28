from scfmsp.controlflowanalysis.AbstractInstruction import AbstractInstruction
from scfmsp.controlflowanalysis.ExecutionPoint import ExecutionPoint
from scfmsp.controlflowanalysis.instructions.RecursionException import RecursionException
from elftools.elf.elffile import ELFFile

class InstructionCall(AbstractInstruction):
    name = 'call'

    def get_execution_time(self):
        oplist = self.oplist.split()
        if(self.register_mode):
            return 4

        if(self.indexed_mode):
            if(oplist[0][1] == '3'): # constant generator -----------------
                return 4
            else:
                return 5

        if(self.indirect_mode):
            return 4

        if(self.immediate_mode):
            if(oplist[0][1] == '2' or oplist[0][1] == '3'):
                return 4
            else:
                return 5

    def execute_judgment(self, ac):
        pass

    def get_successors(self):
        opList = self.oplist.split()
        hex_addr =  opList[0][6] + opList[0][7] + opList[0][4] + opList[0][5]
        call_target = int(hex_addr, 16)


        elf = ELFFile(open(self.file, 'rb'))
        sym_table_name = self.find_symbol_by_addr(elf, call_target)
        callee_function_name = sym_table_name

        # Check for recursion 
        callers = {self.function.name}
        caller = self.get_execution_point().caller
        while caller is not None:
            if callee_function_name in callers:
                raise RecursionException('Recursive successor requested, but recursion is not supported!')
            callers.add(caller.function)
            caller = caller.caller

        target = ExecutionPoint(callee_function_name, call_target, self.get_execution_point().forward(self.length*2))
        return [target,]

    def find_symbol_by_addr(self, elf, addr):
        name = ''
        for section in elf.iter_sections():
            if section.header['sh_type'] == 'SHT_SYMTAB':
                for sym in section.iter_symbols():
                    if sym['st_value'] == addr:
                        secname = elf.get_section(sym['st_shndx'])
                        if sym['st_name'] == 0:
                            name = secname.name
                        else:
                            name =  sym.name
                        return name
        return None