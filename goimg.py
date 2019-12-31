import os
import sys
from google_images_download import google_images_download


class GoogleImageDownloader():

    def getParams(self, keywords):
        google = google_images_download.googleimagesdownload()
        argments = {
            "keywords"         : keywords["search_word"],
            "limit"            : keywords["number"],
            "format"           : keywords["img_format"],
            "output_directory" : keywords["output_dir"],
            "no_directory"     : True
        }
        google.download(argments)

    
    def inputValues(self):
        keywords = {}

        search_word = input("> Enter keyword:")
        while not search_word:
            search_word = input("> Enter keyword:")

        number = input("\n> Enter number:")
        while not number:
            number = input("\n> Enter number:")

        print("\n> 0:jpg, 1:gif, 2:png")
        img_format = ["jpg", "gif", "png"]
        img_format_num = input("> Select format(0~2):")
        while not img_format_num.isdigit() or int(img_format_num) > 2:
            img_format_num = input("> Select format(0~2):")

        output_dir = input("\n> Enter save folder:")
        while not output_dir:
            output_dir = input("> Enter save folder:")
        if not os.path.exists(output_dir):
            os.mkdir("./" + output_dir + "/")

        keywords["search_word"] = search_word
        keywords["number"]      = number
        keywords["img_format"]  = img_format[int(img_format_num)]
        keywords["output_dir"]  = output_dir

        return keywords


    def run(self):
        keywords = self.inputValues()
        self.getParams(keywords)




def main():
    google_down = GoogleImageDownloader()
    google_down.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n> Exit program")
        sys.exit()
