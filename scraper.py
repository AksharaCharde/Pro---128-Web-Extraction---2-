from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

# Website Link
WEBSITE_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

# Initialize The Webdriver
browser = webdriver.Chrome("chromedriver_win32")
browser.get(WEBSITE_URL)

time.sleep(10)

new_scraped_data = []

# Define Data Scrapping Method
def scrape_more_data(hyperlink):
    try:
            page = requests.get(hyperlink)

            ## ADD CODE HERE ##
            soup = BeautifulSoup(browser.page_source, "html.parser")

            temp_list = []

            for tr_tag in soup.find_all("tr", attrs = {"class": "fact_row"}):
                td_tags = td_tag.find_all("td")
               
                for td_tag in td_tags:
                   
                        try: 
                            temp_list.append(td_tag.find_all("div", attrs = {"class": "value"})[0].content[0])
                        except:
                            temp_list.append("")

            

                new_scraped_data.append(temp_list)

    except:
            time.sleep(1)
            scrape_more_data(hyperlink)

planetdf1 = pd.read_csv("updated_scrapperddata.csv")

for index, row in planetdf1.iterrows(): 
    print(row['hyperlink']) 
    scrape_more_data(row['hyperlink']) 
    print(f"Data Scraping at hyperlink {index+1} completed")

scrapped_data = [] 

for row in new_scraped_data: 
    replaced = [] 
    for el in row: 
        el = el.replace("\n", "") 
        replaced.append(el) 
    scrapped_data.append(replaced) 
print(scrapped_data)

# Define Header
headers = ["planet_type", "discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

# Define pandas DataFrame   
new_planetdf1 = pd.DataFrame(scrapped_data, columns = headers)

# Convert to CSV
new_planetdf1.to_csv("new_scrappeddata.csv", index = True, index_label = "id")