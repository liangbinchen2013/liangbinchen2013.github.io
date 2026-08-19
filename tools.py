#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools.py - 博客日常管理与维护工具

用法:
  python tools.py <命令> [参数]

文章管理:
  article list                   列出所有文章
  article create <文章.md>       创建文章(交互式,调用 get_docs.py -D)
  article edit <slug>            打开编辑器修改文章
  article delete <slug>          删除文章
  article rename <旧slug> <新slug>  重命名文章(改 URL)

分类管理:
  category add <slug>            新增分类(交互式,调用 get_docs.py -C)
  category list                  列出所有分类

标签管理:
  tag list                       统计所有标签及出现次数

页面管理:
  page show <about|academic|projects>  显示页面文件内容
  page edit <about|academic|projects>  打开编辑器修改页面

开发与构建:
  dev                             启动本地开发服务器
  check                           类型检查(astro check)
  build                           构建站点(GitHub Pages 模式)
  clean                           清理 Python 编译产物与 pnpm 产物
  preview                         本地预览构建结果

部署:
  deploy                          构建并推送产物到 main 分支(GitHub Pages)

Git 管理:
  git status                      查看工作区状态
  git commit <信息>               提交全部改动
  git push                        推送到远端 source 分支
  git sync                        提交并推送
  git log                         查看提交历史

其他:
  doc                             查看维护文档路径
  help                            显示本帮助
