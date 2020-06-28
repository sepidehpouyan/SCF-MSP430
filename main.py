
import json
import sys

from scfmsp.sidechannelverifier.Analysis import Analysis
from scfmsp.dataextraction.ContainerInitializer import ContainerInitializer
from scfmsp.dataextraction.SyntaxConverter import SyntaxConverter

def main():
    args = sys.argv
    if args is None or len(args) < 2:
        print('Run using a path to a json file')
        return 0

    initializer = ContainerInitializer()
    initializer.parse_file(args[1])
    program = SyntaxConverter.parse_file(initializer.get_file_path(), initializer.get_starting_function())

    analysis = Analysis(program)
    starting_ep = program.functions[initializer.get_starting_function()].first_instruction.get_execution_point()
    starting_ac = initializer.get_starting_ac()
    finishing_ac = initializer.get_finishing_ac()
    timing_sensitive = initializer.get_timing_sensitive()
    result = analysis.analyze(starting_ep, starting_ac, finishing_ac, timing_sensitive)

    output = {
        'result': result.result.name,
        'result_code': result.result.value,
        'execution_point': None if result.ep is None else {
            'function': result.ep.function,
            'address': hex(result.ep.address)
        },
        'unique_ret': str(result.unique_ret)
    }
    print(json.dumps(output))

    return 0

if __name__ == '__main__':
    sys.exit(main())