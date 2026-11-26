#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""摘抄校验：检查技能产物里有没有大段搬用源文档的原句。

为什么需要它：本包对源素材的承诺是「只提炼结构，不搬原句」。但这条一直是口头纪律，
没有校验动作——靠人读一遍，读不出来。LLM 自评更不行（让它判自己有没有抄，答案永远是没抄）。
所以用机器做字符级 n-gram 比对，只回答一个可复核的问题：
目标文件里有多少个连续片段，在源文档里一字不差地出现过。

用法:
    python check_quote.py 目标 对照语料 [更多语料...] [--n 8] [--run 30] [--allow R] [--top 3]

目标可以是单个文件或目录；对照语料可给多个目录/文件。

结构区分（关键）:
    卡片按 RIA 结构写，`## R — 原文` 段本来就是引用源文档，**该段命中不算抄**。
    真正该管的是 I / A1 / A2 / E / B 段——这些是提炼出来的，出现长串照搬就是没提炼。
    所以脚本按 `## ` 切段分别比对，只对非 R 段告警，并把命中落在哪一段直接标出来。

判定（默认阈值）:
    - 非 R 段任一处连续命中 ≥ 30 字  → 告警，需改写
    - 非 R 段重合率 > 20%            → 告警，整段太依赖原文
    两者都未触发 → 通过

设计取舍:
    - 以「字符」为 n-gram 单位，不做分词。中文不需要分词器，且分词错误会掩盖重合。
    - 只比对中文字符，英文与数字剔除（表格拼贴会产生伪长串，见下方注释）。
    - 词表与原句示例用 `<!-- exempt-start 理由 -->…<!-- exempt-end -->` 显式豁免；
      豁免必须写理由，脚本不认「无理由的静默跳过」。
    - 比对前去掉标点、空白与 markdown 标记，所以统计出的连续长度比原文略长（标点不计入）。
      偏保守：宁可多报，不漏报。
    - 脚本不自动判定「违规」，只给出位置与长度。引用一句短语作例证是允许的，判断留给人。
