import re

digitos = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+?')

codigos = ['bcd','ed3','gry','jsn','par','pbt','ham']
codigos_full = ['BCD', 'Exceso de 3', 'Gray', 'Johnson', 'Paridad', 'Pentabit', 'Hamming']

#Agrega los 0 necesarios a la izquierda de n
def toXbits(n, x):
    if len(n)<x:
        for _ in range(x-len(n)):
            n = "0" + n
    return n

#Entre bases numericas y decimal
def bToDec(n, b):
    res = 0
    n = str(n)
    b = int(b)
    for i in range(len(n)):
        index = len(n) - i -1
        val = digitos.index(n[index])
        res += val * (b**i)
    
    if res == 0:
        return '0'*4
    return str(res)

#Entre decimal y bases numéricas
def decToB(n, t):
    res = ""
    n=int(n)
    t=int(t)
    if t == 1 :
        return '1'*n
    if n == 0:
        return '0'*4
    while n > 0:
        d = n%t
        res += digitos[d]
        n = n//t

    return res[::-1]

#BCD
def decToBcd(n):
    res = ""
    for i in n:
        d = decToB(int(i), 2)
        d = toXbits(d, 4)
        res += d
    if n == '0000':
        return '0'*4
    return res

def bcdToDec(n):
    bitsN = ((len(n)//4)+1)*4       #Si n esta en bcd, se rellena con 0 para cumplir con la cantidad de bits
    n = toXbits(n, bitsN)

    res = ''
    for i in range(0,len(n),4):
        d = bToDec(n[i:(i+4)], 2)
        res += d
    
    if n == '0000':
        return '0'*4

    return res

#Gray
def grayToBin(n):
    res = n[0]
    for i in range(0,len(n)-1):
        res += str(int(n[i])^int(n[i+1]))
    return res

def binToGray(n):
    res = n[0]
    for i in n[1:]:
        res += str(int(res[-1])^int(i))
    return res

#Exceso de 3
def decToEd3(n): # usa 6 b
    res = ''
    for i in n:
        d = int(i) + 3
        d = decToB(d,2)
        d = toXbits(d,4)
        res+=d
    return res

def ed3ToDec(n):
    res=''
    for i in range(0,len(n),4):
        res += str(int(bToDec(n[i:i+4], 2))-3)
    return res

#Johnson
def binToJsn(n): #Recibe n en base 2
    n = bToDec(n,2)
    hayBits = False
    cBits = 1
    n = int(n)

    while not hayBits:
        if n < 2*cBits :
            hayBits = True
        else:
            cBits += 1

    return  ('1'*(2*cBits - n)) + ('0'*(n-cBits))

def jsnToBin(n):
    cantCeros = n.count('0')
    resDec = cantCeros + len(n)

    return decToB(resDec, 2)

#Paridad
def paridad(n):
    if n.count('1') % 2 == 0:
        return 1
    return 0

#pentaBit
def penta(n):
    if len(n) % 5 != 0:
        return 0
    for i in range(0, len(n), 5):
        if n[i:i+5].count('1') != 2:
            return 0
    return 1

#Hamming
def hammingCheck(n):        #Recibe n en hamming y retorna el calor corregido
    
    pos1 = [i for i in range(len(n)) if n[i]=='1']  #Guarda las pos con 1
    
    err = 0

    for i in pos1:  #Calculo de la pos con error
        err ^= i
    
    if err != 0 and paridad(n) == 1:    #Hay 2 errores
        return '0'
    if err == 0 and paridad(n) == 1:    #No hay error
        return n

    if n[err] == '1':
        res = n[:err] + '0' + n[err+1:]
    else:
        res = n[:err] + '1' + n[err+1:]

    for i in pos1:
        err ^= i

    if err == 0:
        return res

    return '0'

def hammingToBin(n):   #Recibe n en hamming, lo retorna en binario

    pot = 0
    res = ''

    for i in range(0,len(n)):
        if not(2**pot == i):
            res += n[i]
        else:
            pot += 1
    
    return res


def validar(datos):

    if datos.count(' ') == 2:
        datos = datos.split(' ')
        n, b, t = datos[0], datos[1], datos[2]
    else:
        return False
    cod = ''
    #Revisa a b
    if re.search(r"^\d+", b):   #b es una base numérica
        b = int(b)

        if t == 'ham':
            condiciones = [ b >= 1, b <= 64, 1 <= int(bToDec(hammingToBin(n),2)) <= 1000]
        else:
            condiciones = [ b >= 1, b <= 64, 1 <= int(bToDec(n,b)) <= 1000]

        if not all(condiciones):
            return False

        for i in n:     #Revisa que n este en base b
            if digitos.index(i) >= b:
                return False

    elif b in codigos:

        cod = b     #guarda el código en b

        if re.search(r"^[0-1]+", n) and b in codigos:   #Revisa que n solo contenga 1 y 0
            b = 2
        else:
            return False

        if cod == 'par':
            if paridad(n) == 0:
                return False
        elif cod == 'pbt':
            if penta(n) == 0:
                return False
    
    else:
        return False
    #Revisa a t
    if re.search(r"^\d+", t):
        t = int(t)
        condiciones = [t >= 1, t <= 64]

        if not all(condiciones):
            return False

    else:
        if (t not in codigos):
            return False
    
    return (n, cod, str(b), str(t))


def decToCod(n,t): #Recibe n en decimal y lo tranforma al codigo t
    
    res = n
    if t == 'bcd':
        res = decToBcd(n)
        return res
    elif t == 'ed3':
        res = decToEd3(n)
        return res

    nEnBin = decToB(n, 2)

    if t == 'gry':
        res = binToGray(nEnBin)
    elif t == 'jsn':
        res = binToJsn(nEnBin)
    elif t == 'par':
        res = paridad(nEnBin)
    elif t == 'pbt':
        res = penta(nEnBin)
    elif t == 'ham':
        res = hammingCheck(nEnBin)

    return res

datos = input()

while datos != '-':

    datos = validar(datos)

    if not datos:
        print('Entrada invalida')
        datos  = input()
        continue

    n, cod, b, t = datos

    if (not cod) and re.search(r"^\d+", t): #b y t son numericos            

        nEnDec = bToDec(n, b)
        
        nEnt = decToB(nEnDec, t)

    elif not cod:   #b es numerico y t es codigo

        if b == '2' and t == 'ham': #Para no perder los ceros al inicio
            nEnt = hammingCheck(n)
        elif b == '2' and t == 'pbt':   #Para no perder los ceros
            nEnt = penta(n)
        else:
            nEnt = bToDec(n, b)
            
            nEnt = decToCod(nEnt, t)

    elif cod == 'bcd':
        
        nEnt = bcdToDec(n)

        if re.search(r"^\d+", t):
            nEnt = decToB(nEnt, t)
  
        nEnt = decToCod(nEnt, t)

    elif cod == 'gry':

        nEnBin = grayToBin(n)

        nEnDec = bToDec(nEnBin, 2)

        if re.search(r"^\d+", t):
            nEnt = decToB(nEnDec, t)

        nEnt = decToCod(nEnDec, t)    

    elif cod == 'ed3':

        nEnDec = ed3ToDec(n)

        if re.search(r"^\d+", t):
            nEnt = decToB(nEnDec, t)

        nEnt = decToCod(nEnt, t)

    elif cod == 'jsn':
        nEnBin = jsnToBin(n)
        nEnt = bToDec(nEnBin, 2)

        if re.search(r"^\d+", t):
            nEnt = decToB(nEnt, t)

        nEnt = decToCod(nEnt, t)

    elif cod == 'par':

        nEnt = bToDec(n, 2)

        if re.search(r"^\d+", t):
            nEnt = decToB(nEnt, t)

        nEnt = decToCod(nEnt, t)
    
    elif cod == 'pbt':
        nEnt = bToDec(n,2)
        if re.search(r"^\d+", t):
            nEnt = decToB(nEnt, t)
            
        nEnt = decToCod(nEnt, t)

    elif cod == 'ham':
        
        nEnt = hammingCheck(n)

        nEnt = hammingToBin(nEnt)
        
        nEnt = bToDec(nEnt, 2)

        if re.search(r"^\d+", t):
            nEnt = decToB(nEnt, t)
            
        nEnt = decToCod(nEnt, t)

    if t in  codigos:
        print('Codigo', codigos_full[codigos.index(t)], ':', nEnt)
    else:
        print('Base', t,':', nEnt)
    
    datos  = input()
        


