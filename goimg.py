import os
import time
import datetime
import requests
from random import choice
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException


init()
RED = Fore.RED
GREEN = Fore.GREEN
RESET = Fore.RESET

# ユーザーエージェントのリスト
_user_agents = [
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
]


# _user_agentsからランダムにユーザーエージェントを選ぶ
def random_agent():
    return choice(_user_agents)


time_start = time.time()  # プログラム処理時間の計測
date_now = datetime.datetime.now()  # プログラム実行時の日時
date_str = date_now.strftime("%Y/%m/%d %H:%M")
print(date_str)

SEARCH_WORD = input("> Enter search word: ")  # 入力されたワードの画像がダウンロードされる
while not SEARCH_WORD:
    SEARCH_WORD = input("> Enter search word: ")
DOWNLOAD_LIMIT = int(input("> Enter download limit number: "))  # ダウンロード数の上限
# 画像保存先フォルダ(入力したワードの名前のフォルダが作られそこに画像が保存される)
SAVE_DIR = "./GoogleCrawler/" + SEARCH_WORD + "/"
FILE_NAME = ""  # ファイル名の後ろに0から連番と拡張子がつけられる
TIMEOUT = 30  # 要素の検索のタイムアウト 30秒
ACCESS_WAIT = 3  # アクセスの間隔 3秒
RETRY_NUM = 3  # リトライ回数

# ヘッドレスモードでfirefoxを起動する
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

# タイムアウト設定
driver.implicitly_wait(TIMEOUT)

# webdriver起動時間
time_driver = time.time()
print("[+] Webdriver起動完了: ", f"{time_driver - time_start:.1f}s")

# Google画像検索ページを取得
url = f"https://www.google.com/search?q={SEARCH_WORD}&tbm=isch"
driver.get(url)

# Google画像検索ページ取得時間
time_geturl = time.time()
print("[+] Google画像検索ページ取得: ", f"{time_geturl - time_driver:.1f}s")

# 画像のサムネイルを取得
thumb_elems = driver.find_elements(By.CSS_SELECTOR, "#islmp img")
thumb_alts = [thumb.get_attribute("alt") for thumb in thumb_elems]
count = len(thumb_alts) - thumb_alts.count("")
print("[+] サムネイル画像取得数: ", count)

while count < DOWNLOAD_LIMIT:
    # ページの一番下までスクロールする
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(ACCESS_WAIT)

    # 画像のサムネイルを取得
    thumb_elems = driver.find_elements(By.CSS_SELECTOR, "#islmp img")
    thumb_alts = [thumb.get_attribute("alt") for thumb in thumb_elems]

    count = len(thumb_alts) - thumb_alts.count("")
    print("[+] サムネイル画像取得数: ", count)

# サムネイルをクリックしたら表示される領域を取得する
img_frame_elems = driver.find_element(By.ID, "islsp")

# 画像保存先フォルダの作成
os.makedirs(SAVE_DIR, exist_ok=True)

# ヘッダーの作成
HEADERS = {"User-Agent": random_agent()}
print("[+] HTTP HEADER: ", HEADERS)

# ダウンロード対象のファイルの拡張子
IMG_EXTS = (".jpg", ".jpeg", ".png", ".gif")


# 拡張子を取得
def get_extension(url):
    url_lower = url.lower()
    for img_ext in IMG_EXTS:
        if img_ext in url_lower:
            extension = ".jpg" if img_ext == ".jpeg" else img_ext
            break
    else:
        extension = ""
    return extension


# urlの画像を取得しファイルに書き込む
def download_image(url, path, loop):
    result = False
    for i in range(loop):
        try:
            res = requests.get(url, headers=HEADERS, stream=True, timeout=10)
            res.raise_for_status()
            with open(path, "wb") as f:
                f.write(res.content)
        except requests.exceptions.SSLError:
            print(RED + "[!] SSLエラー" + RESET)
        except requests.exceptions.RequestException as e:
            print(RED + f"[!] requestsエラー({e}): {i + 1}/{RETRY_NUM}" + RESET)
            time.sleep(ACCESS_WAIT)
        else:
            result = True
            break
    return result


# サムネイル画像取得時間
time_thumnails = time.time()
print("[+] サムネイル画像取得", f"{time_thumnails - time_geturl:.1f}s")
print("-" * 50)
print("[*] ダウンロード開始")

# ダウンロード
EXCLUSION_URL = "https://lh3.googleusercontent.com/"
count = 0
url_list = []
for thumb_elem, thumb_alt in zip(thumb_elems, thumb_alts):
    if thumb_alt == "":
        continue

    print(GREEN + f"{count}: {thumb_alt}" + RESET)

    for i in range(RETRY_NUM):
        try:
            thumb_elem.click()
        except ElementClickInterceptedException:
            print(RED + f"[!] clickエラー: {i + 1}/{RETRY_NUM}" + RESET)
            time.sleep(ACCESS_WAIT)
        else:
            break
    else:
        print(RED + "[!] キャンセル" + RESET)
        continue

    time.sleep(ACCESS_WAIT)

    alt = thumb_alt.replace("'", "\\'")
    try:
        img_elem = img_frame_elems.find_element(
            By.CSS_SELECTOR, f"img[alt=\'{alt}\']")
    except NoSuchElementException:
        print(RED + "[!] img要素探索エラー" + RESET)
        print(RED + "[!] キャンセル" + RESET)
        continue

    # urlの取得
    thumb_url = thumb_elem.get_attribute("src")

    for i in range(RETRY_NUM):
        url = img_elem.get_attribute("src")
        if EXCLUSION_URL in url:
            print(RED + "[!] 除外対象url" + RESET)
            url = ""
            break
        elif url == thumb_url:
            print(f"[?] urlチェック: {i + 1}/{RETRY_NUM}")
            time.sleep(ACCESS_WAIT)
            url = ""
        else:
            break

    if url == "":
        print(RED + "[!] キャンセル" + RESET)
        continue

    # 画像を取得しファイルへ保存
    ext = get_extension(url)
    if ext == "":
        print(RED + "[!] urlに拡張子が含まれないのでキャンセル" + RESET)
        print(RED + "→ " + RESET + f"{url}")
        continue

    filename = f"{FILE_NAME}{count}{ext}"
    path = SAVE_DIR + filename
    result = download_image(url, path, RETRY_NUM)
    if result is False:
        print(RED + "[!] キャンセル" + RESET)
        continue
    url_list.append(f"{filename}: {url}")

    # ダウンロード数の更新と終了判定
    count += 1
    if count >= DOWNLOAD_LIMIT:
        break


time_end = time.time()
print("[*] ダウンロード終了", f"{time_end - time_thumnails:.1f}s")
print("-" * 50)
total = time_end - time_start
total_str = f"プログラム終了時間: {total:.1f}s({total/60:.2f}min)"
count_str = f"画像ダウンロード数: {count}"
print(total_str)
print(count_str)

# urlをファイルへ保存
path = SAVE_DIR + "_url_list.txt"
with open(path, "w", encoding="utf-8") as f:
    f.write(date_str + "\n")
    f.write(total_str + "\n")
    f.write(count_str + "\n")
    f.write("\n".join(url_list))

driver.quit()
