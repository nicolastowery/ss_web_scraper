from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time


# SS mfn (hyphen) and sku
sprayer_supplies = 'csv/ss_products.csv'

# SD mfn (no hyphen)
sprayer_depot_mfn = 'csv/sd_mfn.csv'

# SD file to write to
sprayer_depot_prices = 'csv/sd_scraped_prices.csv'

# browser setup
options = Options()
browser = webdriver.Chrome(executable_path=r'C:\cmder\bin\chromedriver.exe', options=options)
url = "https://www.sprayerdepot.com/"
browser.get(url)

# locate search box on page
input_field = browser.find_element(By.NAME, 'q')

# open the sprayer_depot_mfn to read from
with open(sprayer_depot_mfn, 'r') as depot_in:
    depot_reader = csv.reader(depot_in)

    # open the sprayer_supples to read from (mfn and sku)
    with open(sprayer_supplies, 'r') as supplies_in:
        supplies_reader = csv.reader(supplies_in)

        # open the sprayer_depot_prices file to write to
        with open(sprayer_depot_prices, 'w', newline="") as csvfile_out:
            writer = csv.writer(csvfile_out, delimiter=',')
            item_count = 0

            # column headers (SD_MFN exists only for testing purposes)
            writer.writerow(['SKU', 'MFN', 'SD_MFN', 'Sprayer Depot'])

            # try is to catch end of iteration
            try:

                # iterate through both the depot and supplies csv files.
                # for each row, write the SKU, MFN, SD_MFN, and price (from the website)
                for row1, row2 in zip(depot_reader, supplies_reader):

                    # item_count only exists for console log
                    item_count += 1
                    item = ""
                    price = ""

                    # clears the search box, primes it for new input
                    input_field.clear()

                    # takes SD_MF, inputs it into the search bar
                    input = row1[0]
                    input_field.send_keys(input)

                    # allows the browser time to load the data
                    time.sleep(2)

                    # finds relevant item code and price
                    # if item queried pulls no result, catch exception
                    try:

                        # pulls the item and price from the page and stores them in variables
                        item = browser.find_element(By.CLASS_NAME, 'item-sku').text.split(": ", 1)[1]
                        price = browser.find_element(By.CLASS_NAME, 'regular').text

                        # checks if item pulled is item queried
                        if item == row1[0]:
                            print(str(item_count) + ": " + row1[0] + " " + item + " " + price)
                            writer.writerow([row2[0], row2[1], row1[0], price])
                        else:  # item is not the item queried
                            print(str(item_count) + ": SD doesn't contain " + row1[0] + ", pulls " + item)
                            writer.writerow([row2[0], row2[1], row1[0], "N/A"])
                    except NoSuchElementException:  # item queried returned no results
                        print(str(item_count) + ": SD doesn't contain " + row1[0])
                        writer.writerow([row2[0], row2[1], row1[0], "N/A"])
            except IndexError:
                print("end of file")
