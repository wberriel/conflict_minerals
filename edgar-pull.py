from lxml import html
import requests
import datetime
from functools import reduce
import begin


# This will return the table row with the latest date when 2 are compared. The
# date element is in index 3 of the list on the edgar site.
def latest_date_summary_elements(item1, item2):
    # datetime objects can be created from year,month,day, which is
    # coincidentally the format we are getting, which is YYYY-MM-DD
    date1 = datetime.datetime.strptime(item1[3].text, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(item2[3].text, "%Y-%m-%d")

    if(date1 > date2):
        return item1

    return item2


# Searches an element for another element with a namespace. If it is found, it
# returns the text of the element or an empty string if it is not.
def get_element_text(text_to_find, namespace, element_to_search):
    found_element = element_to_search.find('{}{}'.format(namespace,
                                                         text_to_find))
    if found_element is not None:
        return found_element.text
    else:
        return ''


# Takes a ticker or CIK and returns a list of lists with values.
def edgarSD(CIK):
    website = 'www.sec.gov'
    request_string = 'https://{}/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=SD&dateb=&owner=include&count=40'
    page = requests.get(request_string.format(website, CIK))
    tree = html.fromstring(page.content)

    # ignore header row (first row)
    entries = tree.xpath('//table[@summary="Results"]/tr[position()>1]')

    # Find the latest date in the array of entries, just to be sure they
    # don't change it from latest first.
    try:
        latest_entry = reduce(latest_date_summary_elements, entries)
    except TypeError:
        print('No SD records found for CIK: {}'.format(CIK))
        return []
    link_to_document = latest_entry[1].find('a').attrib['href']

    document_page = requests.get('https://{}{}'.format(
                                                       website,
                                                       link_to_document
                                                      )
                                 )
    document_page_tree = html.fromstring(document_page.content)

    # ignore the header row (first row), so only rows with position > 1
    document_page_links = document_page_tree.xpath(
        '//table[@summary="Document Format Files"]/tr[position()>1]')

    # We want the information table and we want the xml version of it.
    for row in document_page_links:
        if row[3].text.upper() == 'EX-1.01':
            if 'htm' in row[2].text_content():
                html_link = row[2].find('a').get('href')
                break

    return '{}{}'.format(website, html_link)


@begin.start(auto_convert=True)
def run(cik: 'CIK or Ticker of fund to search' ='AAPL',
        ):
    """Fetch data Special Disclosure Data from www.sec.gov/edgar and print out the link to the latest."""
    html_link = edgarSD(cik)
    print(html_link)
