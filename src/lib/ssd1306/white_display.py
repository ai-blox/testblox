from SSD1306 import SSD1306_128_32
from PIL import Image

#display init stuff
disp = SSD1306_128_32()
disp.begin()
rect = Image.new('1', (disp.width, disp.height), 1)
disp.image(rect)
disp.display()
