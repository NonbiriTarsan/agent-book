# 必要なライブラリをインポート
import boto3

# AssumeRoleを実施
session = boto3.Session(profile_name="admin-agent-book")

# Bedrock呼び出し用のAPIクライアントを作成
client = session.client("bedrock-runtime")

# Converse APIを実行
response = client.converse(
    modelId="apac.amazon.nova-pro-v1:0",  # モデルID
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "text": "こんにちは"  # 入力メッセージ
                }
            ],
        }
    ],
)

# 実行結果のテキストだけを画面に表示
print(response["output"]["message"]["content"][0]["text"])
