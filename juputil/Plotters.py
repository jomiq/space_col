import plotly.graph_objects as go
from SCA.util import norm as norm

def tree_plot(T, show_edges=True, show_nodes=True, show_leaves=False, show_branching=False, node_w=True):
    '''Works > Efficient'''
    x = T.nodes[:T.end,0]
    y = T.nodes[:T.end,1]
    z = T.nodes[:T.end,2]
    
    nx = []
    ny = []
    nz = []



    def addpoint(v):
        nx.append(v[0])
        ny.append(v[1])
        nz.append(v[2])
    
    x_lines = []
    y_lines = []
    z_lines = []
    
    mark_colors = []
    mark_w = []
    
    line_colors = []
    line_w = []
    
    w0 = T.w[0]
    
    for i in range(T.end):
        if show_leaves and len(T.children[i]) == 0:
            addpoint(T.nodes[i])
            mark_w.append(10)
            mark_colors.append('green')
            continue
        if show_branching != 0 and len(T.children[i]) > show_branching:
            addpoint(T.nodes[i])
            mark_w.append(5)
            mark_colors.append('blue')
            continue
        if show_nodes:
            addpoint(T.nodes[i])
            mark_w.append(T.w[i]/w0*25)
            mark_colors.append(i)
            continue


    if show_edges:
    #create the coordinate list for the lines
        for e in T.edges:
            for i in range(2):
                x_lines.append(x[e[i]])
                y_lines.append(y[e[i]])
                z_lines.append(z[e[i]])
            x_lines.append(None)
            y_lines.append(None)
            z_lines.append(None)

    
    #marker
    mark = dict(
            symbol='circle',
            size=mark_w,
            color=mark_colors,           # set color to an array/list of desired values
            colorscale='Portland',          # choose a colorscale
            opacity=1.0,
            line=dict(width=0,
                color='DarkSlateGrey')
        )
    
    linedict = dict(
        color='black',
        width=2
    )
    
    node_data = go.Scatter3d(x=nx, y=ny, z=nz, mode='markers', marker=mark, name='Node')
    line_data = go.Scatter3d(
        x=x_lines,
        y=y_lines,
        z=z_lines,
        mode='lines',
        name='Edge',
        line=linedict
        
    )

    fig = go.Figure(data=[node_data, line_data])

    fig.update_layout(
        width=1200,
        height=1200,
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
    
    scat = go.Scatter3d(x=D[:,0], y=D[:,1], z=D[:,2],
              marker=mark, mode='markers')
    fig = go.Figure(data=scat)
    fig.update_layout(
        title=name,
        width=1200,
        height=700,
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

