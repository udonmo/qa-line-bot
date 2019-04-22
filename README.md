# qa-line-bot
QAするLineボットです。

質問と回答はMicrosoft Azure QnA Makerを使用して作成します。
そのほか、Line Message APIを使用しています。

## 実行手順

.env.sampleを.envにリネームし、以下の鍵の設定をします。

```
LINE_CHANNEL_ACCESS_TOKEN=
LINE_CHANNEL_SECRET=
AZURE_QNAMAKER_URL=
AZURE_QNAMAKER_SUBSCRIPTION_KEY=
```

インターネトからURLへ配置して実行してください。
Message APIは以下に設定する必要があります。  
http://[your host]/callback

## 以下のサービスを使用しています。

Line Message API  
https://developers.line.biz/ja/services/messaging-api/

Microsoft Azure QnA Maker  
https://azure.microsoft.com/ja-jp/services/cognitive-services/qna-maker/

## 以下のSDKを使用しています。
Messaging API SDK  
https://github.com/line/line-bot-sdk-python
