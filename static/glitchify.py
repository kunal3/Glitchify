import random
import binascii
import string
import os
import uuid
import json
import subprocess

def main():

 	inDirs = ['imgIn/', 'imgUpload/']

	glitchFuncs = {
		1:	lineSwitch,
		2:	replaceHex,
		3:  echo
		#4:
	}


	data = {}
	while(1):
		for inDir in inDirs:

			# need some kind of check to only run this if new image added

			for filename in os.listdir(os.getcwd()+"/"+inDir):
				execfile("imgToBmp.py")
				if os.path.splitext(filename)[1][1:] =='bmp':
					f = open(inDir+"/"+filename, "rb")
					image = f.read()
					f.close()
					image = list(image)
					for i in range(0,len(image)):
						image[i] = binascii.hexlify(image[i])
					data = {
						'filename': filename,
						'filesize': len(image),
						'source': inDir,
						'width': int(image[19]+image[18],16),
						'height': int(image[23]+image[22],16),

						'func': random.randint( 1, len(glitchFuncs) ),
						'modChance': random.randint(1,100),
						'lineWidth': (random.randint(1,100)),
						'linesToMove': int(len(image) * random.random()/1000),
						'replaceWith': binascii.hexlify(''.join([random.choice(string.ascii_letters + string.digits + ' ') for n in xrange(3)]))
					}
					data['toReplace'] = image[random.randint(36, data['filesize'] - 8)]
					while(data['toReplace'] in image[random.randint(0,36)]):
						data['toReplace'] = image[random.randint(36, data['filesize'] - 8)]
					key = uuid.uuid1()
					directOutput = subprocess.check_output("curl -X POST -d \'"+json.dumps(data)+"\' https://glitchify.firebaseio.com/images.json",shell = True)
					#os.system("curl -X POST -d \'{\""+str(key)+"\":"+json.dumps(data)+"}\' https://glitchify.firebaseio.com/images.json")
					glitched = glitchFuncs[ data['func'] ](image, data)
					f = open('imgOut/'+data['filename'], "wb")
					s = ""
					for i in range(data['filesize']):
						s+=str(binascii.unhexlify(glitched[i]))
					f.write(s)		
					f.close()

def lineSwitch(image,data):
	totalLines = (int)((len(image) - 36) / float(data['lineWidth']))
	min = int(36 / data['lineWidth']) + (36 % data['lineWidth'] > 0)

	for i in range(min, totalLines-1):  # start at line 4 to not mess up file encoding data 
		if random.randint(1,100) <= data['modChance']:			
			src = i * data['lineWidth']
			dest = random.randint(min, totalLines-1) * data['lineWidth']

			if (src+data['linesToMove'] < data['filesize']) and (dest+data['linesToMove'] < data['filesize']):
			 	for j in range(data['linesToMove']):
			 		temp = image[src+j]
			 		image[src+j] = image[dest+j]
			 		image[dest+j] = temp
	return image

def replaceHex(image,data):
	for i in range(36,data['filesize']/6):
		if image[i] == data['toReplace']:
			image[i] = data['replaceWith']
	
	#replaceWith = binascii.hexlify("  ")
	for i in range(data['filesize']/2, data['filesize']-8):
		if image[i] == data['toReplace']:
			image[i] = data['replaceWith']
	return image

def echo(image, data):
	#return image
	# add fix
	imageCopy = list(image)
	for i in range(36, data['filesize']-4):
		s = hex(int(image[i],16)/2 + int(imageCopy[data['filesize'] - i],16)/2)[2:] 
		#s = "00"
		a = hex(90) 
		if len(s)%2:
			s = "0"+s
		image[i] = s

	return image

main()


