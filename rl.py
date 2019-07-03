import numpy as np
import matplotlib.pyplot as plt 

from matplotlib.widgets import Slider, Button, RadioButtons, TextBox
from matplotlib.colors import  LinearSegmentedColormap

from numpy.ctypeslib import ndpointer
import ctypes 
LL = ctypes.cdll.LoadLibrary
    

colorlist =['xkcd:dark red', #1
            'xkcd:dark blue', #2
            'xkcd:dark green', #3
            'xkcd:magenta', #4
            'xkcd:orange', #5
            'xkcd:violet', #6
            'xkcd:gold', #7
            'xkcd:turquoise', #8
            ]

class Table(object):
    """infinite table where every rows is being RL of the previous one and   """
    cfill = LL('./fill.so').fill
    cfill.argtypes = [
        ctypes.c_int,
        ndpointer(ctypes.c_int,ndim=1),
        ctypes.c_int,
        ctypes.c_int,
        ndpointer(ctypes.c_int,ndim=2,flags='CONTIGUOUS'),
    ] 
    cfill.restypes = None
    
    VD = 5000
    HD = 2000
    
    def __init__(self, code=[1,2], stype = 0. ):		
        super(Table, self).__init__()
        self.code = code
        self.stype = stype
        self.field = np.zeros((self.VD,self.HD,),dtype ='int32')
        self.generate()
        self.cfill(self.genome.size,self.genome,self.VD,self.HD,self.field)
        self.field = self.genome[self.field]        

    def generate(self):
        self.genome = [-1] 
        l = len(self.code)
        dn = 0
        i= -1
        if self.stype=='a':
            while dn<self.VD+self.HD:
                i += 1
                j = i+1
                while( j%(l+1) ==0 ):
                    j//=(l+1)
                self.genome.append(self.code[j%(l+1)-1])
                if self.genome[-1]!=self.genome[-2]:
                    dn+=1
        elif self.stype=='d':
            while dn<self.VD+self.HD:
                i += 1
                j=i+1
                while( j%2 ==0 ):
                    j//=2
                self.genome.append(self.code[((j-1)//2)%l])
                if self.genome[-1]!=self.genome[-2]:
                    dn+=1
        else :
            while dn<self.VD+self.HD:
                i += 1
                self.genome.append(self.code[int(p*i) %l])
                if self.genome[-1]!=self.genome[-2]:
                    dn+=1
        self.genome = np.array(self.genome[1:],dtype='int32') 



    def __str__(self):
        s=""
        for i in range(10):
            for j in range(50):
                s=s+str(self.field[i,j])+' '
            s=s+'\n'
        return s


    def plot(self,x=0,y=0):
        self.hoffset=x
        self.voffset=y
        self.step=1

        axscale = plt.axes([0.25, 0.1, .55, 0.03], facecolor="green")
        self.slscale = Slider(axscale, 'Scale', 1, 2, valinit=1.2, valstep=0.01)
        self.slscale.on_changed(self.update)
        d=int(10**self.slscale.val)
        self.imsize=d
        
        self.ax = plt.axes([0.25, 0.2, .65, 0.7])
        self.im = self.ax.imshow([[.0]], cmap= LinearSegmentedColormap.from_list(
            "thiscmap", colorlist[:max(self.code)], N=25))
        self.cbar = self.ax.figure.colorbar(self.im, ax=self.ax)
        self.cbar.set_ticks(self.code)
        
        axright = plt.axes([0.14, 0.35, 0.04, 0.04])
        axleft = plt.axes([0.06, 0.35, 0.04, 0.04])
        axup = plt.axes([0.1, 0.39, 0.04, 0.04])
        axdown = plt.axes([0.1, 0.31, 0.04, 0.04])
        axstep = plt.axes([0.1, 0.35, 0.04, 0.04])
        self.tbstep = TextBox(axstep,' ',initial=' 1')
        self.tbstep.on_text_change(self.upstep)
        self.bright = Button(axright, r'$\rightarrow$', color="red", hovercolor='green')  
        self.bleft = Button(axleft, r'$\leftarrow$', color="red", hovercolor='green')  
        self.bup = Button(axup, r'$\uparrow$', color="red", hovercolor='green')  
        self.bdown = Button(axdown, r'$\downarrow$', color="red", hovercolor='green')  
        self.bright.on_clicked(self.fright)
        self.bleft.on_clicked(self.fleft)
        self.bup.on_clicked(self.fup)
        self.bdown.on_clicked(self.fdown)
        
        self.update(0)


    def upstep(self,txt):
        self.step=int(eval(self.tbstep.text))

    def fleft(self,val):
        self.hoffset=max(self.hoffset-self.step,0)
        self.update(val)

    def fright(self,val):
        self.hoffset=min(self.HD-self.imsize,self.hoffset+self.step)
        self.update(val)
        
    def fup(self,val):
        self.voffset=max(self.voffset-self.step,0)
        self.update(val)
        
    def fdown(self,val):
        self.voffset=min(self.VD-self.imsize,self.voffset+self.step)
        self.update(val)
        

    def update(self,val):
        d=int(10**self.slscale.val)
        self.imsize=d
        x=self.hoffset
        y=self.voffset
        sideticks=[.5/d-.5+i/d for i in range(d)]
        
        self.ax.set_xticks(sideticks)
        self.ax.set_yticks(sideticks)
        self.ax.set_xticklabels([str(x)]+[' ']*(d-2)+[str(x+d)])
        self.ax.set_yticklabels([str(y)]+[' ']*(d-2)+[str(y+d)])
        self.im.set_data(self.field[y:y+d:1,x:x+d])
        self.im.autoscale()
        
        plt.draw()



main = Table([1,2,3],'d')
# print(main)
main.plot()
plt.show()






