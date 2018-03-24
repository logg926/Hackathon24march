
x=0
y=500

from PIL import Image, ImageFont, ImageDraw, ImageEnhance

source_img = Image.open("mylines.jpg").convert("RGB")


font = ImageFont.truetype("Chunkfive.otf", 72)

text = "very loooooooooooooooooong text"

# get text size
text_size = font.getsize(text)
print
# set button size + 10px margins
button_size = (text_size[0]+20, text_size[1]+20)

# create image with correct size and black background
button_img = Image.new('RGB', button_size, color = 0xFFFFFF)

# put text on button with 10px margins
button_draw = ImageDraw.Draw(button_img)
button_draw.text((x, y), text, font=font)

# put button on source image in position (0, 0)
source_img.paste(button_img, (0, 0))

# save in new file
source_img.save("output.jpg")