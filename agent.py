import os
import json
import subprocess
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

def run_tests():
    try:
        result = subprocess.run(
            ["python", "-m", "pytest"],
            capture_output=True,
            text=True
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

# =========================
# 📦 ツール一覧（LLMに見せる）
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
# 📄 Issue読み込み
# =========================

issue_text = read_file("issue.txt")

messages = [
    {
        "role": "system",
        "content": "あなたはGitHub Issueを解決するAIエージェントです。"
    },
    {
        "role": "user",
        "content": f"Issue内容:\n{issue_text}\n\n最初に実行すべきツールを選んでください。"
    }
]

# =========================
# 🧠 LLM呼び出し（ツール選択）
# =========================

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

# =========================
# 🔍 ツール呼び出し判定
# =========================

if message.tool_calls:
    tool_call = message.tool_calls[0]
    tool_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    print("🧠 LLMが選択したツール:", tool_name)
    print("📦 引数:", arguments)

    # 実行
    if tool_name == "read_file":
        result = read_file(arguments["path"])
    elif tool_name == "write_file":
        result = write_file(arguments["path"], arguments["content"])
    else:
        result = "Unknown tool"

    print("🛠 実行結果:")
    print(result)

else:
    print("LLMはツールを選びませんでした。")
    print(message.content)