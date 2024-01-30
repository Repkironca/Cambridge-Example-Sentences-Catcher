# Cambridge

## Before Launch
### Jan.30
- 成功增加 header，以 abort 為範例爬至該頁面
### Jan.31
- 如果使用者輸入根本不存在的字（e.g. abortt），會直接被跳轉，無法 try-catch
- 用 find("span", class = "eg deg") 把例句單獨抓出來了
- 動詞變化：v-ed 跟 v-ing 還好說，請問你要怎麼抓不規則變化 🐈
- 他現在能分辨是否找到句子，沒找到句子會告訴你
- 我想部分引入 Google 的 Python Coding-Style（真的是部分 🐊）
