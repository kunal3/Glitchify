from PIL import Image
import os
#code in here to scan folder for pngs

inDirs = ['imgIn/', 'imgUpload/']
for inDir in inDirs:
	for filename in os.listdir(os.getcwd()+"/"+inDir):
		if os.path.splitext(filename)[1][1:] in ['jpg','jpeg','png']:
			file_in = inDir+"/"+filename
			img = Image.open(file_in)

			outFile = filename[0:-len(os.path.splitext(filename)[1][1:])]+"bmp"
			file_out = inDir+"/"+outFile
			img.load()
			if len(img.split()) == 4:
			 	# prevent IOError: cannot write mode RGBA as BMP
			 	r, g, b, a = img.split()
			 	img = Image.merge("RGB", (r, g, b))
			 	img.save(file_out)
			else:
			 	img.save(file_out)
			os.remove(inDir+"/"+filename)