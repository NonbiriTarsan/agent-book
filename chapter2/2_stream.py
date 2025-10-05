# 必要なライブラリをインポート
import boto3

# AssumeRoleを実施
session = boto3.Session(profile_name="admin-agent-book")

# Bedrock呼び出し用のAPIクライアントを作成
client = session.client("bedrock-runtime")

# Converse Stream APIを実行
response = client.converse_stream(
    modelId="apac.amazon.nova-pro-v1:0",
    messages=[{"role": "user", "content": [{"text": "いろは歌を詠んで"}]}],
)

# ストリーミングレスポンスを取得して逐次表示
for event in response.get("stream", []):
    if "contentBlockDelta" in event:
        chunk = event["contentBlockDelta"]["delta"]["text"]
        print(chunk, end="")
