#! /usr/bin/env python 
import sys, getopt

def monoalfabeto(options, arguments):
    # Get a full text from an archive and cipher it with our monoalphabet cipher
    # How the cipher works:
    #  The cipher takes a key that is a number, based on that number it creates a cipher alphabet following the next rules:
    #   1. The key is divided by 26, if the result is higher than 1 then the cipher will be repeated that number of times, each time basing the cipher on the previous one
    #   2. The key is divided by 26 and the remainder is used to cipher the first letter of the alphabet
    #   3. The remainder gets incremented by remainder-1 and the result is used to cipher the second letter of the alphabet
    #   4. The result gets incremented by remainder-2 and the result is used to cipher the third letter of the alphabet
    #   5. When the remainder reaches 0 the cipher starts again from the key and the process is repeated
    #  Normally the cipher alphabet is created taking the letters of the alphabet basing on the normal previous cipher, but when it reaches the end of the previous one,
    #  it starts again with the inverted previous alphabet.
    #  Other feature of the cipher is that when a letter is already in the cipher alphabet, it is not added again, 
    #  instead the cipher alphabet is created with the next letter of the alphabet that is not used, following the alphabet that it is using,
    #  doesn't matter if it is the normal or the inversed one.
    #
    #  CAUTION:
    # The cipher is based on module operations, as a result, every key that is a multiple of 26 will have the base alphabet as cipher alphabet.

    # Usage:
    #      monoalfabeto.py [OPTIONS] INPUT_FILE KEY    
    #      monoalfabeto.py [OPTIONS] -i INPUT_FILE -k KEY

    # OPTIONS: 
    #   -i INPUT_FILE, --input=INPUT_FILE -> Set the name of the input file
    #   -k KEY, --key=KEY -> Set the key to the cipher
    #   -o OUTPUT_FILE, --output=OUTPUT_FILE -> Set the name of the output file, default monoalfabeto.mono
    #   -s, --show -> Show progress of the cipher
    #   -v, --verbose -> Verbose mode
    #   -h, --help -> Display manual page

    ALPHABET          = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    INVERSE_ALPHABET  = ['Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
    LENGTH            = len(ALPHABET)
    CIPHER_ALPHABET   = []
    CIPHER_ALPHABET_2 = []

    # Variables to store the options decipher and inverse alphabet
    dec     = False
    inverso = False

    # Get the options from the command line
    for o, a in options:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            input = a
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-k", "--key"):
            b = int(a)
            if b >= 1:
                key = b
        elif o in ("-d", "--decipher"):
            dec = True 
        else:
            assert False, "unhandled option"

    # If the options where not given as options, get them from the arguments
    # Input must always be the first argument
    if 'input' not in locals():
        try:
            input = arguments[0]
        except:
            print("INPUT is mandatory")
            usage()
            sys.exit()

    # The key must be among the other arguments and should be the second one
    if 'key' not in locals():
        try:
            for a in arguments:
                try:
                    b = int(a)
                    if b >= 1:
                        key = b
                        break
                except:
                    continue
            if "key" not in locals():
                raise("KEY is mandatory")
        except:
            print("KEY is mandatory")
            usage()
            sys.exit()
    
    # contador = int((key/26)+1)

    # for x in range(contador):
    #     if x == 0:
    #         for i in range(LENGTH):
    #             if i == 0:
    #                 next = key % LENGTH
    #             else:
    #                 next = next + key % LENGTH
    #             if ALPHABET[next%LENGTH] in CIPHER_ALPHABET:
    #                 next = next+1
    #                 CIPHER_ALPHABET.append(ALPHABET[next%LENGTH])
    #             else:
    #                 CIPHER_ALPHABET.append(ALPHABET[next%LENGTH])
    #     else:
    #         if (x % 2 == 0):
    #             CIPHER_ALPHABET.clear()
    #             for i in range(LENGTH):
    #                 if i == 0:
    #                     next = key % LENGTH
    #                 else:
    #                     next = next + key % LENGTH
    #                 if CIPHER_ALPHABET_2[next%LENGTH] in CIPHER_ALPHABET:
    #                     next = next+1
    #                     CIPHER_ALPHABET.append(CIPHER_ALPHABET_2[next%LENGTH])
    #                 else:
    #                     CIPHER_ALPHABET.append(CIPHER_ALPHABET_2[next%LENGTH])
    #         else:
    #             CIPHER_ALPHABET_2.clear()
    #             for i in range(LENGTH):
    #                 if i == 0:
    #                     next = key % LENGTH
    #                 else:
    #                     next = next + key % LENGTH
    #                 if CIPHER_ALPHABET[next%LENGTH] in CIPHER_ALPHABET_2:
    #                     next = next+1
    #                     CIPHER_ALPHABET_2.append(CIPHER_ALPHABET[next%LENGTH])
    #                 else:
    #                     CIPHER_ALPHABET_2.append(CIPHER_ALPHABET[next%LENGTH])

    # Take the key and prepare the cipher code
    # The key is divided by 26 and thats the number of times the alphabet should be ciphered
    contador = int((key/26)+1)
    # Take the key module 26 to get the remainder and start ciphering
    key  = key % LENGTH
    
    # If the key is 0, the cipher is the same as the alphabet
    if key == 1:
        desc = key
    elif key == 0:
        desc = 1
    else:
        desc = key-1

    # Loop to cipher the alphabet the number of times that the key/26 indicates
    for x in range(contador):
        # If it is the first time, cipher basing on the alphabet
        if x == 0:
            for i in range(LENGTH):
                if i == 0:
                    # The first letter is the key
                    next = key 
                else:
                    # The next letter is the previous one plus the decreasing key
                    next = next + desc
                    desc = desc-1 

                    # The number we add should never be 0, so if it is, we start with the key again
                    if desc == 0:
                        if key == 0:
                            desc = 1
                        else:
                            desc = key
                
                # Every time the index is bigger than 26 we use the inverse alphabet instead of the normal one
                if next > 26 :
                    inverso = not inverso
                    next = next % LENGTH
               
                # Use the inversed alphabet if the flag is set
                if inverso:
                    # Check the letter is not already in the cipher alphabet, if it is look for the next one that is not added
                    if INVERSE_ALPHABET[next%LENGTH] in CIPHER_ALPHABET:
                        for j in range(next%LENGTH, LENGTH*2):
                            if INVERSE_ALPHABET[j%LENGTH] not in CIPHER_ALPHABET:
                                CIPHER_ALPHABET.append(INVERSE_ALPHABET[j%LENGTH])
                                break
                    else:
                        CIPHER_ALPHABET.append(INVERSE_ALPHABET[next%LENGTH])
                else:
                    # Check the letter is not already in the cipher alphabet, if it is look for the next one that is not added
                    if ALPHABET[next%LENGTH] in CIPHER_ALPHABET:
                        for j in range(next%LENGTH, LENGTH*2):
                            if ALPHABET[j%LENGTH] not in CIPHER_ALPHABET:
                                CIPHER_ALPHABET.append(ALPHABET[j%LENGTH])
                                break
                    else:
                        CIPHER_ALPHABET.append(ALPHABET[next%LENGTH])

        # If it is not the first time, cipher basing on the previous ciphered alphabet
        else:
            if (x % 2 == 0):
                
                CIPHER_ALPHABET.clear()

                CIPHER_ALPHABET_2.reverse()
                INVERSE_ALPHABET = CIPHER_ALPHABET_2.copy()
                CIPHER_ALPHABET_2.reverse()
                
                for i in range(LENGTH):
                    if i == 0:
                        # The first letter is the key
                        next = key 
                    else:
                        # The next letter is the previous one plus the decreasing key
                        next = next + desc
                        desc = desc-1 

                        # The number we add should never be 0, so if it is, we start with the key again
                        if desc == 0:
                            if key == 0:
                                desc = 1
                            else:
                                desc = key

                    # Every time the key is bigger than 26 we use the inverse alphabet instead of the normal one
                    if next > 26 :
                        inverso = not inverso
                        next = next % LENGTH
                    
                    # Use the inversed alphabet if the flag is set
                    if inverso:
                        # Check the letter is not already in the cipher alphabet, if it is look for the next one that is not added
                        if INVERSE_ALPHABET[next%LENGTH] in CIPHER_ALPHABET:
                            for j in range(next%LENGTH, LENGTH*2):
                                if INVERSE_ALPHABET[j%LENGTH] not in CIPHER_ALPHABET:
                                    CIPHER_ALPHABET.append(INVERSE_ALPHABET[j%LENGTH])
                                    break
                        else:
                            CIPHER_ALPHABET.append(INVERSE_ALPHABET[next%LENGTH])
                    else:
                        # Check the letter is not already in the cipher alphabet, if it is look for the next one that is not added
                        if CIPHER_ALPHABET_2[next%LENGTH] in CIPHER_ALPHABET:
                            for j in range(next%LENGTH, LENGTH*2):
                                if CIPHER_ALPHABET_2[j%LENGTH] not in CIPHER_ALPHABET:
                                    CIPHER_ALPHABET.append(CIPHER_ALPHABET_2[j%LENGTH])
                                    break
                        else:
                            CIPHER_ALPHABET.append(CIPHER_ALPHABET_2[next%LENGTH])
            else:
                CIPHER_ALPHABET_2.clear()

                CIPHER_ALPHABET.reverse()
                INVERSE_ALPHABET = CIPHER_ALPHABET.copy()
                CIPHER_ALPHABET.reverse()
            
                for i in range(LENGTH):
                    if i == 0:
                        # The first letter is the key
                        next = key
                    else:
                        # The next letter is the previous one plus the decreasing key
                        next = next + desc
                        desc = desc-1 

                        # The number we add should never be 0, so if it is, we start with the key again
                        if desc == 0:
                            if key == 0:
                                desc = 1
                            else:
                                desc = key
                    # Every time the key is bigger than 26 we use the inverse alphabet instead of the normal one
                    if next > 26 :
                        inverso = not inverso
                        next = next % LENGTH   

                    # Use the inversed alphabet if the flag is set
                    if inverso:
                        # Check the letter is not already in the cipher alphabet, if it is look for the next one that is not added
                        if INVERSE_ALPHABET[next%LENGTH] in CIPHER_ALPHABET_2:
                            for j in range(next%LENGTH, LENGTH*2):
                                if INVERSE_ALPHABET[j%LENGTH] not in CIPHER_ALPHABET_2:
                                    CIPHER_ALPHABET_2.append(INVERSE_ALPHABET[j%LENGTH])
                                    break
                        else:
                            CIPHER_ALPHABET_2.append(INVERSE_ALPHABET[next%LENGTH])
                    else:
                        # Check the letter is not already in the cipher alphabet, if it is look for the next one that is not added
                        if CIPHER_ALPHABET[next%LENGTH] in CIPHER_ALPHABET_2:
                            for j in range(next%LENGTH, LENGTH*2):
                                if CIPHER_ALPHABET[j%LENGTH] not in CIPHER_ALPHABET_2:
                                    CIPHER_ALPHABET_2.append(CIPHER_ALPHABET[j%LENGTH])
                                    break
                        else:
                            CIPHER_ALPHABET_2.append(CIPHER_ALPHABET[next%LENGTH])

    # Once the cipher alphabet is created, take the one that belongs to the key
    if contador%2!=0:
        CIPHER = dict(zip(ALPHABET, CIPHER_ALPHABET))
    else:
        CIPHER = dict(zip(ALPHABET, CIPHER_ALPHABET_2))

    #If the decryption flag is set, decipher the text given, otherwise cipher it
    if dec:
        if 'output' not in locals():
            output = "monoalfabeto.txt"
        decipher(ALPHABET, CIPHER, input, output)
    else:
        if 'output' not in locals():
            output = "monoalfabeto.mono"
        cipher(ALPHABET, CIPHER, input, output)
    
    
def cipher(ALPHABET, CIPHER, input, output):
    # Read from the given input where the text should be and cipher it 

    f = open(input, "r")
    text = f.read()
    f.close()

    text = text.upper()
    txt = []

    # Take the whole text as a list of characters
    for letter in text:
        if letter in ALPHABET:
            txt.append(letter)

    cifrado = ""

    # Loop over the text and cipher it using the dictionary that has both, the normal alphabet and the ciphered one
    for x in txt:
        letra = CIPHER[x]
        cifrado += letra

    # Write the ciphered text to the given output
    f = open(output, "w")
    f.write(cifrado)
    f.close()

def decipher(ALPHABET, CIPHER, input, output):
    # Read from the given input where the text should be and decipher it 

    f = open(input, "r")
    text = f.read()
    f.close()

    text = text.upper()
    txt = []

    # Take the whole text as a list of characters
    for letter in text:
        if letter in ALPHABET:
            txt.append(letter)

    deciphered = ""

    # Loop over the text and decipher it using the dictionary that has both, the normal alphabet and the ciphered one
    for x in txt:
        for key, value in CIPHER.items():
            if x == value:
                deciphered += key

    # Write the deciphered text to the given output
    f = open(output, "w")
    f.write(deciphered)
    f.close()


def usage():
    # Print the usage of the program

    # HELP PAGE
    # Get a full text from an archive and cipher it with our monoalphabet cipher
    # How the cipher works:
    #  The cipher takes a key that is a number, based on that number it creates a cipher alphabet following the next rules:
    #   1. The key is divided by 26, if the result is higher than 1 then the cipher will be repeated that number of times, each time basing the cipher on the previous one
    #   2. The key is divided by 26 and the remainder is used to cipher the first letter of the alphabet
    #   3. The remainder gets incremented by remainder-1 and the result is used to cipher the second letter of the alphabet
    #   4. The result gets incremented by remainder-2 and the result is used to cipher the third letter of the alphabet
    #   5. When the remainder reaches 0 the cipher starts again from the key and the process is repeated
    #  Normally the cipher alphabet is created taking the letters of the alphabet basing on the normal previous cipher, but when it reaches the end of the previous one,
    #  it starts again with the inverted previous alphabet.
    #  Other feature of the cipher is that when a letter is already in the cipher alphabet, it is not added again, 
    #  instead the cipher alphabet is created with the next letter of the alphabet that is not used, following the alphabet that it is using,
    #  doesn't matter if it is the normal or the inversed one.
    #
    #  CAUTION:
    # The cipher is based on module operations, as a result, every key that is a multiple of 26 will have the base alphabet as cipher alphabet.

    # Usage:
    #      monoalfabeto.py [OPTIONS] INPUT_FILE KEY    
    #      monoalfabeto.py [OPTIONS] -i INPUT_FILE -k KEY

    # OPTIONS: 
    #   -i INPUT_FILE, --input=INPUT_FILE -> Set the name of the input file
    #   -k KEY, --key=KEY -> Set the key to the cipher
    #   -o OUTPUT_FILE, --output=OUTPUT_FILE -> Set the name of the output file, default monoalfabeto.mono
    #   -s, --show -> Show progress of the cipher
    #   -v, --verbose -> Verbose mode
    #   -h, --help -> Display manual page

    HELP_PAGE = "Get a full text from an archive and cipher it with our monoalphabet cipher\nHow the cipher works:\n The cipher takes a key that is a number, based on that number it creates a cipher alphabet following the next rules:\n  1. The key is divided by 26, if the result is higher than 1 then the cipher will be repeated that number of times, each time basing the cipher on the previous one\n  2. The key is divided by 26 and the remainder is used to cipher the first letter of the alphabet\n  3. The remainder gets incremented by remainder-1 and the result is used to cipher the second letter of the alphabet\n  4. The result gets incremented by remainder-2 and the result is used to cipher the third letter of the alphabet\n  5. When the remainder reaches 0 the cipher starts again from the key and the process is repeated\n Normally the cipher alphabet is created taking the letters of the alphabet basing on the normal previous cipher, but when it reaches the end of the previous one,\n it starts again with the inverted previous alphabet.\n Other feature of the cipher is that when a letter is already in the cipher alphabet, it is not added again, \n instead the cipher alphabet is created with the next letter of the alphabet that is not used, following the alphabet that it is using,\n doesn't matter if it is the normal or the inversed one.\n\n CAUTION:\n The cipher is based on module operations, as a result, every key that is a multiple of 26 will have the base alphabet as cipher alphabet.\n\n Usage:\n     monoalfabeto.py [OPTIONS] INPUT_FILE KEY\n     monoalfabeto.py [OPTIONS] -i INPUT_FILE -k KEY\n\n OPTIONS:\n  -i INPUT_FILE, --input=INPUT_FILE -> Set the name of the input file\n  -k KEY, --key=KEY -> Set the key to the cipher\n  -o OUTPUT_FILE, --output=OUTPUT_FILE -> Set the name of the output file, default monoalfabeto.mono\n  -s, --show -> Show progress of the cipher\n  -v, --verbose -> Verbose mode\n  -h, --help -> Display manual page"
    print(HELP_PAGE)
        
def main():
    try:
        # Get the arguments from the command line
        opts, args = getopt.getopt(sys.argv[1:], "i:k:o:dh", ["input=", "key=", "output=", "decipher", "help"])
    except getopt.GetoptError as err:
        # Print help information and exit:
        print(err)  # Will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    monoalfabeto(opts, args)
    
if __name__ == "__main__":
    main()
