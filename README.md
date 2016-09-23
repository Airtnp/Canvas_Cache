# Canvas_Cache
Cache slow Canvas

## Version
* 0.02

## Intro
* Use urllib/urllib2/cookielib to situmulate login
* Use bs4 to parse html
* Use tesseract-ocr+PIL to recognize captcha
* Use pymysql to connect MySQL database
* I firstly want to write different class for different function, but failed, so the class just mean JaccountLogin and CanvasCache

## Usage
* Install tesseract-ocr (or you can manuelly input the captcha every time)
* Install MySQL
* Replace the username/password in Config.ini
* `python Cache.py`

## Problem
* Canvas is so slow so URLError and SSLError will occur
* Download 

## TODO
* [ ] <del> Write a GUI for it (PyQt) <del/>
* [ ] Improve downloading
* [ ] Use more accurate OCR
* [x] Use database record to improve file downloading
* [ ] Write C# UWP Win 10 Program

## License
* Do whatever you want

## Orz
* orz LukeXuan
* orz JasonQSY
* orz dbshch
* orz tc-imba