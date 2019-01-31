from flask import Flask, render_template, request
import urllib.request
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/recognition", methods=["POST"])
def recognition():
	script = request.form.get("script")
	script = script.split()
	output=[]
	for word in script:
		output.append(word)

	return render_template("processed.html", output=output)

@app.route("/definition/<string:word>")
def definition(word):
	word = purify(word)
	return lookupword(word)




#工具
#把string處理成只有英文字母和空格的字串，給string
def purify(astr):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in astr:
        if i not in alphabet:
            astr = astr.replace(i,' ')
    astr = astr.replace(' s ', ' ')
    astr = astr.replace(' ll ', ' ')
    astr = astr.replace(' m ', ' ')
    
    return astr + ' '

#工具
#利用網路爬蟲抓線上字典資料並是當修剪 ，要給單一單字(string)
def lookupword(word):
    pageurl="http://cdict.info/query/"+word

    page = urllib.request.urlopen(pageurl)

    soup = BeautifulSoup(page, 'html.parser')

    name_box = soup.find('div', attrs={'class': 'resultbox'})
    
    try:
        name = name_box.text.strip() 
    except AttributeError:
        return 'not found'
    else:
        return name