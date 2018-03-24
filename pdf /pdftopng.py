from PythonMagick import Image
 
os.environ["MAGICK_HOME"] = r"path_to_ImageMagick"
 
file = "my.pdf"
to = file.replace(".pdf",".png")
 
p = PythonMagick.Image()    
p.density('300')
p.read(os.path.abspath(file))
p.write(os.path.abspath(to))
 
# the ImageMacgick command line to do it
# cmd = "convert -density 300 -depth 8 -quality 85 {0} {1}".format(file, to)