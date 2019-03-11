
import os
from py2neo import Graph, Node, Relationship, NodeMatcher

def create_call_graph(call_graph_dict):
    graph = Graph('bolt://localhost:7687', username="neo4j", password="yogita")
    #matcher = NodeMatcher(graph)
    #graph.delete_all()

    tx = graph.begin()
    #d = {"func1":["func3","func2","func5"], "func2":["func3"], "func3":["func4","func6"]}

    for k, v in call_graph_dict.iteritems():
        a = Node("Function", name=k)
        tx.merge(a, primary_label="Function", primary_key="name")

        for item in v:
            
            b = Node("Function", name=item)
            tx.merge(b, primary_label="Function", primary_key="name")

            ab = Relationship(a, "calls", b)
            tx.create(ab)

    tx.commit()

    """
            b = list(matcher.match("Function", name=item))
            #print(a)
            if b:
                b = b[0]
            else:
                b = Node("Function", name=item)
    """
    #MATCH (n:Function) RETURN n 
    #alice, bob, carol = [result.one for result in tx.commit()]

def create_dictionary_from_diagraph(diagraph_file):
    db_called = {}

    with open(diagraph_file, 'r') as fd:
        for line in fd:
            line = line.split()
            #print(line)

            if len(line) > 2:
                start, end = line[0].strip('"'), line[2].strip('"')
                #print(start, end)
                start, end = start.lower(), end.lower()
                #if start == "sys_rt_sigaction":
                #    print(start, end)

                if start in db_called:
                    db_called[start].append(end)

                else:
                    db_called[start] = []
                    db_called[start].append(end)

            else:
                #print(line[0].strip('"'))
                s = line[0].strip('"')
                if s not in db_called:
                    db_called[s] = []

    return db_called

path = os.getcwd()
filename = "diagraph_defconfig-441.txt"
call_graph_dict = create_dictionary_from_diagraph(os.path.join(path,filename))
create_call_graph(call_graph_dict)