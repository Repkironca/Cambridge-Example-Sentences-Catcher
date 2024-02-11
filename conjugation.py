import requests as req
from bs4 import BeautifulSoup as bsp

"""
GetConjugation - 回傳所有單字 "理論上" 可能的變化型
INPUT - tar:string，原始單字 ; word_type:string，詞性
OUTPUT - set，裡面裝所有可能變化型，包含原始單字
"""
def GetConjugation(tar, word_type): 

  if (word_type == "noun"): # 名詞，偵測 -s、-es、-ies、-ves 字尾、部分不規則變化
    target_url = "https://zh.wiktionary.org/zh-hant/Appendix:%E8%8B%B1%E8%AF%AD%E4%B8%8D%E8%A7%84%E5%88%99%E5%A4%8D%E6%95%B0"
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    res = req.get(target_url, headers = headers) # 往維基辭典的英語名詞不規則變化爬

    soup = bsp(res.text, "html.parser")
    ret = [] # 所有的單字與變化型，為 "A -> B" 的字串
    for node in soup.find_all("div", class_ = "mw-content-ltr mw-parser-output"):
      for point in node.find_all("li"): # 篩出我要的字串 (這網頁結構有點亂)
       ret.append(point.get_text())

    trans = {} # Dictionary，{原型 : 變化型}，key 是字串，content 是 string-based-tuple
    for tmp in ret: # 把 "A -> B" 的字串轉成 Dictionary
      item = tmp.split(" → ")
      item[1] = item[1].replace(",", "/") # 有的單字會有多種變化型，以逗號分隔
      item[1] = item[1].replace(" *", "") # 有的單字後面會有意義不明的米字號，要刪掉
      edit_item = item[1].split("/") # 有的單字會有多種變化型，以斜線分隔 (對真的很亂)
      trans[item[0]] = tuple(edit_item)

    if (tar in trans): # 如果查的單字有在不規則變化表內
      temp = {tar}
      for item in trans[tar]:
        temp.add(item)
      return temp

    add_es_1 = ["s", "z", "x"] # 複數型後綴是 -es 的單字母字尾
    add_es_2 = ["ss", "ch", "sh"] # 複數型後綴是 -es 的雙字母字尾
    whether_add_es = False

    for tmp in add_es_1: # 驗證 -es 單字母字尾
      if (tar[-1] == tmp):
        whether_add_es = True
    for tmp in add_es_2: # 驗證 -es 雙字母字尾
      if ((str(tar[-2])+str(tar[-1])) == tmp):
        whether_add_es = True

    if (whether_add_es): # 加上 -es 後綴
      return {tar, tar+"es"}

    if (tar[-1] == "y"): # 複數型後綴是去 -y 加 -ies 的狀況
      temp = ""
      for i in range(0, len(tar)-1):
        temp += tar[i]
      return {tar, temp+"ies"}

    if (tar[-1] == "f"): # 複數型後綴是去 -f 加 -ves 的狀況
      temp = ""
      for i in range(0, len(tar)-1):
        temp += tar[i]
      return {tar, temp+"ves"}

    else: # 一般變化，加個 s 就可以傳回去了
      return {tar, tar+"s"}
    
  if (word_type == "verb"): # 動詞，偵測過去式、未來式、進行式、完成式等變化
    target_url = "https://cooljugator.com/en/" + tar # 我終於找到一個可爬的靜態網頁ㄌ
    headers ={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    res = req.get(target_url, headers = headers)

    soup = bsp(res.text, "html.parser")
    exist = {tar}
    for node in soup.find_all("div", class_ = "meta-form"): # 這邊會列出所有時態變化型，但前面可能有贅字
      temp_str = node.get_text() # 為了去除 be 動詞或助詞之類的，分割字串，取最後一個就好
      temp_list = temp_str.split()
      exist.add(temp_list[-1]) # 只把最後一個丟到 set 中

    return exist

  if (word_type == "adjective"): # 形容詞，偵測比較級、最高級變化，但無法判別是否重複字尾，故統一納入資料庫
    ret = {tar}
    if (tar[-1] == "e"):
      ret.update([tar+"r", tar+"st"]) # 字尾是 e，特殊變化
    else:
      ret.update([tar+"er", tar+"est"]) # 不重複字尾
      ret.update([tar+tar[-1]+"er", tar+tar[-1]+"est"]) # 重複字尾
    return ret

  return {tar} # 代表這是未知或無法產生變化型的詞性

  
### Test Area
if "__name__" == "__main__":
  print(GetConjugation("form", "adjective"))