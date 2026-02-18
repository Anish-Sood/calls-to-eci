from bs4 import BeautifulSoup
import detail
import os
import time
import csv

def save_fail(epNo, filename="failed_epics.csv"):    
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        writer.writerow([epNo])

with open("BADNU-DIGTHALI.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")

epic_tags = soup.find_all("span", id=lambda x: x and x.endswith("_epic"))

epic_numbers = [tag.get_text(strip=True) for tag in epic_tags]

results = {"sahi": 0, "galat": 0}
for num in epic_numbers:
    # print(num)
    result = detail.main(num)
    if result == "galat":
        save_fail(num)
    results[result]+=1
    print(results)

accuracy=results["sahi"]/(results["sahi"]+results["galat"])
print(accuracy)

