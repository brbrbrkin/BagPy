import random
import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions
import threading
from threading import Thread
from pyglet.gl import *
import sys
import matplotlib.pyplot as plt
import numpy as np




global caminho

#Change directory
caminho = "C:/Users/Hércules/Desktop/IC/"




window = pyglet.window.Window(1280, 920, "Mochila")
options = DrawOptions() 


zone = pymunk.Space()   
zone.gravity = 0, -1000 

pyglet.gl.glClearColor(255, 255, 255, 255)



glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)





@window.event
def on_draw():

    window.clear()
    handler.bag.draw()
    handler.grafico.draw()

    zone.debug_draw(options)
    
    
    
    


@window.event
def on_key_press(symbol, modifiers):
    global handler
    global caminho
    
    
    if symbol == pyglet.window.key.ENTER:
        

        if handler.atual == 0:

            
            handler.stopThread.set()
            handler.continueThread.set()

            handler.bag.image = handler.img
            handler.grafico.image = handler.graf

            for bodyr in zone.bodies:
                zone.remove(bodyr)
                
            
            for shaper in zone.shapes:
                zone.remove(shaper)

            new_thread = Thread(target=handler.mochila)
            new_thread.start()

            
        
            
            handler.createMochila()
            
            
            
            pyglet.clock.schedule_interval(handler.createObject, 1.0/30)

            pyglet.clock.schedule_once(handler.checkWeight, 1, 20)

            window.flip()

        else: print("Try again")

            
      

    elif symbol == pyglet.window.key.RIGHT:
        
        if handler.atual == 0:
            window.flip()
            handler.bag.image = handler.img

            temp = pyglet.image.load(caminho + "test.png")

            temp.anchor_x = temp.width // 2
            temp.anchor_y = temp.height // 2

            handler.grafico.image = temp

            for bodyr in zone.bodies:
                zone.remove(bodyr)
            
            for shaper in zone.shapes:
                zone.remove(shaper)
            
            window.clear()

            plot()

            handler.stopThread.clear()
            handler.continueThread.set()

            handler.createMochila()

            
            

                
            pyglet.clock.schedule_interval(handler.createObject, 1.0/30)
            

            
            pyglet.clock.schedule_once(handler.checkWeight, 1, 20)

        else: print("Try again")
        
        

        
    elif symbol == pyglet.window.key.LEFT:
        print("Do Y")






def plot():
    global ax
    global fig
    # Data for plotting
    tam = len(np.arange(0,100,1))
    s=[]
    s.append( handler.media)
    for x in range(tam):
        if x == len(s):
            s = np.append(s, 0)

    t = np.arange(0,100,1)
    
    print( handler.media)
    fig, ax = plt.subplots()

    plt.plot(t,s)

    


    ax.set(xlabel='Geracoes (s)', ylabel='Fitness',
        title='Fitness/N de geracoes')
    

    fig.savefig(caminho +"test.png")

    plt.close()



        
