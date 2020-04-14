import json
import requests
import datetime
from bs4 import BeautifulSoup
from tabulate import tabulate

extract_contents = lambda row : [x.text.replace('\n','') for x in row]

class corona:

	def __init__(self):
		self.url = 'https://www.mohfw.gov.in/'
		self.file = 'data.json'
		self.data=[]
		self.current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
		self.connect()

	def save(self,json_data):
		with open(self.file, 'w') as f:
			json.dump(json_data, f)

	def load(self):
		res = {}
		with open(self.file, 'r') as f:
			res = json.load(f)
		return res

	def connect(self):
		self.response = requests.get(self.url).content
		self.soup = BeautifulSoup(self.response, 'html.parser')
		print("Done")

	def format(self,data):
		return data[-1] + "\n\n" + "In {} total cases are {} out of which {} are cured/migrated while the number of deaths are {}".format(data[1],data[2],data[3],data[4])
		
	def last_checked(self,state):
		record = self.load()
		last = []
		for row in record : 
			if row[1] == state:
				row.append(record[-1])
				last.append(row)
				break
		return self.format(last[0])
		
	def process(self,state):
		query = []
		query.append(self.last_checked(state))
		# header = extract_contents(self.soup.tr.find_all('th'))
		# header.append("Time of record")
		header=["ID","State","Total cases","Cured/Discharged","Deaths","Time of record"]
		all_rows = self.soup.find_all('tr')
		for rows in all_rows:
			r = extract_contents(rows.find_all('td'))
			if len(r)==5:
				r[1]=r[1].lower()
				self.data.append(r)
				if r[1] == state:
					r.append(self.current_time)
					query.append(self.format(r))
		
		# table = tabulate(query, headers=header, tablefmt='psql')
		# print(table)
		self.data.append(self.current_time)
		self.save(self.data)
		return query


# obj = corona()
# p = obj.process('maharashtra')
# print(p)






