# Canvas_Cache
Cache slow Canvas

## Version
* 0.01

## Intro
* Use urllib/urllib2/cookielib to situmulate login
* Use bs4 to parse html
* Use tesseract-ocr+PIL to recognize captcha
* Use pymysql to connect MySQL database
* I firstly want to write different class for different function, but failed, so the class just mean JaccountLogin and CanvasCache

## Usage
* Install tesseract-ocr (or you can manuelly input the captcha every time)
* Replace the username/password in LoginJaccount.py
* `python LoginJaccount.py`

## Problem
* Canvas is so slow so URLError and SSLError will occur
* Download 

## TODO
* [.] Write a GUI for it (PyQt)
* [.] Improve downloading
* [.] Use more accurate OCR
* [.] Use database record to improve file downloading

## License
* Do whatever you want

## Orz
* orz LukeXuan
* orz JasonQSY
* orz dbshch
* orz tc-imba