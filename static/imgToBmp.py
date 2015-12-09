from PIL import Image

file_in = "imgInput/fence-echo.jpg"
img = Image.open(file_in)
file_out = "imgInput/fence-echo.bmp"
img.load()
if len(img.split()) == 4:
  # prevent IOError: cannot write mode RGBA as BMP
  r, g, b, a = img.split()
  img = Image.merge("RGB", (r, g, b))
  img.save(file_out)
else:
  img.save(file_out)