from detector import detector

detector1 = detector(10,50,300,10,5)

listaentrada = []
listaentrada = detector1.rand()

listaangulo = []
listaangulo = detector1.rand()

matriztrayec = detector1.matriztrayectoria(listaentrada, listaangulo)

histo = detector1.divisor(matriztrayec, 25, 100)

print(histo)

detector1.pintarparticula1(histo, 1, 10)
detector1.pintarcanal1(histo, 1, 10)
detector1.pintartrayectoria(matriztrayec)






