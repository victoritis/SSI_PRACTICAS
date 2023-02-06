#!/usr/bin/env python
#

# import modules used here -- sys is a very standard one
import sys, argparse, logging
import codecs

SIZE_X=10

# Gather our code in a main() function
def main(args, loglevel):
	logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

	# TODO RC4 Algorithm
	K=args.KEY
	f=cipher
	if(args.decipher):
		print("The decipher code is: " + decipher(K))
	else:		
		print("The final result in hexadecimal is: " + cipher(K))
swapped=[]

def print_binL(msg, L):#Formatting to print Lists with colors using swapped global var
	global swapped
	print(msg + '\n     [\t',end='')
	for i in range(int(len(L)/8)):
		for j in range(SIZE_X):
			pos=i*SIZE_X+j
			msg=int(bin(L[pos])[2:])
			form="%08d"
			if(pos in swapped):
				form='\033[95m'+"%08d"+'\033[0m' #Changing color to RED
			if(pos==len(L)-1):
				print(form % msg,end="  ]\n")
				return None
			print(form % msg,end=", ")
		print()
		print("",end="\t")
	print()
	return None

def KSA(K):
	keylen=len(K)
	S=[]
	T=[]
	#Initialization
	for i in range(256):
		S.append(i)
		T.append(K[i % keylen])
	print_binL("Initial value of S: ",S)
	#print(T)
	j = 0;
	for i in range(256):
		j = (j + S[i] + T[i]) % 256
		S[i], S[j] = S[j], S[i] 
	print_binL("Value of S after initial state: ",S)
	return S

def PRGA(S):
	#Stream generation
	i=0
	j=0
	while(True):
		i = (i + 1) % 256
		j = (j + S[i]) % 256

		global swapped # Global variable to control output printing
		swapped=[i,j]
		S[i], S[j] = S[j], S[i]
		print_binL("Value of S after keystream generation: ",S)
		t = (S[i] + S[j]) % 256
		k = S[t];
		yield k

def get_keystream(key):
    S = KSA(key)
    return PRGA(S)

def cipher(key):
	#Key is in Hex
	key= codecs.decode(key, 'hex_codec')
	key= [c for c in key]
	keystream=get_keystream(key)
	out=[]
	while(True):
		m=input("Write next message character: \n")
		if(len(m)==0):
			return ''.join(out)
		c=m[0]
		print("\n")
		print("ASCII value of "+ c+ ": "+ str(ord(c)))
		print("Binary value of "+ c+ ": "+ str(bin(ord(c)))[2:])
		tmpkeystream=next(keystream)
		tmp = (ord(c) ^ tmpkeystream)
		out.append("%02X" % tmp)
		print("Keystream value: "+ str(bin(tmpkeystream))[2:])
		print("Binary value of cipher character: "+ str(bin(tmp))[2:])
		print("Hexadecimal value of cipher character: "+ "%02X" % tmp)

def decipher(key):
	msg= input("Write cipher message (in hexadecimal): \n")
	key= codecs.decode(key, 'hex_codec') #Change from Hex to Int
	key= [c for c in key]
	keystream=get_keystream(key)
	#Using bytes to Avoid Errors with ASCII conversion
	out=[]
	#msg=bytes.fromhex(msg).decode("utf-8") #Change from Hex to ASCII
	msg=bytes.fromhex(msg)
	for c in msg:
		out.append("%02X" % (c ^ next(keystream)))
	out=codecs.decode(''.join(out), 'hex_codec').decode('ASCII')
	print("ASCII value of decipher code is: "+ ''.join(str(ord(c)) for c in out))
	return out
 
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
	parser = argparse.ArgumentParser( 
	                                description = "Ciphers a message using RC4 Encryption Algorithm. " )

	parser.add_argument(
	                  "-d",
	                  "--decipher",
	                  help = "Decipher RC4",
	                  action="store_true")
	parser.add_argument(
	                  "KEY",
	                  help="Sets key to cipher"
	                  ,metavar="KEY")
	args = parser.parse_args()
	try:
		codecs.decode(args.KEY, 'hex_codec')
	except ValueError as e:
		print("KEY must be an hexadecimal number!")
		quit()

	loglevel = logging.INFO

	main(args, loglevel)