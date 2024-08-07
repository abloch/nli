import requests
from bs4 import BeautifulSoup
from unicodedata import normalize
from datetime import date


BASE_URL = "https://www.nli.org.il"
DATES_ENDPOINT = "/he/newspapers/?a=cl&cl=CL2&e=-------he-20--1--img-txIN%7CtxTI--------------1"

HEADERS = {
    "user-agent": "Mozilla/5.0"
}

session = requests.session()


def get_months_soup():    
    html = session.get(BASE_URL + DATES_ENDPOINT, headers=HEADERS).content
    return BeautifulSoup(html, "html.parser")


def isbadchar(c: chr) -> bool:
    return ord(c) > 5100

def normalized_text(escaped_string: str) -> str:
    decoded = escaped_string.encode('utf-8').decode('utf-8')
    return "".join([ f"" if isbadchar(c) else c for c in decoded ]).strip()


def get_months():
    soup = get_months_soup()
    years_div = soup.css.select("#datebrowserrichardtoplevelcalendar")
    if not years_div:
        raise Exception(f"Couldn't find years div, no #datebrowserrichardtoplevelcalendar tag in {DATES_ENDPOINT}")
    return years_div[0].find_all(class_="nav-item")


def get_months_links():
    return {month['id'].replace("li-", ""): month.a['href'] for month in get_months() if month.a}


def get_nespapers_soup_for_month(date_of_interest: date):
    formatted_month = date_of_interest.strftime("%m-%Y")
    endpoint = get_months_links().get(formatted_month)
    html = session.get(BASE_URL + endpoint, headers=HEADERS).content
    return BeautifulSoup(html, "html.parser")


def isinteresting(paper: str) -> bool:
    return paper in INTERESTING_NEWSPAPERS

def get_nespaper_links_for_month(date_of_interest: date):
    soup = get_nespapers_soup_for_month(date_of_interest)
    date_elements = soup.find_all(class_="datebrowserrichardmonthlevelcalendardaycellcontents")
    ret = {}
    for date_element in date_elements:
        day = normalized_text(date_element.b.text)
        link = date_element.a
        if not link:
            continue
        paper_links = date_element.find_all("a")
        daylink = {
            normalized_text(paper_link.text): paper_link["href"]
            for paper_link in paper_links
            if paper_link.string and paper_link["href"] and not paper_link.parent.find(title="נעול")
        }
        if daylink:
            ret[day] = daylink
    return ret
