# 必要なライブラリをインポート
import feedparser
from strands import Agent, tool
from strands.models import BedrockModel
import boto3

# AssumeRoleを実施
boto3_session = boto3.Session(profile_name="admin-agent-book")

# Bedrock呼び出し用のAPIクライアントを作成
# Create a Bedrock model instance
bedrock_model = BedrockModel(
    model_id="apac.amazon.nova-pro-v1:0",
    temperature=0.3,
    top_p=0.8,
    boto_session=boto3_session,
)


# ツールを定義
@tool
def get_aws_updates(service_name: str) -> list:
    # AWS What's NewのRSSフィードをパース
    feed = feedparser.parse("https://aws.amazon.com/about-aws/whats-new/recent/feed/")
    result = []

    # フィードの各エントリをチェック
    for entry in feed.entries:
        # 件名にサービス名が含まれているかチェック
        if service_name.lower() in entry.title.lower():
            result.append(
                {
                    "published": entry.get("published", "N/A"),
                    "summary": entry.get("summary", ""),
                }
            )

            # 最大3件のエントリを取得
            if len(result) >= 3:
                break

    return result


# エージェントを作成
agent = Agent(model=bedrock_model)

# ユーザー入力を取得
service_name = input("アップデートを知りたいAWSサービス名を入力してください: ").strip()

# プロンプトを指定してエージェントを起動
prompt = f"AWSの{service_name}の最新アップデートを、日付つきで要約して。"
response = agent(prompt)
