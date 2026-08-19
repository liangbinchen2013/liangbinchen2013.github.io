#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean.py - 清理构建与缓存产物

用法:
  python clean.py              清理全部(Python 编译产物 + pnpm 产物)
  python clean.py -p           仅清理 Python 编译产物(__pycache__ / *.pyc / *.pyo)
  python clean.py -n           仅清理 pnpm 产物(node_modules / dist / .astro / .vercel / .wrangler / 日志)
  python clean.py -l           仅列出将删除的内容,不实际删除(预览)
  python clean.py -y           跳过确认直接删除
  python clean.py -h           显示本帮助
"""

import argparse
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

PYTHON_DIRS = ["__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"]
PYTHON_EXT = (".pyc", ".pyo")
PNPM_DIRS = ["node_modules", "dist", ".astro", ".vercel", ".wrangler"]
PNPM_LOG_FILES = ["npm-debug.log", "pnpm-debug.log"]
SKIP_DIRS = {".git", "node_modules"}


def dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path, onerror=lambda e: None):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total


def fmt_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024


def collect(python_only, pnpm_only):
    items = []
    added_dirs = set()

    def add(kind, path):
        size = dir_size(path) if kind == "dir" else os.path.getsize(path)
        items.append((kind, path, size))
        if kind == "dir":
            added_dirs.add(os.path.normcase(path))

    if not python_only:
        for name in PNPM_DIRS:
            p = os.path.join(ROOT, name)
            if os.path.isdir(p):
                add("dir", p)
        for name in PNPM_LOG_FILES:
            p = os.path.join(ROOT, name)
            if os.path.isfile(p):
                add("file", p)

    if not pnpm_only:
        for root, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for d in dirs:
                if d in PYTHON_DIRS:
                    add("dir", os.path.join(root, d))
            for f in files:
                if f.endswith(PYTHON_EXT) and not any(
                    os.path.normcase(os.path.join(root, f)).startswith(d + os.sep)
                    for d in added_dirs
                ):
                    add("file", os.path.join(root, f))

    return items


def main():
    parser = argparse.ArgumentParser(add_help=False, description="清理 Python 与 pnpm 产物")
    parser.add_argument("-p", "--python", action="store_true", help="仅清理 Python 编译产物")
    parser.add_argument("-n", "--pnpm", action="store_true", help="仅清理 pnpm 产物")
    parser.add_argument("-l", "--list", action="store_true", help="仅列出,不删除")
    parser.add_argument("-y", "--yes", action="store_true", help="跳过确认")
    parser.add_argument("-h", "--help", action="store_true", help="显示帮助")
    args = parser.parse_args()

    if args.help:
        print(__doc__)
        return

    items = collect(args.python, args.pnpm)
    if not items:
        print("没有需要清理的产物。")
        return

    items.sort(key=lambda it: it[1])
    total = sum(it[2] for it in items)
    print(f"发现 {len(items)} 项产物,共 {fmt_size(total)}:\n")
    for kind, path, size in items:
        tag = "[目录]" if kind == "dir" else "[文件]"
        print(f"  {tag} {os.path.relpath(path, ROOT):50s} {fmt_size(size)}")

    if args.list:
        print("\n(预览模式,未删除任何内容)")
        return

    if not args.yes and input("\n确认删除? [y/N]: ").strip().lower() != "y":
        print("已取消。")
        return

    for kind, path, size in items:
        if kind == "dir":
            shutil.rmtree(path, ignore_errors=True)
        else:
            try:
                os.remove(path)
            except OSError:
                pass
    print(f"已清理 {len(items)} 项,释放 {fmt_size(total)}。")


if __name__ == "__main__":
    main()