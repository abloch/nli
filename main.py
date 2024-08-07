from sys import argv
from nli import *
from pprint import pprint
from random import choice
from datetime import datetime

INTERESTING_NEWSPAPERS = [
    "מעריב", "הארץ", "על המשמר", "כותרת ראשית", "הצפה", "מעריב", "דבר", "הבקר", "למרחב", "קול העם", "חדשות", "כל העיר (ירושלים)"
]

INTERESTING_YEARS = list(range(1961, 1987))  # older are hard to read and mostly irrelevant, newer are copyrighted


if len(argv) > 1:
    date = datetime.strptime(argv[1], "%d/%m")
else:
    date = datetime.now()

random_year = choice(INTERESTING_YEARS)
random_date = date.replace(year=random_year)


print(f"getting newspapers for: {random_date.date()}")
papers = get_nespaper_links_for_month(random_date).get(str(random_date.day), {})

interesting_papers = {
    paper: BASE_URL + link
    for paper, link in papers.items()
    if isinteresting(paper)
}
pprint(interesting_papers)