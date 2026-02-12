import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# 1. Issue読み込み
with open("issue.txt", "r", encoding="utf-8") as f:
    issue_text = f.read()

# 2. 対象コード読み込み
with open("target_code.py", "r", encoding="utf-8") as f:
    code_text = f.read()

# 3. LLMに修正案を依頼
prompt = f"""
あなたは優秀なPythonエンジニアです。

【Issue内容】
{issue_text}

【現在のコード】
{code_text}

修正後のコードのみを出力してください。
"""

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": prompt}],
)

new_code = response.choices[0].message.content

print("===== 修正案 =====")
print(new_code)
