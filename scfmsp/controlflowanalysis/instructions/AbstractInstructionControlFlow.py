from scfmsp.controlflowanalysis.AbstractInstruction import AbstractInstruction
from scfmsp.controlflowanalysis.ExecutionPoint import ExecutionPoint


class AbstractInstructionControlFlow(AbstractInstruction):
    def __init__(self, function):
        super(AbstractInstructionControlFlow, self).__init__(function)

    def get_branch_target(self):

        opList = self.oplist.split()
        temp = '{0:04b}'.format(int(opList[0][3],16))
        if(temp[2]=='0'):
            part3 = int(temp[2])*512 + int(temp[3])*256
            part1 =  int(opList[0][1],16)
            part2 =  (int(opList[0][0],16))*16
            offset =  part1 + part2 + part3
        else:
            temp = '{0:04b}'.format(int(opList[0][3],16))
            part3 = int(self.rev(temp[2]))*512 + int(self.rev(temp[3]))*256
            temp1 = '{0:04b}'.format(int(opList[0][1],16))
            part1 = (int(self.rev(temp1[0])) * 8) + (int(self.rev(temp1[1])) * 4) + (int(self.rev(temp1[2])) * 2) + (int(self.rev(temp1[3])) * 1)
            temp2 = '{0:04b}'.format(int(opList[0][0],16))
            part2 = ((int(self.rev(temp2[0])) * 8) + (int(self.rev(temp2[1])) * 4) + (int(self.rev(temp2[2])) * 2) + (int(self.rev(temp2[3])) * 1)) * 16
            offset =  (part1 + part2 + part3 + 1) * (-1)
        addr = self.address + 2*(offset)+2
        target = ExecutionPoint(self.function.name, addr, self.function.caller)
        
        return target

    def rev(self, arr):
        if(arr == '0'):
            arr = '1'
        else:
            arr = '0'
        return arr
