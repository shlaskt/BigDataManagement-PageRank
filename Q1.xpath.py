from lxml import html
import requests

URL = "https://en.wikipedia.org/wiki/Andy_Ram"
URL2 = "https://en.wikipedia.org/wiki/Anastasia_Rodionova"
URL3 = "https://en.wikipedia.org/wiki/Vera_Zvonareva"
partner_path = "//table[contains(@class,'sortable')]/tbody/tr/td[count(../../tr/th[contains(text(),'Partner')]/preceding-sibling::th)+1]/a[1]/@href"
opponents_path = "//table[contains(@class,'sortable')]/tbody/tr/td[count(../../tr/th[contains(text(), 'Opponents')]/preceding-sibling::th)+1]/a[1]/@href"
coach_path = "//table[@class = 'infobox vcard']/tbody/tr/th[contains(text(),'Coach')]/../td//a/@href[contains(., 'wiki')]"


def find_partners(doc):
    partners = []
    for i in doc.xpath(partner_path):
        partners.append(i)
    return partners


def find_opponents(doc):
    opponents = []
    for i in doc.xpath(opponents_path):
        opponents.append(i)
    return opponents


def find_coaches(doc):
    coaches = []
    for i in doc.xpath(coach_path):
        coaches.append(i)
    return coaches


def main():
    page = requests.get(URL3)
    doc = html.fromstring(page.content)
    related_people = []
    related_people += (find_partners(doc))
    related_people += (find_opponents(doc))
    related_people += find_coaches(doc)
    for i in related_people:
        print(i)


if __name__ == '__main__':
    main()
