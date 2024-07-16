# Automated-Web-Scraping-of-Indian-Postal-Codes-Using-Selenium
This script uses Selenium to scrape pincode information from the India Post website. The user is prompted to enter a state and district, and the script navigates through the website to retrieve and save the relevant pincode information in a CSV file.
### Requirements
- Python
- ChromeDriver
- Selenium
### Steps
1. Prompt User Input:
   - The script starts by asking the user to input the state and district.
    
3. Setup Selenium WebDriver:
   - Initializes the ChromeDriver with optional headless mode.
     
4. Navigate to Website:
   - Opens the India Post website and maximizes the browser window.
     
5. Select State and District:
   - Finds the dropdown elements for the state and district, and selects the user-provided options.
     
6. Enter Captcha:
   - Manually you have to enter the captcha.
     
7. Search and Scrape Data:
   - Clicks the search button and waits for the results to load.
   - Iterates through the pagination and extracts the pincode information, storing it in a Pandas DataFrame.
     
8. Save Results:
   - Removes duplicate entries and saves the DataFrame to a CSV file with a timestamp in the filename.
     
9. Close WebDriver:
   - Closes the browser window.
     
