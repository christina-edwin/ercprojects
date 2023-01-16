#import files
import matplotlib.pyplot as plt
from shapely.geometry import Polygon,LineString
import random



#global variables
coords1=[(0,4),(0.25,3.75),(0.25,0.25),(1,0.25),(1,3),(2,3),(2,2.25),(1.5,2.25),(1.5,0.25),(3.75,0.25),(4,0),(0,0)]
coords2=[(0,4),(0.25,3.75),(2.5,3.75),(2.5,2),(3,2),(3,3.75),(3.75,3.75),(3.75,0),(4,0),(4,4)]
poly1=Polygon(coords1)
poly2=Polygon(coords2)

LI_NODES = []
LI_CONNECT = []
limit=5000

start_coords=(0.5,0.5)
end_coords=(3.5,3.5)


isJoined = False

fig,axs=plt.subplots()


axs.fill([x[0] for x in coords1],[y[1] for y in coords1],alpha=1,fc='#000000',ec='none')
axs.fill([x[0] for x in coords2],[y[1] for y in coords2],alpha=1,fc='#000000',ec='none')



plt.xticks([(float)(i/2) for i in range(0,9)])
plt.yticks([(float)(j/2) for j in range(0,9)])




#class for node
class Node:
    def __init__(self,xcoord,ycoord,weight,connect,marker,markersize):
        self.xcoord=xcoord
        self.ycoord=ycoord
        self.weight=weight
        self.connect=connect
        self.marker=marker
        self.markersize=markersize
        plt.plot([self.xcoord],[self.ycoord],self.marker,markersize = self.markersize)

    def Los(self):
        global isJoined
        line=LineString([[self.xcoord,self.ycoord],[end_coords[0],end_coords[1]]])
        if not (line.intersects(poly1) or line.intersects(poly2)):
            isJoined=True
            plt.plot([self.xcoord,end_coords[0]],[self.ycoord,end_coords[1]],'go-')

start = Node(start_coords[0], start_coords[1], 0, 0, 'bo', 20)
end = Node(end_coords[0], end_coords[1], 0, 0, 'bo', 20)

def dist(Node, x, y):
    return ((Node.xcoord-x)**2+(Node.ycoord-y)**2)**(0.5)

LI_NODES.append(start)

cv=0
while (cv<limit and (not isJoined)):
    plt.pause(0.01)
    x,y=random.random()*4,random.random()*4
    min=float('inf') 
    joiningnode=None 

    for node in LI_NODES:
        line=LineString([[node.xcoord,node.ycoord],[x,y]])
        if (dist(node,x,y)<1 and not (line.intersects(poly1) or line.intersects(poly2))) and dist(node,x,y)<min:
            min=dist(node,x,y)
            joiningnode=node
        
    if joiningnode:
        line=LineString([[joiningnode.xcoord,joiningnode.ycoord],[x,y]])
        if (dist(joiningnode,x,y)<1 and not (line.intersects(poly1) or line.intersects(poly2))):
            plt.plot([joiningnode.xcoord,x],[joiningnode.ycoord,y],'yo-',markersize=5)
        LI_NODES.append(Node(x,y,dist(joiningnode,x,y)+joiningnode.weight,LI_NODES.index(joiningnode),'yo',5))
        LI_NODES[-1].Los()

    cv+=1
plt.title('Path Planning',fontdict={'fontname':'Ariel','fontsize':20})

LI_CONNECT.append(len(LI_NODES)-1)
while LI_NODES[LI_CONNECT[-1]].connect!=0:
    LI_CONNECT.append(LI_NODES[LI_CONNECT[-1]].connect)
LI_CONNECT.append(0)

plt.plot([LI_NODES[LI_CONNECT[i]].xcoord for i in range(len(LI_CONNECT))], [LI_NODES[LI_CONNECT[i]].ycoord for i in range(len(LI_CONNECT))], 'go-')
plt.show()