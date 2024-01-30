import requests as req
from bs4 import BeautifulSoup as bsp

class Crawler:

  def ReturnStatus(num): # 顯示訪問狀態，不過我沒有用 try-catch 去抓 exception

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
  

  def Filter(li):

    tmp = []
    deleted = 0
    for i in range(0, len(li)):
      i -= deleted
      split_item = li[i].split()
      if (len(split_item) <= 3):
        # print(f"delete li[{i}], which is {li[i]} ans its size = {len(split_item)}")
        del(li[i])
        deleted += 1

    return li


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


  def PrintAll(tar):

    tmp_list = Crawler.GetSentence(tar)
    if (len(tmp_list) == 0):
      print("No sentence found!")
    else:
      for i in range (0, len(tmp_list)):
        print(tmp_list[i])

Crawler.PrintAll("appeal")