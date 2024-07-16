## Importing Required libraries
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import datetime as dt

## Prompt user for input
state = input("Enter the State Name: ")
district = input("Enter the District Name(All letters in Capital): ")

## Path to the ChromeDriver
chromedriver_path = r'C:/Users/ppsam/OneDrive/Desktop/DP/chromedriver-win64/chromedriver.exe'  
service = Service(chromedriver_path)   

## Setup Selenium WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service = service, options = options)

## url of the website to scrape
url = "https://www.indiapost.gov.in/vas/pages/findpincode.aspx"
driver.get(url)
driver.maximize_window

## select the state from the dropdown
element_dropdown = driver.find_element("id", "ctl00_SPWebPartManager1_g_28a6af46_5d77_4b7e_aaa2_68d16bfca954_ctl00_drpStates")
select = Select(element_dropdown)
try:
    select.select_by_visible_text(state)
except NoSuchElementException:
    print('The state does not exist')
    
## select the district from the dropdown
element_dropdown = driver.find_element("id", "ctl00_SPWebPartManager1_g_28a6af46_5d77_4b7e_aaa2_68d16bfca954_ctl00_drpDistricts")
select = Select(element_dropdown)
try:
    select.select_by_visible_text(district)
except NoSuchElementException:
    print('The district does not exist')
    
## Wait to type the captcha
time.sleep(15)

## Click the search button
search_button = driver.find_element(By.ID, 'ctl00_SPWebPartManager1_g_28a6af46_5d77_4b7e_aaa2_68d16bfca954_ctl00_btnSearch')
search_button.click()
time.sleep(3)

## Initialize a DataFrame to store the results
pincode_df = pd.DataFrame(columns = ['PostOffice', 'Pincode', 'District'])

## Page Handling
j=2
prev_n = '1'
while True:
    row = driver.find_elements(By.XPATH, f'//*[@id="ctl00_SPWebPartManager1_g_28a6af46_5d77_4b7e_aaa2_68d16bfca954_ctl00_gvPinCodeDetails"]/tbody/tr[12]/td/table/tbody/tr[1]/td')
#     print(len(row))
    for i in range(j,len(row)+1):
        time.sleep(4)
        
        ## Find the next page button
        next_page_button = driver.find_element(By.XPATH, f'//*[@id="ctl00_SPWebPartManager1_g_28a6af46_5d77_4b7e_aaa2_68d16bfca954_ctl00_gvPinCodeDetails"]/tbody/tr[12]/td/table/tbody/tr[1]/td[{i}]')
        n = next_page_button.text
        if (prev_n=='...' and (int(n)%10) != 2):
            continue
        
        ## Extract data from the current page
        post_offices = driver.find_elements(By.XPATH, '//*[@id="ctl00_SPWebPartManager1_g_28a6af46_5d77_4b7e_aaa2_68d16bfca954_ctl00_gvPinCodeDetails"]//tbody/tr/td[1]')
        pincodes = driver.find_elements(By.XPATH, '//*[@id="ctl00_SPWebPartManager1_g_28a6af46_5d77_4b7e_aaa2_68d16bfca954_ctl00_gvPinCodeDetails"]//tbody/tr/td[2]')
        districts = driver.find_elements(By.XPATH, '//*[@id="ctl00_SPWebPartManager1_g_28a6af46_5d77_4b7e_aaa2_68d16bfca954_ctl00_gvPinCodeDetails"]//tbody/tr/td[3]')
        time.sleep(5) 
        
        ## Append the data to the DataFrame 
        for k in range(10):   
            pincode_df = pd.concat([pincode_df, pd.DataFrame([[post_offices[k].text, pincodes[k].text, districts[k].text]], columns = ['PostOffice', 'Pincode', 'District'])])

        
        time.sleep(2)
        
        ## Click the next page button
        prev_n = n
        next_page_button.click()
        if i==len(row):
            j=3
        
    time.sleep(2)
    ## Condition to exit from the while loop
    if (len(row)<11):
        break

## Remove the duplicates
pincode_df.drop_duplicates(inplace = True)

## Save the DataFrame in csv format
formatted_date = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
pincode_df.to_csv(f"{district}_{formatted_date}.csv", index=False, header=True)
print(f"Scraping completed. Data saved to {district}_{formatted_date}.csv")

## Close the webdriver
driver.quit()