import json

import math

from scfmsp.sidechannelverifier.AssignmentCollection import AssignmentCollection
from scfmsp.sidechannelverifier.SecurityLevel import SecurityLevel

class ContainerInitializer:
    def __init__(self):
        self.data = {}

    def parse_file(self, file):
        string = ''
        with open(file) as f:
            for line in f:
                string += line

        self.parse_string(string)

    def parse_string(self, string):
        self.data = json.loads(string)

    def get_file_path(self):
        return self.data['file']

    def set_parameters(self, ac, parameters, to):
        r = 12
        for param in parameters:
            size = param['size']
            used_total = math.ceil(size / 2)
            if param['confidential']:
                for i in range(0, used_total):
                    ac.ra.set('r' + str(r + i), to)
            r += used_total

    def get_starting_ac(self):
        ac = AssignmentCollection.bottom()
        self.set_parameters(ac, self.data['parameters'], SecurityLevel.HIGH)
        ac.mem = SecurityLevel.HIGH if self.data.get('memory', False) else SecurityLevel.LOW
        return ac

    def get_finishing_ac(self):
        ac = AssignmentCollection.top()
        self.set_parameters(ac, [self.data['result']], SecurityLevel.LOW)
        ac.mem = SecurityLevel.LOW if self.data['result'].get('memory', False) else SecurityLevel.HIGH
        return ac

    def get_starting_function(self):
        return self.data['starting_function']

    def get_include_functions(self):
        return self.data.get('include_functions', None)

    def get_timing_sensitive(self):
        return self.data.get('timing_sensitive', True)
