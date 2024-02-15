import crawler as cr
import conjugation as conjugation
import random
import time # 測試用

class ProblemSetter():
	answer = ""
	vocabularies = [] # 本機中的單字庫
	sentences = [] # 特定單字翻到，能用的句子
	accept_words = set() # 可能的動詞變化型
	word_type = set() # 這個詞有的所有詞性
	trash = set() # 使用者指定不應出現的句子編號
	punctuation_set = {",", ".", "\"", "?", "!", ";", "(", ")", "-", "..."} # 要辨識出的標點符號
	from_word_list = 1

	"""
	__init__ - 初始化，使此物件擁有單字表和指定單字的所有句子
	INPUT - word:string，準備要用來出題的單字
	OUTPUT - None
	"""
	def __init__(self, word, from_word_list):
		self.answer = word
		self.from_word_list = from_word_list
		try: # 嘗試尋找 word_list.txt
			with open("word_list.txt", "r", encoding = "utf-8") as word_list: # 從 word_list.txt 讀入字庫
				row_word = word_list.read()
				process = row_word.split("\n") # 這邊的預設間格符號是換行
				for tmp in process:
					if (tmp != ""):
						self.vocabularies.append(tmp)
		except FileNotFoundError: # 找不到檔案
			print("Warring: Couldn't find \"word_list.txt\" in the same folder with \"userinput.py\"")
			print("To fix the problem, please create a file named \"word_list.txt\" and NEVER edit its name or location")

		self.sentences = cr.Crawler.GetSentence(cr.Crawler, word) # 先讀入可用例句
		self.word_type = cr.Crawler.GetType(cr.Crawler, word) # 再讀入所有詞性
		for type_ in iter(self.word_type): # 針對所有詞性，嘗試讀入所有可能變化型
			if (type_ == "noun" or type_ == "verb" or type_ == "adjective"): # 這三個是可能有變化型的
				self.accept_words.update(list(conjugation.GetConjugation(word, type_)))
			elif (type_ == "phrase" or type_ == "phrasal verb" or type_ == "saying" or type_ == "idiom"): # 這些字要分割
				temp_list = word.split()
				for item in temp_list:
					item_type = cr.Crawler.GetType(cr.Crawler, item)
					self.accept_words.update(list(conjugation.GetConjugation(item, item_type)))
			else: # 剩下的根本不存在變化型
				self.accept_words.add(word)
	

	"""
	RandIntExclude - 在指定範圍內產生一個數字，但排除某些選項
	INPUT - up、down:int，取值上下限，左閉右閉 ; exclude:set，裡面裝有所有要排除的數字
	OUTPUT - int，隨機取數結果
	備註：這麼做其實速度頗不穩定，但我沒想到其他辦法，如果要保持隨機性，只能相信數學
	"""
	def RandIntExclude (self, down, up, exclude):
		ret = random.randint(down, up)
		return ret if (ret not in exclude) else self.RandIntExclude(down, up, exclude)


	"""
	PunctuationFixer - 修正標點符號所帶來的干擾
	INPUT - word:string，要修正的單字
	OUTPUT - string，修正後的單字
	"""
	def PunctuationFixer (self, word):
		char_list = [*word] # 把 char_list 用 chr 拆開
		for i in range(0, len(char_list)):
			if (char_list[i] in self.punctuation_set): # 如果偵測到標點符號
				char_list[i] = "" # 就把它去掉
		word = "".join(char_list) # 最後 merge 回去 return
		return word



	"""
	ProblemGiver - 產生並輸出該單字的一個題目
	INPUT - None
	OUTPUT - list，執行成功的話回傳選項，失敗回傳 empty-list
			 int，執行成功的話回傳句子編號，失敗回傳 -1
	         bool，執行成功或失敗，失敗代表沒有可用句子了。成功的話會順便回傳句子編號
	"""
	def ProblemGiver(self):
		"""time_0 = time.time()"""
		if (len(self.sentences) - len(self.trash) > 0): # 扣掉被使用者 ban 掉的句子後還有可用的
			output_index = self.RandIntExclude(0, len(self.sentences)-1, self.trash) # 從例句庫中選一個
			output_sen = self.sentences[output_index] # 選中的句子
			
			output_sen_list = output_sen.split() # 把句子以單字為單位分割
			for i in range(0, len(output_sen_list)):
				if (self.PunctuationFixer(output_sen_list[i]).lower() in self.accept_words):
				# (上行) 如果目前的單字，在去掉標點符號且轉成小寫後，存在於允許的變化型列表內
					output_sen_list[i] = "___" # 替換

			output_sen = " ".join(output_sen_list) # 再以空格為間格符號 merge 回去
			print(output_sen)
			"""time_1 = time.time()"""

			choice_array = [self.answer, "", "", ""] # 四個選項組成的 list
			trans = {0:"A", 1:"B", 2:"C", 3:"D"} # dictionarry：把 index 換成選項
			
			now_index = 1 # 目前正在處理，choice_array 的 index ( 0 預設是正解，最後會 shuffle() )
			exclude_list = {self.answer} # 避免微乎其微的機率，有兩個選項一模一樣
			while (now_index <= self.from_word_list):
				if (len(self.vocabularies) <= now_index): # 字庫中的字根本不夠，選不出來
					break
				tmp_word = self.answer # 這是等等生出來的字，先設成答案來觸發下個 while
				while (tmp_word in exclude_list): # 確保生出來的字目前不是選項
					index = random.randint(0, len(self.vocabularies)-1) # 隨便挑一個 index 當選項
					tmp_word = self.vocabularies[index]
				choice_array[now_index] = tmp_word # 把完成的選項覆蓋上去
				exclude_list.add(tmp_word) 
				now_index += 1 # 移動指標
			"""time_2 = time.time()"""

			while (now_index <= 2): # 假設現在還沒生成到 D 選項，否則這個 while 不會過
				tmp_word = self.answer
				"""before = time.time()"""
				while (tmp_word in exclude_list):
					tmp_word = cr.Crawler.GetChoice(chr(random.randint(97, 122))) # 隨機字首
				"""after = time.time()"""
				choice_array[now_index] = tmp_word
				exclude_list.add(tmp_word)
				now_index += 1
			"""time_3 = time.time()"""

			while (now_index <= 3): # 生完剩下的選項
				tmp_word = self.answer
				while (tmp_word in exclude_list):
					tmp_word = cr.Crawler.GetChoice(self.answer[0]) # 同字首選項
				choice_array[now_index] = tmp_word 
				exclude_list.add(tmp_word)
				now_index += 1
			"""time_4 = time.time()"""

			random.shuffle(choice_array) # 打亂選項
			print(f"(A) {choice_array[0]}\n(B) {choice_array[1]}\n(C) {choice_array[2]}\n(D) {choice_array[3]}")
			# (上行) 輸出選項
			"""print(f"TIME COST:{time_1 - time_0}, {time_2 - time_1}, {time_3 - time_2}, {time_4 - time_3}, {after - before}")"""
			return choice_array, output_index, True
		else: # 已經沒句子了
			return [], -1, False


	"""
	AnswerChecker : 獲取使用者輸入的答案，並判斷答案的正確與否
	INPUT - choice_array:list，裡面裝著四個選項
	        output_index:int，句子的編號
	OUTPUT - int: -1 代表此題無效換一個，0 ~ 3 代表使用者的答案
	         bool: 代表正確或錯誤，無效會回傳 False
	"""
	detected_answer = ["A", "B", "C", "D", "X"] # 允許的使用者輸入
	def AnswerChecker (self, choice_array, output_index):
		loop_input = True # 在獲取到合法輸入前，這個會保持 True
		user_input = "" # 使用者輸入
		while (loop_input):
			user_input = input()
			if (user_input in self.detected_answer): # 如果是合法輸入，跳出迴圈
				loop_input = False
			else:
				print("Error:answer undefined, please retry")
				print("Tips:Your answer should be either \"A\", \"B\", \"C\" or \"D\". You can also type \"X\" to change a problem")

		trans = {"A":0, "B":1, "C":2, "D":3} # dictionary : 把選項轉回 index
		if (user_input == "X"): # 此句不合法，換一句回來
			self.trash.add(output_index) # 把這句丟進黑名單
			return -1, False
			
		return trans[user_input], (choice_array[trans[user_input]] == self.answer)


### Test Area
if __name__ == "__main__":
	problem_setter = ProblemSetter("duck", 1)
	(choice_array, index, check) = problem_setter.ProblemGiver()
	print(problem_setter.AnswerChecker(choice_array, index))