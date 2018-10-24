import pandas as pd
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from collections import OrderedDict
from io import StringIO

def download_foodsafety_data_and_convert_to_csv(xml_id='FHRS776en-GB.xml', out_fpath='food_safety.csv'):
    """
    Downloads food safety data given the local authority id which can be 
    found at http://ratings.food.gov.uk/open-data/en-GB 
    """
    url = 'http://ratings.food.gov.uk/OpenDataFiles/{}'.format(xml_id)
    response = urlopen(url)
    content = StringIO(response.read().decode())

    def get_info_from_xml():
        etree = ET.parse(content)
        root = etree.getroot()
        for enstab in root.iter('EstablishmentDetail'):
            d = OrderedDict()
            for item in enstab:
                if item.tag == 'Geocode':
                    for ll_info in item:
                        d[ll_info.tag] = float(ll_info.text)
                else:
                    d[item.tag] = item.text
            yield d

    df = pd.DataFrame(list(get_info_from_xml()))
    df.to_csv(out_fpath, index=None)