# my_line_bot
## abstract
pythonの学習と
flask，line_botのお試し

### 現在持っている機能
- 自炊ガチャ
    - 「何が食べたい」と聞くと，食べたいもののレシピのリンクを送ってくる
- 人口無能

## usage
1. pip install
```
pip3 install -r requirements.txt
```
2. add ./instance/private_config.cfg
```
LINE_CHANNEL_SECRET = "<YOUR_LINE_CHANNEL_SECRET>"
LINE_CHANNEL_ACCESS_TOKEN = "<YOUR_CHANNEL_ACCESS_TOKEN>"
```
3. setting
```
$ (editor) start.sh
export FLASK_PORT=<YOUR_PORT>
```
4. start service
```
# nohup ./start.sh &
```


## 勉強元
- 人口無能 : http://sandmark.hateblo.jp/entry/2017/10/07/141339


## references
Japanese Wordnet (vXX) © 2009-2011 NICT, 2012-2015 Francis Bond and 2016-2017 Francis Bond, Takayuki Kuribayashi
linked to http://compling.hss.ntu.edu.sg/wnja/index.en.html
