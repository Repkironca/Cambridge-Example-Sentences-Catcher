import problemcontroller as pc
import crawler as cr
import random

class ProblemSet():
	total_problem = 0
	ac_problem = 0
	wa_problem = 0
	vocabularies = []
	choice_from_list = 1
	trans = {"A":0, "B":1, "C":2, "D":3} # dictionary : 把選項轉回 index

	def __init__ (self, choice_from_list):
		self.choice_from_list = choice_from_list
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

	def initiate(self):
		while (True):
			tmp = input(f"Type the total number of problems you want\n(the number should be no more than your word list size : {len(self.vocabularies)})\n")
			if (tmp.isnumeric()):
				if (int(tmp) <= len(self.vocabularies)):
					self.total_problem = int(tmp)
					break
				else:
					print(f"Error, the number should be no more than your word list size : {len(self.vocabularies)}, detected {int(tmp)}")
			else:
				print(f"Error, expect a number, detected \"{tmp}\"")

		random.shuffle(self.vocabularies)
		(now_index, success_index) = (0, 0)
		force_break = False
		while (success_index < self.total_problem):
			print(f"problem {success_index+1} of {self.total_problem}")
			problem_setter = pc.ProblemSetter("_start_", -1) # 初始值，一定會改變
			(choice_array, sentence_index, success) = ([], 0, False) # 初始值，一定會改變
			while(not success):
				if (now_index >= len(self.vocabularies)):
					force_break = True
					break
				problem_setter = pc.ProblemSetter(self.vocabularies[now_index], self.choice_from_list)
				(choice_array, sentence_index, success) = problem_setter.ProblemGiver()
				now_index += 1
				if (not success):
					print(f"Fail to generate sentense of {self.vocabularies[now_index-1]}, so it will be skipped")
			
			if (force_break): # 完全沒單字了，強制退出
				break

			(result, correct) = problem_setter.AnswerChecker(choice_array, sentence_index)
			if (result == -1): # 這邊如果使用者選擇換題目，要把 now_index-1，才能將單字回溯回去
				now_index -= 1
				continue
			if (correct):
				print("Accepted :)")
				self.ac_problem += 1
			else:
				print(f"Wrong Answer :( , the answer is {problem_setter.answer}")
				self.wa_problem += 1
			
			while (True):
				order = input("type \"$n\" to continue, or you can type \"$s\" to look for the meaning of choices that appeared in the problem\n")
				if (order == "$n"):
					break
				elif (order == "$s"):
					while (True):
						word = input("type the choice name to search for the particular word, or type \"$x\" to exit search page\n")
						if (word == "$x"):
							break
						if (word == "A" or word == "B" or word == "C" or word == "D"):
							output = cr.Crawler.WordSearch(choice_array[self.trans[word]])
							for i in range(1, len(output)+1):
								print(f"{i}. {output[i-1]}")
						else:
							print("Error : Command not defined, you should type either \"A\", \"B\", \"C\", or \"D\"")
				else:
					print("Error : Command not defined")

			success_index += 1

		print(f"There were {success_index} problems that worked well,")
		print(f"and you got {self.ac_problem} of them right, while you got {self.wa_problem} of them wrong")
		print(f"AC RATE : {round(self.ac_problem/success_index * 100, 2)} %")

### Test Area
if __name__ == "__main__":
	ps = ProblemSet(1)
	ps.initiate()