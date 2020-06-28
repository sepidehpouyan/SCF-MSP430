from scfmsp.controlflowanalysis.ExecutionPoint import ExecutionPoint


class AbstractInstruction:
    name = ''
    length = 2
    map1 = {}

    def __init__(self, function):
        self.file = ''
        self.program = function.program
        self.function = function

        self.address = 0
        self.length = 0
        self.clock = 0
        self.arguments = ()
        self.oplist = []
        
        self.register_mode = False
        self.indexed_mode =  False
        self.indirect_mode =  False
        self.immediate_mode =  False
        self.dst_register_mode =  False
        self.dst_indexed_mode = False

        self.immediate_dominator = None
        self.immediate_post_dominator = None
        self.predecessors = None

        self.__successors_checked_cache = None
        self.__execution_point = None

    def __unicode__(self):
        return '"%s: %s %s"' % (hex(self.address), self.name, self.arguments)


    def __repr__(self):
        return self.__unicode__()

    def parse(self, op_list):
        instr = ''
        self.oplist = op_list.split()
        temp = '{0:04b}'.format(int(self.oplist[0][0],16))
        temp1 =  '{0:04b}'.format(int(self.oplist[0][3],16))
        temp2 =  '{0:04b}'.format(int(self.oplist[0][2],16))
        # source addressing mode-----------------------------
        if (temp[2] == '0' and temp[3] == '0'):
            self.register_mode =  True
        if (temp[2] == '0' and temp[3] == '1'):
            self.indexed_mode =  True
        if (temp[2] == '1' and temp[3] == '0'):
            self.indirect_mode = True
        if(temp[2] == '1' and temp[3] == '1'):
            self.immediate_mode = True
        # destination addressing mode------------------
        if(temp[0] == '0'):
            self.dst_register_mode = True
        else:
            self.dst_indexed_mode = True

        # Instruction II (1 operand)-----------------------
        if (self.oplist[0][2] == '1'):
            arg1 = int(self.oplist[0][1],16)
            # Length of instructions and arguments ---------------
            if(self.register_mode):
                length = 1
                self.arguments = ('r'+str(arg1),)

            if(self.indirect_mode):
                length = 1
                self.arguments = ('r'+str(arg1),)  

            if(self.indexed_mode):
                length = 2
                if(arg1 == 3):
                    length = 1
                self.arguments = ('r'+str(arg1),)   

            if(self.immediate_mode):
                if (self.oplist[0][1] == '0'):
                    length = 2
                    self.arguments = ('#'+self.oplist[0][6]+self.oplist[0][7]+self.oplist[0][4]+self.oplist[0][5],) 
                else:
                    length = 1
                    self.arguments = ('r'+str(arg1),)
            # Instruction types II------------------------------------------
            if (temp1[2]=='0' and temp1[3]=='0' and temp[0]=='0'):
                if (temp[1] == '1'):
                    instr = 'rrc.b'
                else:
                    instr = 'rrc'
            if (temp1[2]=='0' and temp1[3]=='0' and temp[0]=='1'):
                instr = 'swpb'
            if (temp1[2]=='0' and temp1[3]=='1' and temp[0]=='0'):
                instr = 'rra'
            if (temp1[2]=='0' and temp1[3]=='1' and temp[0]=='1'):
                instr = 'sxt'
            if (temp1[2]=='1' and temp1[3]=='0' and temp[0]=='0'):
                instr = 'push'
            if (temp1[2]=='1' and temp1[3]=='0' and temp[0]=='1'):
                instr = 'call'
            if (temp1[2]=='1' and temp1[3]=='1' and temp[0]=='0'):
                instr = 'reti'   


        # Instruction III-----------------------------------
        elif (self.oplist[0][2] == '2' or self.oplist[0][2] == '3'):
            # Length of instruction
            length = 1
            self.clock = 2
            # Instruction III
            if (temp2[3]=='0' and temp1[0]=='0' and temp1[1]=='0'):
                instr = 'jnz'
            if (temp2[3]=='0' and temp1[0]=='0' and temp1[1]=='1'):
                instr = 'jz'
            if (temp2[3]=='0' and temp1[0]=='1' and temp1[1]=='0'):
                instr = 'jnc'
            if (temp2[3]=='0' and temp1[0]=='1' and temp1[1]=='1'):
                instr = 'jc'
            if (temp2[3]=='1' and temp1[0]=='0' and temp1[1]=='0'):
                instr = 'jn'
            if (temp2[3]=='1' and temp1[0]=='0' and temp1[1]=='1'):
                instr = 'jge'
            if (temp2[3]=='1' and temp1[0]=='1' and temp1[1]=='0'):
                instr = 'jl'
            if (temp2[3]=='1' and temp1[0]=='1' and temp1[1]=='1'):
                instr = 'jmp'


          # Instruction I ------------------------------------
        else:
            arg1 = int(self.oplist[0][3],16)
            arg2 = int(self.oplist[0][1],16)
            # Length of instruction & arguments
            if(self.register_mode and self.dst_register_mode):
                length = 1
                self.clock = 1
                self.arguments = ('r'+str(arg1),'r'+str(arg2),)

            if(self.register_mode and self.dst_indexed_mode):
                length = 2
                self.clock = 4
                if(arg2 == 2):
                    self.arguments = ('r'+str(arg1),'&'+self.oplist[0][6]+self.oplist[0][7]+self.oplist[0][4]+self.oplist[0][5],)
                else:
                    self.arguments = ('r'+str(arg1),'r'+str(arg2),)

            if(self.indexed_mode and self.dst_register_mode):
                length = 2
                if (self.oplist[0][3] == '3'): # constant generator -------------
                    length = 1
                    self.clock = 1
                else:
                    self.clock = 3
                if(arg1 == 2):
                    self.arguments = ('&'+self.oplist[0][6]+self.oplist[0][7]+self.oplist[0][4]+self.oplist[0][5],'r'+str(arg2),)
                else:
                    self.arguments = ('r'+str(arg1),'r'+str(arg2),)   
            if(self.indexed_mode and self.dst_indexed_mode):
                length = 3
                self.clock = 6
                if (self.oplist[0][3] == '3'): # constant generator -------------
                    length = 2
                    self.clock = 4 
                if(arg1 == 2): 
                    self.arguments = ('&'+self.oplist[0][6]+self.oplist[0][7]+self.oplist[0][4]+self.oplist[0][5],'&'+self.oplist[0][10]+self.oplist[0][11]+self.oplist[0][8]+self.oplist[0][9],)
                else:
                    self.arguments = ('r'+str(arg1),'r'+str(arg2),)
            
            if(self.indirect_mode and self.dst_register_mode):
                length = 1
                if (self.oplist[0][3] == '2' or self.oplist[0][3] == '3'): # constant generator -------------
                    self.clock = 1
                else:
                    self.clock = 2
                self.arguments = ('r'+str(arg1),'r'+str(arg2),)

            if(self.indirect_mode and self.dst_indexed_mode):
                length = 2
                if (self.oplist[0][3] == '2' or self.oplist[0][3] == '3'): # constant generator -------------
                    self.clock = 4
                else:
                    self.clock = 5
                if(arg2 == 2):
                    self.arguments = ('r'+str(arg1),'&'+self.oplist[0][6]+self.oplist[0][7]+self.oplist[0][4]+self.oplist[0][5],)
                else:
                    self.arguments = ('r'+str(arg1),'r'+str(arg2),)

            if(self.immediate_mode and self.dst_register_mode):
                if (self.oplist[0][3] == '0'): #-----##------
                    length = 2
                    self.clock = 2
                    self.arguments = ('#'+self.oplist[0][6]+self.oplist[0][7]+self.oplist[0][4]+self.oplist[0][5],'r'+str(arg2),)
                else:# indirect autoincrement -------------------
                    length = 1
                    if (self.oplist[0][3] == '2' or self.oplist[0][3] == '3'): # constant generator -------------
                        self.clock = 1
                    else:
                        self.clock = 2
                    self.arguments = ('r'+str(arg1),'r'+str(arg2),)

            if(self.immediate_mode and self.dst_indexed_mode):
                if (self.oplist[0][3] == '0'):#-----#------
                    length = 3
                    self.clock = 5
                    self.arguments = ('#'+self.oplist[0][6]+self.oplist[0][7]+self.oplist[0][4]+self.oplist[0][5],'r'+str(arg2),)
                else:# indirect autoincrement -----------------------------
                    length = 2
                    if (self.oplist[0][3] == '2' or self.oplist[0][3] == '3'): # constant generator -------------
                        self.clock = 4
                    else:
                        self.clock = 5
                    self.arguments = ('r'+str(arg1),'r'+str(arg1),)

            # Instruction type I --------------------------------------------------------------------------------------------------------------------
            if (self.oplist[0][2] == '4'):
                if (temp[1] == '1'):
                    instr =  'mov.b'
                else:
                    instr =  'mov'
            if (self.oplist[0][2] == '5'):
                if (temp[1] == '1'):
                    instr =  'add.b'
                else:
                    instr =  'add'
            if (self.oplist[0][2] == '6'):
                if (temp[1] == '1'):
                    instr =  'addc.b'
                else:
                    instr =  'addc'
            if (self.oplist[0][2] == '7'):
                if (temp[1] == '1'):
                    instr =  'subc.b'
                else:
                    instr =  'subc'
            if (self.oplist[0][2] == '8'):
                if (temp[1] == '1'):
                    instr =  'sub.b'
                else:
                    instr =  'sub'
            if (self.oplist[0][2] == '9'):
                if (temp[1] == '1'):
                    instr =  'cmp.b'
                else:
                    instr =  'cmp'        
            if (self.oplist[0][2] == 'a'):
                if (temp[1] == '1'):
                    instr =  'dadd.b'
                else:
                    instr =  'dadd'
            if (self.oplist[0][2] == 'b'):
                if (temp[1] == '1'):
                    instr =  'bit.b'
                else:
                    instr =  'bit'
            if (self.oplist[0][2] == 'c'):
                if (temp[1] == '1'):
                    instr =  'bic.b'
                else:
                    instr =  'bic'
            if (self.oplist[0][2] == 'd'):
                if (temp[1] == '1'):
                    instr =  'bis.b'
                else:
                    instr =  'bis'
            if (self.oplist[0][2] == 'e'):
                if (temp[1] == '1'):
                    instr =  'xor.b'
                else:
                    instr =  'xor'
            if (self.oplist[0][2] == 'f'):
                if (temp[1] == '1'):
                    instr =  'and.b'
                else:
                    instr =  'and'

        return instr, length, self.arguments, self.clock, self.register_mode, self.indexed_mode, self.immediate_mode, self.indirect_mode, self.dst_register_mode, self.dst_indexed_mode
    
    def get_info(self, length, address, arguments, clock, oplist, register, index, immediate, indirect, dst_register, dst_index, file):
        self.length = length
        self.address = address
        self.arguments = arguments
        self.clock = clock
        self.oplist = oplist
        self.register_mode =  register
        self.indexed_mode = index
        self.immediate_mode =  immediate
        self.indirect_mode =  indirect
        self.dst_indexed_mode = dst_index
        self.dst_register_mode = dst_register
        self.file =  file

    def get_execution_point(self):
        if self.__execution_point is None:
            self.__execution_point = ExecutionPoint(self.function.name, self.address, self.function.caller)
        return self.__execution_point

    def get_successors(self):        
        return [self.get_execution_point().forward(self.length*2)]

    def get_successors_checked(self):
        if self.__successors_checked_cache is not None:
            return self.__successors_checked_cache
        successors = self.get_successors()
        ret = []
        for succ in successors:
            try:
                self.program.get_instruction_at_execution_point(succ)
                ret.append(succ)
            except:
                pass
        self.__successors_checked_cache = ret
        return ret

    def get_execution_time(self):
        pass

    def get_branching_time(self):
        return 2

    def get_region_then(self):
        return []

    def get_region_else(self):
        return []

    def _get_branchtime(self, region):
        ret = 0
        for ep in region:
            instr = self.program.get_instruction_at_execution_point(ep)
            ret += instr.get_execution_time()
            
            if not (ep == self.get_execution_point()):
                ret -= instr.get_branchtime_then()     
        return ret

    def get_branchtime_then(self):
        return self._get_branchtime(self.get_region_then())

    def get_branchtime_else(self):
        return self._get_branchtime(self.get_region_else())

    def get_junction(self):
        return None

    def execute_judgment(self, ac):
        raise NotImplementedError('Instruction "%s" is lacking an execute_judgment implementation! At %s' %
                                  (self.name, self.get_execution_point()))

