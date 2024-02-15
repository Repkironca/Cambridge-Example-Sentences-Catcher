import probleminitiator as pi
import crawler as cr
import userinput as usip
from urllib import request

user_input = ""
crawler = cr.Crawler()
input_center = usip.UserInput()
from_word_list = 1
version = "1.0.0" # Sementic Versioning
author = "Repkironca"

"""
SetFromWordList - 設定有多少選項要出自字庫
INPUT - value:int，介於 0至3 ，有幾個誘答選項要出自字庫
OUTPUT - None
"""
def SetFromWordList (value):
	if (value >= 0 and value <= 3): # 確認進來的值是合理的
		from_word_list = value
		print(f"the number of words which will be generated from your word list has been successfully set to {value}")
	else:
		print("Error, the value should be between 0 and 3")


"""
InternetCheck - 檢查目前是否有可用網路
INPUT - None
OUTPUT - bool，有網路會回傳 True，反之回傳 False
PS:參考自 https://stackoverflow.com/questions/3764291/how-can-i-see-if-theres-an-available-and-active-network-connection-in-python
"""
def InternetCheck ():
    try:
        request.urlopen("https://www.google.com/", timeout = 1)
        return True
    except request.URLError as err:
    	print("Error, no internet detected")
    return False

print(f"Version:{version}\nAuthor:{author}")
print("Note that all of the choices in problem will never experience any tense conjugation or decoration due to technological barriers")

while (True):
	command = input("\nPlease type your command or type \"$help\" to show the command list\n")
	if (command == "$e"): # Exit
		break

	elif (command == "$sg"): # Simple Get
		input_center.SimpleGet()

	elif (command == "$cl"): # Check List
		input_center.CheckList()

	elif (command == "$mg"): # Multiple Get
		print("Enter your separation signal")
		print("If you want, you may set it to an tap of enter key by typing \"\\n\", or set it to an tap of tab by typing \"\\t\"")
		tmp = input()
		mid = ""
		if (tmp == "\\n"):
			mid = "\n"
		elif (tmp == "\\t"):
			mid = "\t"
		else:
			mid = tmp
		input_center.MultpleGet(mid)

	elif (command == "$fg"): # Get From File
		filename = input("Enter your FULL file name (extension included, e.g. \"file.txt\")\n")
		print("Enter your separation signal")
		print("If you want, you may set it to an tap of enter key by typing \"\\n\", or set it to an tap of tab by typing \"\\t\"")
		tmp = input()
		mid = ""
		if (tmp == "\\n"):
			mid = "\n"
		elif (tmp == "\\t"):
			mid = "\t"
		else:
			mid = tmp
		input_center.GetFromFile(filename, mid)

	elif (command == "$dn"): # Delete By Name
		target_list = []
		while (True):
			print("Enter the words you want to delete, you can only enter one item in a line")
			print("After you finish, type \"$end\" to continue")
			tmp = input()
			if (tmp == "$end"):
				break
			else:
				target_list.append(tmp)
		input_center.DeleteByName(target_list)

	elif (command == "$di"):
		input_center.DeleteByIndex()

	elif (command == "$sd"): # Sort By Dictionary
		input_center.SortByDictionary()

	elif (command == "$move"): # Designated Sort
		success = False
		AB = []
		while (not success):
			success = True
			tmp = input("Please enter two index A and B (separated by a single space), to move the word at A to B\n")
			tmp_list = tmp.split()
			for item in tmp_list:
				if (item.isnumeric()):
					AB.append(int(item))
				else:
					success = False
					AB = []
			if (not success):
				print(f"Error, you can only enter number, detected {tmp}")
		input_center.DesignatedSort(AB[0], AB[1])

	elif (command == "$ss"): # Search Sentences
		word = input("Please enter the word you want to search for example sentences\n")
		if (InternetCheck()):
			sentence_list = crawler.GetSentence(word)
			if (len(sentence_list) > 0):
				for i in range(1, len(sentence_list)+1):
					print(f"{i}. {sentence_list[i-1]}")
			else:
				print("No Sentences Found")

	elif (command == "$sm"): # Search Meanings
		word = input("Please enter the word you want to search for meanings\n")
		if (InternetCheck()):
			meaning_list = crawler.WordSearch(word)
			if (len(meaning_list) > 0):
				for i in range(1, len(meaning_list)+1):
					print(f"{i}. {meaning_list[i-1]}")
			else:
				print("No Result Found")

	elif (command == "$setf"): # Set "From Word List"
		success = False
		while (not success):
			num = input("Enter a number to set how many vocabularies in choices should be generated from your word list\n")
			success = num.isnumeric()
			if (not success):
				print(f"Error, expect a number between 0 and 3, detected {num}")
			else:
				SetFromWordList(int(num))

	elif (command == "$exam"): # initiate
		if (InternetCheck()):
			problem_set = pi.ProblemSet(from_word_list)
			problem_set.initiate()

	elif (command == "$nat"): # cat :)
		output = " ╱|__\n(˚ˎ 。7 \n|、~\\\nじしˍ,)ノ"
		print(output)

	elif (command == "$help"):
		with open("help.txt", "r", encoding = "utf-8") as file:
			output = file.read()
			print(output)
			
	else:
		print("Command not defined. You may type \"$help\" ($ is included but \" aren't) to show the command list")

