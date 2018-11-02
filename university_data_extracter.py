#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    
    def __init__(self, region=None):
        
        if(region == None):
            region = default_region
        print("Extracting Data, please wait...\n")
        
        site = "https://yocket.in/universities/study-in-" + region
        
        self.university_df = pd.DataFrame(columns = ["Name", "Rank", "link"])
        
        while(True):
            page = self.load_page(site)
                
            soup = BeautifulSoup(page.content, "html.parser")
    
            self.get_university_data_current_page(soup)
    
            next_site = soup.find("li", {"class" : "next"}).find('a', href=True)["href"]

            if(next_site == ""):
                break
            else:
                site = "https://yocket.in" + next_site
        
        print(self.university_df)
        
    def load_page(self, site):
        try:
            page = requests.get(site)
        except:
            raise ConnectionError("Check your Internet Connection")
    
        return page
        
    def get_university_data_current_page(self, soup):
        
        university_list = soup.find_all("div", {"class" : "col-sm-9 col-xs-12"})
        
        for university in university_list:
            university_link = "https://yocket.in" + university.find("a", href = True)["href"]
            university_name = university.find("a", href = True).get_text()
            university_rank = university.find("div", class_ = "col-sm-3").get_text()
            self.university_df = self.university_df.append({"Name" : university_name, 
                                                            "link" : university_link, 
                                                            "Rank" : re.sub(r"\W", "", university_rank)}, ignore_index = True)
                
        
if __name__ == "__main__":
    data = UniversityData("germany")