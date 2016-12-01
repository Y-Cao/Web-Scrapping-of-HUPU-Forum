import pandas as pd
import urllib.request
import re
from bs4 import BeautifulSoup

class HUPU_Model():
    def __init__(self):
        self.page=1
        self.frequency={}
        self.content={}
        
    def analyse_page(self):
        url='http://bbs.hupu.com/bxj-'+str(self.page)
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
        response=urllib.request.urlopen(req)
        htmlcontent=response.read()
        self.bsObj=BeautifulSoup(htmlcontent,'lxml')
        
        tags=self.bsObj.find_all('a',id=True,href=True,text=re.compile('.*?('+key_word+')'))
        items=[tag.get_text() for tag in tags]
        return len(items),items
    
    def load_page(self):
        while self.page<=end_page:
            try:
                self.frequency[self.page],self.content[self.page]=self.analyse_page()
                self.page+=1
            except Exception as e:
                print ('Errors occur at page',self.page)
                print (repr(e))
                break
            
    def get_num_threads(self):
        num_threads=len(self.bsObj.find_all('a',id=True,href=True,text=True))
        return num_threads
                
    def show_analysis(self):
        t1=pd.Series(self.frequency)
        t2=pd.Series(self.content)
        result=pd.concat([t1,t2],axis=1)
        result.columns=['frequency','contents']
        result['percentage']=result['frequency']/self.get_num_threads()
        result=result[['frequency','percentage','contents']]
        print (result)
        
    def start(self):
        print ('Loading....')
        self.load_page()
        self.show_analysis()

        
#---------Program starts-----
print ("""
-------------------------
Program name: HUPU BBS scrapping
Version:0.1
Author: Y-Cao
Language:Python 3.5
Operation: Enter the end page and key word
Function:calculate the frequency and percentage of a keyword occuring in the subject line of threads in different pages
---------------------------""")
end_page=int(input('what is the end page of scrapping: '))
key_word=(input('keyword: '))
Model=HUPU_Model()
Model.start()
