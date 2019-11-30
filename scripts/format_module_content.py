from pymongo import MongoClient
from bs4 import BeautifulSoup, element

mongo_client = MongoClient('mongodb+srv://local-home:Wigbhi5M@studentportal-uhvtp.mongodb.net/'
                           '?retryWrites=true&w=majority')
studentportal_db = mongo_client.studentportal
raw_data_db = mongo_client.raw_data


# for elem in raw_data_db.raw_module_teaching_instances.find_one()['html']:
#     print(elem)


def get_instances_for_module(module_code):
    raw_data_module = raw_data_db.raw_module_teaching_instances.find_one({'module_code': module_code})
    html = raw_data_module['html']
    html = html[2:-1]  # Remove b'\n\t\t' at start and b'\n\t' at end
    instances = []
    for i in range(0, len(html) - 1, 2):
        soup1 = BeautifulSoup(html[i].decode('utf-8'), 'html5lib')
        base = soup1.find('div', {'class': 'modCatTable'}).contents
        soup2 = BeautifulSoup(html[i + 1].decode('utf-8'), 'html5lib')
        detail = soup2.find('div', {'class': 'modCatTable2'}).contents

        instance = {}

        if base and detail:
            split_content = base[0].split(',')
            instance['term'] = split_content[0].strip()
            instance['trimester'] = split_content[1].strip()
            tables = soup2.find_all('table')

            cells = tables[0].find_all('td')
            try:
                instance['occurrence'] = cells[1].contents[0].strip()
            except:
                instance['occurrence'] = ''
            try:
                instance['delivery_mode'] = split_content[2].strip()
            except:
                instance['delivery_mode'] = ''
            try:
                instance['delivery_location'] = cells[5].contents[0].strip()
            except:
                instance['delivery_location'] = ''
            try:
                instance['partner'] = split_content[3].strip()
            except:
                instance['partner'] = ''
            instance['delivery_staff_member'] = {}
            try:
                instance['delivery_staff_member']['name'] = cells[9].contents[0].contents[0].strip()
            except:
                instance['delivery_staff_member']['name'] = ''
            try:
                instance['delivery_staff_member']['email'] = cells[9].contents[0].get('href')[7:]
            except:
                instance['delivery_staff_member']['email'] = ''
            instance['module_organiser'] = {}
            try:
                instance['module_organiser']['name'] = cells[11].contents[0].contents[0].strip()
            except:
                instance['module_organiser']['name'] = ''
            try:
                instance['module_organiser']['email'] = (cells[11].contents[0].get('href')[7:])
            except:
                instance['module_organiser']['email'] = ''

            cells = tables[2].find_all('td')
            instance['lta_approach'] = []
            try:
                for line in cells[0].contents:
                    if isinstance(line, element.NavigableString) and line.strip():
                        instance['lta_approach'].append(line.strip())
            except:
                pass
            cells = tables[4].find_all('td')
            instance['formative_assessment'] = []
            try:
                for line in cells[0].contents:
                    if isinstance(line, element.NavigableString) and line.strip():
                        instance['formative_assessment'].append(line.strip())
            except:
                pass
            cells = tables[6].find_all('td')
            instance['summative_assessment'] = []
            try:
                for line in cells[0].contents:
                    if isinstance(line, element.NavigableString) and line.strip():
                        instance['summative_assessment'].append(line.strip())
            except:
                pass

            rows = tables[7].find_all('tr')
            instance['student_activity'] = {}
            instance['student_activity']['activities'] = []
            for row in rows:
                title = row.find('span', {'class': 'title'})
                cells = row.find_all('td')
                if title and title.contents[0].strip() == 'Total Study Hours':
                    instance['student_activity']['total_study_hours'] = cells[2].contents[0].contents[0].strip()
                elif title and title.contents[0].strip() == 'Expected Total Study Hours for Module':
                    instance['student_activity']['expected_total_study_hours'] = cells[2].contents[0].contents[
                        0].strip()
                elif title and title.contents[0].strip() == 'Mode of activity':
                    pass
                elif title and title.contents[0].strip().startswith('Student Activity'):
                    pass
                else:
                    try:
                        mode = cells[0].contents[0]
                    except:
                        mode = ''
                    try:
                        type = cells[1].contents[0]
                    except:
                        type = ''
                    try:
                        study_hours = cells[2].contents[0]
                    except:
                        study_hours = ''
                    instance['student_activity']['activities'].append({
                        'mode': mode,
                        'type': type,
                        'study_hours': study_hours
                    })

            if len(tables) >= 9:
                rows = tables[8].find_all('tr')
            instance['assessment'] = {}
            instance['assessment']['assessments'] = []
            for row in rows:
                title = row.find('span', {'class': 'title'})
                cells = row.find_all('td')
                if title and title.contents[0].strip() == 'Assessment':
                    pass
                elif title and title.contents[0].strip() == 'Type of Assessment':
                    pass
                elif title and title.contents[0].strip() == 'Component 1 subtotal:':
                    instance['assessment']['component1_subtotal'] = cells[1].contents[0].contents[0]
                elif title and title.contents[0].strip() == 'Component 2 subtotal:':
                    instance['assessment']['component2_subtotal'] = cells[1].contents[0].contents[0]
                elif title and title.contents[0].strip() == 'Module subtotal:':
                    instance['assessment']['module_subtotal'] = cells[1].contents[0].contents[0]
                else:
                    try:
                        weighting = cells[1].contents[0].strip()
                    except:
                        weighting = ''
                    try:
                        lo_covered = cells[2].contents[0].strip()
                    except:
                        lo_covered = ''
                    try:
                        week_due = cells[3].contents[0].strip()
                    except:
                        week_due = ''
                    try:
                        split_length = cells[4].contents[0].strip().split(',')
                    except:
                        split_length = []
                    length_hours = ''
                    length_words = ''
                    try:
                        if split_length[0].startswith('HOURS'):
                            length_hours = split_length[0].strip()[7:]
                        elif split_length[0].startswith('WORDS'):
                            length_words = split_length[1].strip()[7:]
                    except:
                        pass
                    try:
                        if split_length[1].startswith('HOURS'):
                            length_hours = split_length[0].strip()[7:]
                        elif split_length[1].startswith('WORDS'):
                            length_words = split_length[1].strip()[7:]
                    except:
                        pass

                    instance['assessment']['assessments'].append({
                        'weighting': weighting,
                        'lo_covered': lo_covered,
                        'week_due': week_due,
                        'length_hours': length_hours,
                        'length_words': length_words
                    })

            instances.append(instance)
    return instances


