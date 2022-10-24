import cv2
import numpy as np
import time
import urllib.request as urllib
from google_images_search import GoogleImagesSearch
from random import randint
import json


class SearchImage:
    def __init__(self):
        self.api_use = 0
        self._set_api()

    def _set_api(self, next_api=False):
        with open('secret_code.json', 'r') as f:
            data = json.load(f)
        GOOGLE_API = data['key']['google_api']
        if next_api:
            self.api_use += 1
            if self.api_use >= len(GOOGLE_API):
                return False
            print(f"-- Using Google API number {self.api_use+1} --")

        self.gis = GoogleImagesSearch(GOOGLE_API[self.api_use], data['key']['google_search_engine_id'])
        return True

    def searchImages(self, query, num=1):
        _example_params = {
            'q': '...',
            'num': 10,
            'safe': 'high|medium|off',
            'fileType': 'jpg|gif|png',
            'imgType': 'clipart|face|lineart|news|photo',
            'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge',
            'imgDominantColor': 'black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow',
            'imgColorType': 'color|gray|mono|trans',
            'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
        }
        _params = {
            'q': query,
            'num': num,
        }
        try:
            self.gis.search(search_params=_params)
        except:
            if self._set_api(True):
                self.searchImages(query, num)
            else:
                print("-- Google API out of limit --")

        return self.gis.results()

    def searchImages_download(self, query, num=1, dir='default'):
        res = self.searchImages(query, num)
        if len(res) != 0:
            for image in res:
                image.resize()
                image.download(f'image/download/{dir}')
            return True
        else:
            return False

    def searchImages_download_rename(self, query, num=1, dir='default'):
        imgs_url = self.searchImages_url(query, num)
        if len(imgs_url) != 0:
            count = 0
            for img_url in imgs_url:
                img = self.urlToImage(img_url)
                filePath = f'image/download/{dir}/{count}.jpg'
                cv2.imwrite(filePath, img)
                count += 1
            return True
        else:
            return False

    def searchImages_url(self, query, num=1):
        imagesURL = []
        res = self.searchImages(query, num)
        for image in res:
            im = image.url
            imagesURL.append(im)
            # image.download('image/from-google')
        return imagesURL

    def urlToImage(self, url):
        try:
            resp = urllib.urlopen(url)
            imgC = np.asarray(bytearray(resp.read()), dtype="uint8")
            return cv2.imdecode(imgC, cv2.IMREAD_COLOR)
        except:
            return None

    def image_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    def imageShow(self, img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)

    def searchImages_show(self, query, num=1):
        imgs_url = self.searchImages_url(query, num)
        if len(imgs_url) != 0:
            for img_url in imgs_url:
                img = self.urlToImage(img_url)
                if not img is None:
                    img = self.image_resize(img, width=720)
                    self.imageShow(img)
                else:
                    print("image not found")
            return True
        else:
            return False

    def searchImages_show_random(self, query, num=5):
        imgs_url = self.searchImages_url(query, num)
        if len(imgs_url) != 0:
            image_index = randint(0, len(imgs_url) - 1)
            img = self.urlToImage(imgs_url[image_index])
            if not img is None:
                img = self.image_resize(img, width=720)
                self.imageShow(img)
                return True
        return False


def main():
    # SearchImage().searchImages_download_rename("Horse", 10, "Horse")
    SearchImage().searchImages_show_random("laptop")


if __name__ == "__main__":
    main()

##########################################
# pip install windows-curses

## Github
# https://github.com/arrrlo/Google-Images-Search
### Control Panel
# https://cse.google.com/cse/setup/basic?cx=12a8dddc91a324428
