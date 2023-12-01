import graphviz


def draw_heap1(L,title):
    #Parcour en largeur
    dot = graphviz.Digraph("aa",comment='A binary tree',node_attr={'color': '#FFB6C1', 'style': 'filled'})
    Tree_Dot=dict()#permet de donner une correpo,dance entre les nodes de A et les labels de Dot
    for i in range(len(L)):
        dot.node(str(i),str(L[i]))
    for i in range((len(L))//2):
        dot.edge(str(i),str(2*i+1))
        if 2*i+2<len(L):
            dot.edge(str(i),str(2*i+2))
    dot.attr(label="\n\n"+title)
    dot.attr(fontsize='20')
    return dot,Tree_Dot

def draw_heap(L,title="Heap"):
    return draw_heap1(L,title)[0]

def draw_tab(L):
    s = graphviz.Digraph('aa', filename='aa.gv',
                        node_attr={'shape': 'record'})
    s.node('tab','|'.join(['<L'+str(i)+'>'+str(L[i]) for i in range(len(L))]))
    for i in range((len(L))//2):
        s.edge('tab:L'+str(i), 'tab:L'+str(2*i+1))
        if 2*i+2<len(L):
            s.edge('tab:L'+str(i), 'tab:L'+str(2*i+2))
    return s

if __name__=="__main__":
    draw_heap([0,1,2,3,4,5],'TAS').view()
    #draw_tab([0,1,2,3,4,5,6]).view()