import json
from tkinter import filedialog
from tkinter import *


class Settings(object):
    def __init__(self):
        try:
            f = open('settings.json')
            self.data = str(f.read())
            f.close()
        except Exception as e:
            print(e)
            print('error code 0')
            return
        self.data = json.loads(self.data)
        self.background_image = self.data['background_image']

    def change_background(self):
        # in this case, the tk window would close after choose image.
        root = Tk()
        root.withdraw()
        path = filedialog.askopenfilename(filetypes=[("image", "*.jpg *.png")], )

        if len(path) == 0:
            return False
        self.data['background_image'] = path
        self.background_image = self.data['background_image']
        try:
            f = open('settings.json', 'w')
            write_data = str(self.data).replace('\'', '\"')
            f.write(write_data)
            f.close()
            return True
        except Exception as e:
            print(e)
            print('error code 1')
            return False
