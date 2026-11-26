# wenlv-video-prompt

文旅短视频提示词蒸馏包：从一条参考片拆解开始，经过叙事结构选型、换城复刻、提示词装配、包装声音、合规改写与反平淡设计，产出「可直接复制去生成」的提示词包。

## 安装

把本仓库内容放到 WorkBuddy 的技能目录：

- 用户级（推荐）：`~/.workbuddy/skills/wenlv-video-prompt`
- 项目级：`<项目>/.workbuddy/skills/wenlv-video-prompt`

新开会话后可用 `@skill:wenlv-video-prompt` 调用。

## 目录结构

- `SKILL.md` — 能力入口：触发条件、七条核心原则、八条交付硬规则、能力路由表。
- `references/` — 7 张能力卡（参考片拆解、叙事结构、提示词装配、换城、合规改写、包装声音、反平淡设计），以及 `cheatsheet.md`（决策规则速查 + 烧钱前预检 18 项）、`glossary.md`、`overview.md`、`capability-index.md`。
- `resources/` — `case-index.md`（36 条反例，16 条为实测）、`check_quote.py`（不搬原句字符级 n-gram 校验脚本）。
- `BUILD_MANIFEST.json` — 技能构建清单。

## 交付规范（三件套，缺一不可）

1. `XX_提示词包_<版本>.md` — 规格文档：结构、槽位、双版本提示词、张力表、预检结果。
2. `prompts_<版本>.json` — 结构化规格：元信息、槽位表、全局前缀双版本、各生成单元双版本镜头句、负向四段式、包装与声音、校验信息。
3. `生成用_可直接复制_<版本>.md` — **真正拿去生成的那一份**：逐单元把全局前缀、主角块、镜头句、负向展开拼好，零占位符、零 `[全局前缀]` 标记，每段一个整段可复制的文本块。

落款/署名/账号角标统一为「环球数字文旅」。

## 证据纪律

结论标注 author-stated / inferred / material-defect / field-tested；用户回传的生成视频视为一次付费实测，必须完成「逐帧验收 → 回提示词找触发词 → 写成 ce 编号回写反例索引与能力卡」的闭环。
