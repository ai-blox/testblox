from SSD1306 import SSD1306_128_32

#display init stuff
disp = SSD1306_128_32(None)
#disp.fill(0)
disp.show()
width = disp.width
height = disp.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
padding = -2
top = padding
bottom = height - padding
x = 0
font = ImageFont.load_default()
#print naar display
draw.rectangle((0, 0, width, height), outline=0, fill=0)
draw.text((x, top + 0), "Probleem ", font=font, fill=255)
draw.text((x, top + 8), "met", font=font, fill=255)
draw.text((x, top + 16), "internetverbinding", font=font, fill=255)
draw.text((x, top + 24), "Volgende test: in 10 sec", font=font, fill=255)
