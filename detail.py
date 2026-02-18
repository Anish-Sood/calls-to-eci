import requests
import ddddocr
import base64
import time

urltogetcaptcha="https://gateway-voters.eci.gov.in/api/v1/captcha-service/generateCaptcha"
urltogetdetails="https://gateway-voters.eci.gov.in/api/v1/elastic/search-by-epic-from-national-display"
proxies={
        "http": "http://bcnkcfeo:iuj01wt7i00z@216.10.27.159:6837/",
        "https": "http://bcnkcfeo:iuj01wt7i00z@216.10.27.159:6837/"
    }

headers = {"Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}

# epNo="HP/04/020/174293"
ocr = ddddocr.DdddOcr()
def solve_with_ddddocr(image_path):
    
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    res = ocr.classification(image_bytes)
    return res


def main(epNo):

    repetitons=5

    for i in range(repetitons):
        try:
            response = requests.get(urltogetcaptcha,proxies=proxies)

            if response.status_code == 200:
                data=response.json()
                captcha_value=data["captcha"]
                captcha_id=data["id"]

                image_bytes = base64.b64decode(captcha_value)
                with open("captcha.jpg", "wb") as f:
                    f.write(image_bytes)
                captcha_ans=solve_with_ddddocr("captcha.jpg")   
                # print(captcha_value)
                # print(captcha_id)
                print(captcha_ans)

                if len(captcha_ans)!=6:
                    continue

                payload={"captchaData": captcha_ans,
                    "captchaId": captcha_id,
                    "epicNumber": epNo,
                    "isPortal": "true",
                    "securityKey": "na",
                    "stateCd":"S08"
                    }
                
                response2=requests.post(urltogetdetails, json=payload, headers=headers, proxies=proxies)
                if response2.status_code==200:
                    data2=response2.json()
                    if data2:
                        # content = data2[0]["content"]
                        # print(content) 
                        return "sahi"

                elif response2.status_code==400:
                    # print("wrong captcha ig")
                    continue
                    # return "galat"
                else:
                    continue
            else:
                continue
        except Exception as e:
            print()
            continue
    

    return "galat"

