from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from json import dumps, load
from os.path import join, dirname
from time import sleep          


def linkedin_login():
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = Chrome(options=options)        #initialising Chrome object

    driver.get('https://www.linkedin.com/checkpoint/lg/login?trk=hb_signin')        #navigating to the LinkedIn login page 

    username = driver.find_element_by_xpath('//input[@id="username"]')
    password = driver.find_element_by_xpath('//input[@id="password"]')

    username.send_keys("ENTER YOUR LinkedIn USERNAME") #type your own username here
    password.send_keys("ENTER YOUR LinkedIn PASSWORD") #type your own password here

    driver.find_element_by_xpath('//div[@class="login__form_action_container "]').click()

    driver.execute_script("window.open('about:blank', 'tab2');")    #switching to a new tab 
    driver.switch_to.window("tab2")
    return driver

def append_json(temp_dict, file_name):
    try:
        temp=load(open(join(dirname(__file__), file_name), "r", encoding='utf-8'))      #reading data in the from the given file and loading it into the temp variable as a dict
        temp.update(temp_dict)
    except:
        temp=temp_dict
    with open(join(dirname(__file__), file_name), "w", encoding='utf-8') as outfile:    #writing the upadted data to the given file
        outfile.write(dumps(temp, indent = 4))
        outfile.close()

def get_num(temp):
    for x in temp:
        if(x.isalpha()): temp=temp.replace(x,'')       #removing alphabets from string
    return temp.strip()


def scrape_part2(career_type, driver, location_state):

    #Fetching details about jobs of given career type in the given State
    url=f'https://www.linkedin.com/jobs/search/?geoId=102713980&keywords={career_type.lower().replace(" ", "%20")}&location=India'
    driver.get(url) 

    #changing location from India to a particular state
    driver.find_element_by_xpath('//input[@id="jobs-search-box-location-id-ember30"]').send_keys(Keys.CONTROL, 'a')
    driver.find_element_by_xpath('//input[@id="jobs-search-box-location-id-ember30"]').send_keys(Keys.BACKSPACE)
    driver.find_element_by_xpath('//input[@id="jobs-search-box-location-id-ember30"]').send_keys(f"{location_state}India")
    sleep(3)        #inducing a short pause to allow the webpage to aptly load
    driver.find_element_by_xpath('//input[@id="jobs-search-box-location-id-ember30"]').send_keys(Keys.ARROW_DOWN)
    driver.find_element_by_xpath('//input[@id="jobs-search-box-location-id-ember30"]').send_keys(Keys.ENTER)
    sleep(3)
    temp_list=[]
    try: 
        for x in driver.find_element_by_xpath('//ul[@class="jobs-search-results__list list-style-none"]').find_elements_by_xpath(".//li"):
            try:
                job_title=x.find_element_by_xpath(".//a[@class='disabled ember-view job-card-container__link job-card-list__title']").text   
                company_name=x.find_element_by_xpath(".//a[@class='job-card-container__link job-card-container__company-name ember-view']").text 
                location=x.find_element_by_xpath(".//ul[@class='job-card-container__metadata-wrapper']").text    
                company_url=x.find_element_by_xpath(".//a[@class='job-card-container__link job-card-container__company-name ember-view']").get_attribute('href')
        
                temp_list.append({'job_title':job_title, 'company_name':company_name, 'location':location, 'company_url':company_url})
            except: pass
    except: pass

    return {career_type:temp_list}
    
def scrape_part3(url, driver):
    driver.get(f'{url}about/')
    try: description=driver.find_element_by_xpath('//p[@class="break-words white-space-pre-wrap mb5 text-body-small t-black--light"]').text
    except: description=None
    
    try: emp_count1=get_num(driver.find_element_by_xpath('//*[text() = "Company size"]/following-sibling::dd').text)
    except: emp_count1=None
    
    try:
        emp_count2=driver.find_element_by_xpath('//*[text() = "Company size"]/following-sibling::dd/following-sibling::dd').text
        emp_count2=get_num(emp_count2[:emp_count2.find('Includes members with current employer listed as')].replace('\n', ''))
    except: emp_count2=None
    
    try: location=driver.find_elements_by_xpath('//div[@class="org-top-card-summary-info-list__info-item"]')[1].text
    except: location=None
    
    return {'Desription':description, 'Location':location, 'Total Employee Count':emp_count1, 'No. of employees on LinkedIn':emp_count2}


def part1_main():
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = Chrome(options=options)        #initialising Chrome object

    z={}
    driver.get('https://www.careerguide.com/career-options')  #navigating to careerguide's webpage
    for x in driver.find_elements_by_xpath("//div[@class='col-md-4'][@style='padding: 15px;']"):
        temp=[]
        #disregarding Institutes in India from the career options list as they're irrelevant to our task of job search on LinkedIn
        if(x.find_element_by_xpath(".//h2[@class='c-font-bold']").text != 'Institutes in India'):       
            for y in x.find_elements_by_xpath(".//li"):
                temp.append(y.text)
            z.update({x.find_element_by_xpath(".//h2[@class='c-font-bold']").text: temp})    
    with open(join(dirname(__file__), 'step1.json'), "w", encoding='utf-8') as outfile:
        outfile.write(dumps(z, indent = 4))     #writing the final data from step 1 of the task to a json file
        outfile.close()
    driver.quit()

def part2_main():
    try: data = load(open(join(dirname(__file__), 'step1.json'), "r", encoding='utf-8'))    #reading the data from step1.json to proceed with step 2
    except:
        part1_main()    #completing step 1 again if the required step1.json file doesn't exist
        data = load(open(join(dirname(__file__), 'step1.json'), "r", encoding='utf-8'))
        
    driver=linkedin_login()         #opening a new Chrome window with an a LinkedIn account logged in
    for location_state in ('Maharashtra', 'Delhi', 'Karnataka', 'Kerala', 'Telangana', 'Rajasthan'): #iterating through 6 states, can be changed according to user perferance
        count=0 #using a count variable to limit our search length for testing purposes
        temp={}
        for x in data.values():
            if(count==5): break
            for y in x:
                if(count==5): break
                temp.update(scrape_part2(y, driver, f'{location_state}, '))     #storing the job type info in a temporary dictionary
                count+=1
        append_json({location_state:temp}, 'step2.json')  #writing the final data from step 2 of the task to a json file
    driver.quit()          #closing all browser windows and ending the WebDriver Session


def part3_main():
    try: data = load(open(join(dirname(__file__), 'step2.json'), "r", encoding='utf-8'))    #reading the data from step2.json to proceed with step 3
    except: 
        part2_main()    #completing step 2 again if the required step2.json file doesn't exist
        data = load(open(join(dirname(__file__), 'step2.json'), "r", encoding='utf-8'))

    driver=linkedin_login()         #opening a new Chrome window with an a LinkedIn account logged in
    count=0 #using a count variable to limit our search length for testing purposes
    for x in data.values():
        if(count==5): break
        for y in x.values():
            if(count==5): break
            for z in y:
                if(count==5): break
                #writing the final data from step 3 of the task to a json file
                append_json({z['company_name']:scrape_part3(z['company_url'], driver)}, 'step3.json')
                count+=1
    driver.quit()           #closing all browser windows and ending the WebDriver Session

#calling any function out of part1_main(), part2_main(), part3_main() will call any preceding functions if the files related to the preceding functions don't already exist

#part1_main()
#part2_main()
part3_main()
