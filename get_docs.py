#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get_docs.py - 博客文章与分类管理工具

用法:
  python get_docs.py -D <文章.md>   创建博客文章(交互式填写标题/描述/标签/分类/URL)
  python get_docs.py -C <分类>      新增文章分类(交互式填写中英文名称)
  python get_docs.py -h             显示本帮助
"""

import os
import re
import sys
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(ROOT, "src", "content", "blogs")
SITE_URL = "https://blog.lbcoj.top"

HEADER_PATH = os.path.join(ROOT, "src", "components", "basic", "Header.astro")
ARTICLE_INDEX_ZH = os.path.join(ROOT, "src", "pages", "article", "index.astro")
ARTICLE_INDEX_EN = os.path.join(ROOT, "src", "pages", "en", "article", "index.astro")
ARTICLE_CAT_ZH = os.path.join(ROOT, "src", "pages", "article", "[category]", "[...page].astro")
ARTICLE_CAT_EN = os.path.join(ROOT, "src", "pages", "en", "article", "[category]", "[...page].astro")

CATEGORY_FILES = [HEADER_PATH, ARTICLE_INDEX_ZH, ARTICLE_INDEX_EN, ARTICLE_CAT_ZH, ARTICLE_CAT_EN]


def usage():
    print(__doc__)
    sys.exit(0)


def die(msg):
    print(f"错误: {msg}")
    sys.exit(1)


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def is_valid_slug(slug):
    return bool(re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug))


def normalize_slug(slug):
    slug = slug.strip().lower().replace(" ", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    return slug.strip("-")


def existing_categories():
    cats = set()
    text = read_file(HEADER_PATH)
    for m in re.finditer(r"'([a-z0-9-]+)':\s*\{", text):
        cats.add(m.group(1))
    return sorted(cats)


def add_category_to_header(slug, zh, en):
    path = HEADER_PATH
    text = read_file(path)

    if re.search(rf"'({slug})':\s*{{", text):
        die(f"分类 '{slug}' 已存在。")

    # categoryMap 中最后一条 { zh: ... } 记录后插入
    entries = list(re.finditer(r"^  '([a-z0-9-]+)':\s*\{ zh: '([^']*)', en: '([^']*)' \},?$", text, re.M))
    if not entries:
        die(f"未能在 {path} 中找到分类映射,请手动添加。")
    last = entries[-1]
    insert_pos = last.end()
    new_line = f"  '{slug}': {{ zh: '{zh}', en: '{en}' }},\n"
    text = text[:insert_pos] + "\n" + new_line + text[insert_pos:]

    # categoryOrder 数组末尾追加
    m = re.search(r"(const categoryOrder = \[[^\]]*)\]", text)
    if m:
        close_pos = m.end() - 1
        items = m.group(1).rstrip()
        if items.endswith("'"):
            text = text[:close_pos] + f", '{slug}'" + text[close_pos:]
        else:
            text = text[:close_pos] + f"'{slug}'" + text[close_pos:]

    write_file(path, text)
    print(f"[OK] 已更新 {os.path.relpath(path, ROOT)}")


def add_category_to_pages(slug, name, paths):
    for path in paths:
        text = read_file(path)

        if re.search(rf"'({slug})':", text):
            print(f"[跳过] {slug} 已存在于 {os.path.relpath(path, ROOT)}")
            continue

        # 找到 categoryMap 中最后一个条目
        entries = list(re.finditer(r"^(\s*)'([a-z0-9-]+)':\s*'([^']*)',?$", text, re.M))
        if not entries:
            die(f"未能在 {path} 中找到分类映射,请手动添加。")
        last = entries[-1]
        indent = last.group(1)
        new_line = f"{indent}'{slug}': '{name}',\n"
        text = text[:last.end()] + "\n" + new_line + text[last.end():]

        # categoryOrder 数组末尾追加
        m = re.search(r"(const categoryOrder = \[[^\]]*)\]", text)
        if m:
            close_pos = m.end() - 1
            items = m.group(1).rstrip()
            if items.endswith("'"):
                text = text[:close_pos] + f", '{slug}'" + text[close_pos:]
            else:
                text = text[:close_pos] + f"'{slug}'" + text[close_pos:]

        write_file(path, text)
        print(f"[OK] 已更新 {os.path.relpath(path, ROOT)}")


def cmd_add_category(slug):
    slug = normalize_slug(slug)
    if not slug:
        die("分类名称不能为空。")
    if not is_valid_slug(slug):
        die("分类只能包含小写字母、数字和连字符(-)。")

    zh = input(f"分类 '{slug}' 的中文名称(如: 技术): ").strip()
    en = input(f"分类 '{slug}' 的英文名称(如: Technical): ").strip()
    if not zh:
        die("中文名称不能为空。")

    print(f"\n即将新增分类: {slug} (中文: {zh} / 英文: {en})")
    add_category_to_header(slug, zh, en)
    add_category_to_pages(slug, zh, [ARTICLE_INDEX_ZH, ARTICLE_CAT_ZH])
    add_category_to_pages(slug, en, [ARTICLE_INDEX_EN, ARTICLE_CAT_EN])

    print(f"\n完成!分类 '{zh}' 已添加到导航下拉菜单和分类页面。")
    print(f"新文章 frontmatter 中填写: category: \"{slug}\"")


def strip_frontmatter(content):
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip("\n")
    return content


def cmd_add_doc(md_path):
    if not os.path.isfile(md_path):
        die(f"找不到文件: {md_path}")
    with open(md_path, "r", encoding="utf-8") as f:
        body = strip_frontmatter(f.read())
    if not body.strip():
        die(f"文件内容为空: {md_path}")

    default_name = os.path.splitext(os.path.basename(md_path))[0]
    print(f"读取文章内容: {md_path} ({len(body)} 字符)")
    print("请填写以下信息(直接回车使用默认值):\n")

    title = input(f"文章标题: ").strip() or default_name
    if len(title) > 60:
        die("标题不能超过 60 个字符。")

    description = input(f"文章描述: ").strip()
    if len(description) > 160:
        die("描述不能超过 160 个字符。")

    tags_raw = input(f"文章标签(逗号分隔, 如: astro,博客): ").strip()
    tags = [t.strip() for t in tags_raw.replace("，", ",").split(",") if t.strip()]

    cats = existing_categories()
    if cats:
        print(f"已有分类: {', '.join(cats)}")
    category = input(f"文章分类(直接回车使用 'tech'): ").strip() or "tech"
    category = normalize_slug(category)
    if not category:
        category = "tech"

    slug = input(f"显示 URL(文章访问路径, 如: my-first-post): ").strip()
    slug = normalize_slug(slug)
    if not slug:
        slug = normalize_slug(default_name)
    if not is_valid_slug(slug):
        die("显示 URL 只能包含小写字母、数字和连字符(-)。")

    post_dir = os.path.join(BLOG_DIR, slug)
    if os.path.exists(post_dir):
        die(f"目录已存在: {post_dir}")

    today = datetime.date.today().isoformat()
    tags_yaml = "[" + ", ".join(tags) + "]" if tags else "[]"
    frontmatter = (
        "---\n"
        f"title: \"{title}\"\n"
        f"description: \"{description}\"\n"
        f"publishDate: {today}\n"
        f"tags: {tags_yaml}\n"
        f"category: \"{category}\"\n"
        "draft: false\n"
        "---\n\n"
    )

    os.makedirs(post_dir, exist_ok=True)
    index_path = os.path.join(post_dir, "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(frontmatter)
        f.write(body)
        f.write("\n")

    print(f"\n[OK] 文章已创建: {os.path.relpath(index_path, ROOT)}")
    print(f"访问地址: {SITE_URL}/article/{slug}")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        usage()

    if args[0] == "-D":
        if len(args) < 2:
            die("-D 需要一个 Markdown 文件路径,例如: python get_docs.py -D 我的文章.md")
        if len(args) > 2:
            die("参数过多,一次只能处理一篇文章。")
        cmd_add_doc(args[1])
    elif args[0] == "-C":
        if len(args) < 2:
            die("-C 需要一个分类名称,例如: python get_docs.py -C my-category")
        if len(args) > 2:
            die("参数过多,一次只能新增一个分类。")
        cmd_add_category(args[1])
    else:
        usage()


if __name__ == "__main__":
    main()
