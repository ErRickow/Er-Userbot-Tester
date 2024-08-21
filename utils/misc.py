from sys import version_info
from .db import db
import git

__all__ = [
    "plugins_help",
    "tolong_anu",
    "requirements_list",
    "python_version",
    "prefix",
    "emo",
    "gitrepo",
    "userbot_version",
]


plugins_help = {}
tolong_anu = {}
requirements_list = []

app = {}

python_version = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"

emo = db.get("core.main", "emo", " ")
prefix = db.get("core.main", "prefix", ".")

try:
    gitrepo = git.Repo(".")
except git.exc.InvalidGitRepositoryError:
    repo = git.Repo.init()
    origin = repo.create_remote(
        "origin", "https://github.com/ErRickow/Er-Userbot-Tester"
    )
    origin.fetch()
    repo.create_head("main", origin.refs.main)
    repo.heads.main.set_tracking_branch(origin.refs.main)
    repo.heads.main.checkout(True)
    gitrepo = git.Repo(".")

if len(gitrepo.tags) > 0:
    commits_since_tag = list(gitrepo.iter_commits(f"{gitrepo.tags[-1].name}..HEAD"))
else:
    commits_since_tag = []
userbot_version = f"0.1.{len(commits_since_tag)}"
