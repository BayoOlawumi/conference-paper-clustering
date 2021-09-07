from urllib.request import urlopen
import csv
url = 'https://sergfuta.herokuapp.com/energy-data'
def getNextPage(url):
    html_bytes = urlopen(url).read()
    html = html_bytes.decode("utf-8")
    start = html.find('"next":')+8
    end = html.find(',"previous')-1
    inihtml = html[start:end]
    if (len(inihtml) > 4):
        main(inihtml)
    else:
        print ('last-page')
        exit()
    

def main(url):
    html_byte = urlopen(url).read()
    html = html_byte.decode("utf-8")
    print('connected')
    start = html.find('results":[{') + 11
    end = len(html)-3
    html = html[start:end]
    htmlList = html.split('},{')
    count = 0
    while ( count < len(htmlList)):
        data = htmlList[count]
        while (data.find('":') > 0):
            index = data.find('":')
            data = data[:index +1] + '~' + data[index +2:]
        htmlList[count] = data
        count +=1
    count = 0
    while ( count < len(htmlList)):
        data = htmlList[count]
        while(data.find('"') != -1 ):
            index = data.find('"')
            if ( index == 0):
                data = data[1:]
            elif ( index == len(data)-1):
                data = data[:index]
            else:
                data = data[:index] + data[index +1:]
        data = dict(x.split("~") for x in data.split(","))
        htmlList[count] = data
        count +=1
    file = open('data_endpoint_file.csv','a', encoding='UTF8')
    fieldnames = ['id','meter_id','timestamp','current','voltage','frequency','power_factor','energy','real_power','reactive_power','apparent_power']
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    writer.writeheader()
    for data in htmlList:
        writer.writerow(data)
    file.close()
    print (url)
    getNextPage(url)
main(url)
    
