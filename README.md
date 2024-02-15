# Cambridge Sentences Catcher

## ZH-TW
### 起源
我在記憶單字時，很難直接看著就完全捕獲，常需要一定的習題來幫助我鞏固記憶
然而我常用的 *Quizlet* 測驗系統太破，純粹中翻英或英翻中難度過低當然想得出來
因此我打算仿造學科能力測驗第一大題的形式，趁著學測放榜前這段空窗期，做出一套專案
使其能透過爬蟲，去獲取 Cambridge Dictionarry 上的單字，再進行挖空，最後出成四選一選擇題

### 執行
我暫時還沒有製作頁面，需要手動執行 ui.py，其餘檔案最好別動否則會爛

### 指令表
中文版等我有空再更新上來，目前你可以直接輸出 $help 來尋找英文版指令表

### 參考資源
原本我其實沒很確定，這鬼想法是否能實作出來
在以 *Cambridge Crawler* 為關鍵字搜尋時，恰好找到了這篇
> https://github.com/mimiliaogo/cambridge-dictionary-crawler

雖然他是使用動態爬蟲，而且我的扣比較偏獨立撰寫（所以雜且菜），不過這篇仍然給了我一些想法與信心
至少證明 Cambridge 是能爬，且有人爬過的

## EN

### Origin
When memorizing vocabulary, I find it challenging to fully grasp the words at once and often need exercises to help reinforce my memory.
However, the Quizlet quiz system I frequently use is too simplistic, with translation exercises being too easy to figure out. 
Therefore, I decided to create a project during the downtime before the release of the university entrance exam results, mimicking the format of the first section of subject proficiency tests.
This project aims to crawl vocabulary from Cambridge Dictionary, create cloze exercises, and finally generate multiple-choice questions.

### Execution
I haven't created a mainpage yet, so you need to manually run ui.py. It's best not to modify other files, or they may malfunction.

### Command List
For now, you can directly output $help to find the English version of the command list.
Maybe I'll create a copy at here later

### References
Initially, I was unsure if this crazy idea could be implemented. However, when searching for Cambridge Crawler as a keyword, I coincidentally found this article:
> https://github.com/mimiliaogo/cambridge-dictionary-crawler

Although it uses dynamic crawling, and my approach is more inclined towards independent development (thus it's more rough),
this article still gave me some ideas and confidence. At the very least, it proves that Cambridge can be crawled and has been crawled by others.
