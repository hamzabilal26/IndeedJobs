import time
import csv
from playwright.sync_api import sync_playwright
from datetime import date
from datetime import datetime
from datetime import timedelta

t_date = date.today().strftime("%m-%d-%y, ")
# print(t_date)

today_date = date.today()
# print(today_date)

yesterday = date.today() - timedelta(days=1)
# print(yesterday)

t_time = datetime.now().strftime("%H:%M:%S")
# print(t_time)


location = input("Enter your location: ")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(f"https://ca.indeed.com/jobs?q=software+developer&l={location}&sc=0kf%3Ajt%28fulltime%29%3B&radius=35&fromage=1&filter=0&vjk=0db17ea830e70ce0")

    # page.goto("https://www.indeed.com/jobs?q=Allied+associates+international&l=United+States&vjk=bfdfae513bf9fa42")

    time.sleep(2)
    page.locator("//a[@class='jcs-JobTitle css-jspxzf eu4oa1w0']")

    next = True
    with open(f'{location} {t_date}{t_time}.csv', 'x', newline='', encoding="utf-8",) as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company name", "Location", "Date Posted", "Salary", "Responsive Employer", "Description", "Website Url", "Indeed Url"])

        while next == True:
            jobs = page.query_selector_all("//a[@class='jcs-JobTitle css-jspxzf eu4oa1w0']")


            for each in jobs:
                each.click()

                time.sleep(4)


                title = page.query_selector("//div[@class='jobsearch-RightPane']//h2/span").inner_text()
                f_title = title.replace("- job post", "")
                print(f_title.strip())

                try:
                    company = page.query_selector("//div[@class='jobsearch-CompanyInfoContainer']//a").inner_text()
                    print(company)
                except:
                    company = " "

                location = page.query_selector("//div[@class='css-6z8o9s eu4oa1w0']/div").inner_text()
                print(location)

                date_posted = page.query_selector("//div[contains(@class, 'vjs-highlight ')]//span[@class='date']").inner_text()
                if "1 day" in date_posted:
                     job_date = yesterday
                else:
                    job_date = today_date

                print(f"Date Posted: {job_date}")

                try:
                    salary = page.query_selector("//div[@id='salaryInfoAndJobType']/span[@class='css-2iqe2o eu4oa1w0']").inner_text()
                    print(salary)
                except:
                    print('Not found')
                    salary = "Not listed"

                desc = page.query_selector("//div[@id='jobDescriptionText']").inner_text()
                print(desc)
                try:
                    web = page.query_selector("//a[@contenthtml='Apply on company site']").get_attribute('href')
                    print(web)
                except:
                    web = "Website Url Not Found"
                    print(web)

                try:
                    indeed = page.query_selector("//span[@id='indeed-apply-widget']").get_attribute('data-indeed-apply-joburl')
                    print(indeed)
                except:
                    indeed = "Indeed Url not found"
                    print(indeed)

                try:
                    res = page.query_selector("//div[@id='employerResponsiveContainer']/div//div").inner_text()
                    # print(res)

                    responsive = "Yes"
                except:
                    responsive = "No"

                print(f"Responsive: {responsive}")

                writer.writerow([f_title.strip(), company, location, job_date, salary, responsive, desc, web, indeed])
                print("..................................")


            try:
                page.locator("//a[@data-testid='pagination-page-next']").click()
                time.sleep(2)
                print("next page found")
            except:
                next = False

                print("........................Process Ended.......................")




#https://www.indeed.com/jobs?q=software+developer&l={location}&sc=0bf%3Aexrec%28%29%2Ckf%3Aexplvl%28ENTRY_LEVEL%29jt%28fulltime%29%3B&radius=25&fromage=1&filter=0&vjk=e688dd7cfe2c88cc