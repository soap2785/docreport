import base64

from twocaptcha import TwoCaptcha

solver = TwoCaptcha('a4e4203d59aeb2ecac2638ea4b3a0280')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def solve_captcha(url) -> str:
    header, encoded_data = url.split(",", 1)
    image_data = base64.b64decode(encoded_data)
    with open("captcha.jpeg", "wb") as f:
        f.write(image_data)
    result = solver.normal('captcha.jpeg')
    return result