class pymunkHandler():
    global caminho

    mutRatio = 0.05
    capacity = 20
    objCount = 10
    atual = 0
    media = []

    bestItems = []

    continueThread = threading.Event()
    stopThread = threading.Event()

    img = pyglet.image.load(caminho +"bag.png")

    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

    img2 = pyglet.image.load(caminho + "bag2.png")

    img2.anchor_x = img.width // 2
    img2.anchor_y = img.height // 2

    bag = pyglet.sprite.Sprite(img, x=690, y=600)

    graf = pyglet.image.load(caminho + "test.png")

    graf.anchor_x = img.width // 2
    graf.anchor_y = img.height // 2    

    grafico = pyglet.sprite.Sprite(graf, x=200, y=230)
    grafico.scale = 0.75

   

    def createObject(self, dt):
        
  
        
        mass = self.bestItems[self.atual].weight
        radius = 10 + self.bestItems[self.atual].weight * 5 
        moment = pymunk.moment_for_circle(mass, 0, radius) 
        body = pymunk.Body(mass, moment)
        body.position = random.randrange(660,700), 500
        
        shape = pymunk.Circle(body, radius)
        shape.color = (random.randrange(0,254), random.randrange(0,254), random.randrange(0,254), 255)
        shape.elasticity = 0.8
        shape.friction = 1.0
        
        
        zone.add(body, shape)
        
        
        self.atual += 1
        if len(self.bestItems)-1 < self.atual:
            pyglet.clock.unschedule(self.createObject)
            self.atual = 0






    def mochila(self, i=0):


        




        if i == 0:       
            itemList = [] 
            for x in range(self.objCount):
                itemList.append(item(self.capacity))
            agentList = []
            for x in range(gen.total):
                agentList.append(cromossomo(self.capacity, self.objCount))

        
        
            genx = gen(agentList)

        genx.agents = genx.fillBag(genx.agents, itemList)

        while i<100:
                        
            tWinners = genx.arena(self.capacity)
        
            if len(tWinners) % 2 > 0:
                tWinners.pop()
            j = 0
            offspring = []
            for x in range(int(len(tWinners)/2)):

                offspring.append(cromossomo(self.capacity, tWinners[j].reproduce(tWinners[j+1], self.mutRatio)))

        

            
            media = genx.meanFit(self.capacity)
            self.media.append(media)
            print("GERACAO: ", i, genx.agents, "MEDIA: ", media)  

             
                


            genx.elimWeak(offspring, self.capacity, itemList)

            genx.getBestItems(self.capacity)
            
            
            self.continueThread.clear()
            
            if self.continueThread.wait():
                pass
                
                       
            if self.stopThread.is_set():
                handler.media = []
                break

            i+=1

    

        

    def createMochila(self):
        mochila1 = pymunk.Segment(zone.static_body, [window.get_size()[0]/2 - 100, window.get_size()[1]/2 -100], [window.get_size()[0]/2 + 200, window.get_size()[1]/2 -100], 8 )
        mochila1.body.elasticity = 0.8
        mochila1.body.friction = 1.0
        mochila1.color = (0, 0, 0, 0)
        zone.add(mochila1)

        mochila2 = pymunk.Segment(zone.static_body, [window.get_size()[0]/2 - 100, window.get_size()[1]/2 -100], [window.get_size()[0]/2 - 100, window.get_size()[1]/2 +200], 8 )
        mochila2.body.elasticity = 0.8
        mochila2.body.friction = 1.0
        mochila2.color = (0, 0, 0, 0)
        zone.add(mochila2)

        mochila3 = pymunk.Segment(zone.static_body, [window.get_size()[0]/2 + 200, window.get_size()[1]/2 -100], [window.get_size()[0]/2 + 200, window.get_size()[1]/2 +200], 8 )
        mochila3.body.elasticity = 0.8
        mochila3.body.friction = 1.0
        mochila3.color = (0, 0, 0, 0)
        zone.add(mochila3)
        

    def checkWeight(self, *args):
        peso = 0
        for shape in zone.shapes:
            if shape.body._get_type() == 0:
                peso += shape.body.mass
                
   
        if peso > args[1]:
            for shape in zone.shapes:
                if shape.body._get_type() == 2:
                    
                    zone.remove(shape)

                    handler.bag.image = handler.img2
                    
                    
                    
       

        
        
        


class item:
    def __init__(self, capacity):
        self.weight = random.randrange(1, capacity/4*10, 1)/10
        self.value = random.randrange(1, 10*10, 1)/10

    def __repr__(self):
        return ("Peso "+str(self.weight)+" Valor "+str(self.value))




