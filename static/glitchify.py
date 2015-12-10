import random
import binascii
import string

#import requests
#from firebase import firebase

def main():

 	inDirs = ['imgIn/', 'imgUpload/']

	glitchFuncs = {
		1:	lineSwitch,
		2:	replaceHex,
		3:  echo
		#4:
	}

	data = {}

	for inDir in inDirs:
		for filename in os.listdir(os.getcwd()+"/"+inDir):
			if os.path.splitext(filename)[1][1:] in ['jpg','jpeg','jiff','png','bmp']:
				# imgToBmp.py
				f = open(filename, "rb")
				image = f.read()
				f.close()
				image = list(image)
				data['filesize'] = len(image)
				for i in range(0,data['filesize']):
					image[i] = binascii.hexlify(image[i])

				data = {
					'filename': filename,
					'source': inDir,
					'width': int(image[19]+image[18],16),
					'height': int(image[23]+image[22],16),

					'func': random.randint( 1, len(glitchFuncs) ),
					'modChance': random.randint(1,100),
					'lineWidth': (random.randint(1,100)/100)*width,
					'linesToMove': (random.random()/1000)*data['filesize'],
					'replaceWith': binascii.hexlify(''.join([random.choice(string.ascii_letters + string.digits + ' ') for n in xrange(3)]))
				}

				data['toReplace'] = image[random.randint(36, data['filesize'] - 8)]
				while(data['toReplace'] in image[random.randint(0,36)]):
					data['toReplace'] = image[random.randint(36, data['filesize'] - 8)]

				key = uuid.uuid1()
				result = firebase.post('/imgData', data, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
				print result

				glitched = glitchFuncs[ func ](image, data)
				print 'Ran '+func

				f = open('imgOut/'+data['filename'], "wb")
				s = ''
				for i in range(data['filesize']):
					s+=str(binascii.unhexlify(glitched[i]))
				f.write(s)		
				f.close()

# 	# THIS IS COMMENTED OUT JUST FOR TESTING
# 	#image = glitchFuncs[random.randint(1,len(glitchFuncs))](image, filesize)
	# image = lineSwitch(image, filesize)
	# print "LINESWITCH"

def lineSwitch(image,data):
	# data['modChance'] = 10  # 10% chance of line modification
	# data['lineWidth'] = 100  # how many 2 char hex numbers to group as a line
	totalLines = (len(image) - 36) / data['lineWidth']
	min = int(36 / data['lineWidth']) + (36 % data['lineWidth'] > 0)

	for i in range(min, totalLines-1):  # start at line 4 to not mess up file encoding data 
		if random.randint(1,100) <= data['modChance']:
			# linesToMove = int(totalLines * random.random()/1000) # grabs anywhere from 0.01 to 1% of the file's lines
			# try moving just one line later
			
			src = i * data['lineWidth']
			# linesToMove = linesToMove*data['lineWidth']
			dest = random.randint(min, totalLines-1) * data['lineWidth']

			temp = image[ src : (src + data['lineWidth']) ]
			image[src] = image[ dest : (dest + data['lineWidth']) ]
			image[dest] = temp

			# if (src+linesToMove < data['filesize']) and (dest+linesToMove < data['filesize']):
			# 	for j in range(linesToMove):
			# 		temp = image[src+j]
			# 		image[src+j] = image[dest+j]
			# 		image[dest+j] = temp
	return image

def replaceHex(image,data):
	# toReplace = image[random.randint(36, data['filesize'] - 8)]
	# replaceWith = binascii.hexlify(''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(3)]))
	
	for i in range(36,data['filesize']/6):
		if image[i] == data['toReplace']:
			image[i] = data['replaceWith']
	
	replaceWith = binascii.hexlify("  ")
	for i in range(data['filesize']/2, data['filesize']-8):
		if image[i] == data['toReplace']:
			image[i] = data['replaceWith']
			# try simply adding int values to the hex
	return image

def echo(image, data):
	imageCopy = list(image)
	for i in range(36, data['filesize']-4):
		#s = hex(int(image[i],16)/2 + int(imageCopy[data['filesize'] - i],16)/2)[2:] 
		s = "00"
		if len(s)%2:
			s = "0"+s
		image[i] = s

	return image

main()


