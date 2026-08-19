# LBC 博客完全维护手册(超级版)

> 本文档是博客「LBCの博客」(https://blog.lbcoj.top) 的**唯一权威维护手册**。
> 涵盖:环境搭建、Git 全命令详解、pnpm 全命令详解、目录结构逐项说明、配置逐字段说明、
> 内容发布、分类标签管理、页面维护、构建部署、日常巡检、故障排查、自定义开发、性能优化、安全备份。
> 建议全文阅读一遍后,日常操作按「第 13 章 日常维护清单」执行。

---

## 目录

1. 项目概览
2. 环境准备
3. 快速上手
4. 目录结构详解
5. 配置详解
6. Git 完全指南
7. pnpm 完全指南
8. 内容管理(写文章)
9. 分类与标签管理
10. 页面管理
11. tools.py 管理工具手册
12. 构建与部署
13. 日常维护清单
14. 常见问题排查(FQA)
15. 安全与备份
16. 自定义开发指南
17. 性能优化
18. 命令速查总表
19. 附录:主题架构解析

---

# 1. 项目概览

## 1.1 项目是什么

本项目是一套基于 **Astro 7.2** 的静态博客系统,源主题为开源项目
[rusin-dev/astro-theme-cyanwind](https://github.com/rusin-dev/astro-theme-cyanwind)(青风主题,MIT 协议),
经过深度个性化定制后成为个人博客「LBCの博客」。

- **在线地址**:https://blog.lbcoj.top
- **GitHub 仓库**:https://github.com/liangbinchen2013/liangbinchen2013.github.io
- **源码分支**:`source`(日常开发、写文章、改代码都在这个分支)
- **部署分支**:`main`(GitHub Pages 直接消费该分支,存放编译后的静态文件,**不要手动改 main**)

## 1.2 技术栈

| 组件 | 版本 | 作用 |
| --- | --- | --- |
| Astro | 7.2.0 | 静态站点生成框架(SSG) |
| Tailwind CSS | 3.4.19 | 原子化 CSS 框架,负责全部样式 |
| TypeScript | 5.9.3 | 类型检查与前端语言 |
| Pagefind | 1.4.0 | 站内全文搜索(构建时生成索引) |
| KaTeX | 0.16.27 | 数学公式渲染 |
| MDX / Markdown | 7.x | 文章书写格式 |
| simple-icons | 15.22.0 | 图标库 |
| Waline | 3.8.0 | 评论系统(目前未启用) |
| date-fns | 4.1.0 | 日期格式化 |
| shiki | 4.0.2 | 代码高亮 |
| Node.js | 26.x | 运行时 |
| pnpm | 11.x | 包管理器 |

## 1.3 仓库结构(两个分支)

```
GitHub 仓库:liangbinchen2013/liangbinchen2013.github.io
├── source 分支 ───── 全部源码(本手册所在分支)
└── main 分支 ──────── 构建产物(dist 编译输出,仅供 GitHub Pages)
```

**核心原则:**
1. 永远只在 `source` 分支上开发、写文章、提交。
2. `main` 分支只接受「构建产物推送」,由 `tools.py deploy` 命令自动完成。
3. 日常写文章时**不需要**动 `main` 分支,发布时构建推送即可。

## 1.4 本地目录概览

```
/home/user/Desktop/astro-theme-cyanwind-main/
├── src/                   # 全部源码(核心)
│   ├── pages/             # 页面(路由)
│   ├── content/           # 内容集合(文章等)
│   ├── components/        # 组件
│   ├── layouts/           # 布局
│   ├── plugins/           # 自定义插件
│   ├── assets/            # 图片等静态资源(被 import 的)
│   └── site.config.ts     # 站点主配置文件
├── public/                # 公共静态文件(直接拷贝到站点根)
├── get_docs.py            # 文章/分类生成脚本
├── tools.py               # 日常维护管理脚本
├── MAINTENANCE.md         # 本文档
├── package.json           # 依赖与脚本
├── astro.config.mjs       # Astro 构建配置
├── tailwind.config.mjs    # Tailwind 配置
├── tsconfig.json          # TypeScript 配置
└── LICENSE                # MIT 许可证(务必保留)
```

---

# 2. 环境准备

## 2.1 本机环境清单

| 软件 | 版本要求 | 说明 |
| --- | --- | --- |
| Linux | 任意发行版 | 本项目在 Linux 上开发 |
| miniconda3 | 最新 | Python 环境(脚本依赖),安装于 `~/miniconda3` |
| Python | 3.x | `get_docs.py` / `tools.py` 的运行环境 |
| Node.js | >= 22(本机 26.x) | Astro 运行要求 |
| pnpm | 9+ (本机 11.x) | 包管理器 |
| git | 2.x | 版本控制 |
| GitHub CLI (gh) | 2.97+ | GitHub API 操作(推送/查状态) |
| FastGithub | 本机 127.0.0.1:38457 | GitHub 访问代理(网络必需) |

## 2.2 激活 Python 环境(关键!)

**所有 Python 脚本、git、gh、pnpm 命令,必须先激活 conda 环境:**

```bash
source ~/miniconda3/bin/activate
```

激活后可以执行 `which python3` 确认版本。不激活的话 `python3`、`git`、`gh` 可能不可用或版本不对。

## 2.3 GitHub 访问代理(FastGithub)

由于网络环境,访问 GitHub 必须走本机 FastGithub 代理。**需要联网的 git 操作**(push / pull / clone)前必须设置:

```bash
export HTTPS_PROXY=http://127.0.0.1:38457
export HTTP_PROXY=http://127.0.0.1:38457
export ALL_PROXY=http://127.0.0.1:38457
```

`tools.py` 的 `git push`、`deploy` 命令内部已自动设置,无需手动 export。

**验证代理是否可用:**

```bash
curl -I -x http://127.0.0.1:38457 https://github.com 2>/dev/null | head -3
```

如果 FastGithub 没启动(返回 502/无法连接),先启动它再继续。

## 2.4 Git 证书配置(重要)

FastGithub 代理会替换 GitHub 证书,导致 git 报 `SSL certificate problem`。
**针对本仓库**已配置关闭校验(仅此仓库,不影响全局):

```bash
git config http.sslVerify false
```

如果克隆新副本后发现 git 报证书错误,执行上面这行即可。

## 2.5 安装依赖

```bash
# 1. 激活环境
source ~/miniconda3/bin/activate
# 2. 进入项目目录
cd /home/user/Desktop/astro-theme-cyanwind-main
# 3. 安装依赖(pnpm 有全局锁文件 pnpm-lock.yaml,不要用 npm/yarn 混装)
pnpm install
```

安装失败时(网络问题),可以临时换用国内镜像:

```bash
pnpm config set registry https://registry.npmmirror.com
pnpm install
# 之后可以改回来
pnpm config set registry https://registry.npmjs.org
```

## 2.6 编辑器建议

- VS Code + 插件:`Astro`(官方语言服务)、`Prettier`、`Tailwind CSS IntelliSense`、`esbenp.prettier-vscode`
- `tools.py` 的 `page edit` / `article edit` 使用 `$EDITOR` 环境变量,默认 `nano`。
  想用 vim:`export EDITOR=vim`

---

# 3. 快速上手

## 3.1 日常开发三件套

| 目标 | 命令 |
| --- | --- |
| 本地实时预览 | `pnpm dev` |
| 类型检查 | `pnpm check` |
| 完整构建 | `DEPLOYMENT_PLATFORM=github pnpm run build:github` |

## 3.2 完整开发循环(示例)

```bash
source ~/miniconda3/bin/activate
cd /home/user/Desktop/astro-theme-cyanwind-main

# 1. 写一篇文章
python3 get_docs.py -D 我的文章.md

# 2. 本地预览
pnpm dev
# 浏览器打开 http://localhost:4321

# 3. 类型检查(确保没有 schema 错误)
pnpm check

# 4. 提交源码
python3 tools.py git sync "feat: 新增文章 xxx"

# 5. 发布上线
python3 tools.py deploy
```

## 3.3 常用脚本速查(package.json)

| 脚本 | 实际执行 | 用途 |
| --- | --- | --- |
| `pnpm dev` | `astro dev` | 开发服务器(热更新) |
| `pnpm dev:force` | `astro dev --force` | 强制忽略缓存启动 |
| `pnpm dev:stop` | `astro dev stop` | 停止开发服务器 |
| `pnpm check` | `astro check` | TypeScript + 内容 schema 检查 |
| `pnpm build` | `astro check && astro build` | 检查并构建 |
| `pnpm run build:github` | 同上 | GitHub Pages 模式构建 |
| `pnpm preview` | `astro preview` | 预览构建产物 |
| `pnpm sync` | `astro sync` | 重新生成内容集合类型 |
| `pnpm format` | prettier 全项目格式化 | 代码风格统一 |
| `pnpm lint` | eslint --fix | 自动修复代码规范 |
| `pnpm run quality` | lint + sync + check + format | 一键质量检查 |
| `pnpm clean` | 删除 .astro/.vercel/dist/.wrangler | 清理构建产物 |
| `pnpm clean:all` | clean + 删除 node_modules | 彻底清理 |

## 3.4 清理与重建

```bash
# 只清理构建产物(推荐,保留依赖)
pnpm clean

# 彻底清理(含依赖,之后需要 pnpm install)
pnpm clean:all
```

注意:`astro build` 每次都会**清空 dist 目录**,包括里面的 `.git`。
所以发布时 `tools.py deploy` 会在 dist 里重新 `git init`,这是**正常流程**,不要惊慌。

---# 4. 目录结构详解

> 本章逐目录、逐文件说明。★ = 日常最常接触。

## 4.1 根目录文件

| 路径 | 说明 |
| --- | --- |
| `package.json` | 项目元信息、依赖清单、脚本命令(见 3.3) |
| `pnpm-lock.yaml` | pnpm 锁文件,锁定每个依赖的精确版本,**必须提交** |
| `astro.config.mjs` | Astro 构建配置(适配器、集成、插件、i18n、sitemap) |
| `tailwind.config.mjs` | Tailwind 主题色、内容扫描路径 |
| `tsconfig.json` | TypeScript 编译配置(路径别名 @/ 等) |
| `postcss.config.mjs` | PostCSS 配置(autoprefixer) |
| `.gitignore` | Git 忽略清单(见 6.12) |
| `.gitattributes` | Git 属性(换行符处理等) |
| `.prettierignore` | Prettier 忽略清单 |
| `.prettierrc` | Prettier 格式化规则 |
| `.vscode/` | VS Code 推荐配置 |
| `.editorconfig` | 编辑器通用缩进规则 |
| `LICENSE` | MIT 许可证 ★ 保留原版权声明,不可删除 |
| `README.md` / `README_en.md` | 项目介绍(中/英) |
| `get_docs.py` | 文章与分类生成脚本 ★ |
| `tools.py` | 日常维护管理脚本 ★ |
| `MAINTENANCE.md` | 本文档 ★ |
| `dist/` | 构建产物(被 gitignore,运行时生成) |
| `.astro/` | Astro 内部缓存(被 gitignore) |
| `.vercel/` | Vercel 输出(被 gitignore,本机无实际作用) |
| `node_modules/` | 依赖(被 gitignore,`pnpm install` 生成) |

## 4.2 `src/` 源码目录 ★

### 4.2.1 `src/pages/` — 页面(路由)★

Astro 文件路由规则:**文件名 = URL 路径**。

| 文件/目录 | 路由 | 说明 |
| --- | --- | --- |
| `index.astro` | `/` | 首页 ★ |
| `en/index.astro` | `/en/` | 英文首页 |
| `article/index.astro` | `/article` | 文章列表页(按分类聚合)★ |
| `article/[slug]/index.astro` | `/article/{文章URL}` | 单篇文章页 ★ |
| `article/[category]/[...page].astro` | `/article/分类/第N页` | 分类分页列表 |
| `en/article/*` | `/en/article/*` | 英文版文章区 |
| `academic/index.astro` | `/academic` | 学术页面(占位) |
| `en/academic/index.astro` | `/en/academic` | 英文学术页 |
| `projects/index.astro` | `/projects` | 项目展示页(占位) |
| `en/projects/index.astro` | `/en/projects` | 英文项目页 |
| `about/index.astro` | `/about` | 关于页面(占位) |
| `en/about/index.astro` | `/en/about` | 英文关于页 |
| `terms/*.astro` | `/terms/*` | 隐私政策、服务条款等 8 个法务页面 |
| `404.astro` | `/404` | 404 页面 |
| `rss.xml.ts` | `/rss.xml` | RSS 订阅源 |
| `search/index.astro` | `/search` | 搜索页(Pagefind) |
| `robots.txt.ts` | `/robots.txt` | 搜索引擎爬虫规则 |

**页面文件内部结构**(以 article 列表页为例):

```astro
---
// 1. frontmatter 脚本区:写 JS/TS 逻辑
import PageLayout from '@/layouts/BaseLayout.astro'
const allPosts = await getBlogCollection()
---
<!-- 2. 模板区:写 HTML + JSX 表达式 -->
<PageLayout title="文章">
  {allPosts.map(post => <p>{post.data.title}</p>)}
</PageLayout>
```

### 4.2.2 `src/content/` — 内容集合 ★

| 路径 | 说明 |
| --- | --- |
| `config.ts` | 内容集合定义(schema 校验规则)★ |
| `blogs/` | 博客文章集合 ★★ 每篇文章一个目录 |
| `blogs/{slug}/index.md` | 单篇文章(文件名 `index.md` 固定) |
| `collection/docs.md` | 示例/存档文档(可删除) |

**文章目录规则**(核心!):

```
src/content/blogs/
└── my-first-post/        ← 目录名 = 显示 URL(即 slug)
    └── index.md          ← 正文 + frontmatter
```

文章访问地址 = `https://blog.lbcoj.top/article/{目录名}`。
例如 `src/content/blogs/hello-world/index.md` 的地址是
`https://blog.lbcoj.top/article/hello-world`。

### 4.2.3 `src/components/` — 组件 ★

| 目录 | 内容 |
| --- | --- |
| `basic/` | Header(导航栏)、Footer(页脚)等基础组件 ★ |
| `pages/` | 文章预览卡片、分页器、文章内容等页面组件 ★ |
| `user/` | 用户自定义组件(Icon、Button、Card、Tabs、Spoiler、Timeline、FormattedDate 等)★ |
| `advanced/` | 高级组件(评论 Comment、图片灯箱等) |
| `links/` | 友链组件(已删除,仅留说明) |
| `about/` | 关于页组件(ToolSection 等) |
| `projects/` | 项目展示组件(ProjectSection) |
| `academic/` | 学术页组件(如有) |

### 4.2.4 `src/layouts/` — 布局

| 文件 | 用途 |
| --- | --- |
| `BaseLayout.astro` | 基础布局(HTML 骨架、SEO、主题色)★ |
| `CommonPage.astro` | 普通页面布局(带标题、目录、评论区)★ |
| `ArticleLayout.astro` | 文章页布局(面包屑、目录、上一篇下一篇)★ |
| `TermLayout.astro` | 法务条款页布局 |

### 4.2.5 `src/plugins/` — 自定义插件

| 文件 | 用途 |
| --- | --- |
| `remark-plugins.ts` | 阅读时间统计、图片 zoomable 标记 |
| `remark-directives.ts` | 自定义指令 |
| `luogu-blocks.ts` | 洛谷题目卡片插件 ★ |
| `rehype-auto-link-headings.ts` | 标题自动锚点 |
| `shiki-transformers.ts` | 代码高亮增强(复制按钮、行号、diff 标记) |
| `output-copier.ts` | 构建产物复制(Vercel 专属,本机报 ENOENT 属正常) |
| `friendCircle.ts` | 朋友圈插件(已删除) |

### 4.2.6 `src/schemas/` — Zod 校验 schema

| 文件 | 用途 |
| --- | --- |
| `content.ts` | 内容集合 schema |
| `header.ts` | 导航菜单 schema(默认菜单) |
| `links.ts` | 友链 schema(已删除) |
| `theme-config.ts` | 主题配置 schema(全部可选字段) |

### 4.2.7 `src/types/` — 类型定义

| 文件 | 用途 |
| --- | --- |
| `theme-config.ts` | 主题配置类型(对应 site.config.ts 的 theme) |
| `integrations-config.ts` | 集成配置类型(Pagefind、Waline、typography 等) |
| `user-config.ts` | 用户配置总类型 |
| `index.ts` | 类型统一导出 |

### 4.2.8 `src/server.ts` — 数据查询函数 ★

内容集合的封装查询,写页面逻辑时常用:

| 函数 | 用途 |
| --- | --- |
| `getBlogCollection()` | 获取全部中文文章(按日期排序) |
| `getBlogCollectionEn()` | 获取全部英文文章 |
| `getUniqueCategories()` | 去重分类列表 |
| `getUniqueTags()` | 去重标签列表 |
| `getCollectionsByCategory()` | 按分类筛选 |
| `sortMDByDate()` | 按日期排序 |
| `getPostCollections()` | 文章 + 分页 |

### 4.2.9 其他 `src/` 文件

| 文件 | 用途 |
| --- | --- |
| `site.config.ts` | ★★★ 站点主配置(见第 5 章) |
| `axi-integration.ts` | 主题集成(解析 config、注入插件) |
| `styles/global.css` | 全局样式(字体、暗色模式等)★ |
| `assets/` | 被 import 的图片(头像 278105203.png 等)★ |

## 4.3 `public/` — 公共静态文件 ★

`public/` 下所有文件会**原样复制**到站点根目录,无需 import 直接可用:

| 路径 | 说明 |
| --- | --- |
| `favicon/` | 站点图标(favicon.ico、favicon-256x256.png、site.webmanifest)★ |
| `avatar/avatar.png` | 头像(被 some 页面引用) |
| `fonts/` | 字体文件 |
| `images/` | 其他图片 |

**注意区分** `public/` 与 `src/assets/`:
- `public/` 里的文件用普通路径引用,如 `/favicon/favicon.ico`
- `src/assets/` 里的文件需要 `import` 引用(会被构建工具处理压缩)

## 4.4 `node_modules/` 与锁文件

- `node_modules/`:`pnpm install` 生成,**永不手动修改**、**永不提交**
- `pnpm-lock.yaml`:**必须提交**,保证所有人构建出一模一样的依赖版本

---

# 5. 配置详解

## 5.1 `src/site.config.ts` — 站点主配置 ★★★

这是博客的「总开关」,几乎一切个性化都改这里。分三个导出对象:

### 5.1.1 `theme` — 主题配置

```ts
export const theme: ThemeUserConfig = {
  // === 基础 ===
  title: "LBCの博客",          // 站点标题(中文)
  titleEn: "LBC's Blog",       // 英文标题
  author: 'LBC',               // 作者名(页脚版权)
  author_en: 'LBC',            // 英文作者名
  description: 'LBC的个人博客，记录一堆内容。',  // 站点描述(SEO)
  description_en: "LBC's Personal Blog – A Collection of Random Stuff.",
  favicon: '/favicon/favicon.ico',      // 图标路径(相对 public)
  locale: {                    // 日期/语言本地化
    lang: 'en-US',
    attrs: 'en_US',
    dateLocale: 'en-US',
    dateOptions: { day: 'numeric', month: 'short', year: 'numeric' }
  },
  logo: { src: 'src/assets/278105203.png', alt: 'Avatar' },  // 首页 Logo 头像
  titleDelimiter: '|',         // 标题分隔符(SEO)
  prerender: true,             // 全站静态预渲染(SSG 必须 true)
  npmCDN: 'https://cdn.jsdmirror.cn/npm',   // npm CDN 镜像

  // === 头部导航 ===
  header: {
    menu: [                    // ★ 导航菜单(增删页面时改这里)
      { title: '文章', titleEn: 'Articles', link: '/article' },
      { title: '学术', titleEn: 'Academic', link: '/academic' },
      { title: '项目', titleEn: 'Projects', link: '/projects' },
      { title: '关于', titleEn: 'About', link: '/about' }
    ]
  },

  // === 页脚 ===
  footer: {
    registration: {},          // ICP 备案信息(可选,留空则隐藏)
    credits: true,             // 是否显示「Powered by Astro & Axi」署名
    social: {                  // ★ 社交链接
      github: 'https://github.com/liangbinchen2013',
      luogu: 'https://www.luogu.com.cn/user/1432496'
    }
  },

  // === 内容 ===
  content: {
    externalLinksContent: ' ↗',        // 外链后缀图标
    blogPageSize: 15,                  // ★ 每页文章数(分页大小)
    externalLinkArrow: true,           // 外链箭头
    share: ['weibo', 'x', 'bluesky']   // 分享按钮
  },

  // === 个人信息 ===
  personal: {
    location: 'China',                 // 所在地(页脚)
    githubUsername: 'liangbinchen2013',
    email: 'liangbinchen2013@outlook.com',
    googleScholar: '',                 // Google 学术(可选)
    blogStartDate: '2026-08-19',       // 博客创建日期(页脚统计)
    domains: {
      main: 'blog.lbcoj.top',          // 主域名 ★
      githubPages: 'blog.lbcoj.top',   // GitHub Pages 域名(写死为自定义域名)
    }
  }
}
```

### 5.1.2 `integ` — 集成配置

```ts
export const integ: IntegrationUserConfig = {
  pagefind: true,   // 是否启用全文搜索(构建时索引)
  quote: {          // 首页随机一言
    server: 'https://v1.hitokoto.cn/?c=i',
    target: '(data) => data.hitokoto || "Error"'
  },
  typography: {     // 文章排版 CSS 类
    class: 'break-words prose prose-axi dark:prose-invert ...'
  },
  mediumZoom: {     // 图片点击放大
    enable: true,
    selector: '.prose .zoomable',
  },
  waline: {         // 评论系统(enable: false 表示关闭)
    enable: false,
    emoji: ['bmoji', 'weibo', 'qq'],
    additionalConfigs: { pageview: true, comment: true }
  }
}
```

### 5.1.3 `terms` — 法务页面列表

```ts
export const terms: CardListData = {
  title: 'Terms content',
  list: [ ... ]   // 8 个条款页面的链接数组
}
```

## 5.2 `astro.config.mjs` — 构建配置

关键点(一般不用改):

```js
const platform = process.env.DEPLOYMENT_PLATFORM || 'vercel'
// 构建时通过环境变量选择适配器:
//   DEPLOYMENT_PLATFORM=github  → 纯静态输出到 dist/ (本站用这个)
//   DEPLOYMENT_PLATFORM=vercel → 输出到 .vercel/output
//   DEPLOYMENT_PLATFORM=cloudflare → Cloudflare 模式

export default defineConfig({
  site: 'https://blog.lbcoj.top',      // ★ 站点地址(sitemap/RSS 用它)
  output: 'static',
  integrations: [
    // 内容集合、sitemap、RSS、自定义插件(luogu 卡片、阅读时间、代码高亮增强)
  ],
  markdown: {
    shikiConfig: { themes: {...} },    // 代码高亮主题
    remarkPlugins: [...], rehypePlugins: [...],  // 数学公式、GFM、目录
  },
  i18n: {
    defaultLocale: 'zh',
    locales: ['zh', 'en'],             // 中英双语
    routing: { prefixDefaultLocale: false }
  }
})
```

## 5.3 `tailwind.config.mjs` — 主题色

```js
theme: {
  extend: {
    colors: {
      primary: ...,   // 主色调(全站强调色)
      border: ..., background: ...,
      foreground: ...,
      // 暗色模式: .dark 前缀下一套
    }
  }
}
```

改主题色只需改这里的颜色值,全站自动生效(亮/暗两套)。

## 5.4 `tsconfig.json` — 路径别名

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]   // @/xxx = src/xxx
    }
  }
}
```

代码里 `import config from '@/site-config'` 即 `src/site-config.ts`。

## 5.5 `src/content/config.ts` — 文章 schema

每篇文章的 frontmatter 都要通过这个校验,字段如下(详见 8.3):

```ts
z.object({
  title: z.string().max(60),        // 标题,最多 60 字符
  description: z.string().max(160), // 描述,最多 160 字符
  publishDate: z.coerce.date(),     // 发布日期(必须)
  updatedDate: z.coerce.date().optional(),  // 更新日期(可选)
  heroImage: z.string().optional(), // 封面图(可选)
  tags: z.array(z.string()).default([]),    // 标签数组
  category: z.string().optional(),  // 分类
  language: z.string().optional(),  // 语言标记(zh/en)
  draft: z.boolean().default(false),// 草稿(不发布)
  comment: z.boolean().default(true),// 评论区开关
  pixivLink: z.string().optional()  // Pixiv 链接(可选)
})
```

---
# 4. 目录结构详解

> 本章逐目录、逐文件说明。★ = 日常最常接触。

## 4.1 根目录文件

| 路径 | 说明 |
| --- | --- |
| `package.json` | 项目元信息、依赖清单、脚本命令(见 3.3) |
| `pnpm-lock.yaml` | pnpm 锁文件,锁定每个依赖的精确版本,**必须提交** |
| `astro.config.mjs` | Astro 构建配置(适配器、集成、插件、i18n、sitemap) |
| `tailwind.config.mjs` | Tailwind 主题色、内容扫描路径 |
| `tsconfig.json` | TypeScript 编译配置(路径别名 @/ 等) |
| `postcss.config.mjs` | PostCSS 配置(autoprefixer) |
| `.gitignore` | Git 忽略清单(见 6.12) |
| `.gitattributes` | Git 属性(换行符处理等) |
| `.prettierignore` | Prettier 忽略清单 |
| `.prettierrc` | Prettier 格式化规则 |
| `.vscode/` | VS Code 推荐配置 |
| `.editorconfig` | 编辑器通用缩进规则 |
| `LICENSE` | MIT 许可证 ★ 保留原版权声明,不可删除 |
| `README.md` / `README_en.md` | 项目介绍(中/英) |
| `get_docs.py` | 文章与分类生成脚本 ★ |
| `tools.py` | 日常维护管理脚本 ★ |
| `MAINTENANCE.md` | 本文档 ★ |
| `dist/` | 构建产物(被 gitignore,运行时生成) |
| `.astro/` | Astro 内部缓存(被 gitignore) |
| `.vercel/` | Vercel 输出(被 gitignore,本机无实际作用) |
| `node_modules/` | 依赖(被 gitignore,`pnpm install` 生成) |

## 4.2 `src/` 源码目录 ★

### 4.2.1 `src/pages/` — 页面(路由)★

Astro 文件路由规则:**文件名 = URL 路径**。

| 文件/目录 | 路由 | 说明 |
| --- | --- | --- |
| `index.astro` | `/` | 首页 ★ |
| `en/index.astro` | `/en/` | 英文首页 |
| `article/index.astro` | `/article` | 文章列表页(按分类聚合)★ |
| `article/[slug]/index.astro` | `/article/{文章URL}` | 单篇文章页 ★ |
| `article/[category]/[...page].astro` | `/article/分类/第N页` | 分类分页列表 |
| `en/article/*` | `/en/article/*` | 英文版文章区 |
| `academic/index.astro` | `/academic` | 学术页面(占位) |
| `en/academic/index.astro` | `/en/academic` | 英文学术页 |
| `projects/index.astro` | `/projects` | 项目展示页(占位) |
| `en/projects/index.astro` | `/en/projects` | 英文项目页 |
| `about/index.astro` | `/about` | 关于页面(占位) |
| `en/about/index.astro` | `/en/about` | 英文关于页 |
| `terms/*.astro` | `/terms/*` | 隐私政策、服务条款等 8 个法务页面 |
| `404.astro` | `/404` | 404 页面 |
| `rss.xml.ts` | `/rss.xml` | RSS 订阅源 |
| `search/index.astro` | `/search` | 搜索页(Pagefind) |
| `robots.txt.ts` | `/robots.txt` | 搜索引擎爬虫规则 |

**页面文件内部结构**(以 article 列表页为例):

```astro
---
// 1. frontmatter 脚本区:写 JS/TS 逻辑
import PageLayout from '@/layouts/BaseLayout.astro'
const allPosts = await getBlogCollection()
---
<!-- 2. 模板区:写 HTML + JSX 表达式 -->
<PageLayout title="文章">
  {allPosts.map(post => <p>{post.data.title}</p>)}
</PageLayout>
```

### 4.2.2 `src/content/` — 内容集合 ★

| 路径 | 说明 |
| --- | --- |
| `config.ts` | 内容集合定义(schema 校验规则)★ |
| `blogs/` | 博客文章集合 ★★ 每篇文章一个目录 |
| `blogs/{slug}/index.md` | 单篇文章(文件名 `index.md` 固定) |
| `collection/docs.md` | 示例/存档文档(可删除) |

**文章目录规则**(核心!):

```
src/content/blogs/
└── my-first-post/              ← 目录名 = 显示 URL(即 slug)
    └── index.md                ← 正文 + frontmatter
```

文章访问地址 = `https://blog.lbcoj.top/article/{目录名}`。
例如 `src/content/blogs/hello-world/index.md` 的地址是
`https://blog.lbcoj.top/article/hello-world`。

### 4.2.3 `src/components/` — 组件 ★

| 目录 | 内容 |
| --- | --- |
| `basic/` | Header(导航栏)、Footer(页脚)等基础组件 ★ |
| `pages/` | 文章预览卡片、分页器、文章内容等页面组件 ★ |
| `user/` | 用户自定义组件(Icon、Button、Card、Tabs、Spoiler、Timeline、FormattedDate 等)★ |
| `advanced/` | 高级组件(评论 Comment、图片灯箱等) |
| `links/` | 友链组件(已删除,仅留说明) |
| `about/` | 关于页组件(ToolSection 等) |
| `projects/` | 项目展示组件(ProjectSection) |
| `academic/` | 学术页组件(如有) |

### 4.2.4 `src/layouts/` — 布局

| 文件 | 用途 |
| --- | --- |
| `BaseLayout.astro` | 基础布局(HTML 骨架、SEO、主题色)★ |
| `CommonPage.astro` | 普通页面布局(带标题、目录、评论区)★ |
| `ArticleLayout.astro` | 文章页布局(面包屑、目录、上一篇下一篇)★ |
| `TermLayout.astro` | 法务条款页布局 |

### 4.2.5 `src/plugins/` — 自定义插件

| 文件 | 用途 |
| --- | --- |
| `remark-plugins.ts` | 阅读时间统计、图片 zoomable 标记 |
| `remark-directives.ts` | 自定义指令 |
| `luogu-blocks.ts` | 洛谷题目卡片插件 ★ |
| `rehype-auto-link-headings.ts` | 标题自动锚点 |
| `shiki-transformers.ts` | 代码高亮增强(复制按钮、行号、diff 标记) |
| `output-copier.ts` | 构建产物复制(Vercel 专属,本机报 ENOENT 属正常) |
| `friendCircle.ts` | 朋友圈插件(已删除) |

### 4.2.6 `src/schemas/` — Zod 校验 schema

| 文件 | 用途 |
| --- | --- |
| `content.ts` | 内容集合 schema |
| `header.ts` | 导航菜单 schema(默认菜单) |
| `links.ts` | 友链 schema(已删除) |
| `theme-config.ts` | 主题配置 schema(全部可选字段) |

### 4.2.7 `src/types/` — 类型定义

| 文件 | 用途 |
| --- | --- |
| `theme-config.ts` | 主题配置类型(对应 site.config.ts 的 theme) |
| `integrations-config.ts` | 集成配置类型(Pagefind、Waline、typography 等) |
| `user-config.ts` | 用户配置总类型 |
| `index.ts` | 类型统一导出 |

### 4.2.8 `src/server.ts` — 数据查询函数 ★

内容集合的封装查询,写页面逻辑时常用:

| 函数 | 用途 |
| --- | --- |
| `getBlogCollection()` | 获取全部中文文章(按日期排序) |
| `getBlogCollectionEn()` | 获取全部英文文章 |
| `getUniqueCategories()` | 去重分类列表 |
| `getUniqueTags()` | 去重标签列表 |
| `getCollectionsByCategory()` | 按分类筛选 |
| `sortMDByDate()` | 按日期排序 |
| `getPostCollections()` | 文章 + 分页 |

### 4.2.9 其他 `src/` 文件

| 文件 | 用途 |
| --- | --- |
| `site.config.ts` | ★★★ 站点主配置(见第 5 章) |
| `axi-integration.ts` | 主题集成(解析 config、注入插件) |
| `styles/global.css` | 全局样式(字体、暗色模式等)★ |
| `assets/` | 被 import 的图片(头像 278105203.png 等)★ |

## 4.3 `public/` — 公共静态文件 ★

`public/` 下所有文件会**原样复制**到站点根目录,无需 import 直接可用:

| 路径 | 说明 |
| --- | --- |
| `favicon/` | 站点图标(favicon.ico、favicon-256x256.png、site.webmanifest)★ |
| `avatar/avatar.png` | 头像(被 some 页面引用) |
| `fonts/` | 字体文件 |
| `images/` | 其他图片 |

**注意区分** `public/` 与 `src/assets/`:
- `public/` 里的文件用普通路径引用,如 `/favicon/favicon.ico`
- `src/assets/` 里的文件需要 `import` 引用(会被构建工具处理压缩)

## 4.4 `node_modules/` 与锁文件

- `node_modules/`:`pnpm install` 生成,**永不手动修改**、**永不提交**
- `pnpm-lock.yaml`:**必须提交**,保证所有人构建出一模一样的依赖版本

---

# 5. 配置详解

## 5.1 `src/site.config.ts` — 站点主配置 ★★★

这是博客的「总开关」,几乎一切个性化都改这里。分三个导出对象:

### 5.1.1 `theme` — 主题配置

```ts
export const theme: ThemeUserConfig = {
  // === 基础 ===
  title: "LBCの博客",          // 站点标题(中文)
  titleEn: "LBC's Blog",       // 英文标题
  author: 'LBC',               // 作者名(页脚版权)
  author_en: 'LBC',            // 英文作者名
  description: 'LBC的个人博客，记录一堆内容。',  // 站点描述(SEO)
  description_en: "LBC's Personal Blog – A Collection of Random Stuff.",
  favicon: '/favicon/favicon.ico',      // 图标路径(相对 public)
  locale: {                    // 日期/语言本地化
    lang: 'en-US',
    attrs: 'en_US',
    dateLocale: 'en-US',
    dateOptions: { day: 'numeric', month: 'short', year: 'numeric' }
  },
  logo: { src: 'src/assets/278105203.png', alt: 'Avatar' },  // 首页 Logo 头像
  titleDelimiter: '|',         // 标题分隔符(SEO)
  prerender: true,             // 全站静态预渲染(SSG 必须 true)
  npmCDN: 'https://cdn.jsdmirror.cn/npm',   // npm CDN 镜像

  // === 头部导航 ===
  header: {
    menu: [                    // ★ 导航菜单(增删页面时改这里)
      { title: '文章', titleEn: 'Articles', link: '/article' },
      { title: '学术', titleEn: 'Academic', link: '/academic' },
      { title: '项目', titleEn: 'Projects', link: '/projects' },
      { title: '关于', titleEn: 'About', link: '/about' }
    ]
  },

  // === 页脚 ===
  footer: {
    registration: {},          // ICP 备案信息(可选,留空则隐藏)
    credits: true,             // 是否显示「Powered by Astro & Axi」署名
    social: {                  // ★ 社交链接
      github: 'https://github.com/liangbinchen2013',
      luogu: 'https://www.luogu.com.cn/user/1432496'
    }
  },

  // === 内容 ===
  content: {
    externalLinksContent: ' ↗',        // 外链后缀图标
    blogPageSize: 15,                  // ★ 每页文章数(分页大小)
    externalLinkArrow: true,           // 外链箭头
    share: ['weibo', 'x', 'bluesky']   // 分享按钮
  },

  // === 个人信息 ===
  personal: {
    location: 'China',                 // 所在地(页脚)
    githubUsername: 'liangbinchen2013',
    email: 'liangbinchen2013@outlook.com',
    googleScholar: '',                 // Google 学术(可选)
    blogStartDate: '2026-08-19',       // 博客创建日期(页脚统计)
    domains: {
      main: 'blog.lbcoj.top',          // 主域名 ★
      githubPages: 'blog.lbcoj.top',   // GitHub Pages 域名(写死为自定义域名)
    }
  }
}
```

### 5.1.2 `integ` — 集成配置

```ts
export const integ: IntegrationUserConfig = {
  pagefind: true,   // 是否启用全文搜索(构建时索引)
  quote: {          // 首页随机一言
    server: 'https://v1.hitokoto.cn/?c=i',
    target: '(data) => data.hitokoto || "Error"'
  },
  typography: {     // 文章排版 CSS 类
    class: 'break-words prose prose-axi dark:prose-invert ...'
  },
  mediumZoom: {     // 图片点击放大
    enable: true,
    selector: '.prose .zoomable',
  },
  waline: {         // 评论系统(enable: false 表示关闭)
    enable: false,
    emoji: ['bmoji', 'weibo', 'qq'],
    additionalConfigs: { pageview: true, comment: true }
  }
}
```

### 5.1.3 `terms` — 法务页面列表

```ts
export const terms: CardListData = {
  title: 'Terms content',
  list: [ ... ]   // 8 个条款页面的链接数组
}
```

## 5.2 `astro.config.mjs` — 构建配置

关键点(一般不用改):

```js
const platform = process.env.DEPLOYMENT_PLATFORM || 'vercel'
// 构建时通过环境变量选择适配器:
//   DEPLOYMENT_PLATFORM=github  → 纯静态输出到 dist/ (本站用这个)
//   DEPLOYMENT_PLATFORM=vercel → 输出到 .vercel/output
//   DEPLOYMENT_PLATFORM=cloudflare → Cloudflare 模式

export default defineConfig({
  site: 'https://blog.lbcoj.top',      // ★ 站点地址(sitemap/RSS 用它)
  output: 'static',
  integrations: [
    // 内容集合、sitemap、RSS、自定义插件(luogu 卡片、阅读时间、代码高亮增强)
  ],
  markdown: {
    shikiConfig: { themes: {...} },    // 代码高亮主题
    remarkPlugins: [...], rehypePlugins: [...],  // 数学公式、GFM、目录
  },
  i18n: {
    defaultLocale: 'zh',
    locales: ['zh', 'en'],             // 中英双语
    routing: { prefixDefaultLocale: false }
  }
})
```

## 5.3 `tailwind.config.mjs` — 主题色

```js
theme: {
  extend: {
    colors: {
      primary: ...,   // 主色调(全站强调色)
      border: ..., background: ...,
      foreground: ...,
      // 暗色模式: .dark 前缀下一套
    }
  }
}
```

改主题色只需改这里的颜色值,全站自动生效(亮/暗两套)。

## 5.4 `tsconfig.json` — 路径别名

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]   // @/xxx = src/xxx
    }
  }
}
```

代码里 `import config from '@/site-config'` 即 `src/site-config.ts`。

## 5.5 `src/content/config.ts` — 文章 schema

每篇文章的 frontmatter 都要通过这个校验,字段如下(详见 8.3):

```ts
z.object({
  title: z.string().max(60),        // 标题,最多 60 字符
  description: z.string().max(160), // 描述,最多 160 字符
  publishDate: z.coerce.date(),     // 发布日期(必须)
  updatedDate: z.coerce.date().optional(),  // 更新日期(可选)
  heroImage: z.string().optional(), // 封面图(可选)
  tags: z.array(z.string()).default([]),    // 标签数组
  category: z.string().optional(),  // 分类
  language: z.string().optional(),  // 语言标记(zh/en)
  draft: z.boolean().default(false),// 草稿(不发布)
  comment: z.boolean().default(true),// 评论区开关
  pixivLink: z.string().optional()  // Pixiv 链接(可选)
})
```

---# 6. Git 完全指南

> 本章从零讲透 Git,包含本博客的所有分支操作、常用命令、疑难场景。
> 日常 90% 的操作只需记住:add、commit、push、pull、status、log。

## 6.1 Git 是什么

Git 是一个分布式版本控制系统,用于追踪文件的每次修改。
本博客的所有代码和文章都存在 Git 仓库里,由 GitHub 托管。

**三大区域概念:**

```
工作区(你看到的文件)
   │  git add
   ▼
暂存区(即将提交的改动)
   │  git commit
   ▼
本地仓库(.git 目录里的历史)
   │  git push
   ▼
远程仓库(GitHub 服务器)
```

## 6.2 初始化与克隆

### 克隆仓库(在新机器上获取代码)

```bash
# 设置代理后克隆
export HTTPS_PROXY=http://127.0.0.1:38457
export ALL_PROXY=http://127.0.0.1:38457
git clone https://github.com/liangbinchen2013/liangbinchen2013.github.io.git
cd liangbinchen2013.github.io
git checkout source          # 切到源码分支(默认是 main,即构建产物)
```

### 全新初始化(本机已做,了解即可)

```bash
git init -b source    # 初始化仓库,默认分支名为 source
git remote add origin https://github.com/liangbinchen2013/liangbinchen2013.github.io.git
```

## 6.3 查看状态:git status

**最高频命令,操作前先看一眼:**

```bash
git status                  # 简略状态
git status --short          # 极简格式(本仓库默认习惯)
```

输出解读:

| 标记 | 含义 |
| --- | --- |
| `??` | 未跟踪的新文件(还没 add) |
| `M` | 已修改(第一列 = 暂存区状态,第二列 = 工作区状态) |
| `A` | 新增到暂存区 |
| `D` | 已删除 |
| `MM` | 暂存后又改了工作区 |

## 6.4 提交:add + commit ★

```bash
# 1. 把改动加入暂存区
git add -A                      # 加入全部改动(最常用)
git add src/site.config.ts      # 只加某个文件
git add src/content/blogs/      # 只加某个目录

# 2. 提交
git commit -m "feat: 新增文章 xxx"
```

**提交信息规范(重要):**

| 前缀 | 场景 | 示例 |
| --- | --- | --- |
| `feat:` | 新功能/新文章 | `feat: 新增文章「Hello World」` |
| `fix:` | 修 bug | `fix: 修复暗色模式下文字看不清` |
| `chore:` | 杂项/工具 | `chore: 更新维护文档` |
| `docs:` | 文档 | `docs: 补充配置说明` |
| `refactor:` | 重构 | `refactor: 重构文章卡片组件` |
| `style:` | 格式 | `style: 统一代码缩进` |
| `init:` | 初始化 | `init: 博客源码` |

```bash
# 一行命令搞定 add + commit(本仓库 tools.py 也是这么做的)
git add -A && git commit -m "feat: 新增文章 xxx"
```

## 6.5 查看历史:git log

```bash
git log                        # 完整历史
git log --oneline              # 一行一条(最常用)★
git log --oneline -10          # 只看最近 10 条
git log --oneline --graph      # 带分支图
git log --all --oneline        # 所有分支的历史
git log -p                     # 看每次提交的具体改动
git log --oneline -- src/site.config.ts   # 只看某个文件的历史
```

本仓库提交历史示例:

```
1dfd7de feat: 移除友情链接功能(页面/组件/配置/朋友圈插件)
9e597e4 feat: 新增 get_docs.py 文章/分类管理脚本
81b55b9 chore: 移除原作者 fork 同步工作流
168c58c init: 博客源码(基于 astro-theme-cyanwind 2.0.0, MIT 协议)
```

## 6.6 查看差异:git diff

```bash
git diff                       # 工作区 vs 暂存区(未 add 的改动)
git diff HEAD                  # 工作区 vs 最近一次提交(全部未提交改动)
git diff --stat                # 只显示改了多少行
git diff 168c58c 1dfd7de       # 两个提交之间的差异
git diff -- src/site.config.ts # 只看某个文件的差异
```

## 6.7 分支:git branch ★

本博客只有两个分支:`source`(源码)和 `main`(部署产物)。

```bash
git branch                     # 列出本地分支(当前分支带 * 号)
git branch -a                  # 列出本地 + 远程分支
git branch -r                  # 只看远程分支

git branch 新分支名             # 新建分支
git switch 分支名               # 切换分支(新写法)
git checkout 分支名             # 切换分支(老写法)
git switch -c 新分支名          # 新建并切换
git branch -d 分支名            # 删除分支(已合并的安全删除)
git branch -D 分支名            # 强制删除分支
```

**分支策略(本博客):**

```
source 分支:日常开发、写文章、改配置(你的工作地)
main 分支:部署产物,由 tools.py deploy 自动推送,不要手动操作
```

## 6.8 远程仓库:git remote ★

```bash
git remote -v                  # 查看远程地址
git remote add origin <url>    # 添加远程
git remote remove origin       # 移除远程
git remote set-url origin <url> # 修改远程地址
```

本仓库远程:

```
origin  https://github.com/liangbinchen2013/liangbinchen2013.github.io.git (fetch)
origin  https://github.com/liangbinchen2013/liangbinchen2013.github.io.git (push)
```

## 6.9 推送:git push ★

```bash
# 首次推送(建立跟踪关系)
git push -u origin source

# 之后只需
git push

# 或明确指定分支
git push origin source

# 强制推送(危险!会覆盖远端,见 6.15)
git push -f origin main
```

**本仓库约定:**
- `source` 分支:**普通推送** `git push origin source`
- `main` 分支:只用 `git push -f origin main` 推送构建产物(因为每次构建都是全新 init,历史必然不同,必须 -f)

**推送前必须设置 FastGithub 代理:**

```bash
export HTTPS_PROXY=http://127.0.0.1:38457
export ALL_PROXY=http://127.0.0.1:38457
```

## 6.10 拉取:git pull / git fetch

```bash
git fetch origin              # 只下载远端信息,不改本地
git pull origin source        # 下载并合并远端 source 到本地
git pull --rebase origin source  # 以变基方式拉取(历史更干净)
```

**什么时候需要 pull?**
- 换了电脑/重新 clone 后,远端有新提交时
- 多设备协作时(本博客单人维护,很少需要)

## 6.11 撤销与回滚 ★

### 撤销工作区修改(未 add)

```bash
git restore 文件名            # 丢弃工作区改动,恢复到上次提交
git restore .                 # 丢弃全部工作区改动 ★
```

### 撤销暂存(已 add 未 commit)

```bash
git restore --staged 文件名   # 从暂存区移除(文件改动保留)
```

### 修改刚才的提交

```bash
git add -A
git commit --amend            # 把新改动并入上一个提交(会打开编辑器改信息)
git commit --amend -m "新信息" # 顺便改提交信息
```

### 回滚提交

```bash
git reset --soft HEAD~1       # 撤销最近一次提交,改动回到暂存区
git reset --mixed HEAD~1      # 撤销提交+暂存,改动回到工作区(默认)
git reset --hard HEAD~1       # ★危险★ 彻底删除最近一次提交及改动
git reset --hard 168c58c      # 回滚到指定提交(其后的提交全部丢弃)
git revert 1dfd7de            # 生成一个"反向提交"来抵消某次提交(安全,不丢历史)
```

**规则:**
- 已经 push 到远端的提交,**不要用 reset 回滚**,用 `git revert` 或新提交覆盖
- 回滚前先 `git stash` 或备份,防止丢失工作

## 6.12 暂存:git stash(急救工具)

改到一半突然要干别的,又不想提交:

```bash
git stash                     # 把工作区改动暂时收起来
git stash list                # 查看暂存列表
git stash pop                 # 恢复最近的暂存并删除记录
git stash apply               # 恢复但不删除记录
git stash drop                # 丢弃某个暂存
```

## 6.13 忽略文件:.gitignore ★

`.gitignore` 里列出的文件不会被 git 跟踪。本仓库忽略的内容:

```bash
# 构建产物(重装环境后自动生成,不需要提交)
dist/
.astro/
.vercel/
.wrangler

# 依赖
node_modules/

# 日志
*.log

# 环境变量(可能含密钥)
.env
.env.production

# 系统文件
.DS_Store
```

**注意:**
- 被忽略的文件不会出现在 `git status` 里,也不会被 `git add -A` 添加
- 想强制添加被忽略的文件:`git add -f 文件名`(一般不需要)
- 修改 `.gitignore` 后,`git status` 立即生效,无需其他操作

## 6.14 查看配置:git config

```bash
git config --global user.name "liangbinchen2013"
git config --global user.email "liangbinchen2013@outlook.com"
git config user.name          # 查看
git config --list             # 列出全部配置
git config --global --edit    # 编辑全局配置
```

**本仓库关键配置(务必保持):**

```bash
git config http.sslVerify false   # 关闭 SSL 校验(FastGithub 需要)
```

## 6.15 强制推送(git push -f)什么时候用 ★

`-f` 会用本地历史**覆盖**远端历史,远端旧提交全部丢弃。

| 场景 | 是否用 -f |
| --- | --- |
| 推送 main 分支构建产物 | 必须用(每次构建都是全新历史) |
| 单人仓库,把本地 reset 后的历史同步到远端 | 可以用 |
| 多人协作仓库 | 绝对不要 |

**危险操作前的自检清单:**
1. 确定远端没有别人需要的提交?→ `git log origin/source --oneline`
2. 本地历史包含远端所有想要的提交?→ `git log --oneline`
3. 确认无误后再 push

## 6.16 合并冲突处理

多人(或多设备)同时改同一文件,`git pull` 时可能冲突:

```
Auto-merging src/site.config.ts
CONFLICT (content): Merge conflict in src/site.config.ts
```

冲突文件里会这样标记:

```
<<<<<<< HEAD
这是你的改动
=======
这是远端的改动
>>>>>>> origin/source
```

**处理步骤:**

```bash
# 1. 打开冲突文件,手动选择保留哪段(删掉 <<<<<<< ======= >>>>>>> 标记)
# 2. 保存后:
git add src/site.config.ts
git commit -m "fix: 解决合并冲突"
```

**本博客单人维护,遇到冲突大概率是:**
- 在不同设备上都有未提交的改动
- 误改了 main 分支
解决方式:手动合并或 `git checkout -- .` 放弃本地改动重新 pull。

## 6.17 Tag 打标签(发布版本)

```bash
git tag                       # 查看标签
git tag v1.0.0                # 打标签(轻量)
git tag -a v1.0.0 -m "第一个版本"  # 带注释的标签
git push origin v1.0.0        # 推送标签
git tag -d v1.0.0             # 删除本地标签
```

本博客可选使用,给每次大改版打标签,方便回滚。

## 6.18 GitHub CLI(gh)常用操作

```bash
# 需要先登录(浏览器授权)
gh auth login

# 常用命令
gh repo view liangbinchen2013/liangbinchen2013.github.io   # 查看仓库
gh api repos/liangbinchen2013/liangbinchen2013.github.io/branches  # 分支列表
gh api repos/liangbinchen2013/liangbinchen2013.github.io/commits/main  # main 最新提交
gh api -X POST repos/liangbinchen2013/liangbinchen2013.github.io/pages  # 开启 Pages
```

**注意**:gh 的 token 没有 `workflow` 权限,推送含 `.github/workflows` 的文件会被拒。
本项目已删除全部 workflow 文件,不受影响。如果未来要加 GitHub Actions,需要重新授权:

```bash
gh auth logout && gh auth login --scopes workflow,repo
```

## 6.19 本仓库 Git 工作流总结(日常版)★

```bash
# ========= 写一篇文章 =========
python3 get_docs.py -D 我的文章.md          # 生成文章
# 编辑 src/content/blogs/xxx/index.md 内容...

# ========= 检查并预览 =========
pnpm check && pnpm dev

# ========= 提交源码 =========
git status --short                          # 确认改动内容
git add -A
git commit -m "feat: 新增文章「我的文章」"

# ========= 推送到 GitHub =========
export HTTPS_PROXY=http://127.0.0.1:38457
export ALL_PROXY=http://127.0.0.1:38457
git push origin source

# ========= 发布上线 =========
python3 tools.py deploy                     # 构建 + 推送 main(自动设代理)
```

或者用工具脚本一步到位:

```bash
python3 tools.py git sync "feat: 新增文章「我的文章」"   # 提交+推送 source
python3 tools.py deploy                                     # 发布到线上
```

---# 7. pnpm 完全指南

> pnpm 是比 npm 更快、更省磁盘的包管理器。本项目所有依赖都由 pnpm 管理。

## 7.1 安装 pnpm

```bash
# 推荐:通过 corepack(随 Node.js 附带)
corepack enable pnpm

# 或通过 npm 全局安装
npm install -g pnpm

# 验证
pnpm --version        # 本机为 11.x
```

## 7.2 安装依赖

```bash
pnpm install           # 安装全部依赖(读取 package.json + pnpm-lock.yaml)
pnpm install --frozen-lockfile   # 严格按锁文件安装(CI 环境用)
```

**第一次在新机器上跑项目,必做:**

```bash
source ~/miniconda3/bin/activate
cd /home/user/Desktop/astro-theme-cyanwind-main
pnpm install
```

## 7.3 常用命令

| 命令 | 作用 |
| --- | --- |
| `pnpm dev` | 启动开发服务器(热更新,默认 http://localhost:4321) |
| `pnpm build` | 类型检查 + 构建 |
| `pnpm check` | 只做类型检查 |
| `pnpm preview` | 预览构建产物 |
| `pnpm add <包名>` | 安装运行时依赖 |
| `pnpm add -D <包名>` | 安装开发依赖 |
| `pnpm remove <包名>` | 移除依赖 |
| `pnpm update` | 更新依赖到允许的最新版本 |
| `pnpm outdated` | 查看过期依赖 |
| `pnpm run <脚本>` | 运行 package.json 里的脚本 |
| `pnpm clean` | 清理构建产物(本项目自定义脚本) |
| `pnpm exec <命令>` | 在项目环境里执行命令 |
| `pnpm list` | 列出已安装依赖 |

## 7.4 本项目脚本详解

```bash
pnpm dev              # 本地开发(改文件自动刷新)★ 日常
pnpm check            # 类型检查,发布前必跑 ★
pnpm run build:github # 完整构建(GitHub Pages 模式)★ 发布用
pnpm preview          # 预览 dist 产物
pnpm run quality      # 全流程质检(lint + check + format)
pnpm clean            # 删除构建产物
```

## 7.5 依赖管理注意事项

1. **不要混用 npm/yarn**:包管理器一旦换成别的,锁文件冲突会导致依赖损坏。统一用 pnpm。
2. **lock 文件必须提交**:`pnpm-lock.yaml` 决定所有人的依赖版本。
3. **node_modules 被 gitignore**:重装依赖用 `pnpm install` 即可,不用提交。
4. **镜像加速**(网络慢时):

```bash
pnpm config set registry https://registry.npmmirror.com
pnpm install
# 恢复官方源
pnpm config set registry https://registry.npmjs.org
```

5. **pnpm 的硬链接机制**:node_modules 里的文件是硬链接,直接手改 node_modules 里的文件不会影响实际包内容,排查问题要找源码。

## 7.6 Node 版本

Astro 7 需要 Node >= 20。本机 Node 26.5.1 完全兼容。检查版本:

```bash
node -v
pnpm -v
```

版本不对时考虑用 nvm 管理(Node 版本管理器),本项目不做强制要求。

---

# 8. 内容管理(写文章)★★★

> 本章是日常最高频操作:怎么写一篇文章并发布。

## 8.1 最快路径(推荐)

```bash
source ~/miniconda3/bin/activate
cd /home/user/Desktop/astro-theme-cyanwind-main

# 1. 先写好正文(纯 Markdown,不需要 frontmatter)
#    比如创建 /tmp/文章草稿.md 或 我的文章.md
#    内容示例:
#      这是一篇测试文章。
#      ## 小标题
#      - 列表1
#      - 列表2

# 2. 一键生成文章(交互式填写元信息)
python3 get_docs.py -D 我的文章.md
```

脚本会依次询问(按顺序):

| 询问 | 说明 | 示例 |
| --- | --- | --- |
| 文章标题 | 必填,最长 60 字符,回车默认取文件名 | 我的第一篇文章 |
| 文章描述 | 必填,最长 160 字符,用于 SEO | 记录我的第一篇博客 |
| 文章标签 | 逗号分隔,可留空 | astro,博客,教程 |
| 文章分类 | 回车默认 tech,列出已有分类 | tech |
| 显示 URL | 文章访问路径,只允许小写字母/数字/连字符 | my-first-post |
| 发布日期 | 回车自动取今天(脚本自动获取时间)★ | 2026-08-19 |
| 更新日期 | 可选,回车跳过 | 2026-08-20 |

生成后:

- 文件:`src/content/blogs/my-first-post/index.md`
- 地址:`https://blog.lbcoj.top/article/my-first-post`
- 提示信息会直接打印访问地址

## 8.2 文章生命周期(完整流程)

```bash
# 创建
python3 get_docs.py -D 草稿.md

# 编辑内容(推荐用工具)
python3 tools.py article edit my-first-post

# 或直接改文件
nano src/content/blogs/my-first-post/index.md

# 预览
pnpm dev    # 浏览器开 http://localhost:4321/article/my-first-post

# 检查
pnpm check

# 提交 + 发布
python3 tools.py git sync "feat: 新增文章 my-first-post"
python3 tools.py deploy
```

## 8.3 frontmatter 字段大全 ★

每篇文章头部用 `---` 包裹的元信息区叫 frontmatter:

```markdown
---
title: "我的第一篇文章"            # 标题(必填,<=60字)
description: "记录第一篇博客"       # 描述(必填,<=160字,SEO)
publishDate: 2026-08-19            # 发布日期(必填,YYYY-MM-DD)
updatedDate: 2026-08-20            # 更新日期(可选)
heroImage: "/images/cover.png"     # 封面图(可选,放 public 下)
tags: [astro, 博客, 教程]           # 标签数组(可选)
category: "tech"                   # 分类(可选,必须与分类表一致)
language: "zh"                     # 语言(可选)
draft: false                       # 草稿:true 则不发布(可选)
comment: true                      # 评论区开关(可选)
pixivLink: ""                      # Pixiv 链接(可选)
---

正文从这里开始,支持完整 Markdown 语法。
```

**frontmatter 校验规则(src/content/config.ts):**
- `title` 超过 60 字符 → 构建失败
- `description` 超过 160 字符 → 构建失败
- `publishDate` 格式错误 → 构建失败
- 未知字段 → 构建失败(zod strict)

**草稿技巧:** `draft: true` 的文章不会出现在列表页,但本地 `pnpm dev` 仍可预览。写完初稿后把 draft 改为 false 再发布。

## 8.4 Markdown 语法支持

项目已启用 `remark-gfm`,支持 GFM(GitHub Flavored Markdown):

```markdown
# 一级标题
## 二级标题
### 三级标题

**粗体**  *斜体*  ~~删除线~~  `行内代码`

> 引用块

- 无序列表
- 无序列表

1. 有序列表
2. 有序列表

[链接文字](https://example.com)
![图片描述](/images/xxx.png)

| 表头1 | 表头2 |
| --- | --- |
| 单元格 | 单元格 |

- [x] 已完成任务
- [ ] 未完成任务
```

### 代码块(带语法高亮)

```markdown
```python
def hello():
    print("Hello, World!")
```
```

代码块增强功能(shiki):
- 复制按钮:鼠标悬停代码块右上角
- 语言标签:代码块左上角显示语言名
- 行高亮/增删标记:

```markdown
```js{1,3}   // 高亮第 1、3 行
// [!code ++]  // 标记为新增
// [!code --]  // 标记为删除
// [!code error]  // 标记为错误
// [!code warning] // 标记为警告
```
```

### 数学公式(KaTeX)

```markdown
行内公式:$E = mc^2$

独立公式:
$$
\frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
$$
```

### 目录(自动生成)

文章页右侧自动生成标题目录(TOC),无需手动写。

## 8.5 主题自带内容组件

文章内可直接使用以下组件(import 自 `@/components/user`):

### Tabs 标签页

```astro
---
import { Tabs, TabItem } from '@/components/user'
---
<Tabs>
  <TabItem label="方法一">
    方法一的内容
  </TabItem>
  <TabItem label="方法二">
    方法二的内容
  </TabItem>
</Tabs>
```

### Spoiler 折叠

```astro
---
import { Spoiler } from '@/components/user'
---
<Spoiler title="点击展开答案">
  隐藏的内容
</Spoiler>
```

### Steps 步骤

```astro
---
import { Steps } from '@/components/user'
---
<Steps>
  第一步的内容
</Steps>
```

### Timeline 时间线

```astro
---
import { Timeline } from '@/components/user'
---
<Timeline>
  时间线条目
</Timeline>
```

## 8.6 图片管理

| 图片位置 | 引用方式 | 特点 |
| --- | --- | --- |
| `public/images/` | `![](/images/xxx.png)` | 原样复制,适合封面/永久图 |
| `src/assets/` | import 引用 | 构建时优化压缩 |
| 外部链接 | `![](https://...)` | 直接引用,依赖外站 |

**建议:** 文章图片统一放 `public/images/`。也可以放文章目录内:

```markdown
src/content/blogs/my-post/
├── index.md
└── image.png        # 相对引用:![](./image.png)
```

## 8.7 英文版文章

本博客支持中英双语。英文站点由 `getBlogCollectionEn()` 读取。
**中文站是主要维护对象**,英文页面(article/en/*)按需维护。

## 8.8 RSS 订阅

站点自动生成 RSS:`https://blog.lbcoj.top/rss.xml`。
RSS 内容取自 frontmatter 的 title/description/publishDate,无需额外维护。

## 8.9 搜索索引

Pagefind 在构建时自动生成全文搜索索引:
- 新文章构建后自动进入搜索
- 删除文章后构建自动移除
- 无需手动维护索引文件
# 9. 分类与标签管理 ★

## 9.1 分类体系

目前分类(导航下拉菜单):

| slug | 中文名 | 英文名 |
| --- | --- | --- |
| `tech` | 技术 | Technical |
| `life` | 生活 | Daily Life |
| `solution` | 题解 | Solution |

分类在**五个文件**中定义(必须同步修改,否则导航/列表/分页不一致):

```
src/components/basic/Header.astro              ← 导航下拉菜单(中英双语映射)
src/pages/article/index.astro                  ← 中文分类列表页
src/pages/en/article/index.astro               ← 英文分类列表页
src/pages/article/[category]/[...page].astro   ← 中文分类分页(含排序)
src/pages/en/article/[category]/[...page].astro← 英文分类分页
```

## 9.2 新增分类(推荐用脚本)★

```bash
python3 get_docs.py -C 新分类slug
```

交互式输入中英文名称后,脚本自动同步修改上述五个文件:
- `categoryMap` 增加 `slug` → 中英文名称的映射
- `categoryOrder` 数组末尾追加 slug

示例:

```bash
python3 get_docs.py -C book
# 输入中文名称:读书
# 输入英文名称:Reading
```

之后文章 frontmatter 写 `category: "book"` 即可。

**手动新增分类**(不用脚本时)的步骤:

1. 打开 `src/components/basic/Header.astro`,在 categoryMap 里加一行:

```ts
'book': { zh: '读书', en: 'Reading' },
```

2. 在 categoryOrder 数组追加:`'book'`
3. 同样操作 `src/pages/article/index.astro` 和 `en` 版:`'book': '读书'`
4. 同样操作 `src/pages/article/[category]/[...page].astro` 和 `en` 版
5. `pnpm check` 确认无误

## 9.3 删除分类

1. 先把所有使用该分类的文章改到其他分类(或删除文章)
2. 按 9.2 的反向操作,从五个文件中移除映射和顺序
3. `pnpm check` + 提交

## 9.4 分类顺序调整

`categoryOrder` 数组的顺序就是导航下拉菜单和分类列表的显示顺序。
例如想让「题解」排第一:

```ts
const categoryOrder = ['solution', 'tech', 'life']
```

## 9.5 标签管理

标签**不需要注册**,写进文章 frontmatter 的 `tags` 数组即可,自动聚合。

查看全部标签及统计:

```bash
python3 tools.py tag list
```

标签规范建议:
- 统一小写/统一大写,避免 `Astro` 和 `astro` 变成两个标签
- 常用标签固定几个:astro、博客、教程、题解、算法、生活……

---

# 10. 页面管理 ★

## 10.1 页面总览

| 页面 | 路由 | 文件 | 当前状态 |
| --- | --- | --- | --- |
| 首页 | `/` | `src/pages/index.astro` | 已定制 |
| 文章 | `/article` | `src/pages/article/index.astro` | 已定制 |
| 学术 | `/academic` | `src/pages/academic/index.astro` | 占位,待填 |
| 项目 | `/projects` | `src/pages/projects/index.astro` | 占位,待填 |
| 关于 | `/about` | `src/pages/about/index.astro` | 占位,待填 |
| 法务 | `/terms/*` | `src/pages/terms/*.astro` | 已替换域名/邮箱 |
| 404 | `/404` | `src/pages/404.astro` | 默认 |
| 搜索 | `/search` | `src/pages/search/index.astro` | 默认 |

**导航菜单控制位置:** `src/site.config.ts` 的 `header.menu`(见 5.1.1)。

## 10.2 查看/编辑页面(用工具)★

```bash
# 查看某个页面内容
python3 tools.py page show about      # about / academic / projects
python3 tools.py page show academic
python3 tools.py page show projects

# 编辑某个页面
python3 tools.py page edit about
```

## 10.3 首页(index.astro)

首页结构:简介卡片(头像 + 作者 + 社交链接)、一言(quote)、
最近文章、分类统计、页脚统计。

**自定义首页内容**就是编辑 `src/pages/index.astro` 的模板区。

## 10.4 学术页面(academic/index.astro)

当前为占位页,包含「关于我 / 研究爱好 / 专栏 / 开源仓库」四个区块。
编辑方式:`python3 tools.py page edit academic`

主要用到的组件:
- `PublicationSection`:专栏/出版物列表
- `ResearchProjectSection`:研究项目
- `SimpleIcon`:simple-icons 图标

## 10.5 项目页面(projects/index.astro)

当前为占位页,`<ProjectSection project={[]} />` 里传入空数组。
**新增项目时:**

```astro
<ProjectSection
  project={[
    {
      name: '我的项目',
      description: '项目介绍',
      link: 'https://github.com/liangbinchen2013/xxx',
      // 其他字段见 ProjectSection.astro 的 interface Props
    }
  ]}
/>
```

## 10.6 关于页面(about/index.astro)

占位页,含「工具」区块(ToolSection 组件)。
用 `python3 tools.py page edit about` 编辑。

## 10.7 新增一个页面(进阶)

1. 在 `src/pages/` 下新建 `我的页面/index.astro`(目录名 = 路由)
2. 模板参考现有页面,使用 `CommonPage` 布局:

```astro
---
import PageLayout from '@/layouts/CommonPage.astro'
const headings = [
  { depth: 2, slug: 'section-1', text: '第一节' }
]
---
<PageLayout title='我的页面' {headings} info={{ slug: '/我的页面', hideComment: true }}>
  <h2 id='section-1'>第一节<a class='anchor' href='#section-1'>#</a></h2>
  <p>内容</p>
</PageLayout>
```

3. 在 `site.config.ts` 的 `header.menu` 里加导航项
4. 如需英文版,再建 `src/pages/en/我的页面/index.astro`
5. `pnpm check` 验证

## 10.8 删除一个页面

1. 删除 `src/pages/xxx/`(及 en 版)
2. 从 `site.config.ts` 的 `header.menu` 移除导航项
3. 删除相关链接引用(页脚/首页等)
4. `pnpm check` 验证
# 11. tools.py 管理工具手册 ★★

> `tools.py` 是本博客的「一站式维护面板」,日常 80% 的操作都可以用它完成。
> 所有命令都要先激活 Python 环境:`source ~/miniconda3/bin/activate`

## 11.1 查看帮助

```bash
python3 tools.py help
python3 tools.py -h
```

## 11.2 文章管理(article)

### 列出全部文章

```bash
python3 tools.py article list
```

输出示例:

```
共 1 篇文章:

  my-first-post                    我的第一篇文章  (2026-08-19)
```

每行显示:slug(目录名)、标题、发布日期、是否草稿。

### 创建文章(调用 get_docs.py)

```bash
python3 tools.py article create 我的文章.md
```

等价于 `python3 get_docs.py -D 我的文章.md`,交互式填写元信息。

### 编辑文章

```bash
python3 tools.py article edit my-first-post
```

用 `$EDITOR`(默认 nano)打开 `src/content/blogs/my-first-post/index.md`。

### 删除文章

```bash
python3 tools.py article delete my-first-post
```

会先显示文章信息,确认后(`y`)才删除整个文章目录。**删除不可恢复,请先确认。**

### 重命名文章(改 URL)

```bash
python3 tools.py article rename 旧slug 新slug
```

把 `src/content/blogs/旧slug/` 改名为 `新slug`,文章地址随之变为
`/article/新slug`。注意:改名后旧地址 404,如被外链引用需谨慎。

## 11.3 分类管理(category)

### 列出分类

```bash
python3 tools.py category list
```

### 新增分类

```bash
python3 tools.py category add 新slug
```

等价于 `python3 get_docs.py -C 新slug`,交互式输入中英文名称,
自动同步五个文件(见 9.2)。

## 11.4 标签统计(tag)

```bash
python3 tools.py tag list
```

输出按使用次数降序排列:

```
共 3 个标签:
  astro                    2 篇
  博客                     1 篇
  教程                     1 篇
```

## 11.5 页面管理(page)

```bash
python3 tools.py page show about       # 打印关于页源码
python3 tools.py page show academic    # 打印学术页源码
python3 tools.py page show projects    # 打印项目页源码
python3 tools.py page edit about       # 编辑关于页
```

## 11.6 开发与构建

```bash
python3 tools.py dev        # 启动开发服务器(pnpm dev)
python3 tools.py check      # 类型检查(pnpm check)
python3 tools.py build      # 构建(GitHub Pages 模式)
python3 tools.py preview    # 预览构建产物
python3 tools.py clean      # 清理 dist/.astro/.vercel
```

## 11.7 一键部署(deploy)★★★

```bash
python3 tools.py deploy
```

**这是发布上线的唯一推荐命令**,内部流程:

1. 构建:`DEPLOYMENT_PLATFORM=github pnpm run build:github`
2. 在 dist 里写入 `CNAME`(内容 `blog.lbcoj.top`)和 `.nojekyll`
3. `git init`(因为每次构建 dist 都会被清空,包括 .git)
4. 提交全部产物
5. 自动设置 FastGithub 代理
6. `git push -f origin main` 强制推送到部署分支
7. 输出部署地址

**执行完约等 1-3 分钟,然后:**
- GitHub Pages 自动重新构建(状态可以在 GitHub Actions / Pages 页面查看)
- 访问 https://blog.lbcoj.top 验证

**注意:**
- deploy 前请先 `pnpm check`(deploy 内部 build 已含 check)
- 部署失败通常 = 构建失败,看输出定位问题(见第 14 章)
- 如果域名没生效,检查 Cloudflare DNS 的 CNAME 记录是否指向 `liangbinchen2013.github.io`

## 11.8 Git 快捷操作(git)

```bash
python3 tools.py git status              # 查看改动(等价 git status --short)
python3 tools.py git log                 # 最近 20 条提交
python3 tools.py git commit "提交信息"    # add -A + commit
python3 tools.py git push                # 推送 source(自动设代理)
python3 tools.py git sync "提交信息"      # commit + push 一步到位 ★
```

## 11.9 其他

```bash
python3 tools.py doc        # 输出维护文档路径
```

## 11.10 tools.py 日常使用组合 ★

```bash
# 写文章 → 发布 一条龙
python3 tools.py article create 我的文章.md   # 生成
python3 tools.py article edit my-post        # 改内容
python3 tools.py git sync "feat: 新增文章 my-post"   # 提交源码
python3 tools.py deploy                      # 发布上线
```# 12. 构建与部署 ★★★

## 12.1 部署架构

```
你的电脑                               GitHub                        Cloudflare          访客
┌────────────────┐  push source  ┌────────────────────┐
│ 源码 (source)   │──────────────▶│ 仓库(源码)          │
└────────────────┘               │ liangbinchen2013.  │
┌────────────────┐  push -f main ┌────────────────────┐
│ 构建产物 dist   │──────────────▶│ Pages(部署分支)     │──▶ blog.lbcoj.top ──▶ 浏览器
└────────────────┘               │ 静态文件            │
                                 └────────────────────┘
```

1. 源码存放在 `source` 分支
2. 构建产物(纯静态文件)强制推送到 `main` 分支
3. GitHub Pages 直接服务 `main` 分支内容
4. 自定义域名 `blog.lbcoj.top` 通过 Cloudflare DNS 的 CNAME 指向 `liangbinchen2013.github.io`

## 12.2 GitHub Pages 配置(一次性,已配置)

- Settings → Pages:
  - Source: **Deploy from a branch**
  - Branch: `main` / `/(root)`
  - Custom domain: `blog.lbcoj.top`(仓库里有 CNAME 文件,自动生效)
  - Enforce HTTPS:开启

## 12.3 DNS 配置(Cloudflare,已配置)

| 记录类型 | 名称 | 内容 | 代理状态 |
| --- | --- | --- | --- |
| CNAME | blog | liangbinchen2013.github.io | DNS only(灰云,重要!)|

**关键坑:** Cloudflare 记录如果开了橙色代理(Proxied),GitHub Pages 的证书
签发与重定向会出问题,站点可能打不开或 HTTPS 异常。
**必须把 blog 记录改为 DNS only(灰云)。**

## 12.4 完整发布流程(Checklist)★

```bash
# 0. 前置检查
source ~/miniconda3/bin/activate
git status --short          # 工作区干净,或有意提交的改动

# 1. 提交源码(见 6.19)
python3 tools.py git sync "feat: 更新 xxx"

# 2. 构建并部署(自动完成 check + build + push main)
python3 tools.py deploy

# 3. 验证
curl -s -o /dev/null -w "%{http_code}" https://blog.lbcoj.top   # 期望 200
# 浏览器访问 https://blog.lbcoj.top 确认新内容
```

## 12.5 手动构建产物检查

```bash
# 构建后本地检查产物内容
python3 tools.py build
ls dist/                    # 应有 index.html、article/、pagefind/、CNAME 等
find dist -name "*.html" | wc -l   # 页面总数
```

构建日志关键行:

```
[build] 31 page(s) built in 9.59s     ← 页面数量与耗时
[build] Complete!
[output-copier] ... ENOENT ...        ← Vercel 插件噪音,无视(见 14.x)
```

## 12.6 发布回滚

**方案 A:回滚源码 + 重新部署(推荐)**

```bash
# 找到要回滚到的提交
git log --oneline
# 用 revert 生成反向提交(保留历史)
git revert 1dfd7de
python3 tools.py git sync "revert: 回滚到 xxx"
python3 tools.py deploy
```

**方案 B:直接推送旧构建产物(main 分支)**

如果线上出错而本地源码已改坏,可直接部署旧版本:

```bash
# 在 GitHub 上查看 main 分支历史,复制某次部署的 commit hash
git fetch origin
git checkout origin/main~1    # 或指定 commit
# 将该目录推送回 main(需要重新 init,复杂)
```

**日常建议**:只维护好源码,回滚就走方案 A,不要手动折腾 main。

## 12.7 构建性能

- 首次构建较慢(需编译 + Pagefind 索引),后续有缓存会快
- 文章多时 Pagefind 索引占主要时间,属正常
- 构建失败先看报错第一行(见第 14 章)

---

# 13. 日常维护清单 ★

> 按频率执行,保证博客健康。

## 13.1 每次写文章后(必做)

- [ ] `pnpm check` 通过(标题/描述长度、日期格式、schema)
- [ ] 本地 `pnpm dev` 预览过文章渲染效果
- [ ] `python3 tools.py git sync "feat: ..."` 提交源码
- [ ] `python3 tools.py deploy` 发布
- [ ] 浏览器确认 https://blog.lbcoj.top 正常

## 13.2 每周(建议)

- [ ] `python3 tools.py article list` 检查文章列表(无异常 slug)
- [ ] `python3 tools.py tag list` 检查标签是否统一(大小写/拼写)
- [ ] `python3 tools.py git log` 确认提交记录整洁
- [ ] 检查首页/文章页在手机上的显示(响应式)

## 13.3 每月

- [ ] `pnpm outdated` 查看依赖更新,择机升级(先备份,升级后全量测试)
- [ ] 检查 404 页面、RSS(https://blog.lbcoj.top/rss.xml)
- [ ] 检查搜索功能:/search 可搜到最新文章
- [ ] 检查自定义域名与 HTTPS 证书(GitHub 自动续期,确认无警告)
- [ ] 清理:没用的分类、重复标签、废弃的图片文件

## 13.4 每季度

- [ ] `pnpm run quality` 全流程质检(lint/check/format)
- [ ] 备份:本地源码目录压缩归档或推送到私有仓库
- [ ] 检查主题上游是否有重要更新(rusin-dev/astro-theme-cyanwind)
- [ ] 更新维护文档(如果有新流程/新命令)

## 13.5 换电脑/迁移环境

```bash
# 新机器步骤(全量):
source ~/miniconda3/bin/activate
export HTTPS_PROXY=http://127.0.0.1:38457
export ALL_PROXY=http://127.0.0.1:38457
git clone https://github.com/liangbinchen2013/liangbinchen2013.github.io.git
cd liangbinchen2013.github.io
git checkout source
git config http.sslVerify false
pnpm install
# 验证:
pnpm check && pnpm dev
```

## 13.6 断网/离线工作

- 写文章、改代码**不需要联网**(除首次 pnpm install)
- 只有 push / deploy / 升级依赖需要网络
- 离线期间可以正常写文章,联网后统一提交推送

---

# 14. 常见问题排查(FQA)

## 14.1 构建报 ENOENT(output-copier)

```
[output-copier] [sitemap] Error copying files: Error: ENOENT ... './dist/client'
```

**原因**:`output-copier` 是 Vercel 专属插件,在 GitHub Pages 模式下找不到
Vercel 目录,属预期行为。
**处理**:无视。构建日志显示 `[build] Complete!` 即成功。

## 14.2 push 报 SSL certificate problem

```
fatal: unable to access ... SSL certificate problem
```

**原因**:FastGithub 代理证书替换,git 校验证书失败。
**处理**:

```bash
git config http.sslVerify false
```

(本仓库已配置,若新 clone 需要重新执行)

## 14.3 push 报 refusing to allow an OAuth App to create or update workflow

```
! [remote rejected] source -> source (refusing to allow an OAuth App to create
or update workflow `.github/workflows/xxx.yml` without `workflow` scope)
```

**原因**:gh 登录的 token 没有 `workflow` 权限,而提交里含 `.github/workflows/`。
**处理**:本项目已删除全部 workflow 文件。若未来要加,重新授权:

```bash
gh auth logout && gh auth login --scopes workflow,repo
```

## 14.4 构建失败:Invalid content entry data

```
Error: ... invalid-content-entry-data-error
Location: src/content/blogs/xxx/index.md
```

**原因**:文章 frontmatter 不符合 schema(标题超长、日期格式错、字段写错等)。
**处理**:
1. 打开报错的文件,对照 8.3 的字段表检查
2. 常见错误:title 超 60 字、description 超 160 字、publishDate 不是日期
3. 修正后重新 `pnpm check`

## 14.5 页面打不开 404

- 文章地址:`/article/{目录名}` —— 检查目录名拼写
- 检查 `git status` 是否未提交/未部署(写了文章没 deploy)
- 检查 `tools.py deploy` 是否成功,`gh api .../commits/main` 看 main 最新提交
- GitHub Pages 构建有延迟(1-3 分钟),稍等刷新
- 本地看:是否 `pnpm dev` 中

## 14.6 站点打不开/HTTPS 异常(域名问题)

1. 检查 Cloudflare:`blog.lbcoj.top` 记录必须是 **DNS only(灰云)**
2. 检查 GitHub Pages 设置:CNAME 为 `blog.lbcoj.top`,`Enforce HTTPS` 开启
3. 检查仓库根 `CNAME` 文件内容(只在 main 分支,由 deploy 写入)
4. 域名解析验证:

```bash
dig blog.lbcoj.top CNAME +short   # 应输出 liangbinchen2013.github.io
```

## 14.7 搜索搜不到新文章

Pagefind 索引在构建时生成。重新 `python3 tools.py deploy` 即可。
浏览器端索引缓存:强制刷新(Ctrl+Shift+R)。

## 14.8 改配置不生效

- 改了 `site.config.ts` 后必须重新构建(dev 模式会热更新,部署需重新 build)
- 改了 `astro.config.mjs` 后有时需要 `pnpm dev:force` 或重启 dev
- 改了 schema 后需要 `pnpm sync` 重新生成类型

## 14.9 依赖安装失败

```bash
# 换镜像重试
pnpm config set registry https://registry.npmmirror.com
pnpm install
# 或清缓存重装
pnpm clean:all && pnpm install
```

## 14.10 pnpm check 报很多类型错误

- 检查是否运行过 `pnpm sync`(改了 schema 后必做)
- 检查是否是 conda 环境没激活(pnpm 版本不对)
- 检查 node 版本:`node -v` 需 >= 20

## 14.11 误删/误改恢复

| 场景 | 恢复命令 |
| --- | --- |
| 改了文件没提交 | `git restore 文件`(会丢改动) |
| 删了文件没提交 | `git restore 文件` |
| 提交错了想改信息 | `git commit --amend -m "新信息"` |
| 回滚最近一次提交(未推送) | `git reset --hard HEAD~1` |
| 已推送的错误提交 | `git revert <hash>` 后重新 deploy |
| 想找回被删的提交 | `git reflog` 找 hash 后 `git reset --hard <hash>` |

## 14.12 文章没出现在列表页

1. 检查 frontmatter `draft` 是否为 false
2. 检查 `category` 是否为已有分类(未注册的分类文章会出现在列表,
   但导航下拉/分类页看不到 → 用 `get_docs.py -C` 注册)
3. 检查 `publishDate` 是否为未来日期(列表按日期排序)
4. 检查目录结构:`src/content/blogs/{slug}/index.md`(必须是 index.md)

## 14.13 图片不显示

- `public/` 路径引用:`/images/xxx.png`(带前导斜杠)
- `src/assets/` 引用:`import` 后使用
- 文件名大小写敏感,Linux 上 `X.png` 和 `x.png` 是不同文件
- 图片过大时用压缩工具,加载慢

## 14.14 邮箱/链接等个人信息错误

统一在 `src/site.config.ts` 修改(见 5.1.1):
- 邮箱:`personal.email`
- 社交:`footer.social`
- 域名:`personal.domains.main`
- 头像:`logo.src`(图片放 `src/assets/`)

## 14.15 FastGithub 连不上

```bash
# 验证代理
curl -I -x http://127.0.0.1:38457 https://github.com
# 没反应则重启 FastGithub 程序,再试
```

---

# 15. 安全与备份

## 15.1 凭据安全

- **绝不要把 token/密码写进代码或提交**。`.gitignore` 已忽略 `.env`
- gh 登录 token 存在系统 keyring,不外泄
- 邮箱等公开信息放在 `site.config.ts` 属正常(博客本来公开)

## 15.2 备份策略

| 层级 | 频率 | 方式 |
| --- | --- | --- |
| 源码 | 每次提交 | GitHub source 分支(异地备份) |
| 构建产物 | 每次部署 | GitHub main 分支 |
| 本地 | 每季度 | 打包压缩存档 |
| 图片/附件 | 随文章 | 文章目录内或 public/images |

```bash
# 本地手动备份(可选)
tar -czf blog-backup-$(date +%Y%m%d).tar.gz --exclude=node_modules --exclude=dist --exclude=.astro --exclude=.git .
```

## 15.3 恢复流程

```bash
# 源码丢失 → 从 GitHub 恢复
git clone https://github.com/liangbinchen2013/liangbinchen2013.github.io.git
cd liangbinchen2013.github.io
git checkout source
pnpm install
```

## 15.4 版权与许可

- 本项目使用 **MIT 协议**,`LICENSE` 文件包含原作者版权声明,**必须保留**
  (MIT 协议要求保留版权声明,否则违约)
- 页脚保留了主题署名链接(开源约定),不建议删除
- 文章内容版权归作者所有,转载需注明出处

---# 16. 自定义开发指南(进阶)

> 面向想要深度修改博客的开发者。请先通读第 4、5 章。

## 16.1 开发环境

```bash
source ~/miniconda3/bin/activate
pnpm dev                      # http://localhost:4321
pnpm dev:check                # 类型检查实时 + 开发服务器
```

改代码后 dev 自动热更新;改 `astro.config.mjs` 等配置文件后需要重启。

## 16.2 修改主题色

文件:`tailwind.config.mjs`

```js
colors: {
  primary: {
    DEFAULT: 'rgb(14 165 233)',   // 亮色主色(天蓝)
    dark: 'rgb(56 189 248)',      // 暗色主色
  },
  // ...
}
```

改完刷新即生效。全站按钮、链接、强调色都是 primary。

## 16.3 修改导航栏

文件:`src/site.config.ts` → `header.menu`

```ts
menu: [
  { title: '文章', titleEn: 'Articles', link: '/article' },
  { title: '学术', titleEn: 'Academic', link: '/academic' },
  // 加一个:
  { title: '留言', titleEn: 'Guestbook', link: '/guestbook' },
]
```

样式修改:组件 `src/components/basic/Header.astro`。

## 16.4 修改首页布局

文件:`src/pages/index.astro`
主要区块:
- 个人卡片(头像、名字、简介、社交)
- 一言(quote 配置见 5.1.2)
- 最新文章列表
- 分类统计

## 16.5 修改文章页布局

文件:
- 布局:`src/layouts/ArticleLayout.astro`
- 内容渲染:`src/components/pages/` 下文章相关组件
- 上一篇/下一篇、目录、评论开关都在这里控制

## 16.6 新增自定义组件

以「加一个音乐卡片组件」为例:

1. 创建 `src/components/user/MusicCard.astro`:

```astro
---
interface Props {
  title: string
  artist: string
  link?: string
}
const { title, artist, link } = Astro.props
---
<a {href={link}} class='block rounded-xl border border-border bg-card p-4 hover:shadow-md transition-all'>
  <p class='font-medium text-foreground'>{title}</p>
  <p class='text-sm text-muted-foreground'>{artist}</p>
</a>
```

2. 在 `src/components/user/index.ts` 导出:

```ts
export { default as MusicCard } from './MusicCard.astro'
```

3. 文章里使用:

```astro
---
import { MusicCard } from '@/components/user'
---
<MusicCard title='晴天' artist='周杰伦' link='https://...' />
```

4. `pnpm check` 验证

## 16.7 新增 remark 插件(处理 Markdown)

在 `src/plugins/` 下建 `remark-xxx.ts`,然后:

```ts
// astro.config.mjs
import { remarkXxx } from './src/plugins/remark-xxx.ts'
export default defineConfig({
  markdown: {
    remarkPlugins: [remarkXxx, ...]
  }
})
```

## 16.8 多语言(i18n)

- 默认语言:`zh`,由 `astro.config.mjs` 的 `i18n` 配置
- 英文页面放在 `src/pages/en/` 下
- 英文文章通过 `getBlogCollectionEn()` 获取
- 导航菜单的中英文名称分别写在 `header.menu` 的 `title` 和 `titleEn`

## 16.9 评论系统(Waline)启用

当前 `integ.waline.enable: false`。启用步骤:
1. 部署一个 Waline 服务端(参考 waline.js.org)
2. `src/site.config.ts` 里:

```ts
waline: {
  enable: true,
  server: 'https://你的waline地址',
  emoji: ['bmoji', 'weibo', 'qq'],
}
```

3. 重新构建部署。文章 frontmatter 的 `comment: false` 可单篇关闭。

## 16.10 代码规范

- 运行 `pnpm run quality` 统一格式与 lint
- 提交前跑 `pnpm check`
- 组件用 PascalCase 命名文件,函数/变量 camelCase
- 页面文件全部小写(路由 URL 大小写敏感)

---

# 17. 性能优化

## 17.1 现状与基准

静态站已经很快(HTML 预渲染)。主要优化点:图片、字体、JS 体积。

## 17.2 图片优化

- 大图转 WebP/AVIF,压缩到合适尺寸
- 封面图放 `public/images/`,用 `loading="lazy"`(文章页已内置)
- 不要用超高清大图做头像/Logo

## 17.3 字体

- `public/fonts/` 里按需保留字体子集
- 少用中文字体全量文件(几 MB),用系统字体栈或子集化

## 17.4 构建分析(可视化打包体积)

`astro.config.mjs` 里已注释 `visualizer` 插件,取消注释后:

```bash
pnpm build
# 构建后生成 stats.html,用浏览器打开查看体积分布
```

## 17.5 首屏加载

- 首页图片(头像)用小尺寸
- 社交图标用 simple-icons(SVG,体积小)
- 需要时给组件加 `client:load` / `client:visible` 指令控制水合时机

## 17.6 Pagefind 索引

- 搜索索引构建时生成,页面多时构建慢但索引本身有压缩
- 不需要搜索可设 `integ.pagefind: false`(不推荐,搜索是特色功能)

---

# 18. 命令速查总表 ★★★

> 打印出来贴显示器前。所有命令在项目根目录执行,前提 `source ~/miniconda3/bin/activate`。

## 18.1 日常高频

| 场景 | 命令 |
| --- | --- |
| 创建文章 | `python3 get_docs.py -D 文章.md` |
| 新增分类 | `python3 get_docs.py -C slug` |
| 文章列表 | `python3 tools.py article list` |
| 编辑文章 | `python3 tools.py article edit <slug>` |
| 删除文章 | `python3 tools.py article delete <slug>` |
| 本地预览 | `pnpm dev` |
| 类型检查 | `pnpm check` |
| 提交+推送源码 | `python3 tools.py git sync "feat: ..."` |
| 构建+发布 | `python3 tools.py deploy` |

## 18.2 Git

| 场景 | 命令 |
| --- | --- |
| 看状态 | `git status --short` |
| 全部提交 | `git add -A && git commit -m "信息"` |
| 推 source | `git push origin source` |
| 看历史 | `git log --oneline -10` |
| 撤销未提交改动 | `git restore .` |
| 回滚已推送提交 | `git revert <hash>` |
| 看 diff | `git diff` |
| 暂存改动 | `git stash` / `git stash pop` |

## 18.3 pnpm

| 场景 | 命令 |
| --- | --- |
| 安装依赖 | `pnpm install` |
| 开发服务器 | `pnpm dev` |
| 构建 | `pnpm run build:github` |
| 检查 | `pnpm check` |
| 清理 | `pnpm clean` |
| 加依赖 | `pnpm add 包名` / `pnpm add -D 包名` |
| 看过期 | `pnpm outdated` |

## 18.4 网络(联网操作前)

```bash
export HTTPS_PROXY=http://127.0.0.1:38457
export HTTP_PROXY=http://127.0.0.1:38457
export ALL_PROXY=http://127.0.0.1:38457
```

## 18.5 验证线上状态

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://blog.lbcoj.top        # 200
curl -s https://blog.lbcoj.top/rss.xml | head -5                       # RSS
curl -s -o /dev/null -w "%{http_code}\n" https://blog.lbcoj.top/article  # 文章页
gh api repos/liangbinchen2013/liangbinchen2013.github.io/commits/main -q '.commit.message'  # main 最新部署
```

---

# 19. 附录:主题架构解析

> 了解「青风主题」如何工作,方便深度定制。

## 19.1 构建链路

```
源码(.astro/.md)
   │  Astro 编译(读取 src/pages 路由 + src/content 内容)
   ▼
静态 HTML/CSS/JS(dist/)
   │  Pagefind 索引 + sitemap + RSS
   ▼
GitHub Pages 服务(main 分支)
```

## 19.2 数据流

```
src/content/blogs/*/index.md
        │  getBlogCollection() (src/server.ts)
        ▼
