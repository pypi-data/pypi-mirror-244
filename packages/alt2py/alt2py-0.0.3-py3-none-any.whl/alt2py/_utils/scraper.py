import requests
import os
import urllib
from bs4 import BeautifulSoup

def get_challenge_links():
    urls = [
        'https://community.alteryx.com/t5/Weekly-Challenge/Weekly-Challenge-Index-amp-Welcome-Page-1/td-p/48275',
        'https://community.alteryx.com/t5/Weekly-Challenge/Weekly-Challenge-Index-amp-Welcome-Page-2/td-p/1135098'
    ]

        
    challenge_list = []
    
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        challenge_list += soup.find_all('table')[-1].find_all('tr')[1:]

    data = [];
    for challenge in challenge_list[300:]:
        cols = challenge.find_all('td')
        datum = {
            "Number":cols[0].text,
            "Name":cols[1].text,
            "Difficulty":cols[2].text,
            "Topics":cols[3].text,
            "Url":cols[1].find('a').get('href')
        }
        print(datum)
        data.append(datum)
        response2 = requests.get(datum["Url"])
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        
        dls = soup2.find('div',{'id':'attachments_0'})

        if dls:
            dls = dls.find_all('a',{'download':True})
        else:
            print("downloaded 0 files for challenge - "+datum["Number"])
            continue

        folder_name = "challenges/" + datum["Number"]
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            
        # Download the file and save it
        for dl in dls:
            href = dl.get('href')
            save_path = os.path.join(folder_name, href.split('/')[-1])
            urllib.request.urlretrieve("https://community.alteryx.com" + href, save_path)
        print("downloaded " + str(len(dls)) + " files for challenge - "+datum["Number"])
        
    return data

# Test the function
print("start")

challenge_links = get_challenge_links()
