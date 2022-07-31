#How to save scraped data to a database
from bs4 import BeautifulSoup
import sqlite3
import requests


#print(p)
def getCompetitions(url):

    
    #create connection for crawler db
    conn = sqlite3.connect('artinfo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE comp(name TEXT, link TEXT, image TEXT, deadline TEXT, info TEXT)''')


    page1 = requests.get(url)
    html1 = page1.text
    soup1 = BeautifulSoup(html1, 'lxml')
    bod = soup1.find('body')
    main = bod.find('main', class_='menucima')
    con1 = main.find('div', class_='tuttoconprende')
    con2 = con1.find('section', class_='sec2')
    #all competitions
    comps = con2.find_all('article')

    for com in comps:
        h = com.find('header')

        #required info
        link = h.find('a')
        image = link.find('img')
        name = h.find('h3')

        info = com.find('p')
        d = com.find('div')
        deadline = d.find('time', class_='deadline2')

        c.execute('''INSERT INTO comp VALUES(?,?,?,?,?)''',(str(name.text), str(link.get('href')), str(image.get('src')), str(deadline.text), str(info.text)))
        print(name.text)
        print(link.get('href'))
        print(image.get('src'))
        print(deadline.text)
        print(info.text)



    conn.commit()
    print('completed.')
    c.execute('''SELECT * FROM comp''')
    #data array
    results = c.fetchall()
    
    return results




#url = soup.findAll(attrs = {'class': 'Owners-ownerImage-27R'})
"""c.execute('''INSERT INTO info VALUES(?)''',(url))
conn.commit()
print('complete.')
"""



"""
#close connection
conn.close()

print(url)
print(url1)"""