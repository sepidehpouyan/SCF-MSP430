import networkx as nx
from graphviz import Digraph


class NetworkXConvert:
    def __init__(self, program):
        self.program = program

    def create_graph_from(self, starting_ep):
        visited = set()
        to_visit = [starting_ep]
        graph = nx.DiGraph()
        g = Digraph('G', filename='CFG.gv')  
        count = 0
        while len(to_visit) > 0:
            count += 1
            
            current_ep = to_visit.pop(0) 
            current_instr = self.program.get_instruction_at_execution_point(current_ep)
            for succ_ep in current_instr.get_successors_checked():
                graph.add_edge(current_ep, succ_ep)

                g.edge(str(hex(current_instr.address)), str(hex(self.program.get_instruction_at_execution_point(succ_ep).address)),label=None)
                #g.edge(current_instr, self.program.get_instruction_at_execution_point(succ_ep),label=None)

                if succ_ep not in visited:
                    visited.add(succ_ep)
                    to_visit.append(succ_ep)

        g.view()
        self.program.possible_exit_points = [ep for ep in graph if graph.out_degree(ep) == 0]
        if len(self.program.possible_exit_points) > 0 and self.program.exit_point is None:
            self.program.exit_point = self.program.possible_exit_points[-1]

        imm_doms = nx.immediate_dominators(graph, starting_ep)

        graph_reverse = graph.reverse()
        post_doms = [nx.immediate_dominators(graph_reverse, exit_ep) for exit_ep in self.program.possible_exit_points]

        for ep in graph:
            instr = self.program.get_instruction_at_execution_point(ep)

            possible_post_dominators = {pd.get(ep, None) for pd in post_doms}
            if len(possible_post_dominators) == 1:
                instr.immediate_post_dominator = possible_post_dominators.pop()

            instr.predecessors = graph.predecessors(ep)
            instr.immediate_dominator = imm_doms[ep]

        return graph
