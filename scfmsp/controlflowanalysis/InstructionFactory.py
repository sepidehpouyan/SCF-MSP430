from scfmsp.controlflowanalysis.instructions.InstructionMov import InstructionMov
from scfmsp.controlflowanalysis.instructions.InstructionAdd import InstructionAdd
from scfmsp.controlflowanalysis.instructions.InstructionAddc import InstructionAddc
from scfmsp.controlflowanalysis.instructions.InstructionSubc import InstructionSubc
from scfmsp.controlflowanalysis.instructions.InstructionSub import InstructionSub
from scfmsp.controlflowanalysis.instructions.InstructionCmp import InstructionCmp
from scfmsp.controlflowanalysis.instructions.InstructionDadd import InstructionDadd
from scfmsp.controlflowanalysis.instructions.InstructionBit import InstructionBit
from scfmsp.controlflowanalysis.instructions.InstructionBic import InstructionBic
from scfmsp.controlflowanalysis.instructions.InstructionBis import InstructionBis
from scfmsp.controlflowanalysis.instructions.InstructionXor import InstructionXor
from scfmsp.controlflowanalysis.instructions.InstructionAnd import InstructionAnd
from scfmsp.controlflowanalysis.instructions.InstructionRrc import InstructionRrc
from scfmsp.controlflowanalysis.instructions.InstructionRra import InstructionRra
from scfmsp.controlflowanalysis.instructions.InstructionSwpb import InstructionSwpb
from scfmsp.controlflowanalysis.instructions.InstructionSxt import InstructionSxt
from scfmsp.controlflowanalysis.instructions.InstructionPush import InstructionPush
from scfmsp.controlflowanalysis.instructions.InstructionCall import InstructionCall
from scfmsp.controlflowanalysis.instructions.InstructionReti import InstructionReti
from scfmsp.controlflowanalysis.instructions.InstructionJmp import InstructionJmp
from scfmsp.controlflowanalysis.instructions.InstructionJn import InstructionJn
from scfmsp.controlflowanalysis.instructions.InstructionJc import InstructionJc
from scfmsp.controlflowanalysis.instructions.InstructionJl import InstructionJl
from scfmsp.controlflowanalysis.instructions.InstructionJz import InstructionJz



class InstructionFactory:
    instructions = {
        
        'mov': InstructionMov,
        'mov.b': InstructionMov,
        'add': InstructionAdd,
        'add.b': InstructionAdd,
        'addc': InstructionAddc,
        'addc.b': InstructionAddc,
        'subc': InstructionSubc,
        'subc.b': InstructionSubc,
        'sub': InstructionSub,
        'sub.b': InstructionSub,
        'cmp': InstructionCmp,
        'cmp.b': InstructionCmp,
        'dadd': InstructionDadd,
        'dadd.b': InstructionDadd,
        'bit': InstructionBit,
        'bit.b': InstructionBit,
        'bic': InstructionBic,
        'bic.b': InstructionBic,
        'bis': InstructionBis,
        'bis.b': InstructionBis,
        'xor': InstructionXor,
        'xor.b': InstructionXor,
        'and': InstructionAnd,
        'and.b': InstructionAnd,
        'jl': InstructionJl,
        'jge': InstructionJl,
        'jnz': InstructionJz,
        'jne': InstructionJz,
        'jz': InstructionJz,
        'jeq': InstructionJz,
        'jmp': InstructionJmp,
        'jn': InstructionJn,
        'jc': InstructionJc,
        'jhs': InstructionJc,
        'jnc': InstructionJc,
        'jlo': InstructionJc,
        'rrc': InstructionRrc,
        'rrc.b': InstructionRrc,
        'swpb': InstructionSwpb,
        'rra': InstructionRra,
        'sxt': InstructionSxt,
        'push': InstructionPush,
        'call': InstructionCall,
        'reti': InstructionReti,
    }

    @staticmethod
    def get_instruction(func_name, function):
        if func_name in InstructionFactory.instructions:
            func = InstructionFactory.instructions[func_name](function)
            return func
        else:
            raise NotImplementedError('Instruction "%s" is not implemented.' % func_name)

    @staticmethod
    def copy_instruction(instr, function=None):
        instr_copy = InstructionFactory.get_instruction(instr.name,function if function is not None else instr.function)
        instr_copy.address = instr.address
        instr_copy.length = instr.length
        instr_copy.clock = instr.clock
        instr_copy.arguments = instr.arguments
        instr_copy.oplist = instr.oplist
        instr_copy.register_mode = instr.register_mode
        instr_copy.indexed_mode = instr.indexed_mode
        instr_copy.indirect_mode = instr.indirect_mode
        instr_copy.immediate_mode = instr.immediate_mode
        instr_copy.dst_register_mode = instr.dst_register_mode
        instr_copy.dst_indexed_mode = instr.dst_indexed_mode
        instr_copy.file = instr.file
        
        return instr_copy