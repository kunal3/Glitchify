import random
import binascii
import string
import os
import json
import subprocess
from threading import Thread

def main():

	glitchFuncs = {
		1:	lineSwitch,
		2:	replaceHex,
		3:  echo
		#4:
	}

	#run = 1
	data = {}
	while(1):

		req = json.loads(subprocess.check_output("curl https://glitchify.firebaseio.com/requests.json",shell = True))
		for key in req:
			run = int(req[key]['run'])
			upload = int(req[key]['upload'])
			filename = str(req[key]['filename'])
			modLevel = str(req[key]['modLevel'])

		#upload = 0
		#filename = "monalisa.bmp"
		#modLevel = "Low"
		if run:
			run = 0
			if upload and os.path.splitext(filename)[1][1:] !='bmp':	
				execfile("imgToBmp.py")
				inDir = "imgUpload/"
			if not upload:
				inDir = "imgIn/"
			# NEED TO WAIT HERE FOR IMGTOBMPY to finish
			
			f = open(inDir+filename, "rb")
			image = f.read()
			f.close()
			image = list(image)
			for i in range(0,len(image)):
				image[i] = binascii.hexlify(image[i])
			if modLevel == "Low":
				modChance = 5
			elif modLevel == "Medium":
				modChance = random.randint(7,20)
			else:
				modChance = random.randint(21,100)
			data = {
				'upvote': 0,
				'downvote': 0,
				'filename': filename,
				'filesize': len(image),
				'source': inDir,
				'width': int(image[19]+image[18],16),
				'height': int(image[23]+image[22],16),

				#'func': random.randint( 1, len(glitchFuncs) ),
				'modChance': modChance,
				'lineWidth': int(random.randint(1,100)*(modChance+100)/1000.0+1),
				'linesToMove': int(random.randint(1,100)*(modChance+100)/1000.0 + 1),
			}
			data['toReplace'] = image[random.randint(36, data['filesize'] - 8)]
			while(data['toReplace'] in image[random.randint(0,36)]):
				data['toReplace'] = image[random.randint(36, data['filesize'] - 8)]
			
			data['replaceWith'] = hex(int(data['toReplace'],16)+256)[2:]
			if len(data['replaceWith'])%2:
				data['replaceWith'] = "0"+data['replaceWith']
			#data['replaceWith']= binascii.hexlify(''.join([random.choice(string.ascii_letters + string.digits + ' ') for n in xrange(2)]))
			#difference = abs(int(data['toReplace'],16) - int(data['replaceWith'],16))
			#while difference 			

			directOutput = subprocess.check_output("curl -X POST -d \'"+json.dumps(data)+"\' https://glitchify.firebaseio.com/images.json",shell = True)
			#print data['lineWidth']
			#print data['linesToMove']

			for i in range(0,7):
				if i==0:
					glitched = lineSwitch(list(image), data)
				if i==1:
					glitched = replaceHex(list(image), data)
				if i==2:
					glitched = echo(list(image), data)
				if i==3:
					glitched = lineSwitch(replaceHex(list(image),data),data)
				if i==4:
					glitched = lineSwitch(echo(list(image),data),data)
				if i==5:
					glitched = replaceHex(echo(list(image),data),data)
				if i==6:
					glitched = lineSwitch(echo(replaceHex(list(image),data),data),data)
				Thread(target=writeImage, args=[glitched, data, i]).start()

def writeImage(glitched,data, num):
	f = open('imgOut/'+str(num)+"_output.bmp", "wb")
	s = ""
	for i in range(data['filesize']):
		s+=str(binascii.unhexlify(glitched[i]))
	f.write(s)		
	f.close()

def lineSwitch(image,data):
	totalLines = (int)((len(image) - 50) / float(data['lineWidth']))
	for i in range(50, totalLines-4):   
		if random.randint(1,100) <= data['modChance']:			
			src = i * data['lineWidth']
			dest = random.randint(50, totalLines-4) * data['lineWidth']

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
	
	for i in range(data['filesize']/2, data['filesize']-8):
		if image[i] == data['toReplace']:
			image[i] = data['replaceWith']
	return image

def echo(image, data):
	imageCopy = list(image)
	for i in range(50, data['filesize']-50):
		if random.randint(1,100) <= data['modChance']+50:
			s = hex(int(image[i],16)/2 + int(imageCopy[data['filesize'] - i],16)/2)[2:] 
			if len(s)%2:
				s = "0"+s
			image[i] = s

	return image

main()


