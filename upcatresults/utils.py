import re

STUDENT_NUMBER_RE = re.compile(r'(\d{4}-?\d{5})')

def student_number_processor(student_number):
    if STUDENT_NUMBER_RE.search(student_number):
        return student_number.replace('-', '')
    return None

def year_processor(year):
    return year if year in range(2000, 2100) else None

