from google_images_search import GoogleImagesSearch


def search_on_google(name, count):
    """
    Searches name on google.com and parse image urls
    :return dict image urls
    """
    # your keys here
    gis = GoogleImagesSearch('api_key', 'search_system_id')
    _search_params = {
        'q': name,
        'num': count,
        'fileType': 'jpg|png',
        'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
        # 'safe': 'active|high|medium|off|safeUndefined',  ##
        # 'imgType': 'clipart|face|lineart|stock|photo|animated|imgTypeUndefined',  ##
        # 'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge|imgSizeUndefined',  ##
        # 'imgDominantColor':
        # 'black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow|imgDominantColorUndefined', ##
        # 'imgColorType': 'color|gray|mono|trans|imgColorTypeUndefined'  ##
    }
    gis.search(search_params=_search_params)
    return [image.url for image in gis.results()]
