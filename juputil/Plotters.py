import plotly.graph_objects as go
from numpy.linalg import norm as norm
def decimate_four(T):
    edges = []
    def walk(i):
        for j in T.children[i]:
            edges.append((i,j))
            walk(j)
    
    for i in range(T.nroots):
        walk(i)

    return edges

def decimate_tree(T):
    edges = []
    def walk(i):
        if len(T.children[i]) == 1:
            return walk(T.children[i][0])
        elif len(T.children[i]) > 1:
            for c in T.children[i]:
                edges.append((i, walk(c)))

        return i
    
    for i in range(T.nroots):
        walk(i)
    
    return edges

def tree_plot(T, pointsize=10, show_edges=True, show_nodes=True, show_leaves=True, show_branching=False, decimate=False):
    '''Works > Efficient'''
    if decimate:
        show_nodes = False
        show_branching = True

    nodes = []
    node_w = pointsize * T.w/max(T.w)
    nodes_labels = []
    nodes_color = []

    max_children = max([len(c) for c in T.children])

    leaves = []
    leaves_labels = []
    

    branches = []
    branches_w = []
    branches_color = []
    branches_labels = []

    for i, n in enumerate(T.nodes[:T.end]):
        nchild = len(T.children[i])
        
        if show_nodes:
            nodes.append(n)
            nodes_labels.append(f'N{i}')
            nodes_color.append(i/T.end) 

        if nchild == 0:
            leaves.append(n)
            leaves_labels.append(f'L{i}')

        elif nchild > 1:
            branches.append(n)
            branches_w.append(node_w[i] + 3)
            branches_labels.append(f'{i}:{nchild}')
            branches_color.append(nchild/max_children)
        
    x_lines = []
    y_lines = []
    z_lines = []

    edges = []
    if show_edges:
        if decimate:
            edges = decimate_tree(T)
        else:
            edges = T.edges

        x = T.nodes[:T.end, 0]
        y = T.nodes[:T.end, 1]
        z = T.nodes[:T.end, 2]
        # oh this hack sucks
        for e in edges:
            for i in range(2):
                x_lines.append(x[e[i]])
                y_lines.append(y[e[i]])
                z_lines.append(z[e[i]])
            x_lines.append(None)
            y_lines.append(None)
            z_lines.append(None)

    
    # markers
    node_mark = dict(
            symbol='circle',
            size=node_w,
            color=nodes_color,           # set color to an array/list of desired values
            colorscale='Portland',          # choose a colorscale
            opacity=1.0,
            line=dict(width=0,
            color='DarkSlateGrey')
    )
 
    leaf_mark = dict(
            symbol='circle',
            size=pointsize/5,
            color='green',           # set color to an array/list of desired values
            colorscale='Portland',          # choose a colorscale
            opacity=1.0,
            line=dict(width=0,
            color='DarkSlateGrey')
    )

    branches_mark = dict(
            symbol='circle',
            size=branches_w,
            color=branches_color,           # set color to an array/list of desired values
            colorscale='Portland',          # choose a colorscale
            opacity=1.0,
            line=dict(width=0,
            color='DarkSlateGrey')
    )
    
    linedict = dict(
        color='black',
        width=2
    )

    res_data = []
    def myzip(V):
        return [v[0] for v in V], [v[1] for v in V], [v[2] for v in V]
    if show_nodes:
        X = myzip(nodes)
        res_data.append(go.Scatter3d(x=X[0], y=X[1], z=X[2], \
            name='Nodes',
            text=nodes_labels,
            mode='markers', 
            marker=node_mark))    
    if show_leaves:
        X = myzip(leaves)
        res_data.append(go.Scatter3d(x=X[0], y=X[1], z=X[2], \
            name='Leaf',
            text=leaves_labels,
            mode='markers',
            marker=leaf_mark))
    if show_branching:
        X = myzip(branches)
        res_data.append(go.Scatter3d(x=X[0], y=X[1], z=X[2], \
            name='Branching nodes',
            text=branches_labels,
            mode='markers',
            marker=branches_mark))
    if show_edges:
        res_data.append(go.Scatter3d(x=x_lines, y=y_lines, z=z_lines, \
            name='Edge',
            mode='lines',
            line=linedict))

 



    fig = go.Figure(data=res_data)

    fig.update_layout(
        width=800,
        height=600,
        autosize=False,
        scene=dict(
            camera=dict(
                up=dict(
                x=0,
                y=0,
                z=1
                ),
            eye=dict(
                x=0,
                y=1.0707,
                z=1,
                ),
            ),
            xaxis = dict(
                 backgroundcolor="rgb(255, 255, 255)",
                 gridcolor="white",
                 showbackground=False,
                 zerolinecolor="white",
                ),
            yaxis = dict(
                backgroundcolor="rgb(255, 255, 255)",
                 gridcolor="white",
                 showbackground=False,
                 zerolinecolor="white",
                ),
            zaxis = dict(
                backgroundcolor="rgb(230, 230,200)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white",
                ),

            aspectratio = dict( x=1, y=1, z=1 ),
            aspectmode = 'data'
        )
    )
    
    fig.show()
    
