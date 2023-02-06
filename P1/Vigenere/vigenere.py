#! /usr/bin/env python 
import sys, getopt

def vigenere(options, arguments):
    # Get a full text from an archive and cipher it with vigenere cipher

    #Usage:
    #      vigenere.py [OPTIONS] INPUT_FILE KEY    
    #      vigenere.py [OPTIONS] -i INPUT_FILE -k KEY

    # OPTIONS: 
    #   -i INPUT_FILE, --input=INPUT_FILE -> Set the name of the input file
    #   -k KEY, --key=KEY -> Set the key to the cipher
    #   -o OUTPUT_FILE, --output=OUTPUT_FILE -> Set the name of the output file, default vigenere.vig
    #   -h, --help -> Display manual page

    ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    # LENGTH = len(ALPHABET)
    # CIPHER_ALPHABET = []
    dec      = False
    output   = "vigenere.vig"

    for o, a in options:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            input = a
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-k", "--key"):
            key = a
        elif o in ("-d", "-decipher"):
            dec = True 
        else:
            assert False, "unhandled option"

    if 'input' not in locals():
        try:
            input = arguments[0]
        except:
            print("INPUT is mandatory")
            usage()
            sys.exit()

    if 'key' not in locals():
        try:
            key = arguments[1]
        except:
            try:
                key = arguments[0]
            except:
                print("KEY is mandatory")
                usage()
                sys.exit()
    
    # Take the key and prepare the cipher code
    
    key = key.upper()
    for i in range(len(key)):
        if key[i] not in ALPHABET:
            print("The key must be only letters")
            sys.exit()

    # Generamos una lista de listas con el alfabeto rotado tantas veces como letras tenga la clave, puede dar problemas si la clave es muy larga 
    # CIPHER = []
    # key = list(key)

    # for i in range(len(key)):
    #     CIPHER.append(ALPHABET[ALPHABET.index(key[i])::]+ALPHABET[:ALPHABET.index(key[i])])
    
    # Utilizamos la fórmula matemática de Vigenere para crear el cifrado, pasamos la clave a int y también el texto y con la función chr() pasamos el resultado a string
    key = list(key)
 
    if dec:
        decipher(key, input, output)
    else:
        cipher(key, input, output)
    
    
def cipher(key, input, output):
    # Read from the given input where the text should be and cipher it 

    f = open(input, "r")
    text = f.read()
    f.close()

    text = text.upper()
    text_as_int = [ord(i) for i in text]
    key_as_int = [ord(i) for i in key]
    ciphered = ""

    for x in range(len(text_as_int)):
        value = (text_as_int[x] + key_as_int[x%len(key)])%26
        ciphered += chr(value + 65) #Para obtener las letras mayúsculas utilizamos +65 , para las minúsculas +97


    print(ciphered)

    f = open(output, "w")
    f.write(ciphered)
    f.close()


def decipher(key, input, output):
    # Read from the given input where the text should be and decipher it 

    f = open(input, "r")
    text = f.read()
    f.close()

    text = text.upper()
    text_as_int = [ord(i) for i in text]
    key_as_int = [ord(i) for i in key]
    deciphered= ""

    for x in range(len(text_as_int)):
        value = (text_as_int[x] - key_as_int[x%len(key)])%26
        deciphered += chr(value + 65) #Para obtener las letras mayúsculas utilizamos +65 , para las minúsculas +97


    print(deciphered)

    f = open(output, "w")
    f.write(deciphered)
    f.close()
    


def usage():
    help_page = "Usage:\n\t vigenere.py [OPTIONS] INPUT_FILE KEY\n\t vigenere.py [OPTIONS] -i INPUT_FILE -k KEY\n\nOPTIONS:\n\t -i INPUT_FILE, --input=INPUT_FILE -> Set the name of the input file\n\t -k KEY, --key=KEY -> Set the key\n\t -o OUTPUT_FILE, --output=OUTPUT_FILE -> Set the name of the output file, default vigenere.vig\n\t -h, --help -> Display manual page"
    print( help_page )
        
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:k:o:dh", ["input=", "key=", "output=", "decipher", "help"])
    except getopt.GetoptError as err:
        # Print help information and exit:
        print(err)  # Will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    vigenere(opts, args)
    
if __name__ == "__main__":
    main()
