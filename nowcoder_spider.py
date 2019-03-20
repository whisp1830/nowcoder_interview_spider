import requests,re
from bs4 import BeautifulSoup

def get_interview_exp(url):
	"""
		获取每个面经内的标题和正文
	"""
	res = []
	exp = requests.get(url)
	soup = BeautifulSoup(exp.text,"lxml")
	res.append(soup.title.text)
	for item in soup.find(name='div',attrs={"class":"post-topic-des nc-post-content"}):
		reg = re.compile('<[^>]*>')
		item = str(item).replace("<br/>","\n")
		item = reg.sub('',item)
		res.append(item)
	with open(soup.title.text+".txt","w") as f:
		f.writelines(res)
	

def get_urls(url,interview_urls):
	"""
		获取牛客网面经笔经页面所有面经URL
	"""
	menu = requests.get(url)
	soup = BeautifulSoup(menu.text,"lxml")
	for i in soup.find_all(name="a",attrs={"target":"_blank"}):
		s = i['href']
		if "pos" in s and "page" in s:
			interview_urls.add("https://www.nowcoder.com/"+s)


def get_menus(pages,interview_urls):
	"""
		在牛客网面经笔经页面翻页
	"""
	base_menu = "https://www.nowcoder.com/discuss?type=2&order=0&pageSize=30&query=&page="
	for i in range(pages):
		get_urls(base_menu+str(i+1),interview_urls)


if __name__ == "__main__":

	interview_urls = set()

	get_menus(3,interview_urls)
	
	for i in interview_urls:
		get_interview_exp(i)

