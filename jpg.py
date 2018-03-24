# with the Tkinter canvas, drawings can only be saved as .ps files 
# use PIL to draw simultaneuosly to memory and then save to file
# PIL allows .png .jpg .gif or .bmp file formats

#background_color = 'black'
bgcolor = 0x000000
title_text1 = 'Hero French'
title_text2 = 'Policeman'
font_type_for_title= "Chunkfive.otf"
 
text_content = ["mama is y handsome kljzshdflkhasdlkf  jhsldkjfhlaksjdhflkjahsdf and dad is very pretty","this is the text 2 of thing"]

content_color=0xFFFFFF
size_for_title_1=72
size_for_title_2=56

size_for_content=35
offset_of_content = 40

title_color= 0xFFFFFF

column = 2
#todo length of content
offsetoftextbelowcolumn = 10
length_of_one_cell = 400
title_height = 150
width = 700


width = width
height = title_height+column*length_of_one_cell
#import Tkinter as tk

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageEnhance
import textwrap
#root = tk.Tk()
#root.title("drawing lines")
# some color constants for PIL
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0,128,0)






# create the drawing canvas
#cv = tk.Canvas(root, width=width, height=height, bg=background_color)
#cv.pack()
# create empty PIL image and draw objects to draw on
# PIL draws in memory only, but the image can be saved
image = Image.new("RGB", (width, height), color=bgcolor)
draw = ImageDraw.Draw(image)


def warning():
    font = ImageFont.truetype(font_type_for_title, size_for_title_1)
    if  width<font.getsize(title_text1)[0]:
        print("warning title 1 is too long")
    font = ImageFont.truetype(font_type_for_title, size_for_title_2)
    if  width<font.getsize(title_text2)[0]:
        print("warning title 2 is too long")
#make title
def make_title():
    font = ImageFont.truetype(font_type_for_title, size_for_title_1)
    text_size = font.getsize(title_text1)
    #print(text_size)
    
    xforthis = width/2-text_size[0]/2
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((xforthis, 15),title_text1, fill = title_color,font=font)
    

    font = ImageFont.truetype(font_type_for_title, size_for_title_2)
    text_size = font.getsize(title_text2)
    #print(text_size)
    xforthis = width/2-text_size[0]/2
    draw.text((xforthis, 80),title_text2,fill = title_color,font=font)


def draw_index_line():
    # draw horizontal lines
    x1 = 0
    x2 = width
    # for k in range(0, 500, 50):
    #     y1 = k
    #     y2 = k
    y1 = title_height
    y2 = y1
        # Tkinter (visible)
        #cv.create_line(x1, y1, x2, y2)
        # PIL (to memory for saving to file)
    draw.line((x1, y1, x2, y2), white)   

    k = title_height
    for i in range(0,column):
        k=k+length_of_one_cell
        y1 = k
        y2 = k  
        draw.line((x1, y1, x2, y2), white)  

    # # draw vertical lines
    # y1 = 0
    # y2 = 450
    # for k in range(0, 500, 50):
    #     x1 = k
    #     x2 = k
    #     # Tkinter
    #     #cv.create_line(x1, y1, x2, y2)
    #     # PIL
    #     draw.line((x1, y1, x2, y2), white)

def totextbox():
    total=title_height
    for i in range(0,column):
        y = total

        font_size=size_for_content
        font = ImageFont.truetype(font_type_for_title, font_size, encoding='unic')

        margin = 20
        offset = offset_of_content
        for line in textwrap.wrap(text_content[i], width= int((width-margin)/font_size)):
            draw.text((margin, offset+total), line, font=font, fill=content_color)
            offset += font.getsize(line)[1]

        total = total + length_of_one_cell

totextbox()
warning()
make_title()
draw_index_line()
# # Tkinter canvas object can only be saved as a postscipt file
# which is actually a postscript printer language text file
#cv.postscript(file="mylines.ps", colormode='color')
# PIL image can be saved as .png .jpg .gif or .bmp file
filename = "mylines.jpg"
image.save(filename)
#root.mainloop()