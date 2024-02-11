class UserInput:
	
	vocabularies = [] # 單字表

	"""
	AutoModify - 自動把對單字表做的變更複寫到 word_list.txt 上
	INPUT - None
	OUTPUT - None
	"""
	def AutoModify (self):
		try: # 嘗試打開 "word_list.txt"
			with open ("word_list.txt", "w", encoding = "utf-8") as word_list: # 直接覆寫
				for tmp in self.vocabularies:
					word_list.write(f"{tmp}\n")
		except FileNotFoundError: # 找不到 "word_list.txt"
				print("Warring: Couldn't find \"word_list.txt\" in the same folder with \"userinput.py\"")
				print("To fix the problem, please create a file named \"word_list.txt\" and NEVER edit its name or location")


	"""
	__init__ - 初始化，會嘗試尋找一個叫 "word_list.txt" 的文件，裡面是目前所有的單字
	INPUT - None
	OUTPUT - None
	"""
	def __init__(self):
		try:
			with open ("word_list.txt", "r+", encoding = "utf-8") as word_list: # 嘗試打開 "word_list" 來讀取上次單字
				row_word = word_list.read()
				word = row_word.split("\n") # 間格符號預設是換行，基本上使用者不該動這份檔案
				print(f"Start, size = {len(word)}, and it is \"{word[0]}\"")
				for tmp in word:
					if (tmp != ""):
						self.vocabularies.append(tmp)

			self.AutoModify()
		except FileNotFoundError:
			print("Warring: Couldn't find \"word_list.txt\" in the same folder with \"userinput.py\"")
			print("To fix the problem, please create a file named \"word_list.txt\" and NEVER edit its name or location")

	"""
	CheckList - 印出單字表內所有單字且編號
	Input - None
	Output - None
	"""
	def CheckList (self):
		for i in range(0, len(self.vocabularies)):
			print(f"{i+1}. {self.vocabularies[i]}") # +1 是為了讓標號從 1 開始


	"""
	SimpleGet - 從 terminal 吃進一個單字，碰到換行結束
	INPUT - None
	OUTPUT - None
	"""
	def SimpleGet (self):
		word = input()
		if (not (word in self.vocabularies)): # 單字庫中沒有這個字
			self.vocabularies.append(word) # 在發現 "\n" 前，會不斷一直吃，接受片語
			print(f"\"{word}\" has been successfully added to your word list")
		self.AutoModify()


	"""
	MultipleGet - 從 terminal 一次性獲取多個單字，單字與單字間用間格符號分開，換行永遠被視為一個間格符號
	INPUT - mid:string，間格符號
	OUTPUT - None
	"""
	def MultipleGet (self, mid): # 從 terminal 獲取多個單字 [mid: string，間格符號]
		total = [] # 所有要推的單字
		fail = [] # 沒推進去的
		success = [] # 有推進去的

		while (True):
			word = input()

			if (word == "$end$"): # 只有看到 " $end$ " 時，才會停止繼續吃單字
				break
			word_list = word.split(mid) # 分割單字
			for tmp in word_list:
				if (not (tmp in self.vocabularies)): # 如果字庫中沒有這個字
					success.append(tmp) 
					self.vocabularies.append(tmp)
				else: # 字庫中已經有這個字了
					fail.append(tmp)

		print("\"", end = " ") # （到下一個空行前）輸出成功推進去的字
		for i in range(0, len(success)):
			print(f"{success[i]}", end = "、" if (i != len(success)-1) else " ")
		print("\" have been successfully added to your word list")

		if (len(fail) != 0): # （如果存在）輸出沒推進去的字
			print("While \"", end = " ")
			for i in range(0, len(fail)):
				print(f"{fail[i]}", end = "、" if (i != len(fail)-1) else " ")
			print(f"\"{" is" if (len(fail) == 1) else " are"} already in your wordlist") # 三元運算子為了英文語法
		
		self.AutoModify()


	"""
	GetFromFile - 從使用者指定的檔案中一次性讀入多個單字，單字與單字間用間格符號分開，預設換行不是間格符號
	INPUT - filename:string，檔案名稱 ; mid:string，間格符號
	OUTPUT - None
	"""
	def GetFromFile (self, filename, mid): # 從檔案中抓單字 [filename:string，檔案名稱 ; mid:string，間格符號]
		success = []
		fail = []
		try: # 因為可能找不到檔案，用 try-except 比較安全
			with open(filename, "r", encoding = "utf-8") as f: # 打開檔案
				word = f.read() # 直接讀到 EOF
				word_list = word.split(mid) # 分割整份文件
				for tmp in word_list:
					if (not (tmp in self.vocabularies)): # 如果字庫中沒有這個字
						success.append(tmp) 
						self.vocabularies.append(tmp)
					else: # 字庫中已經有這個字了
						fail.append(tmp)

				print("\"", end = " ") # (到下一個空行前) 輸出成功推進去的字
				for i in range(0, len(success)):
					print(f"{success[i]}", end = "、" if (i != len(success)-1) else " ")
				print("\" have been successfully added to your word list")

				if (len(fail) != 0): # (如果存在)輸出沒推進去的字
					print("While \"", end = " ")
					for i in range(0, len(fail)):
						print(f"{fail[i]}", end = "、" if (i != len(fail)-1) else " ")
					print(f"\"{" is" if (len(fail) == 1) else " are"} already in your wordlist") # 三元運算子為了英文語法
				
				self.AutoModify()

		except FileNotFoundError: # 防止找不到檔案直接跳錯
			print(f"file \" {filename} \" not found")
			print("You may incorrectly type the file name,\nor your file isn't in the same folder with \" userinput.py \"")


	"""
	DeleteByName - 直接指定特定名稱的單字（支援多單字）刪除，會過濾掉超範圍索引、非數字等雜訊
	INPUT - target_list:string-based-list，要刪除的單字
	OUTPUT - None
	"""
	def DeleteByName (self, target_list):
		success = [] # 成功刪掉的
		fail = [] # 沒有刪掉的
		for tmp in target_list: 
			if (tmp in self.vocabularies): # 如果單字庫中有要刪除的目標
				self.vocabularies.remove(tmp)
				success.append(tmp)
			else: # 單字庫中根本沒有這個字
				fail.append(tmp)

		print("\"", end = " ") # （到下一個空行前）輸出成功刪除的單字
		for i in range(0, len(success)):
			print(f"{success[i]}", end = "、" if (i != len(success)-1) else " ") 
		print(f" \" {" has" if (len(success) == 1) else " have"} been successfully removed from your word list")

		if (len(fail) > 0): # 輸出沒有成功刪除的單字
			print("While \"", end = " ")
		for i in range(0, len(fail)):
			print(f"{fail[i]}", end = "、" if (i != len(fail)-1) else " ")
		print(f" \" {"isn't" if (len(success) == 1) else "are't"} in your word list")

		self.AutoModify()


	"""
	DeleteByIndex - 指定欲刪除的項目編號 (1-based)
	Input - None
	Output - None
	"""
	def DeleteByIndex (self):
		target_string = input() # 獲取輸入
		target_list = target_string.split(" ")
		index_list = [] # 拿來存放轉換過的 index
		success = [] # 成功刪除的單字
		fail = [] # 超範圍的索引或雜訊

		for tmp in target_list:
			try: # 避免吃到非數字
				index = int(tmp)
				if (index >= 1 and index <= len(self.vocabularies)):
					index -= 1 # 要把 1-based 轉成 0-based
					if (not (index in index_list)): # 避免有人打很多次一模一樣的索引
						index_list.append(index)
				else:
					fail.append(index)
			except ValueError: # 如果吃到什麼奇怪的東西，直接跳過這邊
				fail.append(tmp)
				continue

		index_list.sort() # 絕對要由小到大，否則會溢位

		removed = 0 # 因為刪除東西後會改變後面所有元素的 index，要用這個來校正
		for index in index_list:
			if (index >= 0 and index < len(self.vocabularies)):
				index -= removed
				removed += 1
				success.append(self.vocabularies[index])
				del(self.vocabularies[index])

		print("\"", end = " ") # 輸出成功刪除的單字
		for i in range(0, len(success)):
			print(f"{success[i]}", end = "、" if (i != len(success)-1) else " ")
		print(f"\" {"has" if (len(success) == 1) else "have"} been successfully removed from your word list")

		if (len(fail) > 0): # 輸出刪除失敗的索引
			print("index = \"", end = " ")
			for i in range(0, len(fail)):
				print(f"{fail[i]}", end = "、" if (i != len(fail)-1) else " ")
			print(f"\" {"hasn't" if (len(success) == 1) else "haven't"} been removed because these indexes are out of range")

		self.AutoModify()


	"""
	SortByDictionary - 按照字典序自動重新編號單字庫
	INPUT - None
	OUTPUT - None
	"""
	def SortByDictionary (self):
		self.vocabularies.sort()
		self.AutoModify()


	"""
	DesignatedSort - 使用者直接指定一個單字，把它插入某處
	INPUT - index:int，要移動的單字位置 ; target:int，要插入到哪個地方
	OUTPUT - None
	"""
	def DesignatedSort (self, index, target):
		if (index >= 1 and index <= len(self.vocabularies) and target >= 1 and target <= len(self.vocabularies)): # 確保 index 合法
			index -= 1 # 把 1-based 校正回 0-based
			target -= 1
			tmp = self.vocabularies[index] # 暫放目標單字
			del(self.vocabularies[index]) # 刪除目標單字
			self.vocabularies.insert(target, tmp) # 插入目標單字

			print(f"{tmp} has been successfully moved to {target+1}")

		else:
			print(f"Exception : Your index is out of range\nIt should be between 1 and {len(self.vecabularies)}")


### Test Area
if __name__ == "__main__":
	test = UserInput()
	test.GetFromFile("test.txt", "\n")
	test.CheckList()
	test.DeleteByIndex()
	test.CheckList()
	test.GetFromFile("test.txt", "\n")
	test.DesignatedSort(5, 1)
	test.CheckList()