"""

import datetime
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(ROOT, "src", "content", "blogs")
REMOTE = "https://github.com/liangbinchen2013/liangbinchen2013.github.io.git"
DOC_PATH = os.path.join(ROOT, "MAINTENANCE.md")

PAGES = {
    "about": os.path.join(ROOT, "src", "pages", "about", "index.astro"),
    "academic": os.path.join(ROOT, "src", "pages", "academic", "index.astro"),
    "projects": os.path.join(ROOT, "src", "pages", "projects", "index.astro"),
}


def run(cmd, **kwargs):
    print(f">>> {cmd}", flush=True)
    return subprocess.run(cmd, shell=True, cwd=ROOT, **kwargs)


def conda_env():
    os.environ["PATH"] = os.path.expanduser("~/miniconda3/bin") + os.pathsep + os.environ.get("PATH", "")


def can_connect(url, timeout=6, proxies=None):
    try:
        handler = urllib.request.ProxyHandler(proxies or {})
        opener = urllib.request.build_opener(handler)
        req = urllib.request.Request(url, method="HEAD")
        with opener.open(req, timeout=timeout) as resp:
            return True
    except Exception:
        return False


def github_env():
    proxy = "http://127.0.0.1:38457"
    if can_connect("https://github.com"):
        print("[网络] GitHub 直连可用,无需代理。")
        return
    if can_connect("https://github.com", proxies={"http": proxy, "https": proxy}):
        print(f"[网络] 直连不可用,使用代理 {proxy}。")
        os.environ.update({
            "HTTPS_PROXY": proxy,
            "HTTP_PROXY": proxy,
            "ALL_PROXY": proxy,
        })
        return
    print("[网络] 直连与代理均不可用,将直接重试(可能超时失败)。")


def die(msg):
    print(f"错误: {msg}")
    sys.exit(1)


def is_valid_slug(slug):
    return bool(re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug))


def normalize_slug(slug):
    slug = slug.strip().lower().replace(" ", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    return slug.strip("-")


def list_articles():
    articles = []
    if os.path.isdir(BLOG_DIR):
        for name in sorted(os.listdir(BLOG_DIR)):
            index = os.path.join(BLOG_DIR, name, "index.md")
            if os.path.isfile(index):
                articles.append((name, index))
    return articles


def read_frontmatter(index_path):
    text = open(index_path, encoding="utf-8").read()
    fm = {}
    m = re.search(r"^---\n(.*?)\n---", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip().strip("\"'")
    return fm


def cmd_article_list():
    articles = list_articles()
    if not articles:
        print("当前没有任何文章。")
        return
    print(f"共 {len(articles)} 篇文章:\n")
    for slug, index in articles:
        fm = read_frontmatter(index)
        title = fm.get("title", slug)
        draft = " [草稿]" if fm.get("draft") == "true" else ""
        print(f"  {slug:32s} {title}{draft}  ({fm.get('publishDate', '?')})")


def cmd_article_create(md):
    run(f"python3 get_docs.py -D \"{md}\"")


def cmd_article_edit(slug):
    slug = normalize_slug(slug)
    index = os.path.join(BLOG_DIR, slug, "index.md")
    if not os.path.isfile(index):
        die(f"找不到文章: {slug}")
    editor = os.environ.get("EDITOR", "nano")
    run(f"{editor} \"{index}\"")
    print(f"已编辑: {index}")


def cmd_article_delete(slug):
    slug = normalize_slug(slug)
    index = os.path.join(BLOG_DIR, slug, "index.md")
    if not os.path.isfile(index):
        die(f"找不到文章: {slug}")
    fm = read_frontmatter(index)
    print(f"即将删除文章: {slug} ({fm.get('title', '?')})")
    ans = input("确认删除? [y/N]: ").strip().lower()
    if ans != "y":
        print("已取消。")
        return
    import shutil
    shutil.rmtree(os.path.join(BLOG_DIR, slug))
    print(f"已删除: {os.path.join(BLOG_DIR, slug)}")


def cmd_article_rename(old, new):
    old, new = normalize_slug(old), normalize_slug(new)
    old_dir, new_dir = os.path.join(BLOG_DIR, old), os.path.join(BLOG_DIR, new)
    if not os.path.isdir(old_dir):
        die(f"找不到文章: {old}")
    if os.path.exists(new_dir):
        die(f"目标已存在: {new}")
    os.rename(old_dir, new_dir)
    print(f"已重命名: /article/{old} -> /article/{new}")


def cmd_category_list():
    sys.path.insert(0, ROOT)
    from get_docs import existing_categories
    cats = existing_categories()
    print(f"共 {len(cats)} 个分类:")
    for c in cats:
        print(f"  {c}")


def cmd_category_add(slug):
    run(f"python3 get_docs.py -C \"{slug}\"")


def cmd_tag_list():
    from collections import Counter
    counter = Counter()
    for slug, index in list_articles():
        fm = read_frontmatter(index)
        m = re.search(r"^tags:\s*\[(.*?)\]", open(index, encoding="utf-8").read(), re.M)
        if m:
            for t in m.group(1).split(","):
                t = t.strip().strip("\"'")
                if t:
                    counter[t] += 1
    if not counter:
        print("当前没有任何标签。")
        return
    print(f"共 {len(counter)} 个标签:")
    for tag, count in counter.most_common():
        print(f"  {tag:24s} {count} 篇")


def cmd_page_show(name):
    path = PAGES.get(name)
    if not path:
        die(f"未知页面: {name}(可选: {', '.join(PAGES)})")
    print(open(path, encoding="utf-8").read())


def cmd_page_edit(name):
    path = PAGES.get(name)
    if not path:
        die(f"未知页面: {name}(可选: {', '.join(PAGES)})")
    editor = os.environ.get("EDITOR", "nano")
    run(f"{editor} \"{path}\"")


def cmd_dev():
    conda_env()
    run("pnpm dev", check=False)


def cmd_check():
    conda_env()
    run("pnpm check", check=False)


def cmd_build():
    conda_env()
    os.environ["DEPLOYMENT_PLATFORM"] = "github"
    return run("pnpm run build:github", check=False).returncode == 0


def cmd_clean():
    run(f"python3 {os.path.join(ROOT, 'clean.py')} -y")


def cmd_preview():
    conda_env()
    run("pnpm preview", check=False)


def cmd_deploy():
    if not cmd_build():
        die("构建失败,部署中止。")
    github_env()
    import shutil
    dist = os.path.join(ROOT, "dist")
    if not os.path.isdir(dist):
        die("dist 目录不存在。")
    cmds = [
        f'printf "blog.lbcoj.top" > CNAME && touch .nojekyll',
        "git init -q -b main",
        "git config http.sslVerify false",
        "git add -A",
        f'git -c user.name="liangbinchen2013" -c user.email="liangbinchen2013@outlook.com" commit -q -m "deploy: {datetime.date.today().isoformat()} 站点更新"',
        f"git remote add origin {REMOTE}",
        "git push -f origin main",
    ]
    for c in cmds:
        print(f">>> {c}")
        r = subprocess.run(c, shell=True, cwd=dist)
        if r.returncode != 0 and "remote add" not in c:
            die(f"部署失败:{c}")
        if r.returncode != 0 and "remote add" in c:
            print("(remote 已存在,跳过)")
    print("部署完成:https://blog.lbcoj.top")


def cmd_git_status():
    run("git status --short")


def cmd_git_commit(msg):
    run('git add -A && git commit -m "' + msg + '"')


def cmd_git_push():
    github_env()
    run("git push origin source")


def cmd_git_sync(msg):
    cmd_git_commit(msg)
    cmd_git_push()


def cmd_git_log():
    run("git log --oneline -20")


def cmd_doc():
    print(DOC_PATH)


def usage():
    print(__doc__)
    sys.exit(0)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        usage()

    cmd, *rest = args

    if cmd == "article":
        sub = rest[0] if rest else "list"
        if sub == "list":
            cmd_article_list()
        elif sub == "create":
            if len(rest) < 2:
                die("用法: tools.py article create <文章.md>")
            cmd_article_create(rest[1])
        elif sub == "edit":
            if len(rest) < 2:
                die("用法: tools.py article edit <slug>")
            cmd_article_edit(rest[1])
        elif sub == "delete":
            if len(rest) < 2:
                die("用法: tools.py article delete <slug>")
            cmd_article_delete(rest[1])
        elif sub == "rename":
            if len(rest) < 3:
                die("用法: tools.py article rename <旧slug> <新slug>")
            cmd_article_rename(rest[1], rest[2])
        else:
            die(f"未知子命令: article {sub}")
    elif cmd == "category":
        sub = rest[0] if rest else "list"
        if sub == "list":
            cmd_category_list()
        elif sub == "add":
            if len(rest) < 2:
                die("用法: tools.py category add <slug>")
            cmd_category_add(rest[1])
        else:
            die(f"未知子命令: category {sub}")
    elif cmd == "tag":
        if rest and rest[0] == "list":
            cmd_tag_list()
        else:
            die("用法: tools.py tag list")
    elif cmd == "page":
        sub = rest[0] if rest else "show"
        if len(rest) < 2:
            die("用法: tools.py page <show|edit> <about|academic|projects>")
        if sub == "show":
            cmd_page_show(rest[1])
        elif sub == "edit":
            cmd_page_edit(rest[1])
        else:
            die(f"未知子命令: page {sub}")
    elif cmd == "dev":
        cmd_dev()
    elif cmd == "check":
        cmd_check()
    elif cmd == "build":
        cmd_build()
    elif cmd == "clean":
        cmd_clean()
    elif cmd == "preview":
        cmd_preview()
    elif cmd == "deploy":
        cmd_deploy()
    elif cmd == "git":
        sub = rest[0] if rest else "status"
        if sub == "status":
            cmd_git_status()
        elif sub == "commit":
            if len(rest) < 2:
                die("用法: tools.py git commit <提交信息>")
            cmd_git_commit(" ".join(rest[1:]))
        elif sub == "push":
            cmd_git_push()
        elif sub == "sync":
            if len(rest) < 2:
                die("用法: tools.py git sync <提交信息>")
            cmd_git_sync(" ".join(rest[1:]))
        elif sub == "log":
            cmd_git_log()
        else:
            die(f"未知子命令: git {sub}")
    elif cmd == "doc":
        cmd_doc()
    else:
        usage()


if __name__ == "__main__":
    main()