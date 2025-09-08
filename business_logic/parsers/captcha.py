import base64
import os

from twocaptcha import TwoCaptcha

solver = TwoCaptcha('a4e4203d59aeb2ecac2638ea4b3a0280')


def solveCaptcha(url) -> dict:
    header, encodedData = url.split(",", 1)
    imageData = base64.b64decode(encodedData)

    with open("captcha.png", "wb") as f:
        f.write(imageData)

    result = solver.normal('captcha.png')
    os.remove('captcha.png')

    return result