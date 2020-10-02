from gid_joeclinton.google_images_download import google_images_download


def input_command():

    keyword = input(">>> Enter keyword: ")
    while not keyword:
        keyword = input(">>> Enter keyword: ")

    print("[format number] 0:jpg, 1:gif, 2:png")
    img_format = ["jpg", "gif", "png"]
    img_format_num = input(">>> Select format number(0~2): " )
    while not img_format_num:
        if img_format_num.isdigit() or int(img_format_num) > 2:
            img_format_num = input(">>> Select format number(0~2): ")

    limit = input(">>> Enter limit: ")
    while not limit:
        limit = input(">>> Enter limit: ")

    return keyword, img_format, img_format_num, limit




def download_images():
    inputcommand = input_command()
    res = google_images_download.googleimagesdownload()
    argments = {
        "keywords"         : inputcommand[0],
        "format"           : inputcommand[1][int(inputcommand[2])],
        "limit"            : inputcommand[3],
    }
    try:
        res.download(argments)
    except Exception as e:
        raise e


def main():
    download_images()

if __name__ == "__main__":
    main()
