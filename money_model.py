import mesa
import random
import numpy as np

class MoneyAgent(mesa.Agent):

    def _init_(self,unique_id,model):
        super()._init_(unique_id,model)
        self.counter = 0


    def step(self):
        self.move()
        self.clean()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.counter = self.counter + 1
        print("Limpieza (porcentaje)" + str(self.model.limpiasPorCen()) + str(self.count))
        #Imprimir el porcentaje de limpieza 


    def clean(self):
        if self.model.isDirty(self.pos):
            self.model.setDirty(self.pos)
        pass

class MoneyModel(mesa.Model):


    def _init_(self, N, width, height, percent):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.celdas_suc = int(round((width * height) * percent))
        self.celdas_lim = (width * height) - self.celdas_suc 
        self.matrixSuc = np.zeros([width,height]) # matriz sucia 
        heightCont = 0 # alto de la matriz
        widthCont = 0 # ancho de la matriz
        sucCont = self.celdas_suc #numero de celdas sucias por %
        var = 1 

        for x in self.matrixSuc:
            if width < sucCont:
                while heightCont < height and var == 1:
                    widthCont = 0
                    while widthCont < width and var == 1:
                        if sucCont > 0:
                            self.matrixSuc[widthCont][heightCont] = 1
                            widthCont = widthCont + 1
                            sucCont = sucCont - 1
                        else:
                            var = 0  
                    heightCont = heightCont + 1            
            else:
                while widthCont < width and var == 1:
                    
                    if sucCont > 0:
                        self.matrixSuc[widthCont][heightCont] = 1
                        widthCont = widthCont + 1
                        sucCont = sucCont - 1
                        if sucCont <= 0:
                            var = 0
                            pass
                    else:
                        var = 0 
        heightCont = 0
        widthCont = 0
        if width < height:
            while widthCont < width:
                np.random.shuffle(self.matrixSuc[widthCont])
                widthCont = widthCont + 1
            self.arregloImprimir()
        else:
            while heightCont < height:
                np.random.shuffle(self.matrixSuc[heightCont])
                heightCont = heightCont + 1
            self.arregloImprimir()

        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
        

        self.grid.place_agent(a, (1,1))

    def step(self):
        self.schedule.step()

    def arregloImprimir(self):  
        print(self.matrixSuc)

    def isDirty(self, new_position):
        x,y = new_position
        if self.matrixSuc[x][y] == 1:
            return True
        else:
            return False

    def setDirty(self,new_position):
        x,y = new_position
        self.celdas_suc = self.celdas_suc - 1
        self.celdas_lim = self.celdas_lim + 1
        self.matrixSuc[x][y] = 0
    
    def limpiasPorCen(self):   # porcentaje de celdas limpias
        return(self.celdas_lim/(self.width*self.height))*100
        pass