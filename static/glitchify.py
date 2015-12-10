import random
import binascii
import string

# #import requests
# #from firebase import firebase

# #import uuid

# #fb = firebase.FirebaseApplication('https://glitchify.firebaseio.com', None)

def main():

 	filename = "imgIn/michael.bmp"
 	print "HI MICAEHL"
# 	# ADD CODE HERE TO CALL IMG_TO_BMP
# 	# NO ERROR CHECK ON FILESIZE LARGER THAN MACHINE'S MEMORY
# 	
	f = open(filename, "rb")
	image = f.read()
	f.close()
	print "FUCKING OPEN THIS FUCKING FILE" 
 	image = list(image)
 	filesize = len(image)
 	for i in range(0,filesize):
 		image[i] = binascii.hexlify(image[i])
	#here
	glitchFuncs = {
		1:	lineSwitch,
		2:	replaceHex,
		3:  echo
		#4:
	}

	widthPixels =  int(image[19]+image[18],16)
	width = widthPixels*3
	lengthPixels =  int(image[23]+image[22],16)
	length = lengthPixels*3

# 	# THIS IS COMMENTED OUT JUST FOR TESTING
# 	#image = glitchFuncs[random.randint(1,len(glitchFuncs))](image, filesize)
# 	#image = echo(image, filesize)

	f = open("imgOut/output.bmp", "wb")
	s = ""
	for i in range(filesize):
		s+=str(binascii.unhexlify(image[i]))
	f.write(s)		
	f.close()

# #	key = uuid.uuid1()
# #	result = firebase.post('/imgData', image, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
# #	print result

def lineSwitch(image,filesize):
	pass
# 	modificationChance = 10  # 10% chance of line modification
# 	lineWidth = 100  # how many 2 char hex numbers to group as a line
# 	totalLines = len(image)/lineWidth

# 	for i in range(4, totalLines):  # start at line 4 to not mess up file encoding data 
# 		if random.randint(1,100) <= modificationChance:
# 			linesToMove = int(totalLines * random.random()/1000) # grabs anywhere from 0.01 to 1% of the file's lines
# 			# try moving just one line later
			
# 			source = i*lineWidth
# 			linesToMove = linesToMove*lineWidth
# 			destination = random.randint(4, totalLines)*lineWidth

# 			if (source+linesToMove < filesize) and (destination+linesToMove < filesize):
# 				for j in range(linesToMove):
# 					temp = image[source+j]
# 					image[source+j] = image[destination+j]
# 					image[destination+j] = temp
# 	return image

def replaceHex(image,filesize):
	pass
# 	toReplace = image[random.randint(36, filesize - 8)]
# 	replaceWith = binascii.hexlify(''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(3)]))
	
# 	for i in range(36,filesize/6):
# 		if image[i]==toReplace:
# 			image[i]=replaceWith
	
# 	replaceWith = binascii.hexlify("  ")
# 	for i in range(filesize/2, filesize-8):
# 		if image[i]==toReplace:
# 			image[i]=replaceWith
# 			# try simply adding int values to the hex
# 	return image

def echo(image, filesize):
	pass
# #	copyChance = 5
# 	imageCopy = list(image)
# 	for i in range(36, filesize-4):
# #		if random.randint(1,100) <= copyChance:
# 			s = hex(int(image[i],16)/2 + int(imageCopy[filesize - i],16)/2)[2:]
# 			if len(s)%2:
# 				s = "0"+s
# 			image[i] = s

# 	return image

main()


