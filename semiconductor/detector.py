import random as rd
import numpy as np
from scipy.stats import norm
from scipy.integrate import simpson
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Rectangle

class detector:

    def __init__(self, numcanales, anchocanal, espesor, ancholayers, numero):
        self.numcanales = numcanales
        self.anchocanal = anchocanal
        self.espesor = espesor
        self.ancholayers = ancholayers
        self.numero = numero

        self.anchototal = float(numcanales)*float(anchocanal)
        self.numlayers = int(float(espesor)/float(ancholayers))


    def rand(self):
        listax = []
        for _ in range(self.numero):
            listax.append(rd.random()*self.anchototal)
        
        return listax
    
    def barrido(self, posinicial, paso):
        listax = []
        for i in range(self.numero):
            if (posinicial+paso*i) > self.anchototal:
                break
            else:
                listax.append(posinicial+paso*i)

        return listax

    def igual(self, posinicial):
        listax = []
        for _ in range(self.numero):
            listax.append(posinicial)

        return listax
    
    def randang(self):
        listax = []
        for _ in range(self.numero):
            listax.append(rd.random()*180-90)
        
        return listax
    
    def barridoang(self, anguloinicial, paso):
        listax = []
        for i in range(self.numero):
            if (anguloinicial+paso*i >= 90) or (anguloinicial+paso*i <= -90):
                break
            else:
                listax.append(anguloinicial+paso*i)

        return listax

    def igualang(self, anguloinicial):
        listax = []
        for _ in range(self.numero):
            listax.append(anguloinicial)


        return listax
                

    def matriztrayectoria(self, posiciones, angulos):

        matriz = []

        for i in range(self.numero):
            fila = []  
            for j in range(self.numlayers+1):
                fila.append(0)  
            matriz.append(fila) 

        for i in range(self.numero):
            for j in range(self.numlayers+1):
                if angulos[i]==0:
                    matriz[i][j] = posiciones[i]

                else:
                    matriz[i][j] = (0+j*self.ancholayers)*1/np.tan((90-angulos[i])*(np.pi/180))+posiciones[i]

        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if (matriz[i][j] <= 0) or (matriz[i][j] >= self.anchototal):
                    matriz[i][j] = np.nan

        return matriz
    
    
    def divisor(self, matriz, desv, altura):

        histograma = []
        fila = []

        eventos = 0
        
        for i in range(len(matriz)):            
            eventos = eventos + len(matriz[i])
        for _ in range(eventos):
            fila = [0] * self.numcanales
            histograma.append(fila)
        
        contador = 0
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                
                if np.isnan(matriz[i][j]):
                    contador = contador + 1
                    continue

                linx = []
                datos = []
                pos = 0
                integrales = []
                limites = []
                limindices = []
                limindices.append(0)

                
                
                pos = matriz[i][j]

                gaussiana1 = gaussiana(pos, desv, altura)

                linx = gaussiana1.distr()[0]
                datos = gaussiana1.distr()[1]

                

                for s in range(len(linx)):
                    if (s > len(linx)-1):
                            break
                    if (linx[s]<0) or (linx[s]>self.anchototal):
                        linx = np.delete(linx, s)
                        datos = np.delete(datos, s)
                        s = s-1
                    
                if len(linx) == 0:
                    continue
                    
                for n in range(self.numcanales):
                    if (self.anchocanal*n >= min(linx)) and (self.anchocanal*n <= max(linx)):
                        limit = n*self.anchocanal
                        limites.append(limit)

                        t = self.anchototal
                        indice = 0
                        for m in range(len(linx)):
                            tt = abs(linx[m]-limit)
                            if tt < t:
                                t = tt
                                indice = m
                        if (t<=abs((max(linx)-min(linx))/len(linx))) and (indice != 0):
                            limindices.append(indice)
                        elif (t<=abs((max(linx)-min(linx))/len(linx))) and (indice == 0):
                            limindices.append(1)

                if not limites:
                    limites.append(pos)

                if limindices[-1] != len(linx):
                    limindices.append(len(linx))
                else:
                    limindices.insert(-1,998)

                for k in range(len(limindices)-1):

                    linxnuevo = linx[limindices[k]:limindices[k+1]]
                    datosnuevo = datos[limindices[k]:limindices[k+1]]

                    integrales.append(simpson(y = datosnuevo ,x = linxnuevo))

                histograma1 = histogramaclase(self.numcanales, self.anchocanal)
                histograma[contador][:] = histograma1.suma(limites, integrales)[:]
                contador = contador + 1


        histogramabueno = []
        filat = []

        for _ in range(eventos):
            filat = [0] * self.numcanales
            histogramabueno.append(filat)

        for b in range(len(matriz)):
            for _ in range(len(matriz[b])):
                if len(histograma) == 0:
                    break
                histogramabueno[b] = [x + y for x, y in zip(histogramabueno[b], histograma[0])]
                histograma = np.delete(histograma, 0, axis = 0)

        for l in range(len(histogramabueno) - 1, -1, -1):
            if all(x == 0 for x in histogramabueno[l]):
                del histogramabueno[l]
        
        return histogramabueno
    

    def pintarparticula(self, lista):
        listax = []
        for g in range(self.numcanales):
            listax.append(g+1)

        lista = np.array(lista)
        dim = lista.shape
        colores = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        if len(dim) > 1:
            ax = plt.subplot()

            
            for i in range(len(lista)):
                color_actual = colores[i % len(colores)]
                ax.plot(listax, lista[i], marker='o', linestyle='-', color=color_actual, label=f'Partícula {i + 1}')

            ax.set_xlabel('Canales')
            ax.set_ylabel('')
            ax.set_title('Histograma')

            ax.legend()
            ax.xaxis.set_major_locator(ticker.MultipleLocator(2))

            plt.show()

        elif len(dim) == 1:
            ax = plt.subplot()


            ax.plot(listax, lista, marker='o', linestyle='-', color='b', label='Partícula')

            ax.set_xlabel('Canales')
            ax.set_ylabel('')
            ax.set_title('Histograma')

            ax.legend()

            plt.show()


    def pintarparticula1(self, lista, canalinicial, canalfinal):
        listax = []
        for g in range(canalinicial, canalfinal+1, 1):
            listax.append(g)

        lista = np.array(lista)
        dim = lista.shape
        colores = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        if len(dim) > 1:
            ax = plt.subplot()

            
            for i in range(len(lista)):
                color_actual = colores[i % len(colores)]
                ax.plot(listax, lista[i][canalinicial-1:canalfinal], marker='o', linestyle='-', color=color_actual, label=f'Partícula {i+1}')

            ax.set_xlabel('Canales')
            ax.set_ylabel('')
            ax.set_title('Histograma')

            ax.legend()
            ax.xaxis.set_major_locator(ticker.MultipleLocator(2))

            plt.show()

        elif len(dim) == 1:
            ax = plt.subplot()


            ax.plot(listax, lista[canalinicial-1:canalfinal], marker='o', linestyle='-', color='b', label='Partícula {i+1}')

            ax.set_xlabel('Canales')
            ax.set_ylabel('')
            ax.set_title('Histograma')

            ax.legend()

            plt.show()

    def pintarcanal1(self, lista, canalinicial, canalfinal):

        listax = []
        for t in range(len(lista)):
            listax.append(t)

        lista = np.array(lista)
        colores = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        ax = plt.subplot()

            
        for i in range(canalinicial, canalfinal+1, 1):
            color_actual = colores[i % len(colores)]
            columna_i = [fila[i-1] for fila in lista]
            ax.plot(listax, columna_i, marker='o', linestyle='-', color=color_actual, label=f'Canal {i}')

        ax.set_xlabel('Canales')
        ax.set_ylabel('')
        ax.set_title('Histograma')

        ax.legend()

        plt.show()

    def pintartrayectoria(self, matriztrayectoria):

        lista = np.array(matriztrayectoria)

        ax = plt.subplot()

        
        for i in range(len(lista)):
            listay = []

            for k in range(len(lista[i])):
                    listay.append(self.ancholayers*k)

            ax.plot(lista[i], listay, marker='o', linestyle='-', color='r', markersize=3, label=f'Partícula {i + 1}')

        ax.set_xlabel('Canales')
        ax.set_ylabel('')
        ax.set_title('Histograma')


        rect = Rectangle((0, 0), self.anchototal, self.espesor, color='k', alpha=0.5)  # alpha controla la transparencia (opcional)
        ax.add_patch(rect)

        plt.show()



        



class histogramaclase:
    def __init__(self, numcanales, anchocanal):
        self.numcanales = numcanales
        self.anchocanal = anchocanal

    def suma(self, limites, integrales):
            lista = []
            for _ in range(self.numcanales):
                lista.append(0)

            for j in range(len(limites)):
                limites[j] = int(limites[j]/self.anchocanal)

            limites.append(limites[-1]+1)
            for i in range(len(integrales)):
                lista[limites[i]-1] = integrales[i]

            return lista


    
    

class gaussiana:
    def __init__(self, media, desv, altura):
        self.media = media
        self.desv = desv
        self.altura = altura

    def distr(self):
            
        linx = np.linspace(self.media-3*self.desv, self.media+3*self.desv, 1000) 
        gau = self.altura*norm.pdf(linx, self.media, self.desv) 

        matriz = [linx, gau]

        return matriz
    


    
    



"""
class entrada(detector):
    def __init__(self, numero, angulo, anchototal):
        super().__init__(detector.anchototal)
        self.numero = numero
        self.angulo = angulo

    def random(self):
        listax = []
        for _ in range(self.numero-1):
            listax.append(rd.random()*self.anchototal)
"""
