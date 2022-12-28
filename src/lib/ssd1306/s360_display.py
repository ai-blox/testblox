from SSD1306 import SSD1306_128_32
from PIL import Image, ImageDraw, ImageFont

#display init stuff
disp = SSD1306_128_32()
#disp.fill(0)

disp.begin()
width = disp.width
height = disp.height

disp.clear()
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
padding = 0
top = padding
bottom = height - padding
x = 0
font= ImageFont.load_default()
#font = ImageFont.truetype('Minecraftia.ttf', 20)
draw.text((x, top + 0), "S360 Box", font=font, fill=255)
disp.image(image)
disp.display()
