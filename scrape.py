import requests
from bs4 import BeautifulSoup
import cPickle as pickle
from datetime import datetime as dt
import csv


VERBOSE = True
DEBUG = True


class bike(object):
    def __init__(self, i):
        '''
        Takes ResultSet from bs4 scrape of SGBIKEMART
        '''
        self.name = i[0].text.strip('\n')
        self.url = 'https://www.sgbikemart.com.sg' + i[0].a['href']
        self.photo = 'https://www.sgbikemart.com.sg' + i[1].div.contents[1].a['href']
        self.list_price = i[7].text.strip(' \n')
        self.list_reg_yr = i[8].text.strip(' \n').split(':')[1].strip()
        self.list_bike_type = i[9].text.strip(' \n').split(':')[1].strip()
        self.list_cc = i[10].text.strip(' \n')
        self.list_mileage = i[11].text.strip(' \n')
        self.list_comments = i[12].text.strip(' \n')
        self.list_date = i[18].text.split(':')[1].strip(' \n')
        self.list_type = i[19].text.strip(' \n')
        self.full_date = i

with open('honda.pickle', 'r') as f:
    bike_list = pickle.load(f)

with open('honda.csv', 'wb') as f:
    csvwriter = csv.writer(f)
    for b in bike_list:
        csvwriter.writerow([b.name,
                            b.url,
                            b.list_price,
                            b.list_reg_yr,
                            b.list_cc,
                            b.list_mileage,
                            b.list_date,
                            b.list_type,
        ])


def get_listings(model, page):
    URL = 'https://www.sgbikemart.com.sg/listing/usedbikes/listing/'\
        '?page={}&bike_type=&user=&monthly_from=&price_from='\
        '&reg_year_to=2019&license_class=2B&status=&price_to='\
        '&reg_year_from=1970&category=&monthly_to=&bike_model={}'.format(
            page,
            model
        )

    result = requests.get(URL)
    assert result.status_code == 200
    c = result.content

    soup = BeautifulSoup(c, features='html.parser')
    match = soup.find_all('div', class_='pmd-card pmd-z-depth')

    data = []

    for i in match:
        listing = i.find_all('div')
        try:
            assert listing[0]['class'][1] == 'text-center-xs'
            data.append(listing)
        except AssertionError:
            if DEBUG: print('Not a match')
        except IndexError:
            if DEBUG: print('Not a match')

    return data

# model = 'honda'
model = 'yamaha'
bike_list = []
page = 1

while True:
    data = get_listings(model, page)
    if len(data) == 0:
        break
    if VERBOSE: print page
    for i in data:
        bike_list.append(bike(i))
        print(bike_list[-1].name)
    page += 1

# with open('honda.pickle', 'wb') as f:
#     pickle.dump(bike_list, f)


with open('yamaha.pickle', 'wb') as f:
    pickle.dump(bike_list, f)
