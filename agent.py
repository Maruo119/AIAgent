import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# =========================
# 🛠 ツール実装
# =========================

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return "File written successfully."

# =========================
# 📦 ツール定義
# =========================

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "指定したファイルを読み込む",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "指定したファイルを書き換える",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    }
]

# =========================
# 📄 初期情報
# =========================

issue_text = read_file("issue.txt")

messages = [
    {
        "role": "system",
        "content": "あなたはGitHub Issueを解決するAIエージェントです。"
    },
    {
        "role": "user",
        "content": f"""
Issue内容:
{issue_text}

このプロジェクトには以下のファイルがあります:
- target_code.py

まず target_code.py を読み込み、その後修正してください。
"""
    }
]

# =========================
# 🔁 1ターン目（read_file）
# =========================

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    tool_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    print("🧠 1回目選択:", tool_name)

    if tool_name == "read_file":
        file_content = read_file(arguments["path"])

        # 🔥 ここが重要：結果をLLMに返す
        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": file_content
        })

        # =========================
        # 🔁 2ターン目（write_file）
        # =========================

        response2 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message2 = response2.choices[0].message

        if message2.tool_calls:
            tool_call2 = message2.tool_calls[0]
            tool_name2 = tool_call2.function.name
            arguments2 = json.loads(tool_call2.function.arguments)

            print("🧠 2回目選択:", tool_name2)

            if tool_name2 == "write_file":
                result = write_file(arguments2["path"], arguments2["content"])
                print("🛠 実行結果:", result)
            else:
                print("Unexpected tool:", tool_name2)

        else:
            print("LLMがwrite_fileを選びませんでした。")

else:
    print("LLMがツールを選びませんでした。")
