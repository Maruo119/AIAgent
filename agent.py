import os
import json
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# =========================
# 🛠 ツール
# =========================

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return "File written successfully."

def run_tests():
    result = subprocess.run(
        ["python", "-m", "pytest"],
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr

# =========================
# 📦 ツール定義
# =========================

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

# =========================
# 初期メッセージ
# =========================

issue_text = read_file("issue.txt")

messages = [
    {"role": "system", "content": "あなたはIssueを解決するAIエージェントです。"},
    {"role": "user", "content": f"""
Issue:
{issue_text}

対象ファイルは target_code.py です。
テストが通るまで修正してください。
"""}
]

# =========================
# 🔁 最大3ステップ
# =========================

for step in range(3):

    print(f"\n===== STEP {step+1} =====")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if not message.tool_calls:
        print("LLMがツールを選びませんでした")
        break

    tool_call = message.tool_calls[0]
    tool_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments or "{}")

    print("🧠 選択:", tool_name)

    # ツール実行
    if tool_name == "read_file":
        result = read_file(arguments["path"])
    elif tool_name == "write_file":
        result = write_file(arguments["path"], arguments["content"])
    elif tool_name == "run_tests":
        result = run_tests()
    else:
        result = "Unknown tool"

    print("🛠 結果:", result[:500])

    # LLMに結果を渡す
    messages.append(message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })

    # テスト成功なら終了
    if tool_name == "run_tests" and "failed" not in result.lower():
        print("🎉 テスト成功！")
        break
