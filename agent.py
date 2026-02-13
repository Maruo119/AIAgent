import os
import json
import subprocess
import requests
from dotenv import load_dotenv
from openai import OpenAI
from git import Repo
import datetime

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

def get_github_issue(owner, repo, issue_number):
    """GitHubのissueを取得"""
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {}
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    issue_data = response.json()
    return issue_data["title"], issue_data["body"]

def create_branch(repo_path, issue_number):
    repo = Repo(repo_path)
    branch_name = f"ai-fix-issue-{issue_number}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    new_branch = repo.create_head(branch_name)
    new_branch.checkout()
    
    return branch_name

def commit_changes(repo_path, message):
    repo = Repo(repo_path)
    repo.git.add(A=True)
    repo.index.commit(message)

def push_branch(repo_path, branch_name):
    repo = Repo(repo_path)
    origin = repo.remote(name='origin')
    origin.push(branch_name)

def create_pull_request(owner, repo, branch_name, issue_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    
    headers = {
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "title": f"AI Fix for Issue #{issue_number}",
        "head": branch_name,
        "base": "main",
        "body": f"Automated fix for issue #{issue_number}"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 201:
        raise Exception(response.text)

    return response.json()["html_url"]

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

# GitHubのリポジトリとissue情報を環境変数から取得
github_owner = os.getenv("GITHUB_OWNER", "")
github_repo = os.getenv("GITHUB_REPO", "")
github_issue_number = os.getenv("GITHUB_ISSUE_NUMBER", "")

if github_owner and github_repo and github_issue_number:
    try:
        issue_title, issue_body = get_github_issue(github_owner, github_repo, github_issue_number)
        issue_text = f"{issue_title}\n\n{issue_body}"
        print(f"✅ GitHubからissueを取得しました: {github_owner}/{github_repo}#{github_issue_number}")
        print(f"\n📌 Issue Title: {issue_title}")
        print(f"\n📝 Issue Text:\n{issue_text}\n")
    except Exception as e:
        print(f"❌ GitHubからissueを取得できませんでした: {e}")
        issue_text = read_file("issue.txt")
        print(f"\n📝 Issue Text:\n{issue_text}\n")
else:
    print("⚠️ GitHub情報が不足しているため、issue.txtを使用します")
    issue_text = read_file("issue.txt")
    print(f"\n📝 Issue Text:\n{issue_text}\n")

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


repo_path = "."
issue_number = 10
owner = "Maruo119"
repo_name = "AIAgent"

branch_name = create_branch(repo_path, issue_number)

commit_changes(repo_path, f"AI fix for issue #{issue_number}")

push_branch(repo_path, branch_name)

pr_url = create_pull_request(owner, repo_name, branch_name, issue_number)

print("🎉 PR created:", pr_url)