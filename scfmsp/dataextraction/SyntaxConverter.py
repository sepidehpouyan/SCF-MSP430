from scfmsp.controlflowanalysis.InstructionFactory import InstructionFactory
from scfmsp.controlflowanalysis.AbstractInstruction import AbstractInstruction
from scfmsp.controlflowanalysis.Function import Function
from scfmsp.controlflowanalysis.Program import Program
from elftools.elf.elffile import ELFFile

class SyntaxConverter:
    @staticmethod
    def parse_file(file, starting_function):
        elf = ELFFile(open(file, 'rb'))
        sym_table, section_name = SyntaxConverter.find_symbol_by_name(elf, starting_function)
        starting_function_size = sym_table['st_size']
        starting_function_address = sym_table['st_value']
        ret = Program()
        return SyntaxConverter.parse_elf(file, elf, starting_function, starting_function_address, starting_function_size, section_name, ret, caller= None, call_dic={})

    @staticmethod
    def parse_elf(file, elf, starting_function, start_addr, size, section_name, ret, caller, call_dic):
        i =  0
        current_func = Function(starting_function, ret, file)
        ret.add_function(current_func)
        section = elf.get_section_by_name(section_name)
        sh_addr = section['sh_addr']
        sh_size = section['sh_size']
        if(size == 0): # sometime the size is 0
            size = sh_size
        offset = start_addr - sh_addr
        stop_offset = offset + size
        code = section.data()[offset:stop_offset]
        opcode = ""
        for b in code:
            opcode += "%02x" % b
        
        address =  start_addr
        callers = set()
        caller = list()
    
        while(i < len(opcode)):
            op_list =  opcode.split()
            abs_instr = AbstractInstruction(current_func)
            instr_string, length, arguments, clock, register, index, immediate, indirect, dst_register, dst_index = abs_instr.parse(op_list[0][i:])
            if(instr_string == ""): # --------- this will be changed later (sancus instruction)
                return ret
            instr = InstructionFactory.get_instruction(instr_string, function=current_func)
            instr.get_info(length, address, arguments, clock, op_list[0][i:], register, index, immediate, indirect, dst_register, dst_index, file)
            current_func.add_instruction(instr)

            if(instr_string == 'call' and op_list[0][i+1] == '0'):
                hex_addr =  op_list[0][i+6] + op_list[0][i+7] + op_list[0][i+4] + op_list[0][i+5]
                call_target = int(hex_addr, 16)

                elf = ELFFile(open(file, 'rb'))
                sym_table_name, sym_table_size, section_name = SyntaxConverter.find_symbol_by_addr(elf, call_target)
                callee_function_name = sym_table_name
                callee_function_size = sym_table_size

                # Check for recursionn -------------------------
                callers.clear()
                if caller is not None:
                    caller.clear()

                if(call_target ==  start_addr):
                    return ret   
                else:
                    count = 0
                    call_dic.setdefault(call_target, []).append(start_addr)
                    callers = {start_addr}
                    tmp = call_dic.get(start_addr)
                    if tmp is not None:
                        caller.extend(tmp)
                    while len(caller) > 0:
                        first_caller =  caller.pop(0)
                        if(len(callers) == count):
                            return ret
                        if (call_target in callers):
                            return ret
                        count = len(callers)
                        callers.add(first_caller)
                        temp = call_dic.get(first_caller)
                        if temp is not None:
                            caller.extend(temp)
              
                SyntaxConverter.parse_elf(file, elf, callee_function_name, call_target, callee_function_size, section_name, ret, current_func, call_dic)

            i = i + (length * 4)
            address = address + (length * 2)  
        return ret
    
    @staticmethod
    def find_symbol_by_addr(elf, addr):
        name = ''
        size = 0
        for section in elf.iter_sections():
            if section.header['sh_type'] == 'SHT_SYMTAB':
                for sym in section.iter_symbols():
                    if sym['st_value'] == addr:
                        secname = elf.get_section(sym['st_shndx'])
                        if sym['st_name'] == 0:
                            name = secname.name
                        else:
                            name =  sym.name
                        size = sym['st_size']
                        return name, size, secname.name
        return None

    
    @staticmethod
    def find_symbol_by_name(elf, name):
        for section in elf.iter_sections():
            if section.header['sh_type'] == 'SHT_SYMTAB':
                for sym in section.iter_symbols():
                    if sym.name == name:
                        secname = elf.get_section(sym['st_shndx'])
                        return sym, secname.name
        return None
