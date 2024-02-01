import requests as req
from bs4 import BeautifulSoup as bsp

class Crawler:

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
  @staticmethod
  def GetSentence(tar): # 把例句丟進來

    target_url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/" + tar
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    res = req.get(target_url, headers = headers)
    Crawler.ReturnStatus(res.status_code) # 顯示訪問狀態

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
  @staticmethod
  def PrintAll(tar):
    tmp_list = Crawler.GetSentence(tar)
    if (len(tmp_list) == 0):
      print("No sentence found!")
    else:
      for i in range (0, len(tmp_list)):
        print(tmp_list[i])
    
"""
===Test Area===

crab = Crawler()
crab.PrintAll("Appeal")
"""