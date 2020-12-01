from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import csv
import codecs
import re
import datetime


with open("separate_counter.txt", "r") as cnt:
    counter = cnt.read()

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.alza.cz/wearables/18855068.htm#f&cst=0&cud=0&pg=1-50&prod=&sc=1022")
print("20 seconds timeout to load whole page in selenium.")
sleep(20)


res = driver.page_source

soup = BeautifulSoup(res, "html.parser")

pretty_soup = soup.prettify()

html_file = open("htmls/alza_main1.html", "wb")
html_file.write(pretty_soup.encode('utf-8'))
html_file.close()

new_file = open("htmls/alza" + counter + ".html", "wb")
new_file.write(pretty_soup.encode('utf-8'))
new_file.close()

driver.quit()

print("5 seconds timeout")
sleep(5)

iter_num = open("separate_counter.txt", "r")
iter_cnt = int(iter_num.read())
iter_num.close()
iter_cnt += 1
iter_num_update = open("separate_counter.txt", "w")
iter_num_update.write(str(iter_cnt))
iter_num_update.close()


with open("separate_counter.txt", "r") as cnt:
    a = cnt.read()
    now = datetime.datetime.now()
    formated_time = now.strftime("%d.%m")
    file_name = formated_time + "." + a


scrap_file = codecs.open("htmls/alza_main.html", "r", "utf-8")

soup = BeautifulSoup(scrap_file, "lxml")

regex = re.compile(".*box browsingitem.*")
regex_class_condition = re.compile(".*avl.*")


with open("csvs/" + file_name + ".csv", 'w', encoding="utf-8", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Product name", "Condition", "Order Number", "Description", "Rating", formated_time])

    for product in soup.find_all("div", class_=regex):

        name_tag = product.find("div", class_="fb").a.text
        refined_name_tag = " ".join(name_tag.split())

        condition = product.find("div", class_=regex_class_condition).span.text
        refined_condition = re.findall(
            r"(Skladem|Rozbaleno skladem|Na cestě|Na objednávku|Očekáváme|Použité skladem|Těšíme se|Zánovní skladem)", condition[0:40])
        refined_condition = " ".join(refined_condition)

        order_nr = product.find("span", class_="code").text
        refined_order_nr = " ".join(order_nr.split())

        description = product.find("div", class_="Description").text
        refined_description = " ".join(description.split())
        try:
            rating = product.find("div", class_="star-rating-wrapper")["title"]
            refined_rating = rating[10:13]
        except KeyError:
            refined_rating = None

        try:
            price = product.find("span", class_="c2").text
            refined_price = re.findall(r"[0-9]+", price)
            refined_price = " ".join(refined_price)
        except AttributeError:
            refined_price = None

        csv_writer.writerow([refined_name_tag, refined_condition, refined_order_nr, refined_description, refined_rating, refined_price])

scrap_file.close()

print("Finished")
raise SystemExit