def stat_plot(T, normal_to_size=False):
    s = T.get_stats()

    ages = [i for i in range(len(s))]
    size = [v.sz for v in s]

    
    
    activation = [v.act for v in s]
    growth = [(size[i+1]-size[i]) for i in range(0, len(size)-1)]
    growth.insert(0,0)
    
    actlabels = [str(x) for x in activation]
    glabels = [str(x) for x in growth]
    
    scale_dsz = 1
    sclae_act = 1
    if normal_to_size:
        scale_dsz = size[len(size)-1]/max(growth)
        scale_act = size[len(size)-1]/max(activation)
        for i in range(len(ages)):
            growth[i] = growth[i]*scale_dsz
            activation[i] = activation[i]*scale_act
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=ages, y=size,
                    name='Size',
                    marker_color=size
                    ))
    fig.add_trace(go.Scatter(x=ages, y=activation,
                    mode='lines',
                    name='Activation',
                    text=actlabels))
    fig.add_trace(go.Scatter(x=ages, y=growth,
                    mode='lines',
                    name='Growth',
                    text=glabels))

    fig.show()

def dist_plot(D, name='', psize=1):
    c = [norm(v) for v in D]
    mark = dict(
            symbol='circle',
            size=psize,
            color=c,                # set color to an array/list of desired values
            colorscale='Portland',   # choose a colorscale
            opacity=1.0,
            line=dict(width=0,
            color='DarkSlateGrey')
        )
    
    xp = []
    yp = []
    zp = []
    for v in D:
        xp.append(v[0])
        yp.append(v[1])
        zp.append(v[2])

    scat = go.Scatter3d(x=xp, y=yp, z=zp,
              marker=mark, mode='markers')
    fig = go.Figure(data=scat)
    fig.update_layout(
        title=name,
        width=800,
        height=600,
        autosize=False,
        scene=dict(
            camera=dict(
                up=dict(
                x=0,
                y=0,
                z=1
                ),
            eye=dict(
                x=0,
                y=1.0707,
                z=1,
                ),
            ),
            xaxis = dict(
                 backgroundcolor="rgb(255, 255, 255)",
                 gridcolor="white",
                 showbackground=False,
                 zerolinecolor="white",
                ),
            yaxis = dict(
                backgroundcolor="rgb(255, 255, 255)",
                 gridcolor="white",
                 showbackground=False,
                 zerolinecolor="white",
                ),
            zaxis = dict(
                backgroundcolor="rgb(230, 230,200)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white",
                ),

            aspectratio = dict( x=1, y=1, z=1 ),
            aspectmode = 'data'
        )
    )
    fig.show()

def histogram_plot(D, title='', bins=3000):

    df = go.Histogram(x=D, nbinsx=bins, name=title)

    fig = go.Figure(data=df)
    fig.show()

