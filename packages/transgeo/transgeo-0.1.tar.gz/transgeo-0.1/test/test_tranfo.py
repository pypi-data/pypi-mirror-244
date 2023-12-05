from PIL import Image, ImageDraw
import random
import transgeo as tg


with Image.new('RGBA', (800, 800), "black") as img,\
     Image.new('RGBA', (800, 800), "black") as img2:
    ctx = ImageDraw.Draw(img2)

    N = 50
    for i in range(N):
        n = i / N * 360
        A = (400, 400)
        B = (800, 400)
        angle = int(n / 10) * 10
        C = tg.rotation(B, angle, A)
        pt = (random.normalvariate(400, 150), random.normalvariate(400, 150))
        coul = f"hsv({int(n)}, 100%, 100%)"
        ctx.line([pt, tg.saxiale(pt, A, C)])

    img = Image.alpha_composite(img, img2)
    img.save("test_transfo.png")
