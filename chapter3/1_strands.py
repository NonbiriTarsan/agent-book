# 必要なライブラリをインポート
from strands import Agent
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
# エージェントを作成して起動
agent = Agent(model=bedrock_model)
agent("Strandsってどういう意味？")
