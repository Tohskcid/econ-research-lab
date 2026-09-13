#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
經濟學門學術期刊評比 (2019年林明仁等更新版) 檢索工具
Journal Matcher CLI: Quickly verify if a journal belongs to Top 5, A+, A, or TSSCI Core.
"""

import sys
import argparse
import difflib
import json
from typing import Dict, Optional, Tuple, List

# 2019 年科技部/國科會經濟學門學術期刊評比核心資料庫
JOURNAL_DB = {
    # 1. 綜合頂尖 (The Top 5)
    "american economic review": {"tier": "Top 5", "short": "AER", "subfield": "General", "rank_zh": "綜合頂尖"},
    "econometrica": {"tier": "Top 5", "short": "ECMA", "subfield": "General / Theory / Econometrics", "rank_zh": "綜合頂尖"},
    "journal of political economy": {"tier": "Top 5", "short": "JPE", "subfield": "General / Price Theory / Macro", "rank_zh": "綜合頂尖"},
    "quarterly journal of economics": {"tier": "Top 5", "short": "QJE", "subfield": "General Applied", "rank_zh": "綜合頂尖"},
    "review of economic studies": {"tier": "Top 5", "short": "REStud", "subfield": "General Theory / Applied", "rank_zh": "綜合頂尖"},

    # 2. 頂尖評論與綜述 (Leading Survey & Review)
    "journal of economic literature": {"tier": "Leading Survey", "short": "JEL", "subfield": "Review & Survey", "rank_zh": "頂尖評論"},
    "journal of economic perspectives": {"tier": "Leading Survey", "short": "JEP", "subfield": "Policy & Perspectives", "rank_zh": "頂尖觀點"},

    # 3. A+ 級期刊 (Top Field & High General)
    "review of economics and statistics": {"tier": "A+", "short": "REStat", "subfield": "Applied / Empirical", "rank_zh": "A+ 級"},
    "journal of the european economic association": {"tier": "A+", "short": "JEEA", "subfield": "General", "rank_zh": "A+ 級"},
    "economic journal": {"tier": "A+", "short": "EJ", "subfield": "General", "rank_zh": "A+ 級"},
    "international economic review": {"tier": "A+", "short": "IER", "subfield": "General / Theory", "rank_zh": "A+ 級"},
    "quantitative economics": {"tier": "A+", "short": "QE", "subfield": "Econometrics / Empirical", "rank_zh": "A+ 級"},
    "american economic journal: applied economics": {"tier": "A+", "short": "AEJ: Applied", "subfield": "Applied Micro", "rank_zh": "A+ 級"},
    "american economic journal: economic policy": {"tier": "A+", "short": "AEJ: Policy", "subfield": "Public Policy", "rank_zh": "A+ 級"},
    "american economic journal: macroeconomics": {"tier": "A+", "short": "AEJ: Macro", "subfield": "Macroeconomics", "rank_zh": "A+ 級"},
    "american economic journal: microeconomics": {"tier": "A+", "short": "AEJ: Micro", "subfield": "Microeconomics", "rank_zh": "A+ 級"},
    
    # 計量經濟學 A+
    "journal of econometrics": {"tier": "A+", "short": "JoE", "subfield": "Econometrics", "rank_zh": "A+ 級 (計量第一刊)"},
    "econometric theory": {"tier": "A+", "short": "ET", "subfield": "Econometric Theory", "rank_zh": "A+ 級"},
    "journal of business & economic statistics": {"tier": "A+", "short": "JBES", "subfield": "Time Series / Applied Econometrics", "rank_zh": "A+ 級"},
    "journal of applied econometrics": {"tier": "A+", "short": "JAE", "subfield": "Applied Econometrics", "rank_zh": "A+ 級"},

    # 個體理論 A+
    "journal of economic theory": {"tier": "A+", "short": "JET", "subfield": "Micro Theory", "rank_zh": "A+ 級 (個體理論第一刊)"},
    "theoretical economics": {"tier": "A+", "short": "TE", "subfield": "Economic Theory", "rank_zh": "A+ 級"},
    "games and economic behavior": {"tier": "A+", "short": "GEB", "subfield": "Game Theory", "rank_zh": "A+ 級 (賽局理論第一刊)"},

    # 總體、貨幣與金融 A+
    "journal of monetary economics": {"tier": "A+", "short": "JME", "subfield": "Macro / Monetary", "rank_zh": "A+ 級 (總體第一刊)"},
    "journal of finance": {"tier": "A+", "short": "JF", "subfield": "Finance", "rank_zh": "A+ 級 (財務金融頂尖)"},
    "journal of financial economics": {"tier": "A+", "short": "JFE", "subfield": "Finance", "rank_zh": "A+ 級 (財務金融頂尖)"},
    "review of financial studies": {"tier": "A+", "short": "RFS", "subfield": "Finance", "rank_zh": "A+ 級 (財務金融頂尖)"},

    # 各應用領域旗艦 A+
    "journal of labor economics": {"tier": "A+", "short": "JoLE", "subfield": "Labor", "rank_zh": "A+ 級 (勞動第一刊)"},
    "journal of public economics": {"tier": "A+", "short": "JPubE", "subfield": "Public", "rank_zh": "A+ 級 (公共經濟第一刊)"},
    "rand journal of economics": {"tier": "A+", "short": "RAND", "subfield": "Industrial Organization", "rank_zh": "A+ 級 (產經第一刊)"},
    "journal of development economics": {"tier": "A+", "short": "JDE", "subfield": "Development", "rank_zh": "A+ 級 (發展第一刊)"},
    "journal of international economics": {"tier": "A+", "short": "JIE", "subfield": "International Trade / Finance", "rank_zh": "A+ 級 (國貿第一刊)"},
    "journal of health economics": {"tier": "A+", "short": "JHE", "subfield": "Health", "rank_zh": "A+ 級 (健康經濟第一刊)"},
    "journal of environmental economics and management": {"tier": "A+", "short": "JEEM", "subfield": "Environmental", "rank_zh": "A+ 級 (環境第一刊)"},

    # 4. A 級期刊 (Second-Tier Field & Good General)
    "european economic review": {"tier": "A", "short": "EER", "subfield": "General", "rank_zh": "A 級"},
    "journal of economic behavior & organization": {"tier": "A", "short": "JEBO", "subfield": "Behavioral / Org", "rank_zh": "A 級"},
    "journal of human resources": {"tier": "A", "short": "JHR", "subfield": "Labor / Education", "rank_zh": "A 級"},
    "journal of economic dynamics and control": {"tier": "A", "short": "JEDC", "subfield": "Macro Dynamics / Computation", "rank_zh": "A 級"},
    "journal of urban economics": {"tier": "A", "short": "JUE", "subfield": "Urban", "rank_zh": "A 級"},
    "regional science and urban economics": {"tier": "A", "short": "RSUE", "subfield": "Regional / Urban", "rank_zh": "A 級"},
    "journal of industrial economics": {"tier": "A", "short": "JIEc", "subfield": "Industrial Organization", "rank_zh": "A 級"},
    "international journal of industrial organization": {"tier": "A", "short": "IJIO", "subfield": "Industrial Organization", "rank_zh": "A 級"},
    "energy economics": {"tier": "A", "short": "Energy Econ", "subfield": "Energy", "rank_zh": "A 級"},
    "resource and energy economics": {"tier": "A", "short": "REE", "subfield": "Resource / Energy", "rank_zh": "A 級"},
    "journal of money, credit and banking": {"tier": "A", "short": "JMCB", "subfield": "Money & Banking", "rank_zh": "A 級"},
    "journal of international money and finance": {"tier": "A", "short": "JIMF", "subfield": "Intl Finance", "rank_zh": "A 級"},
    "journal of banking & finance": {"tier": "A", "short": "JBF", "subfield": "Banking / Finance", "rank_zh": "A 級"},
    "labour economics": {"tier": "A", "short": "Labour Econ", "subfield": "Labor", "rank_zh": "A 級"},
    "economics letters": {"tier": "A", "short": "Econ Lett", "subfield": "Letters / General", "rank_zh": "A 級"},
    "economic theory": {"tier": "A", "short": "Econ Theory", "subfield": "Theory", "rank_zh": "A 級"},
    "social choice and welfare": {"tier": "A", "short": "SCW", "subfield": "Welfare Theory", "rank_zh": "A 級"},
    "journal of mathematical economics": {"tier": "A", "short": "JMEc", "subfield": "Math Econ", "rank_zh": "A 級"},
    "macroeconomic dynamics": {"tier": "A", "short": "Macro Dyn", "subfield": "Macro", "rank_zh": "A 級"},
    "world bank economic review": {"tier": "A", "short": "WBER", "subfield": "Development / Policy", "rank_zh": "A 級"},
    "oxford bulletin of economics and statistics": {"tier": "A", "short": "OBES", "subfield": "Applied Econometrics", "rank_zh": "A 級"},
    "scandinavian journal of economics": {"tier": "A", "short": "SJE", "subfield": "General", "rank_zh": "A 級"},
    "canadian journal of economics": {"tier": "A", "short": "CJE", "subfield": "General", "rank_zh": "A 級"},
    "public choice": {"tier": "A", "short": "Pub Choice", "subfield": "Political Economy", "rank_zh": "A 級"},
    "health economics": {"tier": "A", "short": "Health Econ", "subfield": "Health", "rank_zh": "A 級"},
    "economic inquiry": {"tier": "A", "short": "Econ Inq", "subfield": "General", "rank_zh": "A 級"},
    "southern economic journal": {"tier": "A", "short": "SEJ", "subfield": "General", "rank_zh": "A 級"},

    # 5. 臺灣國內 TSSCI 經濟學門第一級 / 核心期刊
    "經濟論文叢刊": {"tier": "TSSCI Core", "short": "TER", "subfield": "綜合 (台大經濟)", "rank_zh": "TSSCI 第一級核心"},
    "taiwan economic review": {"tier": "TSSCI Core", "short": "TER", "subfield": "綜合 (台大經濟)", "rank_zh": "TSSCI 第一級核心"},
    "經濟論文": {"tier": "TSSCI Core", "short": "AEP", "subfield": "實證 / 綜合 (中研院經濟所)", "rank_zh": "TSSCI 第一級核心"},
    "academia economic papers": {"tier": "TSSCI Core", "short": "AEP", "subfield": "實證 / 綜合 (中研院經濟所)", "rank_zh": "TSSCI 第一級核心"},
    "經濟研究": {"tier": "TSSCI Core", "short": "Econ Res", "subfield": "綜合 (台北大學經濟)", "rank_zh": "TSSCI 第一級核心"},
    "economic research": {"tier": "TSSCI Core", "short": "Econ Res", "subfield": "綜合 (台北大學經濟)", "rank_zh": "TSSCI 第一級核心"},
    "人文及社會科學集刊": {"tier": "TSSCI Core", "short": "JSSP", "subfield": "人社跨領域 (中研院人社中心)", "rank_zh": "TSSCI 第一級核心"},
    "journal of social sciences and philosophy": {"tier": "TSSCI Core", "short": "JSSP", "subfield": "人社跨領域 (中研院人社中心)", "rank_zh": "TSSCI 第一級核心"},
    "經濟預測與政策": {"tier": "TSSCI Core", "short": "EFP", "subfield": "總體預測與政策 (中研院經濟所)", "rank_zh": "TSSCI 第一級核心"},
    "economic forecasts and policy": {"tier": "TSSCI Core", "short": "EFP", "subfield": "總體預測與政策 (中研院經濟所)", "rank_zh": "TSSCI 第一級核心"}
}

# 建立別名查找表 (Aliases & Acronyms)
ALIAS_MAP = {
    "aer": "american economic review",
    "ecma": "econometrica",
    "jpe": "journal of political economy",
    "qje": "quarterly journal of economics",
    "restud": "review of economic studies",
    "jel": "journal of economic literature",
    "jep": "journal of economic perspectives",
    "restat": "review of economics and statistics",
    "jeea": "journal of the european economic association",
    "ej": "economic journal",
    "ier": "international economic review",
    "qe": "quantitative economics",
    "joe": "journal of econometrics",
    "et": "econometric theory",
    "jbes": "journal of business & economic statistics",
    "jae": "journal of applied econometrics",
    "jet": "journal of economic theory",
    "te": "theoretical economics",
    "geb": "games and economic behavior",
    "jme": "journal of monetary economics",
    "jf": "journal of finance",
    "jfe": "journal of financial economics",
    "rfs": "review of financial studies",
    "jole": "journal of labor economics",
    "jpube": "journal of public economics",
    "rand": "rand journal of economics",
    "jde": "journal of development economics",
    "jie": "journal of international economics",
    "jhe": "journal of health economics",
    "jeem": "journal of environmental economics and management",
    "eer": "european economic review",
    "jebo": "journal of economic behavior & organization",
    "jhr": "journal of human resources",
    "jedc": "journal of economic dynamics and control",
    "jue": "journal of urban economics",
    "rsue": "regional science and urban economics",
    "jiec": "journal of industrial economics",
    "ijio": "international journal of industrial organization",
    "jmcb": "journal of money, credit and banking",
    "jimf": "journal of international money and finance",
    "jbf": "journal of banking & finance",
    "ter": "經濟論文叢刊",
    "叢刊": "經濟論文叢刊",
    "中研院經濟論文": "經濟論文"
}

def lookup_journal(query: str) -> Tuple[Optional[str], Optional[dict], float]:
    """
    Search for a journal by exact name, alias, or fuzzy string match.
    Returns: (canonical_name, details_dict, confidence_score)
    """
    q = query.strip().lower()
    
    # 1. Alias match
    if q in ALIAS_MAP:
        canonical = ALIAS_MAP[q]
        return canonical, JOURNAL_DB.get(canonical), 1.0
    
    # 2. Exact match in DB
    if q in JOURNAL_DB:
        return q, JOURNAL_DB[q], 1.0
    
    # 3. Substring match
    for key, val in JOURNAL_DB.items():
        if q == key or q in key:
            return key, val, 0.95
        if val["short"].lower() == q:
            return key, val, 0.95
    
    # 4. Fuzzy match using difflib
    all_keys = list(JOURNAL_DB.keys())
    matches = difflib.get_close_matches(q, all_keys, n=1, cutoff=0.55)
    if matches:
        best_match = matches[0]
        ratio = difflib.SequenceMatcher(None, q, best_match).ratio()
        return best_match, JOURNAL_DB[best_match], ratio
    
    return None, None, 0.0

def main():
    parser = argparse.ArgumentParser(description="2019 Taiwan NSTC Economics Journal Ranking Lookup")
    parser.add_argument("--check", "-c", type=str, help="Journal name or acronym to check (e.g., AER, QJE, TER, JoE)")
    parser.add_argument("--list-tier", "-l", choices=["Top 5", "Leading Survey", "A+", "A", "TSSCI Core", "All"], help="List journals by tier")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if args.list_tier:
        target_tier = args.list_tier
        results = {}
        for name, data in JOURNAL_DB.items():
            if target_tier == "All" or data["tier"] == target_tier:
                results[name] = data
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"\n=== 2019 評比等級: {target_tier} 期刊清單 (共 {len(results)} 本) ===")
            for name, data in results.items():
                print(f"- [{data['tier']}] {data['short']}: {name.title()} ({data['subfield']})")
        return

    if args.check:
        name, info, score = lookup_journal(args.check)
        if args.json:
            res = {"query": args.check, "matched": name, "score": round(score, 3), "info": info}
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            if info:
                print("\n========================================================")
                print(f"查詢關鍵詞: {args.check}")
                print(f"匹配期刊:   {name.title()} (簡稱: {info['short']})")
                print(f"2019 評比:  【{info['tier']}】 ({info['rank_zh']})")
                print(f"所屬領域:   {info['subfield']}")
                print(f"匹配信心度: {round(score * 100, 1)}%")
                print("========================================================\n")
            else:
                print(f"\n[!] 未在 2019 國科會評比 (林明仁等) A 級以上或 TSSCI 核心中找到: '{args.check}'")
                print("提示: 該期刊可能屬於 B+/B 級，或非純經濟學門評比之期刊。\n")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
