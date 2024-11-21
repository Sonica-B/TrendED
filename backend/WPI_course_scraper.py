import requests
from bs4 import BeautifulSoup
import pandas as pd

index_url = 'https://www.wpi.edu/academics/academic-catalog/course-descriptions'

response = requests.get(index_url)
index_soup = BeautifulSoup(response.text, 'html.parser')

courses_data = []

department_links = index_soup.select('a[href*="/academics/calendar-courses/course-descriptions/"]')

for department_link in department_links:
    department_name = department_link.get_text(strip=True)
    department_url = department_link.get('href')
    if not department_url.startswith('https'):
        department_url = f"https://www.wpi.edu{department_url}"

    department_response = requests.get(department_url)
    department_soup = BeautifulSoup(department_response.text, 'html.parser')

    course_entries = department_soup.select('div.views-row')

    for course_entry in course_entries:
        title_element = course_entry.select_one('h3')
        if title_element:
            code_title_text = title_element.get_text(strip=True)
            code, title = code_title_text.split('.', 1)
            code = code.strip()
            title = title.strip()

        description_element = course_entry.select_one('p')
        description = description_element.get_text(strip=True) if description_element else "Description not found"

        course_data = {
            'Department': department_name,
            'Code': code,
            'Title': title,
            'Description': description
        }

        courses_data.append(course_data)

df = pd.DataFrame(courses_data)

df.to_json('course_descriptions.json', index=False)

print("Data has been exported to course_descriptions.xlsx")
