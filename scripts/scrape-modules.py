import os
import requests
import time
from bs4 import BeautifulSoup
from string import ascii_uppercase, digits
import mechanize
from pymongo import MongoClient

mongo_client = MongoClient('mongodb+srv://server-app:tJFQPyB3TPD2EF9Y@studentportal-uhvtp.mongodb.net/'
                           '?retryWrites=true&w=majority')
studentportal_db = mongo_client.studentportal
raw_data_db = mongo_client.raw_data
module_links_file_path = 'module_links.txt'
finished_module_file_path = 'finished_modules.txt'
base_url = 'https://www.modules.napier.ac.uk/'
done_module_links = []
module_links = []
modules = {}


def only_numerics(seq):
    seq_type = type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))


def first_content_only(elem):
    if elem and len(elem.contents) > 0:
        return elem.contents[0]
    else:
        return ""


def parse_module_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('Module.aspx?ID='):
            module_links.append(href)
            module_links_file.write(href + '\n')


def parse_single_module(module_url):
    br = mechanize.Browser()
    br.open(base_url + module_url)
    response = br.response()

    soup = BeautifulSoup(response.read(), 'html5lib')

    prerequisites_html_utf8 = []
    if soup.find(id='ctl00_ContentPlaceHolder1_LBLpre'):
        prerequisites_html = soup.find(id='ctl00_ContentPlaceHolder1_LBLpre').contents
        for elem in prerequisites_html:
            prerequisites_html_utf8.append(elem.encode(encoding='UTF-8', errors='strict'))

    module_content_description_html_utf8 = []
    if soup.find(id='ctl00_ContentPlaceHolder1_LBLmodcontent'):
        module_content_description_html = soup.find(id='ctl00_ContentPlaceHolder1_LBLmodcontent').contents
        for elem in module_content_description_html:
            module_content_description_html_utf8.append(elem.encode(encoding='UTF-8', errors='strict'))

    learning_outcomes_html_utf8 = []
    if soup.find(id='ctl00_ContentPlaceHolder1_LBLoutcomes'):
        learning_outcomes_html = soup.find(id='ctl00_ContentPlaceHolder1_LBLoutcomes').contents
        for elem in learning_outcomes_html:
            learning_outcomes_html_utf8.append(elem.encode(encoding='UTF-8', errors='strict'))

    reading_list_html_utf8 = []
    if soup.find(id='ctl00_ContentPlaceHolder1_PNLreading'):
        reading_list_html = soup.find(id='ctl00_ContentPlaceHolder1_PNLreading').contents
        for elem in reading_list_html:
            reading_list_html_utf8.append(elem.encode(encoding='UTF-8', errors='strict'))

    module_leader_name = ''
    module_leader_email = ''
    if soup.find(id='ctl00_ContentPlaceHolder1_LBLModleader').find('a'):
        module_leader_name = soup.find(id='ctl00_ContentPlaceHolder1_LBLModleader').find('a').contents[0]
        module_leader_email = soup.find(id='ctl00_ContentPlaceHolder1_LBLModleader').find('a').get('href')

    module = {
        "module_title": first_content_only(soup.find(id='ctl00_ContentPlaceHolder1_LBLtitle')),
        "scqf_level": only_numerics(first_content_only(soup.find(id='ctl00_ContentPlaceHolder1_LBLscqllevel')).strip()),
        "scqf_credit_value": first_content_only(soup.find(id='ctl00_ContentPlaceHolder1_LBLscqlvalue')),
        "ects_credit_value": first_content_only(soup.find(id='ctl00_ContentPlaceHolder1_LBLscqlcredit')),
        "module_code": first_content_only(soup.find(id='ctl00_ContentPlaceHolder1_LBLmoduleCode')),
        "module_leader": {
            "name": module_leader_name,
            "email": module_leader_email
        },
        "school": first_content_only(soup.find(id='ctl00_ContentPlaceHolder1_LBLschool')),
        "subject_area_group": first_content_only(soup.find(id='ctl00_ContentPlaceHolder1_LBLsubject')),
        "prerequisites_html": prerequisites_html_utf8,
        "module_content_description_html": module_content_description_html_utf8,
        "learning_outcomes_html": learning_outcomes_html_utf8,
        "reading_list_html": reading_list_html_utf8
    }

    teaching_instance_html = soup.find(id='ctl00_ContentPlaceHolder1_AccordionOcc').contents
    teaching_instance_html_utf8 = []
    for elem in teaching_instance_html:
        teaching_instance_html_utf8.append(elem.encode(encoding='UTF-8', errors='strict'))

    teaching_instance = {
        "module_code": module["module_code"],
        "html": teaching_instance_html_utf8
    }

    studentportal_db.modules.insert_one(module)
    raw_data_db.raw_module_teaching_instances.insert_one(teaching_instance)
    print("Finished module: " + module["module_code"])


if os.path.exists(finished_module_file_path):
    with open(finished_module_file_path) as finished_module_file:
        for line in finished_module_file:
            done_module_links.append(line)

if os.path.exists(module_links_file_path) and os.path.getsize(module_links_file_path) > 0:
    print("Found existing modules file, continuing.")
else:
    print("Couldn't find existing modules file, creating and populating file before continuing.")
    with open(module_links_file_path, 'w') as module_links_file:
        for c in ascii_uppercase:
            url = base_url + 'Home.aspx?ID=1&Letter=' + c
            parse_module_list(url)

with open(module_links_file_path, 'r') as module_links_file:
    for line in module_links_file:
        if line not in done_module_links:
            parse_single_module(line)
        else:
            print(line.rstrip('\n') + ' found in finished_modules.txt, skipping this line.')