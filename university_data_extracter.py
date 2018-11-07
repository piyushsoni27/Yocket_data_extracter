"""
Created on Sat Nov  3 01:25:02 2018
@author: piyush
"""
import math
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import warnings
import datetime

default_region = "usa"

class UniversityData():
    
    def __init__(self, Region=None):
        warnings.filterwarnings("ignore")
        
        self.region = Region
        if(self.region == None):
            self.region = default_region
        
        self.university_df = pd.DataFrame(columns = ["Name", "Rank", "link", "cs_link", "admit_link"])

        return        
        
    def extract(self):
        site = "https://yocket.in/universities/study-in-" + self.region
        
        print("Extracting Data, please wait...\n")  
        
        while(True):
            soup = self.load_page_soup(site)
            next_site = ""
            self.update_university_data_current_page(soup)
    
            if(soup.find("li", {"class" : "next"})):
                next_site = soup.find("li", {"class" : "next"}).find('a', href=True)["href"]

            print(next_site)
            if(next_site == ""):
                break
            else:
                site = "https://yocket.in" + next_site
        
        return
        
    def load_page_soup(self, site):
        page = requests.get(site, verify=False)
        """
        try:
            page = requests.get(site, verify=False)
        except:
            raise ConnectionError("Check your Internet Connection")
        """
        soup = BeautifulSoup(page.content, "html.parser")
        return soup
        
    def update_university_data_current_page(self, soup):
        
        university_list = soup.find_all("div", {"class" : "col-sm-9 col-xs-12"})
        
        for university in university_list:
            university_link = "https://yocket.in" + university.find("a", href = True)["href"]
            university_name = university.find("a", href = True).get_text()
            university_rank = university.find("div", class_ = "col-sm-3").get_text()
            cs_link = self.get_cs_course_link(university_link)
            admit_link = self.get_admit_link(cs_link)
            self.university_df = self.university_df.append({"Name" : university_name, 
                                                           "link" : university_link, 
                                                           "Rank" : re.sub(r"\W", "", university_rank),
                                                           "cs_link" : cs_link,
                                                           "admit_link" : admit_link}, ignore_index = True)
       
    
        return
    
    def get_cs_course_link(self, site):
        soup = self.load_page_soup(site)
        cs_link = ""

        courses = soup.find("ul", class_ = "university-course-list")
        
        if(courses):
            courses_list = courses.find_all("li")
        
            for course in courses_list:
                if(course.find("a", href=True).get_text() == "Computer Science"):
                    cs_link = "https://yocket.in" + course.find("a", href=True)["href"]
                    """
                    if(course.find("small")):
                        st = course.find("span").get_text(strip=True)
                        print(st)
                        print(re.findall('(?<=Fall deadline:)(.*?)(?=|Send)', st, flags=re.S))
                    """
        return cs_link
    
    def get_admit_link(self, site):
        admit_link = ""
        
        if(site == ""):
            return admit_link

        soup = self.load_page_soup(site)
        
        all_admits = soup.find_all("div", {"class" : "col-sm-4 col-xs-4"})
        
        if(all_admits and all_admits[1]):
            for admit in all_admits:
                if(admit.find("a", href=True) and admit.find("a", href=True).get_text() == "Yocketers admitted"):
                    admit_link = "https://yocket.in" + admit.find("a", href=True)["href"]
        
        return admit_link
        
    def to_dataframe(self):
        return self.university_df
        
        
if __name__ == "__main__":
    data = UniversityData()
    data.extract()
    print(data.to_dataframe())