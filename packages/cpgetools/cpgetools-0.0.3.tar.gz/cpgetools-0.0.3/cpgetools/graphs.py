import graphviz

def draw_graphe(ugraphe):
    dot = graphviz.Graph(comment='A binary tree',node_attr={'color': 'lightblue2', 'style': 'filled'})
    edges=[]
    for node in sorted(ugraphe):
        for adjacent in ugraphe[node]:
            if {node,adjacent} not in edges:
                edges.append({node,adjacent})
    for edge in [tuple(ed) for ed in edges]:
        dot.edge(edge[0],edge[1])
    return dot

def draw_digraphe(Digraph):
    dot = graphviz.Digraph(comment='A binary tree',node_attr={'color': 'lightblue2', 'style': 'filled'})
    for node in sorted(Digraph):
        for adjacent in Digraph[node]:
            dot.edge(node,adjacent)
    return dot
test_ugraph={
    "A":["B","C"],
    "B":["A","D"],
    "C":[],
    "D":["B","A"]
}