页面组件(Article 卡片、列表、分页)
        │  site.config.ts 配置(标题、导航、社交)
        ▼
布局渲染(BaseLayout → CommonPage/ArticleLayout)
        ▼
HTML
```

## 19.3 关键模块职责

| 模块 | 职责 |
| --- | --- |
| `src/axi-integration.ts` | 汇总配置、注入 remark/rehype 插件、处理导航 |
| `src/server.ts` | 内容集合查询层(唯一数据入口) |
| `src/schemas/*` | 所有配置与内容的 Zod 校验 |
| `src/plugins/luogu-blocks.ts` | 洛谷题目块:编译为题目卡片 |
| `src/plugins/shiki-transformers.ts` | 代码块增强:复制/标题/行高亮/diff |
| `src/components/pages/*` | 文章卡片、分页、内容容器 |
| `src/components/basic/Header.astro` | 导航 + 分类下拉(与分类文件联动) |

## 19.4 常见定制入口速查

| 想改什么 | 改哪里 |
| --- | --- |
| 站点标题/描述 | `site.config.ts` theme |
| 导航菜单 | `site.config.ts` header.menu |
| 每页文章数 | `site.config.ts` content.blogPageSize |
| 主题色 | `tailwind.config.mjs` |
| 分类 | `get_docs.py -C` 或 5 个文件 |
| 文章排序 | `src/server.ts` sortMDByDate |
| 代码高亮主题 | `astro.config.mjs` markdown.shikiConfig |
| 页脚内容 | `src/components/basic/Footer.astro` |
| 评论开关 | `site.config.ts` integ.waline + 文章 comment |
| 站点图标 | `public/favicon/` |

## 19.5 版本升级(主题上游)

本项目 fork 自 `rusin-dev/astro-theme-cyanwind`(MIT)。
如需升级主题,谨慎操作(我们已深度定制,直接拉上游会冲突):

```bash
git remote add upstream https://github.com/rusin-dev/astro-theme-cyanwind.git
git fetch upstream
# 查看差异
git diff HEAD upstream/main --stat
# 挑选需要的文件手动合并(推荐)或直接 merge
```

**升级前必做**:完整备份 + 阅读上游 changelog + 升级后 `pnpm run quality` 全量回归。

---

# 附录 A:脚本速记

## get_docs.py

| 命令 | 功能 |
| --- | --- |
| `python3 get_docs.py -D <md>` | 创建文章(自动获取今天的日期作发布日期) |
| `python3 get_docs.py -C <slug>` | 新增分类(自动同步 5 个文件) |
| `python3 get_docs.py -h` | 帮助 |

## tools.py

| 命令 | 功能 |
| --- | --- |
| `article list/create/edit/delete/rename` | 文章管理 |
| `category list/add` | 分类管理 |
| `tag list` | 标签统计 |
| `page show/edit` | 页面管理 |
| `dev/check/build/preview/clean` | 开发构建 |
| `deploy` | 一键发布上线 |
| `git status/commit/push/sync/log` | Git 快捷 |
| `doc` | 文档路径 |

# 附录 B:环境变量速记

| 变量 | 值 | 用途 |
| --- | --- | --- |
| `HTTPS_PROXY` | `http://127.0.0.1:38457` | GitHub 访问代理 |
| `HTTP_PROXY` | `http://127.0.0.1:38457` | GitHub 访问代理 |
| `ALL_PROXY` | `http://127.0.0.1:38457` | GitHub 访问代理 |
| `DEPLOYMENT_PLATFORM` | `github` | 构建平台选择(构建时) |
| `EDITOR` | `nano`/`vim` | tools.py 打开编辑器的选择 |

# 附录 C:版本历史(本项目)

| 提交 | 说明 |
| --- | --- |
| `168c58c` | 初始化:博客源码(MIT 协议) |
| `81b55b9` | 移除原作者 fork 同步工作流 |
| `9e597e4` | 新增 get_docs.py 文章/分类管理脚本 |
| `1dfd7de` | 移除友情链接功能 |
| 后续... | 见 `git log --oneline` |

---

> 本文档由维护者编写,建议随项目演进持续更新。
> 如有新的维护经验,直接补充对应章节并提交。
> 最后更新:2026-08-19# 附录 D:Git 场景演练(完整示例)

> 以下场景全部用「复制粘贴」的完整命令演示,新手可直接照做。

## D1 第一次在新电脑上发布文章

```bash
# 1. 激活环境
source ~/miniconda3/bin/activate

# 2. 设置代理
export HTTPS_PROXY=http://127.0.0.1:38457
export HTTP_PROXY=http://127.0.0.1:38457
export ALL_PROXY=http://127.0.0.1:38457

# 3. 克隆仓库并切到源码分支
git clone https://github.com/liangbinchen2013/liangbinchen2013.github.io.git
cd liangbinchen2013.github.io
git checkout source

# 4. 关闭证书校验(代理必需)
git config http.sslVerify false

# 5. 安装依赖
pnpm install

# 6. 写文章(正文文件先准备好)
python3 get_docs.py -D 我的文章.md

# 7. 预览确认
pnpm check
pnpm dev

# 8. 提交推送
git add -A
git commit -m "feat: 新增文章 我的文章"
git push origin source

# 9. 发布
python3 tools.py deploy
```

## D2 误删了文章,但已经提交过

```bash
# 场景:本地把 src/content/blogs/xxx 整个删了,还没提交
git restore src/content/blogs/xxx        # 恢复被删的目录

# 场景:删了且提交了,但还没推送
git reset --hard HEAD~1                  # 回滚提交,文件回来

# 场景:删了、提交了、推送了
# 找到删除前那次提交的 hash
git log --oneline
git revert <hash>                        # 反向提交恢复
git push origin source
```

## D3 想临时保存没写完的文章去干别的

```bash
git stash                                # 保存所有未提交改动
# ...干别的事...
git stash pop                            # 恢复继续写
```

## D4 写错了提交信息

```bash
git commit --amend -m "正确的信息"
git push origin source --force-with-lease    # 已推送时用(比 -f 安全)
```

## D5 main 分支被误改,恢复部署

```bash
# 直接重新部署覆盖即可
python3 tools.py deploy
```

## D6 检查线上是否已更新

```bash
gh api repos/liangbinchen2013/liangbinchen2013.github.io/commits/main \
  -q '.commit.message'                    # 看 main 最新提交
curl -s -o /dev/null -w "%{http_code}\n" https://blog.lbcoj.top/article/你的slug
```

---

# 附录 E:pnpm 深层机制

## E1 pnpm 的工作原理

- pnpm 用**全局内容寻址存储(hard links)**:同一版本的包全机器只存一份
- `node_modules` 里是指向 store 的硬链接,所以磁盘占用小、安装快
- **不要直接修改 node_modules 里的文件**:改的是硬链接,重启安装后丢失
- 这是 pnpm 与 npm 最大的区别(npm 每个项目都复制一份)

## E2 锁文件 pnpm-lock.yaml

- 记录每个依赖的精确版本与哈希
- 只要 lock 文件不变,任何机器 `pnpm install` 结果一致
- **升级依赖后 lock 会变**,务必把 lock 文件一起提交
- 若 lock 与 package.json 不一致,`pnpm install` 会提示并自动修复

## E3 常见坑

| 现象 | 原因 | 解决 |
| --- | --- | --- |
| `ERR_PNPM_LOCKFILE_CONFIG_MISMATCH` | lock 与配置不符 | `pnpm install` 重新生成 |
| 构建找不到某包 | 依赖没装全 | `pnpm install` |
| 版本冲突 | 多个包依赖不同版本 | `pnpm list` 排查,必要时 `pnpm overrides` |
| 安装极慢 | 网络 | 换 npmmirror 镜像 |

## E4 pnpm overrides 示例

package.json 里已有:

```json
"overrides": {
  "@emmetio/css-parser": "0.5.0"
}
```

当某个间接依赖版本有问题时,可用 overrides 强制指定版本。

---

# 附录 F:文章写作模板

> 新建文章时直接复制这个模板(也可以让 get_docs.py 生成)。

## F1 标准技术文章

```markdown
---
title: "文章标题"
description: "一句话描述(160字内)"
publishDate: 2026-08-19
tags: [教程, astro]
category: "tech"
draft: false
---

## 引言

背景与目的。

## 正文第一部分

内容。

## 总结

要点回顾。
```

## F2 题解文章

```markdown
---
title: "P1001 A+B Problem 题解"
description: "经典入门题 A+B 问题的完整题解"
publishDate: 2026-08-19
tags: [题解, 算法]
category: "solution"
draft: false
---

:::luogu P1001
A + B Problem:输入两个整数,输出它们的和。
:::

## 题目分析

简单模拟即可。

## 参考代码

```cpp
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}
```
```

## F3 生活随笔

```markdown
---
title: "最近的一点感想"
description: "记录最近的生活与思考"
publishDate: 2026-08-19
tags: [生活]
category: "life"
draft: false
---

最近发生的一些事……
```

---

# 附录 G:frontmatter 完整字段参考表

| 字段 | 类型 | 必填 | 限制 | 说明 |
| --- | --- | --- | --- | --- |
| `title` | string | 是 | ≤60 字符 | 文章标题 |
| `description` | string | 是 | ≤160 字符 | 摘要/SEO 描述 |
| `publishDate` | date | 是 | YYYY-MM-DD | 发布日期 |
| `updatedDate` | date | 否 | YYYY-MM-DD | 更新日期 |
| `heroImage` | string | 否 | 路径 | 封面图 |
| `tags` | string[] | 否 | — | 标签数组 |
| `category` | string | 否 | 已注册 slug | 分类 |
| `language` | string | 否 | zh/en | 语言 |
| `draft` | boolean | 否 | true/false | 草稿开关 |
| `comment` | boolean | 否 | true/false | 评论区开关 |
| `pixivLink` | string | 否 | URL | Pixiv 链接 |

---

# 附录 H:部署日志解读

## H1 成功构建日志特征

```
[check] ... passed          ← 类型检查通过
[build] 31 page(s) built in 9.59s   ← 页面数 + 耗时
[build] Complete!           ← 构建完成
[output-copier] ... ENOENT  ← 可无视(见 14.1)
```

## H2 失败构建日志特征

```
[check] Error: ...          ← 类型/schema 错误,看具体文件
[ERROR] [vite] ...          ← 编译错误,看文件路径
invalid-content-entry-data ← 文章 frontmatter 问题(见 14.4)
ELIFECYCLE Command failed with exit code 1  ← 构建失败
```

**通用排查顺序:**
1. 先读**报错第一行**的文件路径
2. 打开该文件对照 schema/语法检查
3. `pnpm check` 单独跑一遍确认
4. 修好重新 build

---

# 附录 I:文件命名与规范约定

| 类别 | 规范 | 示例 |
| --- | --- | --- |
| 文章目录(slug) | 小写字母+数字+连字符 | `my-first-post` |
| 分类 slug | 小写字母+数字+连字符 | `tech`、`solution` |
| 页面文件 | 小写 | `index.astro` |
| 组件文件 | PascalCase | `ArticleCard.astro` |
| 图片资源 | 小写+连字符 | `cover-image.png` |
| 提交信息 | 前缀+冒号+描述 | `feat: 新增文章 xxx` |
| 分支名 | 语义化 | `source`、`main` |

---

# 附录 J:常见术语表

| 术语 | 含义 |
| --- | --- |
| slug | 文章 URL 中的英文标识(目录名) |
| frontmatter | 文章开头的 `---` 元信息区 |
| 分类(category) | 文章归档维度,需注册 |
| 标签(tags) | 文章关键词,自动聚合 |
| 分支(branch) | Git 并行开发线 |
| 提交(commit) | Git 保存的一次快照 |
| 推送(push) | 本地提交上传到远端 |
| 拉取(pull) | 远端更新同步到本地 |
| 构建(build) | 把源码编译成静态站点 |
| 部署(deploy) | 把构建产物发布上线 |
| Pagefind | 本地全文搜索引擎 |
| SSG | Static Site Generation 静态站点生成 |
| SSG/SSR | 静态渲染/服务端渲染(本项目全静态) |
| i18n | 国际化(多语言) |
| CNAME | DNS 别名记录(域名指向) |

---

> 全文完。维护好这份文档,博客就会一直健康运行。
> 有问题先查本文档第 14 章,再不行看构建报错,最后可以找我(维护脚本)帮忙分析。
> 祝写作愉快!# 附录 K:常见任务完整操作步骤(照做版)

## K1 把一篇「洛谷题解」发布上线

```bash
# 1. 准备正文(纯 md,不含 frontmatter)
#    /tmp/p1001.md 内容:题目分析、参考代码等

# 2. 生成文章
python3 get_docs.py -D /tmp/p1001.md
#    标题: P1001 A+B Problem 题解
#    描述: 经典入门题 A+B 的完整题解
#    标签: 题解, 算法, 入门
#    分类: solution
#    URL:  p1001-a-b-problem

# 3. 检查渲染
pnpm check
pnpm dev   # 打开 http://localhost:4321/article/p1001-a-b-problem

# 4. 提交推送
python3 tools.py git sync "feat: 新增题解 P1001"

# 5. 发布
python3 tools.py deploy

# 6. 验证
curl -s -o /dev/null -w "%{http_code}\n" https://blog.lbcoj.top/article/p1001-a-b-problem
# 期望输出 200
```

## K2 修改博客标题

```bash
# 1. 打开配置
nano src/site.config.ts
# 改:theme.title = "新标题"
#     theme.titleEn = "New Title"
#     theme.description / description_en 一起改

# 2. 验证 + 发布
python3 tools.py check   # 或 pnpm check
python3 tools.py git sync "feat: 修改博客标题"
python3 tools.py deploy
```

## K3 添加一个社交链接(如 Bilibili)

```bash
# 1. 打开 site.config.ts,footer.social 里加:
#    bilibili: 'https://space.bilibili.com/你的ID'
#    注意:页脚渲染组件只认识已支持的 key(github/luogu 等),
#    不认识的 key 需要同步修改 src/components/basic/Footer.astro 的渲染逻辑

# 2. 若 Footer 组件里没有对应分支,手动加:
#    查看 Footer.astro 里 social 的渲染代码,仿照 github 的写法加一行

# 3. 检查 + 提交 + 发布
pnpm check
python3 tools.py git sync "feat: 页脚添加 Bilibili 链接"
python3 tools.py deploy
```

## K4 给文章添加封面图

```bash
# 1. 图片放入 public/images/
#    cp cover.png public/images/my-post-cover.png

# 2. 编辑文章 frontmatter 加一行:
#    heroImage: "/images/my-post-cover.png"

# 3. 检查发布
pnpm check && python3 tools.py git sync "feat: 更新封面" && python3 tools.py deploy
```

## K5 修改每页文章数量

```bash
nano src/site.config.ts
# content.blogPageSize: 15 改成 10
python3 tools.py git sync "feat: 每页显示 10 篇文章"
python3 tools.py deploy
```

## K6 重新生成 favicon

```bash
# 用 Pillow(conda 里已装)生成:
python3 -c "
from PIL import Image
img = Image.open('src/assets/278105203.png').convert('RGBA').resize((256, 256))
img.save('public/favicon/favicon-256x256.png')
img.resize((16, 16)).save('public/favicon/favicon.ico')
img.resize((32, 32)).save('public/favicon/favicon-32x32.png')
print('favicon 已更新')
"
python3 tools.py git sync "chore: 更新站点图标"
python3 tools.py deploy
```

## K7 迁移到新电脑(完整版)

```bash
# 新电脑上:
# 1. 安装:miniconda、node、pnpm、git、gh、FastGithub
# 2. 配置 git 身份
git config --global user.name "liangbinchen2013"
git config --global user.email "liangbinchen2013@outlook.com"
# 3. 登录 gh
gh auth login
# 4. 克隆 + 切分支 + 装依赖(见 D1)
# 5. 写个测试文章验证全链路
python3 get_docs.py -D 测试.md   # 然后删除测试文章
python3 tools.py deploy          # 确认能发布
```

## K8 停用/恢复搜索

```bash
# 停用:site.config.ts 里 pagefind: false
# 恢复:pagefind: true
# 然后正常 检查→提交→发布
```

## K9 修改暗色模式主色

```bash
nano tailwind.config.mjs
# 找到 dark 相关颜色,改 primary.dark 等
pnpm dev   # 打开 / 页面切暗色模式预览
python3 tools.py git sync "style: 调整暗色主题色"
python3 tools.py deploy
```

## K10 一键全站质检

```bash
pnpm run quality    # lint + sync + check + format
# 有报错就修,修完再跑一遍直到通过
```

---

# 附录 L:Markdown 语法速查卡

| 语法 | 效果 |
| --- | --- |
| `# 标题` | 一级标题 |
| `## 标题` / `###` / `####` | 二/三/四级标题 |
| `**粗体**` | 粗体 |
| `*斜体*` | 斜体 |
| `~~删除线~~` | 删除线 |
| `` `代码` `` | 行内代码 |
| `> 引用` | 引用块 |
| `- 项` / `1. 项` | 列表 |
| `[文字](URL)` | 链接 |
| `![alt](图片URL)` | 图片 |
| `\| 表 \| 格 \|` | 表格 |
| `$公式$` / `$$公式$$` | 数学公式 |
| `---` | 分隔线 |
| `- [ ] 任务` | 待办 |
| `:::luogu P1001` | 洛谷题目卡片 |
| `<Tabs>` / `<Spoiler>` | 主题组件(见 8.5) |

---

# 附录 M:常见错误信息速查

| 报错(关键词) | 含义 | 处理 |
| --- | --- | --- |
| `invalid-content-entry-data` | 文章 frontmatter 不合法 | 对照附录 G 检查 |
| `SSL certificate problem` | 证书问题 | `git config http.sslVerify false` |
| `refusing to allow an OAuth App` | token 无 workflow 权限 | 重新 gh 授权 |
| `ENOENT ... dist/client` | Vercel 插件噪音 | 无视 |
| `ELIFECYCLE Command failed` | 构建失败 | 看上面具体错误 |
| `Command "pnpm" not found` | 环境没激活 | `source ~/miniconda3/bin/activate` |
| `Failed to connect to github.com` | 代理没开 | 检查 FastGithub 与代理变量 |
| `remote rejected` | 远端拒绝 | 通常要 -f 或权限问题,谨慎处理 |
| `CONFLICT` | 合并冲突 | 见 6.16 |
| `Port 4321 is already in use` | dev 端口占用 | `pnpm dev:stop` 或换端口 |
| `ENOENT ... node_modules` | 依赖缺失 | `pnpm install` |
| `Astro: Failed to load ...` | 配置文件语法错 | 检查 `pnpm check` 输出 |

---

> 本手册至此结束。维护时先查速查表,再看详细章节。
> 祝博客长长久久、越写越好!
# 附录 N:发布前最终检查清单(3 秒版)

每次发布前心里过一遍:

- [ ] 文章能打开(本地 dev 预览过)
- [ ] `pnpm check` 通过
- [ ] frontmatter 无超长字段(title<=60 / description<=160)
- [ ] 标签大小写统一
- [ ] 分类是已注册的 slug
- [ ] 源码已提交:`python3 tools.py git sync "feat: ..."`
- [ ] 已发布:`python3 tools.py deploy`
- [ ] 线上可访问:`curl -s -o /dev/null -w "%{http_code}" https://blog.lbcoj.top` 输出 200
- [ ] 新文章地址直达无 404

全部打勾 = 发布成功,收工。

# 附录 O:维护者备忘

## 本博客关键事实速记

| 事项 | 值 |
| --- | --- |
| 站点地址 | https://blog.lbcoj.top |
| 源码分支 | source |
| 部署分支 | main |
| 作者 | LBC |
| 邮箱 | liangbinchen2013@outlook.com |
| GitHub | liangbinchen2013 |
| 洛谷 | https://www.luogu.com.cn/user/1432496 |
| 头像文件 | src/assets/278105203.png |
| 每页文章数 | 15 |
| 分类 | tech / life / solution |
| 评论系统 | Waline(当前关闭) |
| 搜索 | Pagefind(构建时索引) |
| 主题协议 | MIT(保留原版权声明) |
| 构建命令 | DEPLOYMENT_PLATFORM=github pnpm run build:github |
| 部署命令 | python3 tools.py deploy |

## 环境速记

| 事项 | 值 |
| --- | --- |
| Python 环境 | source ~/miniconda3/bin/activate |
| FastGithub 代理 | http://127.0.0.1:38457 |
| git 证书 | git config http.sslVerify false |
| Node | 26.5.1 |
| pnpm | 11.x |
| 项目目录 | /home/user/Desktop/astro-theme-cyanwind-main |

## 已知噪音(无需处理)

1. 构建时 `output-copier` 的 ENOENT 报错 → Vercel 插件,无视
2. 构建会清空 dist 并重建 .git → deploy 流程设计如此,正常
3. main 分支每次部署都是全新历史 → 所以必须 `git push -f`,正常
4. 本地根目录出现的 dist/.astro/.vercel → 构建产物,gitignore 已忽略

---

（完）

# 附录 P:内容发布规范(个人约定)

## P1 文章命名建议

- 题解类:`P{题号}-{题目名}-题解`(如 `p1001-a-b-problem`)
- 教程类:小写连字符,如 `astro-blog-tutorial`
- 随笔类:日期+主题,如 `2026-08-19-summer-memories`
- 一律小写字母、数字、连字符,不用中文、下划线、空格

## P2 图片管理规范

- 文章配图放 `public/images/`,文件名小写连字符
- 封面尺寸建议 1200x630(社交分享比例)
- 上传前压缩(可用在线工具或 `python3 -c` 用 Pillow 压缩)

## P3 标签白名单建议

```
astro 博客 教程 算法 数据结构 题解 数学 生活 随笔 评测 工具 网站 前端 后端 竞赛
```

新标签可以加,但注意与已有标签区分,避免近义重复(如「算法」和「算法竞赛」)。

## P4 分类使用场景

| 分类 | 用途 |
| --- | --- |
| tech | 技术教程、工具分享、网站建设 |
| life | 生活记录、随笔感想 |
| solution | 洛谷/算法竞赛题解 |
| (新分类) | 按需用 get_docs.py -C 注册 |

## P5 更新频率建议

- 保持稳定节奏(周更或月更),利于读者习惯
- 题解类写完尽快发,算法热度不过夜
- 修 bug、改样式可顺手提交,不必攒批

## P6 质量自查

发布前通读一遍文章:
1. 标题与内容相符
2. 代码块语法正确、可复制运行
3. 图片路径有效
4. 无错别字、无未完成的 TODO 段落
5. 公式渲染正常(如有)

---

# 附录 Q:给未来自己的十句话

1. 先 `source ~/miniconda3/bin/activate`,再谈其他。
2. 动 GitHub 之前,先 export 三个代理变量。
3. 写文章用 `get_docs.py -D`,别手搓 frontmatter。
4. 发布用 `tools.py deploy`,别手动碰 main 分支。
5. 提交信息带上类型前缀:feat/fix/chore/docs。
6. 改配置后跑 `pnpm check`,改 schema 后跑 `pnpm sync`。
7. 构建报错先看第一行,99% 是 frontmatter 问题。
8. ENOENT 是噪音,无视它;Complete! 才是胜利。
9. LICENSE 和页脚署名不要删,那是别人的心血和你的信用。
10. 备份:GitHub 就是最好的备份,勤提交、勤推送。

---

（全文完）
