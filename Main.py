from selenium import webdriver
import csv
import re
from datetime import datetime

def getCredentials():
    """Request login credentials using a GUI."""
    import tkinter
    root = tkinter.Tk()
    root.eval('tk::PlaceWindow . center')
    root.title('Login')
    uv = tkinter.StringVar(root, value='')
    pv = tkinter.StringVar(root, value='')
    userEntry = tkinter.Entry(root, bd=3, width=35, textvariable=uv)
    passEntry = tkinter.Entry(root, bd=3, width=35, show="*", textvariable=pv)
    btnClose = tkinter.Button(root, text="OK", command=root.destroy)
    userEntry.pack(padx=10, pady=5)
    passEntry.pack(padx=10, pady=5)
    btnClose.pack(padx=10, pady=5, side=tkinter.TOP, anchor=tkinter.NE)
    root.mainloop()
    return [uv.get(), pv.get()]

def IsMatch(RetrievedURL):
    x = re.search("((?<=www\.linkedin\.com\/in\/)[a-z]+-[a-z]+(-[a-z0-9]+)?)", RetrievedURL)

    if x:
        return True
    else:
        return False

def PrepareSearchURL(Keywords, CountryCode):
    output = 'https://www.linkedin.com/search/results/people/?geoUrn=%5B%'+CountryCode+'%22%5D&keywords='+Keywords+'&origin=FACETED_SEARCH'
    return output

def Main():
    loginPage = "https://www.linkedin.com/login/pl?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
    username, password = getCredentials()
    searchURL = PrepareSearchURL('.net agile sql','22105072130')
    driver  = webdriver.Chrome(executable_path=r"config\chromedriver.exe")
    pagesToExtract = 6
    outputCsvFilePath = 'output\\' + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".csv"

    f = open(outputCsvFilePath, 'w', newline='',encoding='utf-8') 
    fieldnames = ['URL', 'Name']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    driver.get(loginPage)
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_class_name("login__form_action_container ").click()

    for i in range(1,pagesToExtract):
        if i > 1:
            URLToRetriveData = searchURL + '&page=' + str(i)
        else:
            URLToRetriveData = searchURL

        driver.get(URLToRetriveData)
        profiles = driver.find_elements_by_class_name("app-aware-link")
        for profile in profiles:
            url_to_profile = profile.get_attribute("href")
            if '?' in url_to_profile and url_to_profile.strip != '':
                url_to_profile = url_to_profile.split('?')[0]
                profile_name = profile.accessible_name
                if not 'Wyświetl profil użytkownika' in profile_name and url_to_profile != 'https://www.linkedin.com/search/results/people/' and IsMatch(url_to_profile):
                    writer.writerow({'URL': url_to_profile, 'Name': profile_name})

    f.close()


Main()
