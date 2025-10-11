# 必要なライブラリをインポート
import feedparser
import asyncio  # 追加
import streamlit as st  # 追加
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
        title = entry.get("title", "")
        if isinstance(title, str) and service_name.lower() in title.lower():
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

# ページタイトルと入力欄を表示
st.title("AWSアップデート確認くん")
service_name = st.text_input("アップデートを知りたいAWSサービス名を入力してください：")


# 非同期ストリーミング処理
async def process_stream(service_name, container):
    text_holder = container.empty()
    response = ""
    prompt = f"AWSの{service_name.strip()}の最新アップデートを、日付つきで要約して。"

    # エージェントからのストリーミングレスポンスを処理
    async for chunk in agent.stream_async(prompt):
        if isinstance(chunk, dict):
            event = chunk.get("event", {})

            # ツール実行を検出して表示
            if "contentBlockStart" in event:
                tool_use = (
                    event["contentBlockStart"].get("start", {}).get("toolUse", {})
                )
                tool_name = tool_use.get("name")

                # バッファをクリア
                if response:
                    text_holder.markdown(response)
                    response = ""

                # ツール実行のメッセージを表示
                container.info(f"🔧 {tool_name} ツールを実行中…")
                text_holder = container.empty()

            # テキストを抽出してリアルタイム表示
            if text := chunk.get("data"):
                response += text
                text_holder.markdown(response)


# ボタンを押したら生成開始
if st.button("確認"):
    if service_name:
        with st.spinner("アップデートを確認中..."):
            container = st.container()
            asyncio.run(process_stream(service_name, container))
