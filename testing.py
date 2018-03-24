
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageEnhance
from PIL import ImageOps
import textwrap
title_height = 150
width = 700

size_for_content=30




text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

image = Image.open("mylines.jpg")



draw = ImageDraw.Draw(image)


font_size=size_for_content
font = ImageFont.truetype(font_type_for_title, font_size, encoding='unic')

margin = 20
offset = 20
total=title_height
for line in textwrap.wrap(text_content[i], width= int((width-margin)/font_size)):
    draw.text((margin, offset+total), line, font=font, fill="#aa0000")
    offset += font.getsize(line)[1]


image.save("image.jpg")