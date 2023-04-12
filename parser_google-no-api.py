import requests, lxml, re, urllib.parse, base64
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


def parser(request):
    params = {
        "q": request,
        "sourceid": "chrome",
    }

    html = requests.get("https://images.google.com/search", params=params, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    script_img_tags = soup.find_all('script')

    img_matches = re.findall(r"s='data:image/jpeg;base64,(.*?)';", str(script_img_tags))

    for index, image in enumerate(img_matches):
        try:
            image = image.split('\\')[0]
            # https://stackoverflow.com/a/6966225/15164646
            print(f"data:image/jpeg;base64,{str(image)}")
            final_image = Image.open(BytesIO(base64.b64decode(str(image))))
        except:
            pass


parser("images mouse")
