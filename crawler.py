import requests as req
from bs4 import BeautifulSoup as bsp
import random
import time # 測試用

class Crawler:

  """
  WordTrans - 把片語單字中間的空格改成 - ，降低找不到的機率
  INPUT - tar:string，目標單字
  OUTPUT - string，轉換後的單字
  """
  @staticmethod
  def WordTrans(tar):
    word_list = tar.split(" ") # 分割字串
    ret = "-".join(word_list) # 把字串接回去
    return ret


  """
  ReturnStatus - 顯示訪問狀態
  INPUT - num:int，status code
  OUTPUT - None
  """
  @staticmethod
  def ReturnStatus(num):

    if (num <= 199):
      print(f"Informational responses, status code = {num}\n")
    elif (num <= 299):
      print(f"Successful responses, status code = {num}\n")
    elif (num <= 399):
      print(f"Redirects,, status code = {num}\n")
    elif (num <= 499):
      print(f"Client errors, status code = {num}\n")
    elif (num <= 599):
      print(f"Server errors, status code = {num}\n")
  

  """
  Filter - 過濾器，把字元數 <= 3 的句子刪掉，這些通常不是例句
  INPUT - li:list，爬出來的所有例句
  OUTPUT - li:list，過濾後的句子
  """
  @staticmethod
  def Filter(li):

    tmp = []
    deleted = 0 # 計算刪除了多少東西，等等要校正索引值
    for i in range(0, len(li)):
      i -= deleted # 索引值校正（因為東西刪除後 index 會少 1）
      split_item = li[i].split()
      if (len(split_item) <= 3):
        # print(f"delete li[{i}], which is {li[i]} ans its size = {len(split_item)}")
        del(li[i])
        deleted += 1

    return li


  """
  GetSentence - 爬蟲主軸，去 Cambridge 抓下所有例句
  INPUT - tar:string，要爬的單字
  OUTPUT - ret:string-based-list，過濾後的所有句子，注意可能是 empty list
  """
  def GetSentence(self, tar):

    tar = self.WordTrans(tar) # 先轉換字串
    target_url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/" + tar
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    res = req.get(target_url, headers = headers)
    # Crawler.ReturnStatus(res.status_code) # 顯示訪問狀態

    soup = bsp(res.text, "html.parser")
    ret = [] # 這邊等等會拿來放傳會來的例句
    for node in soup.find_all("span", class_ = "eg deg"): # Cambridge 把例句放在一個叫 eg deg 的 <span>
      ret.append(node.get_text())

    ret = Crawler.Filter(ret)
    return ret # 他有可能丟回 empty list，後續記得判斷


  """
  PrintAll - 測試用，把未過濾過的所有句子丟出來
  INPUT - tar:string，要爬的單字
  OUTPUT - None
  """

  def PrintAll(self, tar):
    tar = self.WordTrans(tar)
    tmp_list = Crawler.GetSentence(self, tar)
    if (len(tmp_list) == 0):
      print("No sentence found!")
    else:
      for i in range (0, len(tmp_list)):
        print(tmp_list[i])
  

  """
  GetType - 獲取特定單字的詞性
  INPUT - tar:string，目標單字
  OUTPUT - string-based-set，可能包含
           [noun, verb, pronoun, conjunction, adjective, interjection, adverb, preposition, phrase, saying, informal, phrasal verb, idiom]
  """
  def GetType(self, tar):

    tar = self.WordTrans(tar) 
    target_url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/" + tar
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    res = req.get(target_url, headers = headers)
    # Crawler.ReturnStatus(res.status_code) # 顯示訪問狀態

    soup = bsp(res.text, "html.parser")
    ret = {"unknown"} # 一個詞可能有很多種詞性，全部用 set 裝 (主要是 Cambridge 偶爾會出現重複詞性)
    for node in soup.find_all("span", class_ = "pos dpos"): # pos dpos 裡面裝的是詞性
      ret.add(node.get_text())

    if (len(ret) > 1): # 只要找得到任何詞性，就把 unknown 刪掉
      ret.remove("unknown")
    return ret

  """
  GetChoice - 生成相似字詞，作為誘答選項
  INPUT - word:string，正解單字
  OUTPUT - string，和正解單字同字首的選項
  """
  @staticmethod
  def GetChoice (word):
    tmp_word = word.split() # 把正解單字分割，為了確認其長度
    word_length = len(tmp_word)

    target_url = "https://dictionary.cambridge.org/browse/english/" + word[0] # 直接搜出所有同字首清單
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    """time_0 = time.time()"""
    res = req.get(target_url, headers = headers)
    soup = bsp(res.text, "html.parser")
    """time_1 = time.time()"""

    herfs = []
    for tmp in soup.find_all("a", class_ = "hlh32 hdb dil tcbd"): # 清單會分類放在超連結
      herfs.append(tmp.get("href")) # 抓出這些連結
    random.shuffle(herfs) # 隨便排列它，確保隨機性
    """time_2 = time.time()"""

    for i in range(0, len(herfs)): # 挑一個連結出來
      """print(f"TIME COST : {time_1 - time_0}, {time_2 - time_1}")"""
      target_url_2 = herfs[i] # 爬過去
      res_2 = req.get(target_url_2, headers = headers)
      soup_2 = bsp(res_2.text, "html.parser")

      for node in soup_2.find_all("span", class_ = "hw haf"): # 再從這個連結中抓出所有同字首的字
        ret_list = node.get_text().split() # 確認抓出來字的長度
        if (word_length == 1 and len(ret_list) == 1): # 如果正解單字長度是 1，那回傳單字長度也是 1
          ret = node.get_text().replace("\n", "")
          return node.get_text()
        if (word_length > 1 and len(ret_list) > 1): # 否則至少要回傳單字長度 > 1 的，看起來才沒那麼瞎
          if (ret_list[-1] == "idiom" or ret_list[-1] == "phrase"): # 不知為何，有時會抓到奇怪後綴，在此修正
            ret_list[-1] = ""
          return " ".join(ret_list) # 把修正後的重新 join 回字串，回傳

  """
  WordSearch : 回傳給定單字的所有意思
  INPUT : word:string，要查詢的單字
  OUTPUT : string-based-list，要輸出的所有內容
  """
  @staticmethod
  def WordSearch (word):
    target_url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/" + word
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    res = req.get(target_url, headers = headers)
    soup = bsp(res.text, "html.parser")

    ret = []
    for node in soup.find_all("span", class_ = "trans dtrans dtrans-se break-cj"):
      ret.append(node.get_text())
    return ret
  
### Test Area
if __name__ == "__main__":
  crab = Crawler()
  # crab.PrintAll("go")
  crab.WordSearch("duck")

