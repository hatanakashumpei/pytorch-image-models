'''
DeepLを使った翻訳を行う関数
入力　翻訳したい英語
出力　翻訳された日本語
例外　入力が文字列でない場合
'''
import time
from typing import Optional
from selenium import webdriver  
import chromedriver_binary
from selenium.webdriver.chrome.options import Options

def TranslationByDeepL( mytext ):
    if mytext =="":
        return ""
    if type(mytext) is not str:
        raise   Exception("文字列ではありません")

    #DeeLのページのURLとCSS Selector
    load_url = "https://www.deepl.com/ja/translator"

    #'21/1/26 Selectorが変更になったっぽくて、要素にアクセスできなくなってたので確認して修正
    input_selector = "#dl_translator > div.lmt__text > div.lmt__sides_container > div.lmt__side_container.lmt__side_container--source > div.lmt__textarea_container.halfViewHeight > div > textarea"
                    #"#dl_translator > div.lmt__sides_container > div.lmt__side_container.lmt__side_container--source > div.lmt__textarea_container > div > textarea"
    Output_selector = "#dl_translator > div.lmt__text > div.lmt__sides_container > div.lmt__side_container.lmt__side_container--target > div.lmt__textarea_container.lmt__textarea_container_no_shadow > div.lmt__translations_as_text > p.lmt__translations_as_text__item.lmt__translations_as_text__main_translation > button.lmt__translations_as_text__text_btn"
                    # "#target-dummydiv"
                    #"#dl_translator > div.lmt__sides_container > div.lmt__side_container.lmt__side_container--target > div.lmt__textarea_container > div.lmt__translations_as_text > p > button.lmt__translations_as_text__text_btn"


    '''
    WebDriverの処理がうまくいかなかったら1秒待機して再度WebDriverの処理を行う
    ただ、10回トライしてダメだったらエラーを返して関数処理終
    以下、WebDriver使うところでは同様の処理
    '''
    errCount=0
    f_succsess=False
    while not f_succsess:
        try: # DeepLにアクセス
            options = Options()
            # options.binary_location = '/usr/bin/google-chrome'
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)  #  driver = webdriver.Chrome()
            driver.get(load_url)
            f_succsess = True
        except Exception  as identifier:
            errCount=errCount+1
            if errCount >=10:
                raise identifier

    #DeepLに英文を送る
    errCount=0
    f_succsess=False
    while not f_succsess:
        try: #DeepLに英文を送る
            print(driver.page_source)
            driver.find_element_by_css_selector(input_selector).send_keys(mytext)
            f_succsess = True
        except Exception  as identifier:              
            errCount=errCount+1
            if errCount >=10:
                raise identifier
            time.sleep(1)

    #フラグ用
    Output_before = ""
    while 1:
        errCount=0
        f_succsess=False
        while not f_succsess:
            try:# DeepLの出力を取得する
                Output = driver.find_element_by_css_selector(Output_selector).get_attribute("textContent")
                f_succsess = True
            except Exception  as identifier:               
                errCount=errCount+1
                if errCount >=10:
                    raise identifier
                time.sleep(1) 
        '''
        取得したoutputが空文字なら、まだ翻訳が終了してないということで、1秒後に再チェック。
        取得したoutputが空文字でない場合、1つ前のoutputと比べて違う内容になってるなら、
        まだ翻訳が終わり切ってないということで1秒後に再チェック。
        取得したoutputが空文字でない場合、1つ前のoutputと同じ内容なら、翻訳終了ということで出力。
        '''        
        if Output != "" : #出力が空文字でないとすれば結果の出力が始まった
            if Output_before == Output:#出力が1つ前の出力と同じなら、出力が完了したってこと
                break
            Output_before = Output            
        time.sleep(1)

    #chromeを閉じる
    driver.close()

    #結果出力
    return Output


def test():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.binary_location = '/usr/bin/google-chrome'
    options.add_argument('--headless')
    options.add_argument('--window-size=1280,1024')

    driver = webdriver.Chrome('chromedriver', options=options)

    driver.get('https://www.google.co.jp/search?q=今日も一日がんばるぞい')
    driver.save_screenshot('screenshot.png')
    driver.quit()


if __name__ == "__main__":
    TranslationByDeepL("tripod")
