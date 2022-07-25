from django.shortcuts import render
import urllib.request
import xlsxwriter
from stackapi import StackAPI 
from bs4 import BeautifulSoup
import json
from django.core.cache import cache
from django.core.paginator import Paginator

def home(request):
    try:
        Tag = request.POST.get('tag')
        if Tag == None:
            Tag = 'stackexchange'
            print("**********************POST GET SUCCESS*********************************")
        else: 
            print("didnt get tag input!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            pass
    except Exception:
        Tag = 'stackexchange'
        
    print(f"Here is the name:  {Tag}")
    head = Tag
    data = scrap(Tag)
    p = Paginator(data, 5)
    page = request.GET.get('page')
    pdata = p.get_page(page)

    return render(request, 'webpage.html', {'pdata':pdata,'head':head,'data':data})

def search(request):
    Tag = request.POST.get('tag')
    data = scrap(Tag)
    head = Tag
    return render(request, 'webpage.html', {'head':head, 'data':data})

def scrap(Tag):
    def get_answer(url):
        content = urllib.request.urlopen(url)
        soup = BeautifulSoup(content,features='lxml')
        try:
            answer = soup.find_all('div',attrs={'class':'accepted-answer'})
            accepted_content = answer[0].contents[1].find('div',attrs = {'class':'post-text'})
            return accepted_content.text
        except Exception :
            return 'not answered'


    tag = Tag
    res = []
    
    if cache.get(tag):
        res = cache.get(tag)
    else:
        site = StackAPI('stackoverflow')
        questions = site.fetch('questions',tagged = tag)
        for i,item in enumerate(questions['items']):
            temp=[]
            ques = (item['title'])
            answ = (get_answer(item['link']).strip())
            temp.append(ques)
            temp.append(answ)
            res.append(temp)
            print(f"{ques} : {answ}")
            print()
            print(i)
            if i > 9:
                break
        cache.set(tag,res)
    return res

