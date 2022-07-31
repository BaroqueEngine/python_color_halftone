from PIL import Image, ImageDraw, ImageStat

def norm(v, a, b):
  return (v - a) / (b - a)

def lerp(a, b, t):
  return a + (b - a) * t

def map(v, a, b, c, d):
  return lerp(c, d, norm(v, a, b))

def convert(src, size, angle, max_radius, channel_index):
    width, height = src.size
    cmyk = src.convert("CMYK").split()
    channel = cmyk[channel_index]
    channel = channel.rotate(angle, expand=True)
    channel_width, channel_height = channel.size
    img = Image.new("L", (channel_width, channel_height))
    canvas = ImageDraw.Draw(img)
    
    for y in range(0, channel_height, size):
        for x in range(0, channel_width, size):
            area = channel.crop((x, y, x + size, y + size))
            stat = ImageStat.Stat(area)
            avg = stat.mean[0]
            r = map(avg, 0, 255, 1, max_radius)
	    
            x0 = x + size / 2 - r
            y0 = y + size / 2 - r
            x1 = x + size / 2 + r
            y1 = y + size / 2 + r
            canvas.ellipse((x0, y0, x1, y1), fill=255)
    
    img = img.rotate(-angle, expand=True)
    
    new_width, new_height = img.size
    px = (new_width - width) // 2
    py = (new_height - height) // 2
    img = img.crop((px, py, px + width, py + height))

    return img

angles = [0, 15, 30]
size = 20
max_radius = 15
src = Image.open("input.jpg")
width, height = src.size

c = convert(src, size, angles[0], max_radius, 0)
m = convert(src, size, angles[1], max_radius, 1)
y = convert(src, size, angles[2], max_radius, 2)
k = Image.new("L", (width, height), 0)

output = Image.merge("CMYK", [c, m, y, k])
output.convert("RGB").save("output.png")