class gen:
    def __init__(self, agentList):
        self.agents = agentList
    total = 10
    itn = 0


    def best(self, capacity):
        i = 0
        for agent in self.agents:
                
            if i == 0:
                atu = agent
                atuidx = 0

            if agent.fitness(capacity) > atu.fitness(capacity):
                atu = agent
                atuidx = i

            i+=1        
        return atu

    def arena(self, capacity):
        
        curArena = []
        random.shuffle(self.agents)

        for x in range(int(self.total/2)):
            curArena.append(self.agents[x])
            
        win = []
        for x in range (int(self.total/5)):
            
            
            i=0
            
            for agent in curArena:
                
                if i == 0:
                    atu = agent
                    atuidx = 0

                if agent.fitness(capacity) > atu.fitness(capacity):
                    atu = agent
                    atuidx = i

                i+=1
                
            if curArena:
                curArena.pop(atuidx)
                win.append(atu)
                
        
        
        return win

    def elimWeak(self, winners, capacity, itemList):
        
        for x in range(len(winners)):
            i=0
            for agent in self.agents:
                if i == 0:
                    atu = agent
                    atuidx = 0
                
                if agent.fitness(capacity) < atu.fitness(capacity):
                    atu = agent
                    atuidx = i
                
                i+=1
            
            self.agents.pop(atuidx)
        i=0

        
        for x in range(len(winners)):
            winList = [winners[i]]
            winners[i] = self.fillBag(winList, itemList)[0]
            self.agents.append(winners[i])
            i+=1


    def meanFit(self, capacity):
        tot = 0
        
        for agent in self.agents:
            tot += agent.fitness(capacity)
            

        return tot/len(self.agents)


    def fillBag(self, agents, itemList):
        
        for agent in agents:
            
            
            agentItems = itemList.copy()
            

            for x in agent.gene:            
                
                
                    if x == 0:
                        j=0
                        for itm in agentItems:
                            if j == 0:
                                atu = itm.weight
                                atuidx = j
                            elif itm.weight < atu:
                                atu = itm.weight
                                atuidx = j
                            j+=1
                        if agentItems:
                            agent.bag.append(agentItems[atuidx])                  
                            agentItems.pop(atuidx)
                  
                                                
            
                    elif x == 1: 
                        j=0
                        for itm in agentItems:
                            if j == 0:
                                atu = itm.value
                                atuidx = j
                            elif itm.value > atu:
                                atu = itm.value
                                atuidx = j
                            j+=1
                        if agentItems:
                            agent.bag.append(agentItems[atuidx])                  
                            agentItems.pop(atuidx)                      

                    elif x == 2:
                        j=0
                        for itm in agentItems:
                            if j == 0:
                                atu = itm.value/itm.weight
                                atuidx = j
                            elif itm.value/itm.weight > atu:
                                atu = itm.value/itm.weight
                                atuidx = j
                            j+=1
                        if agentItems:
                            agent.bag.append(agentItems[atuidx])                  
                            agentItems.pop(atuidx)    

        return agents             
                
    def getBestItems(self, capacity):
        global handler
        i=0
        for agent in self.agents:
            if i == 0:
                atu = agent
                atuidx = 0
            
            if agent.fitness(capacity) > atu.fitness(capacity):
                atu = agent
                atuidx = i
            
            i+=1
        
        handler.bestItems = self.agents[atuidx].bag

            



class cromossomo:
    def __init__(self, capacity, arg):

        if isinstance(arg, int):
            objCount = arg
            self.capacity = capacity
            self.gene =  []
            for x in range(objCount):
                
                self.gene.append(random.randrange(4))

        elif isinstance(arg, list):
            self.gene = arg
            self.capacity = capacity
        
        self.bag = []

    def __repr__(self):
        return (str(self.fitness(self.capacity)))

   

    def __str__(self):
        return (str(self.gene))

    def fitness(self, capacity):
        totValue = 0
        totWeight = 0
        penalty = 1
        
        for x in self.bag:
            totValue = totValue + x.value
            totWeight = totWeight + x.weight
        
        if totWeight > capacity:
            penalty = 0
        

        fit = totValue * penalty

        return int(fit)
        
             

    def reproduce(self, par, mutRatio):
        
        objCount = len(self.gene)
        div = int(random.randrange(objCount - (int(objCount/2))) - int((objCount - int(objCount/2))/2) )

        

        fert1 = self.gene[:(int(objCount/2)+div)]
        fert2 = par.gene[(int(objCount/2)+div):]
        

        offspr = fert1 + fert2

        if random.random() < mutRatio:
            offspr[random.randrange(objCount)] = random.randrange(4)
        
        
        return offspr




def update(dt):
    zone.step(dt)
    for shape in zone.shapes:
        if shape.body.position.y < -100:
            zone.remove(shape.body, shape)


handler = pymunkHandler()



pyglet.clock.schedule_interval(update, 1.0/60)
pyglet.app.run()




  



