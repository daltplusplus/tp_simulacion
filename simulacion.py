import random
import math
import time
from datetime import datetime, timedelta

#variables de estado
nsa = 0
nsb = 0

#datos
taa = []
tab = []
ia = 0

#variables de control
m = 10 #normales
n = 6 #prioritarias

#auxiliares
tf = 60*60*24
t = 0
i_tpsa = 0
i_tpsb = 0
nt = 0
stll = 0
itoa = []
itob = []
staa = 0
stab = 0
ss = 0
stoa = []
stob = []
nta = 0
ntb = 0
sts = 0

HV = 9999999999999999999



#TEF
tpll = 0
tpsa = []
tpsb = [] 

def calcular_ia():
    r = random.random()
    return 4*r +1

def calcular_taa():
    m = 3/50
    while True:
        r1 = random.random()
        r2 = random.random()
        x1 = 15+(40-15)*r1
        y1 = m*r2
        if y1 <= (1/625)*x1-1/250:
            break
    
    return x1

def calcular_tab():
    m = 1/135
    while True:
        r1 = random.random()
        r2 = random.random()
        x1 = 120+(300-120)*r1
        y1 = m*r2
        if y1 <= (1/48600)*x1+1/810:
            break
    
    return x1

def llegada():
    global t, tpll, ia, stll, nt, tpsa, tpsb, i_tpsa, i_tpsb, taa, tab, staa, stab, stoa, stob, nsa, nsb, ntb, nta

    t = tpll
    ia = calcular_ia()
    tpll = t + ia
    stll += t
    nt += 1

    r = random.random()
    if r< 0.8:
        nsa += 1
        if nsa <= n:
            i_tpsa = tpsa.index(HV)
            ta = calcular_taa()
            tpsa[i_tpsa] = t + ta
            staa += ta
            stoa[i_tpsa] += t - itoa[i_tpsa] 
    else:
        nsb += 1
        if nsb <= m:
            i_tpsb = tpsb.index(HV)
            ta = calcular_tab()
            tpsb[i_tpsb] = t + ta
            stab += ta
            stob[i_tpsb] += t - itob[i_tpsb]
    
    print("llegada T= " +str(t))

def salidaA():
    global t, tpsa, i_tpsa, nsa, ss, itoa, taa, staa, nta, sts

    nta +=1
    sts += 1

    t = tpsa[i_tpsa]
    nsa -= 1
    ss += t
    if nsa >= n:
        ta= calcular_taa()
        tpsa[i_tpsa] = t + ta
        staa += ta
    else:
        itoa[i_tpsa] = t
        tpsa[i_tpsa] = HV

    print("salida A, T= " +str(t))

def salidaB():
    global t, tpsb, i_tpsb, nsb, ss, itob, tab, stab, ntb, sts

    ntb += 1
    sts += 1

    t = tpsb[i_tpsb]
    nsb -= 1
    ss += t
    if nsb >= m:
        ta= calcular_tab()
        tpsb[i_tpsb] = t + ta
        stab += ta
    else:
        itob[i_tpsb] = t
        tpsb[i_tpsb] = HV
    
    print("salida B, T= " +str(t))

def indice_menor_valor(lista):
    return min(enumerate(lista), key=lambda x: x[1])[0]

def preparar_vectores():
    global tpsa, tpsb, stoa, stob, n, m

    for k in range(n):
        tpsa.append(HV)
        stoa.append(0)
        itoa.append(0)
    
    for k in range(m):
        tpsb.append(HV)
        stob.append(0)
        itob.append(0)


def imprimir_resultados():
    global ss, stll, nt, nta, ntb, stoa, stob, t
    pss = round((ss-stll)/nt)
    peca = round((ss-stll-staa)/nta)
    pecb = round((ss-stll-stab)/ntb)
    

    print("ss: " + str(ss))
    print("stll: " + str(stll))
    print("staa: " + str(staa))
    print("stab: " + str(stab))
    print("nta: " + str(nta))
    print("ntb: " + str(ntb))
    print("nt: " + str(nt))
   
    print("---RESULTADOS---")
    print("PPS    = " + str(pss) + " segundos")
    print("PEC A  = " + str(peca) + " segundos")
    print("PEC B  = " + str(pecb) +  " segundos")
    
    
    for k in range(n):
        stoa[k] += t - itoa[k]
        pto = round(stoa[k]*100/t)
        print("PTO A" + str(k) + " = " + str(pto) + "%")
    for k in range(m):
        stob[k] += t - itob[k]
        pto = round(stob[k]*100/t)
        print("PTO B" + str(k) + " = " + str(pto) + "%")    



def main():
    global t, tf, i_tpsa, i_tpsb, nsa, nsb, tpsa, tpsb, tpll

    preparar_vectores()
    
    while True:
        i_tpsa = indice_menor_valor(tpsa)
        i_tpsb = indice_menor_valor(tpsb)

        if tpsa[i_tpsa] < tpsb[i_tpsb]:
            if tpsa[i_tpsa] < tpll:
                salidaA()
            else:
                llegada()
        else:
            if tpsb[i_tpsb] < tpll:
                salidaB()
            else:
                llegada()

        if t>tf:
            if nsa > 0 or nsb > 0:
                tpll = HV
            else:
                break 

    imprimir_resultados()






main()