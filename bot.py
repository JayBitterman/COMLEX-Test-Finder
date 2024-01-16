from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time
import datetime

# Select a date range for when you want to take the test
start_date = "2024/3/24"
end_date = "2024/4/11"
# Find test centers close to your zip code
my_zip = "11111"
months = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

# Must have a compatible chromedriver
ser = Service(r"C:\Program Files (x86)\chromedriver.exe")
driver = webdriver.Chrome(service=ser)
while True:
    try:
        driver.get("https://home.pearsonvue.com/Clients/NBOME.aspx")
        time.sleep(1)
        try:
            driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
        except NoSuchElementException:
            pass

        driver.find_element(By.XPATH,
                            "//*[@id='form']/div[4]/div/content/div[2]/div[2]/div/div[1]/div[1]/ul/li[1]/a").click()
        # COMLEX Accomodation/No Accomodation
        driver.find_element(By.XPATH, '//*[@id="buttonGroup_3870-0"]/h2/a').click()
        time.sleep(1)
        #CML1/CML2...
        driver.find_element(By.XPATH, '//*[@id="memberExamSeries_49257-3870_link"]/span[2]').click()

        search_bar = driver.find_element(By.XPATH, '//*[@id="testCentersNearAddress"]')
        search_bar.send_keys(my_zip)
        # Submit search
        driver.find_element(By.XPATH, '//*[@id="addressSearch"]').click()


        def scroll():
            try:
                time.sleep(2)
                showMore = driver.find_element(By.XPATH, '//*[@id="showMore"]')
                # Show more results
                for n in range(5):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    showMore.click()
            except StaleElementReferenceException:
                pass


        scroll()

        # We can enable a Random starting selection, weighted toward closer sites

        # start = random.choices(population=[x for x in range(25)], weights=[52 - i for i in range(0, 50, 2)], k=1)[0]
        # for result_num in range(start, 25):

        # Or always start from the beginning/closest result and loop from there
        for result_num in range(25):
            # Select next result
            driver.find_element(By.XPATH, f'//*[@id="selectedTestCenters:{result_num}"]').click()
            driver.find_element(By.XPATH, '//*[@id="continueBottom"]').click()
            # Find open days within 2 months
            for x in range(2):
                time.sleep(1)
                open_days = driver.find_elements(By.XPATH, '//td[@data-handler="selectDay"]')
                for day in open_days:
                    day_date = datetime.datetime.strptime(str(day.get_dom_attribute("data-year")) + "/" +
                                                          str(months[driver.find_element(By.XPATH,'//*[@class="ui-datepicker-month"]').text]) + "/" + str(day.text), "%Y/%m/%d")
                    if day_date <= datetime.datetime.strptime(end_date, "%Y/%m/%d") and day_date >= datetime.datetime.strptime(start_date, "%Y/%m/%d"):
                        location = driver.find_element(By.ID, 'selectedCentersTable').text
                        # Send notification message
                        print("Found an open spot!\n" + str(day_date) + "\n" + location + "\n")
                # Look at next month
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//*[@class='ui-icon ui-icon-circle-triangle-e']"))).click()
            time.sleep(1.5)
            # Look at other results
            driver.find_element(By.XPATH, '//*[@id="changeTestCenterLink"]').click()
            # Deselect previous result
            scroll()
            driver.find_element(By.XPATH, f'//*[@id="selectedTestCenters:{result_num}"]').click()
    except:
        pass