def parse_prerequisites_html(module):
    module['prerequisites'] = []
    for html in module['prerequisites_html']:
        soup = BeautifulSoup(html.decode('utf-8'), 'html5lib')
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 1:
            print(len(paragraphs))
        for par in paragraphs:
            for line in par.contents:
                if isinstance(line, element.NavigableString):
                    module['prerequisites'].append(line.strip())
    module.pop('prerequisites_html')
    return module


def parse_module_content_description_html(module):
    module['module_content_description'] = []
    for html in module['module_content_description_html']:
        soup = BeautifulSoup(html.decode('utf-8'), 'html5lib')
        paragraphs = soup.find_all('p')
        if len(paragraphs) > 1:
            print(len(paragraphs))
        for par in paragraphs:
            for line in par.contents:
                if isinstance(line, element.NavigableString):
                    module['module_content_description'].append(line.strip())
    module.pop('module_content_description_html')
    return module


def parse_learning_outcomes_html(module):
    module['learning_outcomes'] = []
    for html in module['learning_outcomes_html']:
        if isinstance(html, element.NavigableString):
            continue
        soup = BeautifulSoup(html.decode('utf-8'), 'html5lib')
        paragraphs = soup.find_all('p')
        for par in paragraphs:
            for line in par.contents:
                if isinstance(line, element.NavigableString):
                    module['learning_outcomes'].append(line.strip())
    module.pop('learning_outcomes_html')
    return module


def parse_reading_list_html(module):
    module['reading_list'] = []
    html = module['reading_list_html']
    html = html[1:-1]  # Remove b'\n\t\t' at start and b'\n\t' at end
    for row in html:
        soup = BeautifulSoup(row.decode('utf-8'), 'html5lib')
        reading_list = soup.find_all(id='ctl00_ContentPlaceHolder1_LBLurlreading')
        for item in reading_list:
            if item.find('a'):
                module['reading_list'].append({
                    'name': item.find('a').contents[0],
                    'href': item.find('a').get('href')
                })
    module.pop('reading_list_html')
    return module


# modules = list(studentportal_db.modules.find({'module_code': 'CTR09109'}))
modules = list(studentportal_db.modules.find())

for module in modules:
    try:
        print(module['module_code'])
    except:
        continue
    module = parse_prerequisites_html(module)
    module = parse_module_content_description_html(module)
    module = parse_learning_outcomes_html(module)
    module = parse_reading_list_html(module)
    module['teaching_instances'] = get_instances_for_module(module['module_code'])
    module['_id'] = module['module_code']
    module.pop('module_code')
    studentportal_db.modules.insert_one(module)
    studentportal_db.modules.delete_many({'module_code': module['_id']})
