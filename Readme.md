The detail.py gets Epic Number and then sends requests to ECI. 
The main.py sends epic number to detail.py and logs failed epic number whose captcha was wrong after specific retries.

To Run:
1. Install ddddocr (use Python 3.9)
2. pip install -r requirements.txt
3. python main.py