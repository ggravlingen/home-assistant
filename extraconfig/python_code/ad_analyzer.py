import urllib.request
from bs4 import BeautifulSoup
#import string


link = "https://mobil.blocket.se/stockholm?ca=11&q=elfa&st=s&is=1&l=0&f=p&w=1"

with urllib.request.urlopen( link ) as url:
    s = url.read()

soup = BeautifulSoup(s, 'html.parser')

a = soup.findAll("li", { "class" : "item" })

b = a[0]

optionsTable = [
    [x.text for x in y]
    for y in soup.findAll('p')
]

print(optionsTable)

#for each_tag in a:
#    staininfo_attrb_value = each_tag
#    print(staininfo_attrb_value)


#output = [ x["item_name"] for x in a  ]

#print(output)

#for each_item in soup.findAll("li", { "class" : "item" }):
#	print(each_item['item_title'])


#print(a[0])


#print(soup.prettify())
