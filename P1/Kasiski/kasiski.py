#! /usr/bin/env python 

#Usage> python .\kasiski.py .\5.1.2_fragmento3.vig

import math
import sys, getopt
import string

ESP_FREQ = {'A': 0.11525, 'B': 0.02215, 'C': 0.04019, 'D': 0.05010,
               'E': 0.12181, 'F': 0.00692, 'G': 0.01768,
               'H': 0.00703, 'I': 0.06247, 'J': 0.00493, 'K': 0.00011, 
               'L': 0.04967, 'M': 0.03157, 'N': 0.06712,
               'O': 0.08683, 'P': 0.02510, 'Q': 0.00877, 'R': 0.06871, 
               'S': 0.07977, 'T': 0.04632, 'U': 0.02927,
               'V': 0.01138, 'W': 0.00017, 'X': 0.00215, 'Y': 0.01008, 
               'Z': 0.00467}

def kasiski(opts, args):
    out = ''
    min = 3
    # Get the options from the command line
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            input = a
        elif o in ("-o", "--output"):
            output = a 
        else:
            assert False, "unhandled option"


    # Dado un fichero de entrada con un texto cifrado, implementar el algotimo de Kasiski para descifrarlo
    # El fichero de entrada debe ser un fichero de texto plano
    # El fichero de salida debe ser un fichero de texto plano
    # El fichero de salida debe contener el texto descifrado
    # Kasiski es un algoritmo de ataque de criptosistemas basado en el análisis de frecuencias de aparición de caracteres
    # en el texto cifrado. El algoritmo de Kasiski se basa en la hipótesis de que la longitud de la clave es menor que la
    # longitud del texto cifrado. El algoritmo de Kasiski consiste en buscar en el texto cifrado las repeticiones de
    # caracteres o grupos de caracteres. Si se encuentran repeticiones, se calcula la distancia entre ellas y se comprueba
    # si la distancia es un múltiplo de la longitud de la clave. Al tener varias repeticiones diferentes con distintas distancias
    # se puede calcular la longitud de la clave como el MCD de todas ellas, a no ser que este sea  uno.
    # Las cadenas que se repiten en el texto tienen que tener una longitud mínima de tres caracteres.

    f = open(input, "r")
    text = f.read()
    f.close()

    fragmentos = []
    encontrados = {}

    for i in range(min, len(text) // 2):
        encontrados[i] = {}
        salir = True
        for j in range(0, len(text)-i):
            v = text[j:j+i]
            if v not in encontrados[i]:
                encontrados[i][v] = 1
            else:
                encontrados[i][v] += 1
                salir = False
        if salir:
            break
        for v in encontrados[i]:
            if encontrados[i][v] > 2:
                fragmentos.append(v)
                
    out += "Length  Count  Word        Factor  Location (distance)\n"
    out += "======  =====  ==========  ======  ===================\n"
    claves = {}
    count={}
    for v in fragmentos:
        k = len(v)
        p = []
        for i in range(len(text)):
            if text[i:i+k] == v:
                p.append(i)
        factor = p[1] - p[0]
        for i in range(2, len(p)):
            factor = math.gcd(factor, p[i] - p[i-1])
        distancias = ""
        for i in range(len(p)):
            distancias += "%d " % p[i]
            if i > 0:
                distancias += "(%d) " % (p[i] - p[i-1])
        if(not factor in count):
            count[factor]=0
        count[factor]+=1
        out += "%6d  %5d  %10s  %6d  %s\n" % (k, encontrados[k][v], v, factor, distancias)
    
    print(out)
    #Freq Analysis
    del count[1] # Borramos el mcd==1
    print(count)
    K=max(count,key=count.get)
    print("Key length = "+ str(K))
    l=[] 
    for y in range(K):
        l.append([])
    for i in range(len(text)):
        l[i % K].append(text[i])
    #Obtenemos la clave en base a su longitud
    K=get_key(text,K)
    print("Key = " + K)
    out=''
    #En base a la clave, obtenemos el descifrado
    for i in range(len(text)):
        c=ord(text[i])-65
        out=out+ list(ESP_FREQ.keys())[c-(ord(K[i%len(K)])-65)]

    print("Result: " + out)
    f = open(output, "w")
    f.write(out)
    f.close()

#Calcula las frecuencias de todas las letras en un texto
def get_letter_freq(text):
    text_upper = text.upper()
    letter_counts = {} #Contamos las letras
    for index, letter in enumerate(string.ascii_uppercase):
        letter_counts[letter] = text_upper.count(letter)
    #Calculamos las frecuencias
    freq = {letter: count/len(text) for letter, count in letter_counts.items()} 
    return freq

#Mueve hacia atras el texto el amount especificado
#Más bien aplica el desplazamiento Cesar inverso del valor key
#Es decir devuelve el texto descifrado Cesar con clave key
def inverse_Cesar(text, key):
    out = ''
    letters = string.ascii_uppercase
    for letter in text:
        out += letters[(letters.index(letter)-key) % len(letters)]
    return out

#Obtiene la clave comparando las frecuencias del texto con las del lenguaje
#en todos los posibles casos de Cesar, para poder calcular con mayor
#precision el menor margen de error
def _find_key_letter(text, lf):
    max_diff = 0
    key_letter = ''
    #Para cada letra en el alfabeto
    for count, letter in enumerate(string.ascii_uppercase):
        #Obtenemos el texto Cesar descifrado
        shifted = inverse_Cesar(text=text, key=count)
        #Calculamos la letra en base a la comparacion de las frecuencias
        diff = sum([(ESP_FREQ[letter]-lf[letter]) for letter in shifted])
        #Esto nos da una puntuacion, la mayor puntuacion es la letra que gana
        if diff > max_diff:
            max_diff = diff
            key_letter = letter
    return key_letter

#Obtiene la clave en base a la longitud de clave de un texto cifrado con Vigenere
def get_key(cyphertext, key_len):
    key = ''
    #Dividimos el texto en bloques de longitud de la clave
    blocks = [cyphertext[i:i+key_len] for i in range(0, len(cyphertext)-key_len, key_len)]
    #En base a los bloques creamos las columnas organizadas por longitud de clave
    group_size = len(blocks[0])
    columns = []
    for letter_count in range(group_size):
        column = ''
        for group_count in range(len(blocks)):
            column += blocks[group_count][letter_count]
        columns.append(column)
    #Calculamos las frecuencias
    freq = get_letter_freq(text=cyphertext)
    for column in columns:
        key += _find_key_letter(text=column, lf=freq)
    return key
        

def usage():
    # Print the usage of the program

    # HELP PAGE
    #

    HELP_PAGE = ""
    print(HELP_PAGE)

def main():
    try:
        # Get the arguments from the command line
        opts, args = getopt.getopt(sys.argv[1:], "i:o:h", ["input=", "output=", "help"])
    except getopt.GetoptError as err:
        # Print help information and exit:
        print(err)  # Will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    kasiski(opts, args)
    
if __name__ == "__main__":
    main()
