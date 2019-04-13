# my_line_bot
## usage
1. pip install
```
pip3 install -r requirements.txt
```
2. add ./instance/private_config.cfg
```
LINE_CHANNEL_SECRET = <YOUR_LINE_CHANNEL_SECRET>
LINE_CHANNEL_ACCESS_TOKEN = <YOUR_CHANNEL_ACCESS_TOKEN>
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

