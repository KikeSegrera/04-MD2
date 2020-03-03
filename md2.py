#MD2
import fileinput

def padding(text):
	'''
	Codifica el mensaje a UTF-8 (para trabajar con los valores de los bytes)
	y agrega los bits necesarios para el padding del mismo
	text : mensaje a procesar
	'''
	text = text.replace('\"','')
	text = list(text.encode('utf-8'))
	toadd = 16 - (len(text) % 16)
	pad = [toadd for _ in range(toadd)]
	text += pad
	return text

def checksum(text,S):
	'''
	Realiza la checksum del mensaje agregando 16 bytes al final del mismo
	text : mensaje con padding incluido
	S : arreglo para permutación
	'''
	L,C = 0,[0 for _ in range(16)]
	for i in range(len(text)//16):
		for j in range(16):
			c = text[16 * i + j]
			C[j] = C[j] ^ S[c ^ L]
			L = C[j]
	return text + C

def hashfunc(text,S):
	'''
	Función hash de MD2, realiza un intercambio de bytes en el mensaje, además
	de operaciones XOR con sus bytes y los de la permutación S
	text : mensaje con checksum incluido
	S : arreglo para permutación
	'''
	X = [0 for _ in range(48)]
	for i in range (len(text)//16):
		for j in range(16):
			X[j + 16] = text[16 * i + j]
			X[j + 32] = X[j + 16] ^ X[j]
		t = 0
		for j in range(18):
			for k in range(48):
				t = X[k] ^ S[t]
				X[k] = t
			t = (t + j) % 256
	return X[:16]

def hexa(text):
	"""
	Convierte una cadena de números decimales a hexadecimales de 2 dígitos 
	text : cadena de números a convertir
	"""
	texth = ''
	for c in text:
		h = hex(c)[2:]
		if len(h) < 2:
			h = '0' + h
		texth += h
	return texth

def md2(text):
	'''
	Realiza el algoritmo MD2 utilizando las funciones anteriores
	text : mensaje al que se le quiere aplicar el hash
	'''
	S = [
		41, 46, 67, 201, 162, 216, 124, 1, 61, 54, 84, 161, 236, 240, 6,
		19, 98, 167, 5, 243, 192, 199, 115, 140, 152, 147, 43, 217, 188,
		76, 130, 202, 30, 155, 87, 60, 253, 212, 224, 22, 103, 66, 111, 24,
		138, 23, 229, 18, 190, 78, 196, 214, 218, 158, 222, 73, 160, 251,
		245, 142, 187, 47, 238, 122, 169, 104, 121, 145, 21, 178, 7, 63,
		148, 194, 16, 137, 11, 34, 95, 33, 128, 127, 93, 154, 90, 144, 50,
		39, 53, 62, 204, 231, 191, 247, 151, 3, 255, 25, 48, 179, 72, 165,
		181, 209, 215, 94, 146, 42, 172, 86, 170, 198, 79, 184, 56, 210,
		150, 164, 125, 182, 118, 252, 107, 226, 156, 116, 4, 241, 69, 157,
		112, 89, 100, 113, 135, 32, 134, 91, 207, 101, 230, 45, 168, 2, 27,
		96, 37, 173, 174, 176, 185, 246, 28, 70, 97, 105, 52, 64, 126, 15,
		85, 71, 163, 35, 221, 81, 175, 58, 195, 92, 249, 206, 186, 197,
		234, 38, 44, 83, 13, 110, 133, 40, 132, 9, 211, 223, 205, 244, 65,
		129, 77, 82, 106, 220, 55, 200, 108, 193, 171, 250, 36, 225, 123,
		8, 12, 189, 177, 74, 120, 136, 149, 139, 227, 99, 232, 109, 233,
		203, 213, 254, 59, 0, 29, 57, 242, 239, 183, 14, 102, 88, 208, 228,
		166, 119, 114, 248, 235, 117, 75, 10, 49, 68, 80, 180, 143, 237,
		31, 26, 219, 153, 141, 51, 159, 17, 131, 20
	]

	finalhash = hexa(hashfunc(checksum(padding(text),S),S))
	return finalhash

lines = []

for line in fileinput.input():
	line = line.replace('\n','')
	lines.append(line)

print(md2(lines[0]))