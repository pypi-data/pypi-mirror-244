import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot(fig,x,y,name):
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines',name=name))
def subPlot(fig,x,signals,name,N,amount):
    N=N
    fig =make_subplots(
        rows=N,cols=5,
        subplot_titles=("Box Signal","Saw Signal", "Exponential Signal","Sinusoid Signal","Gaussian Signal")
        )
    fig.update_xaxes(range=[-np.pi,np.pi])
    #fig.update_yaxes(range=[-1,1])

    sample=np.random.choice(np.linspace(0,amount,amount), N, replace=False)
    sample=np.around(sample)
    for i in range(N):
        index=int(sample[i])
        fig.add_trace(
            go.Scatter(
                x=x,y=signals[0,index],name='Constant Signal %d'%i,mode="lines",line_color='red'
            ),
            row=i+1,col=1
        )
    for i in range(N):
        index=int(sample[i])
        fig.add_trace(
            go.Scatter(
                x=x,y=signals[1,index],name='Saw Signal %d'%i,mode="lines",line_color='green'
            ),
            row=i+1,col=2
        )
    for i in range(N):
        index=int(sample[i])
        fig.add_trace(
            go.Scatter(
                x=x,y=signals[2,index],name='Exp Signal %d'%i,mode="lines",line_color='blue'
            ),
            row=i+1,col=3
        )
    for i in range(N):
        index=int(sample[i])
        fig.add_trace(
            go.Scatter(
                x=x,y=signals[3,index],name='Sinusoid Signal %d'%i,mode="lines",line_color='black'
            ),
            row=i+1,col=4
        )
    for i in range(N):
        index=int(sample[i])
        fig.add_trace(
            go.Scatter(
                x=x,y=signals[4,index],name='Gaus Signal %d'%i,mode="lines",line_color='brown'
            ),
            row=i+1,col=5
        )
    fig.update_layout(height=1200,width=1000,showlegend=False, title_text="%d Test Samples of Generated Function"%N)
    return fig

