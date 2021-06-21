import re
import sqlite3
from urllib.request import urlopen
from html import unescape

def main():
    """
    メインの処理。fetch(), scrape(), save()の３つの関数を呼び出す
    """

    html = fetch('http://sample.scraping-book.com/dp')
    books = scrape(html)
    save('books.db', books)

def fetch(url):
    """
    引数urlで与えられたURLのWEBページを取得する。
    WebページのエンコーディングはContent-Typeヘッダーを取得する。
    戻り値: str型のHTML
    """

    f = urlopen(url)
    encoding = f.info().get_content_charset(failobj="url-8")
    html = f.read().decode(encoding)

    return html

def scrape(html):
    """
    引数htmlで与えられたHTMLから正規表現で書籍の情報を抜き出す。
    戻り値: 書籍(dict)のリスト
    """

    books = []

    for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
        # 書籍のURLは itemprop="URL" という属性を持つa要素のhref属性から取得する。
        url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
        url = 'http://gihyo.jp' + url

        # 書籍のタイトルは itemprop="name" という属性を持つp要素から取得する。
        title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
        title = re.sub(r'<.*?>', '', title) # タグを取り除く
        title = unescape(title) # 文字参照を元に戻す

        books.append({'url': url, 'title': title})
        return books
    
def save(db_path, books):
    """
    引数booksで与えられた書籍リストをSQLite3DBに保存する。
    DBのパスは引数db_pathで与えられる。
    戻り値: なし
    """

    conn = sqlite3.connect(db_path)

    c = conn.cursor() # カーソルを取得する

    c.execute('DROP TABLE IF EXISTS books')
    c.execute('''
        CREATE TABLE books (
            title text,
            url text
        )
    ''')

    c.executemany('INSERT INTO books VALUES(:title, :url)', books)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()