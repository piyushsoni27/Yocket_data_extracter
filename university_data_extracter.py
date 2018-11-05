"""
Created on Sat Nov  3 01:25:02 2018
@author: piyush
"""

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
        
        self.university_df = pd.DataFrame(columns = ["Name", "Rank", "link", "cs_link"])
        
        
    def extract(self):
        site = "https://yocket.in/universities/study-in-" + self.region
        
        print("Extracting Data, please wait...\n")  
        
        while(True):
            soup = self.load_page_soup(site)
    
            self.get_update_university_data_current_page(soup)
    
            next_site = soup.find("li", {"class" : "next"}).find('a', href=True)["href"]

            if(next_site == ""):
                break
            else:
                site = "https://yocket.in" + next_site
        
        print(self.university_df)
        return
        
    def load_page_soup(self, site):
        try:
            page = requests.get(site, verify=False)
        except:
            raise ConnectionError("Check your Internet Connection")
        
        soup = BeautifulSoup(page.content, "html.parser")
        return soup
        
    def get_update_university_data_current_page(self, soup):
        
        university_list = soup.find_all("div", {"class" : "col-sm-9 col-xs-12"})
        
        for university in university_list:
            self.university_df["cs_link"] = np.NaN
            university_link = "https://yocket.in" + university.find("a", href = True)["href"]
            university_name = university.find("a", href = True).get_text()
            university_rank = university.find("div", class_ = "col-sm-3").get_text()
            cs_link = self.get_cs_course_link(university_link)
            self.university_df = self.university_df.append({"Name" : university_name, 
                                                           "link" : university_link, 
                                                           "Rank" : re.sub(r"\W", "", university_rank),
                                                           "cs_link" : cs_link}, ignore_index = True)
       
    
        return
    
    def get_cs_course_link(self, site):
        soup = self.load_page_soup(site)
        cs_link = np.NaN

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
        
    def to_dataframe(self):
        return self.university_df
        
        
if __name__ == "__main__":
    data = UniversityData("germany")
    data.extract()
