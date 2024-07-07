---
title: SITCON Hackathon 2024 專案 README 模板
tags: SITCON Hackathon 2024, SITCON,  Hackathon , 2024 ,
GA: 
---
# {42號混凝土拌義大利麵助理}

SITCON Hackathon 2024 成果發表範例

> **競賽議題 & 子議題、專案簡介、使用資源為必填**

## 競賽議題 & 子議題
- 團隊名稱：{ noob.py }
- 成員姓名：{吳秉彥}, {段宇謙}, {莊庭愷}, {陳柏安}
- 競賽議題：{公創新世代：學生力量與科技共創公民參與}
    - 子議題：{智慧城市 X 臺北市政府資訊局}


### 專案簡介
- 用途/功能：
    - 藉由與智慧城市溝通，可以和資料庫對話並取得更多資訊。
- 目標客群&使用情境：
    - 學生：作為社會科學探究與實作的參考資料
    - 一般民眾：有意參與社會公共事務，希望研究特定議題但卻被多餘物件混淆視聽，透過AI能過濾相關數據並文字化輸出
    - 供政府官員、城市規畫師、交通管理員以及其他公共部門工作人員快速分析大數據

- 操作方式：
    - 環境設置
        1. 可以看到 .env 檔案新增了兩個 API，
            * OPENAI_API_KEY<br>
            此為必需新增的 API，否則無法與智慧城市對話。
            * LANGCHAIN_API_KEY<br>
            此為開發用 API，可以透過 LangSmith 看清楚整體 Chain 流程。可加可不加
        2. 必須把修改後的 .env 檔案複製進 Taipei-City-Dashboard-AI 資料夾裡
    - 使用者操作方式<br>
        只需點擊智慧城市按鈕，之後並可與之對話。

### 使用資源
- 企業資源：
    - { OpenAI }<br>
    我們所選用的模型。
- 公開資源：
    - {LangChain}<br>
    有了這個 package，可以更輕鬆的客製化我們的模型。

### 你還想分享的事情
- 開發過程
  - 我們在前端設計了一些看似無用實則無用的功能:3
  - 後端非常的炸裂，全部擠在一個 app.py 裡面
- 遇到的困難
  - 在進行這次的專案之前我們對開發幾乎一無所知，唯一清楚的只有我們想做的事
  - 原本以為只要 figma 用一用就好了，結果是要真的做出東西來。然後發現自己前端後端資料庫和網站原理都不懂，笑死。
- 非常好commit訊息，簡單明瞭<br>
![image](https://hackmd.io/_uploads/SkfcTPvvA.png)

### 成果展示
- 可附上其他專案介紹的投影片/文件等等
> 一些你可能會有的對話，可以看到就算不在資料庫內，在他能力以內依然能回答。
> ![image](https://github.com/ABB00717/Taipei-City-Dashboard/assets/99705287/979111e6-1bcc-4951-aae5-b7a142bca67c)
> 可以根據上下文回答問題。
> ![image](https://github.com/ABB00717/Taipei-City-Dashboard/assets/99705287/e78f010c-fbf8-45a2-bdda-63671e547657)
> 但是他依然很有可能會犯錯 (PS. 台科大在大安區)。
> ![image](https://github.com/ABB00717/Taipei-City-Dashboard/assets/99705287/53ab898f-12d8-483b-97bc-d40bcc5e05b6)