"""

import argparse
import os
import re
import sys

# 白名单：只保留中文字符。英文与数字一并去掉——原因见下方「为什么丢掉英文」。
_KEEP = re.compile(r"[^\u4e00-\u9fff]+")

# 显式豁免块：词表、原句示例这类「必须与原文档一致」的内容，用注释围起来跳过比对。
# 允许豁免，但不允许悄悄豁免——每处豁免必须在注释里写清理由，否则等于把纪律关掉。
_EXEMPT = re.compile(r"<!--\s*exempt-start[^>]*-->.*?<!--\s*exempt-end\s*-->", re.S)


def strip_exempt(text: str) -> str:
    return _EXEMPT.sub("", text)

# 为什么丢掉英文：表格与字段名（character / style / scene / 30fps）在去标点后会首尾相接，
# 拼出 "charactercharacterstyle" 这类伪长串，造成假命中。本包要查的是中文叙事段落有没有
# 被整段搬用，英文占位符名不构成「摘抄原文」，剔除后误报显著下降，中文命中不受影响。


def normalize(text: str) -> str:
    return _KEEP.sub("", text)


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def collect_files(root: str) -> list:
    if os.path.isfile(root):
        return [root]
    out = []
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn.lower().endswith((".md", ".txt")):
                out.append(os.path.join(dirpath, fn))
    return out


def split_sections(text: str) -> list:
    """按 `## ` 标题切段，返回 [(section_title, raw_text)]；首个标题前的内容记为「开头」。"""
    sections, cur_title, buf = [], "（开头）", []
    for line in text.splitlines():
        if line.startswith("## "):
            if buf:
                sections.append((cur_title, "\n".join(buf)))
            cur_title, buf = line[3:].strip(), []
        else:
            buf.append(line)
    if buf:
        sections.append((cur_title, "\n".join(buf)))
    return sections


def grams(text: str, n: int) -> list:
    return [text[i:i + n] for i in range(max(0, len(text) - n + 1))]


def longest_run(text: str, corpus_grams: set, n: int) -> tuple:
    """返回 (最长连续命中字符数, 起始下标)"""
    best, best_at = 0, -1
    start, count = None, 0
    for i in range(max(0, len(text) - n + 1)):
        if text[i:i + n] in corpus_grams:
            if start is None:
                start, count = i, 1
            else:
                count += 1
            length = n + count - 1
            if length > best:
                best, best_at = length, start
        else:
            start, count = None, 0
    return best, best_at


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("corpus", nargs="+")
    ap.add_argument("--n", type=int, default=8, help="n-gram 长度（字符），默认 8")
    ap.add_argument("--run", type=int, default=30, help="非引用段单处连续命中阈值（字），默认 30")
    ap.add_argument("--ratio", type=float, default=0.20, help="非引用段重合率阈值，默认 0.20")
    ap.add_argument("--allow", default="R", help="允许引用的段落前缀，默认 R；传空串则全段都查")
    ap.add_argument("--top", type=int, default=3, help="每份文件最多列几处命中")
    args = ap.parse_args()

    targets = collect_files(args.target)
    corpus_files = []
    for c in args.corpus:
        corpus_files.extend(collect_files(c))
    if not targets or not corpus_files:
        print("目标或语料为空")
        return 2

    corpus_grams = set()
    corpus_chars = 0
    for p in corpus_files:
        t = normalize(read_text(p))
        corpus_chars += len(t)
        corpus_grams.update(grams(t, args.n))

    print(f"对照语料：{len(corpus_files)} 个文件 / {corpus_chars} 字 / {len(corpus_grams)} 个 {args.n}-gram")
    print(f"目标：{len(targets)} 个文件 / 允许引用段：{args.allow or '（无）'}")
    print("")
    print("文件 | 非引用段字数 | 重合率 | 最长连续(段) | 判定")
    print("-" * 78)

    flagged = []
    for p in targets:
        sections = split_sections(strip_exempt(read_text(p)))
        free_chars = free_hits = free_grams = 0
        worst = (0, -1, "")
        for title, raw in sections:
            norm = normalize(raw)
            if not norm:
                continue
            if args.allow and title.startswith(args.allow):
                continue  # R 段：引用原文属设计内，不参与判定
            gs = grams(norm, args.n)
            free_chars += len(norm)
            free_hits += sum(1 for g in gs if g in corpus_grams)
            free_grams += len(gs)
            run_len, run_at = longest_run(norm, corpus_grams, args.n)
            if run_len > worst[0]:
                worst = (run_len, run_at, title)

        ratio = (free_hits / free_grams) if free_grams else 0.0
        run_len, run_at, run_sec = worst
        flags = []
        if run_len >= args.run:
            flags.append(f"「{run_sec}」段连引 {run_len} 字")
        if ratio > args.ratio:
            flags.append(f"重合率超 {args.ratio:.0%}")
        verdict = "；".join(flags) if flags else "通过"
        print(f"{os.path.basename(p)} | {free_chars} | {ratio:.1%} | {run_len}（{run_sec or '-'}） | {verdict}")
        if flags:
            flagged.append((p, sections, run_len, run_at, run_sec, ratio))

    if flagged:
        print("\n可疑位置（脚本不判定违规，供人工改写）：")
        for p, sections, run_len, run_at, run_sec, ratio in flagged:
            print(f"\n  {p}   非引用段重合率 {ratio:.1%}")
            for title, raw in sections:
                if title != run_sec:
                    continue
                norm = normalize(raw)
                s = max(0, run_at - 10)
                e = min(len(norm), run_at + run_len + 10)
                print(f"    段「{title}」连引 {run_len} 字：…{norm[s:e]}…")
        return 1

    print("\n结果：通过（非引用段无长串搬用）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
