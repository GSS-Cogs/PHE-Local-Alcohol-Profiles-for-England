# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
from gssutils import *
import requests

scraper = Scraper('https://www.gov.uk/government/collections/local-alcohol-profiles-for-england-lape')
scraper
# -

scraper.select_dataset(latest=True)
scraper

dist = scraper.distribution(title='Local Alcohol Profiles for England')
dist

# +
dist.downloadURL = 'https://fingertipsws.phe.org.uk/api/all_data/csv/' + \
    'by_profile_id?parent_area_code=e92000001&parent_area_type_id=6&child_area_type_id=102&profile_id=87'
dist.mediaType = 'text/csv'

from io import BytesIO
table = pd.read_csv(BytesIO(scraper.session.get(dist.downloadURL, verify=False).content))
table
# -

table.rename(index=str,
               columns={
                   'Indicator ID':'Indicator',
                   'Area Code' :'Geography',
                   'Time period':'Period',
                   'Upper CI 95.0 limit': 'CI Upper',
                   'Lower CI 95.0 limit': 'CI Lower'
               }, inplace = True)
table.count()

table = table[table['Category Type'].isnull() == True]
table = table.dropna(subset=['Value'])
table.count()

table = table[['Geography','Period','Sex', 'Age','Indicator',\
                       'Value','CI Upper','CI Lower']]

table['Sex'] = table['Sex'].map(
    lambda x: {
        'Female' : 'F', 
        'Male' : 'M',
        'Persons': 'T' ,
        }.get(x, x))

table['Period'] = table['Period'].map(
    lambda x: {
        '2008/09' : 'gregorian-interval/2008-04-01T00:00:00/P1Y',
        '2009/10' : 'gregorian-interval/2009-04-01T00:00:00/P1Y', 
        '2010/11' : 'gregorian-interval/2010-04-01T00:00:00/P1Y', 
        '2011/12' : 'gregorian-interval/2011-04-01T00:00:00/P1Y', 
        '2012/13' : 'gregorian-interval/2012-04-01T00:00:00/P1Y', 
        '2013/14' : 'gregorian-interval/2013-04-01T00:00:00/P1Y',
        '2014/15' :'gregorian-interval/2014-04-01T00:00:00/P1Y', 
        '2015/16' : 'gregorian-interval/2015-04-01T00:00:00/P1Y', 
        '2016/17' : 'gregorian-interval/2016-04-01T00:00:00/P1Y', 
        '2017/18' :'gregorian-interval/2017-04-01T00:00:00/P1Y', 
        '2006/07 - 08/09': 'gregorian-interval/2006-04-01T00:00:00/P3Y',
       '2007/08 - 09/10' : 'gregorian-interval/2007-04-01T00:00:00/P3Y', 
        '2008/09 - 10/11': 'gregorian-interval/2008-04-01T00:00:00/P3Y', 
        '2009/10 - 11/12': 'gregorian-interval/2009-04-01T00:00:00/P3Y',
       '2010/11 - 12/13': 'gregorian-interval/2010-04-01T00:00:00/P3Y', 
        '2011/12 - 13/14': 'gregorian-interval/2011-04-01T00:00:00/P3Y', 
        '2012/13 - 14/15': 'gregorian-interval/2012-04-01T00:00:00/P3Y',
       '2013/14 - 15/16': 'gregorian-interval/2013-04-01T00:00:00/P3Y', 
        '2014/15 - 16/17': 'gregorian-interval/2014-04-01T00:00:00/P3Y', 
        '2015/16 - 17/18': 'gregorian-interval/2015-04-01T00:00:00/P3Y', 
        '2008' : 'year/2008',
       '2009': 'year/2009', '2010': 'year/2010', '2011': 'year/2011', '2012': 'year/2012', 
        '2013': 'year/2013', '2014': 'year/2014', '2015': 'year/2015', '2016': 'year/2016',
       '2017': 'year/2017', 
        '2006 - 08' :'gregorian-interval/2006-01-01T00:00:00/P2Y', 
        '2007 - 09' :'gregorian-interval/2007-01-01T00:00:00/P2Y', 
        '2008 - 10': 'gregorian-interval/2008-01-01T00:00:00/P2Y', 
        '2009 - 11' :'gregorian-interval/2009-01-01T00:00:00/P2Y',
       '2010 - 12': 'gregorian-interval/2010-01-01T00:00:00/P2Y', 
        '2011 - 13': 'gregorian-interval/2011-01-01T00:00:00/P2Y', 
        '2012 - 14' :'gregorian-interval/2012-01-01T00:00:00/P2Y', 
        '2013 - 15' : 'gregorian-interval/2013-01-01T00:00:00/P2Y', 
        '2014 - 16' :'gregorian-interval/2014-01-01T00:00:00/P2Y',
       '2015 - 17':'gregorian-interval/2015-01-01T00:00:00/P2Y', 
        '2004 - 06' :'gregorian-interval/2004-01-01T00:00:00/P2Y', 
        '2005 - 07': 'gregorian-interval/2005-01-01T00:00:00/P2Y', 
        '2011 - 14' : 'gregorian-interval/2011-01-01T00:00:00/P3Y'       
        }.get(x, x))

table['Age'].unique()

table['Age'] = table['Age'].map(
    lambda x: {
        'All ages' : 'all', 
        '<18 yrs' : 'under-18', 
        '<75 yrs' : 'under-75', 
        '<40 yrs' : 'under-40', 
        '40-64 yrs' : '40-64',
        '65+ yrs' : 'ag1/65-plus', 
        '16+ yrs' : '16-plus', 
        '16-64 yrs (M), 16-61 yrs (F)' : 'agr/16-61-or-64',
        '17+ yrs' : '17-plus',
        '18+ yrs' : '18-plus', 
        '18-75 yrs' : "18-75 yrs"        
        }.get(x, x))


def user_perc(x):
    
    if str(x) == '91917':
        return 'Rate per 1,000 accidents'
    elif ((str(x) ==  '91182') | (str(x) == '92772')) :
        return 'Count'
    elif ((str(x) ==  '92447') | (str(x) == '91123') | (str(x) == '92774') |\
         (str(x) ==  '92776') | (str(x) == '92778') | (str(x) == '93193')) :
        return 'Percentage'
    elif ((str(x) ==  '92763') | (str(x) == '92765') | (str(x) == '92768') | (str(x) ==  '92770')) :
        return 'Volume'   
    else:
        return 'Rate per 100,000 persons'    
table['Measure Type'] = table.apply(lambda row: user_perc(row['Indicator']), axis = 1)


def user_perc(x):
    
    if str(x) == '92772':
        return 'premises-licensed-per-sq-km'
    elif ((str(x) ==  '92763') | (str(x) == '92765') | (str(x) == '92768') | (str(x) ==  '92770')) :
        return 'litres-alcohol-per-adult'   
    else:
        return 'people'    
table['Unit'] = table.apply(lambda row: user_perc(row['Indicator']), axis = 1)

table = table[['Geography','Period','Sex', 'Age','Indicator',\
                       'Value','Measure Type','Unit', 'CI Lower','CI Upper']]

out = Path('out')
out.mkdir(exist_ok=True, parents=True)
table.drop_duplicates().to_csv(out / 'observations.csv', index = False)

scraper.dataset.family = 'health'
scraper.dataset.theme = THEME['health-social-care']
with open(out / 'dataset.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

table


