import graphviz
def root(A):
    if A!=[]:
        return str(A[0])
def left_child(A):
    if A!=[]:
        return A[1]
def right_child(A):
    if A!=[]:
        return A[2]
def is_empty(A):
    return A==[]

def tree_from_dfs(sequence):
    level_tree={0:[]}
    for i in range(len(sequence)-1,-1,-1):
        if 2*i+1 not in level_tree:
            level_tree[i]=[sequence[i],[],[]]
        else:
            fils_guache=level_tree[2*i+1]
            level_tree.pop(2*i+1)
            if 2*i+2 not in level_tree:
                level_tree[i]=[sequence[i],fils_guache,[]]
            else:
                fils_droit=level_tree[2*i+2]
                level_tree.pop(2*i+2)
                level_tree[i]=[sequence[i],fils_guache,fils_droit]
    return level_tree[0]

def draw_tree1(A,title):
    
    #Parcour en largeur
    dot = graphviz.Digraph("aa",comment='A binary tree',node_attr={'color': '#FFB6C1', 'style': 'filled'})
    Tree_Dot=dict()#permet de donner une correpo,dance entre les nodes de A et les labels de Dot
    if A==[]:
        return dot,Tree_Dot
    file=[(A,-1)]
    i=0
    while file!=[]:
        T,i_pere=file.pop(0)
        dot.node(str(i),str(root(T)))
        if i!=0:
            dot.edge(str(i_pere),str(i))
        Tree_Dot[root(T)]=i
        gauche=left_child(T)
        droit=right_child(T)
        if gauche!=[]:
            file.append((gauche,i)) 
        if droit!=[]:
            file.append((droit,i))
        i+=1
    dot.attr(label=title)
    dot.attr(fontsize='20')
    return dot,Tree_Dot

def draw_tree(A,title=""):
    """Draw a graph that represent the tree:
    input: 
        - A: is a list that represent the tree A
        - title: is a string to be printed with the graph of the tree
    Output:
        a raphviz object it will be drawen directly if you use a notebbok,
        or you can use .view() otherwise if use this function in a .py file, the  graph then will be printed in your defaut pdf viewer.
    """
    return draw_tree1(A,title)[0]

def animate_secuence(Tree,sequence,titel="a sequence"):
    dot,Tree_Dot=draw_tree1(Tree,titel)
    dot.attr(label=titel)
    dot.attr(fontsize='20')
    yield dot
    sequence2=[]
    i=0
    while True:
        i=i%len(sequence)
        node=sequence[i]
        sequence2.append(node)
        #dot.node("#sequence#",titel+"\n=["+"\n".join(sequence2)+"]",shape="rectangle")
        dot.attr(label=titel+"=\n["+"  ".join(sequence[:i+1])+"]",shape="rectangle")
        dot.node(str(Tree_Dot[node]),color="red")
        yield dot
        dot.node(str(Tree_Dot[node]),color="lightblue")
        i+=1


testTree=["+",["*",[4,[],[]],[5,[],[]]],["/",[6,[],[]],[7,[],[]]]]