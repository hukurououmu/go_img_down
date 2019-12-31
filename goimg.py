import os
from google_images_download import google_images_download


keyword = input("> Enter keyword:")
while not keyword:
    keyword = input("> Enter keyword:")

print("> 0:jpg, 1:gif, 2:png")
img_format = ["jpg", "gif", "png"]
img_format_num = input("> Select number(0~2):")
while not img_format_num:
    if img_format_num.isdigit() or int(img_format_num) > 2:
        img_format_num = input("> Select number(0~2):")

limit = input("> Enter limit:")
while not limit:
    limit = input("> Enter limit:")

save_dir = input("> Enter save folder:")
while not save_dir:
    save_dir = input("> Enter save folder:")
if not os.path.exists(save_dir):
    os.mkdir("./" + save_dir + "/")


def downloadImage():
    response = google_images_download.googleimagesdownload()
    argments = {
        "keywords"         : keyword,
        "format"           : img_format[int(img_format_num)],
        "limit"            : limit,
        "output_directory" : save_dir,
        "no_directory"     : True
    }
    try:
        response.download(argments)
    except FileNotFoundError:
        argments = {
            "keywords"         : keyword,
            "format"           : img_format[int(img_format_num)],
            "limit"            : limit,
            "output_directory" : save_dir,
            "no_directory"     : True
        }
        try:
            response.download(argments)
        except:
            pass


def main():
    downloadImage()

if __name__ == "__main__":
    main()
