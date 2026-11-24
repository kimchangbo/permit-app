import streamlit as st
# =====================================================================
# ★ 공통 디자인 키트 (10번 케이슨 토압 EP 양식과 통일)
#   선명한 글씨 · 컬러 표/카드 · 아래첨자 · 한눈에 보기 · 납품용 Excel 마감
# =====================================================================
import html as _kit_html
import re as _kit_re

KIT_INK, KIT_NAVY, KIT_BLUE, KIT_LINE = "#0f172a", "#1e3a8a", "#1d4ed8", "#cbd5e1"
KIT_ACCENT = ["#1d4ed8", "#9d174d", "#047857", "#0e7490", "#b45309", "#6d28d9"]

KIT_CSS = """
<style>
/* ---- 글씨 선명하게 (흐린 회색·투명도 제거) ---- */
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li{color:#0f172a}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p, .stCaption{color:#334155 !important;opacity:1 !important}
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label{color:#1e293b !important;opacity:1 !important;font-weight:600}
[data-testid="stMarkdownContainer"] blockquote{color:#1e293b !important;background:#f1f5f9;border-left:4px solid #3b82f6;
  padding:8px 12px;margin:6px 0 12px;border-radius:0 6px 6px 0}
[data-testid="stMarkdownContainer"] blockquote p{color:#1e293b !important;font-size:0.93rem;line-height:1.6}
[data-testid="stAlert"] p, [data-testid="stAlert"] li{color:#0f172a !important}
/* ---- 제목 ---- */
[data-testid="stMarkdownContainer"] h2{color:#1e3a8a}
[data-testid="stMarkdownContainer"] h3{color:#1e3a8a;border-left:6px solid #1d4ed8;padding-left:10px}
[data-testid="stMarkdownContainer"] h4{color:#1e3a8a;border-left:5px solid #1d4ed8;padding-left:8px;margin-top:1.2rem}
[data-testid="stExpander"] summary p{font-weight:700;color:#1e3a8a}
.stTabs [data-baseweb="tab"] p{font-weight:700}
.stTabs [aria-selected="true"] p{color:#1d4ed8}
/* ---- 마크다운 표 : 남색 머리 · 줄무늬 · 첫 열 강조 ---- */
[data-testid="stMarkdownContainer"] table{border-collapse:collapse;width:100%;font-size:0.9rem;margin:4px 0 12px}
[data-testid="stMarkdownContainer"] thead th{background:#1e3a8a !important;color:#ffffff !important;font-weight:700;
  border:1px solid #94a3b8 !important;padding:6px 8px;text-align:center !important}
[data-testid="stMarkdownContainer"] thead th *{color:#ffffff !important}
[data-testid="stMarkdownContainer"] tbody td{border:1px solid #cbd5e1 !important;color:#0f172a;padding:5px 8px}
[data-testid="stMarkdownContainer"] tbody tr:nth-child(even) td{background:#f8fafc}
[data-testid="stMarkdownContainer"] tbody td:first-child{font-weight:700;color:#1e3a8a}
/* 스타일 지정이 없는 HTML 표 머리(<th>) · 셀 */
[data-testid="stMarkdownContainer"] table th:not([style]){background:#1e3a8a;color:#ffffff;font-weight:700;border:1px solid #94a3b8;padding:6px 8px}
[data-testid="stMarkdownContainer"] table th:not([style]) *{color:#ffffff}
[data-testid="stMarkdownContainer"] table td:not([style]){border:1px solid #cbd5e1}
/* ---- st.table 표 ---- */
[data-testid="stTable"] table{border-collapse:collapse;width:100%;font-size:0.9rem}
[data-testid="stTable"] thead th{background:#1e3a8a !important;color:#ffffff !important;font-weight:700;
  border:1px solid #94a3b8 !important;text-align:center !important}
[data-testid="stTable"] thead th *{color:#ffffff !important}
[data-testid="stTable"] tbody th{color:#1e3a8a !important;font-weight:700;background:#eff6ff}
[data-testid="stTable"] tbody td{color:#0f172a !important;border:1px solid #cbd5e1 !important}
[data-testid="stTable"] tbody tr:nth-child(even) td{background:#f8fafc}
/* ---- 지표(metric) 카드 ---- */
[data-testid="stMetric"]{background:#ffffff;border:1px solid #e2e8f0;border-top:4px solid #1d4ed8;border-radius:10px;
  padding:10px 14px;box-shadow:0 1px 3px rgba(15,23,42,.08)}
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] p{color:#334155 !important;font-weight:700 !important;opacity:1 !important}
[data-testid="stMetricValue"]{color:#1d4ed8;font-weight:800}
[data-testid="stColumn"]:nth-child(6n+2) [data-testid="stMetric"]{border-top-color:#9d174d}
[data-testid="stColumn"]:nth-child(6n+2) [data-testid="stMetricValue"]{color:#9d174d}
[data-testid="stColumn"]:nth-child(6n+3) [data-testid="stMetric"]{border-top-color:#047857}
[data-testid="stColumn"]:nth-child(6n+3) [data-testid="stMetricValue"]{color:#047857}
[data-testid="stColumn"]:nth-child(6n+4) [data-testid="stMetric"]{border-top-color:#0e7490}
[data-testid="stColumn"]:nth-child(6n+4) [data-testid="stMetricValue"]{color:#0e7490}
[data-testid="stColumn"]:nth-child(6n+5) [data-testid="stMetric"]{border-top-color:#b45309}
[data-testid="stColumn"]:nth-child(6n+5) [data-testid="stMetricValue"]{color:#b45309}
[data-testid="stColumn"]:nth-child(6n) [data-testid="stMetric"]{border-top-color:#6d28d9}
[data-testid="stColumn"]:nth-child(6n) [data-testid="stMetricValue"]{color:#6d28d9}
.kit-wrap{overflow-x:auto;margin:6px 0 16px}
</style>
"""


def kit_layout(ratio=(1, 2.4), title="📥 입력 조건"):
    """10번 양식 화면 배치 : 좌측 = 입력란(테두리 상자) / 우측 = 결과.
    반환한 입력 상자(col_in)에 입력 위젯을 넣고, 이 호출 이후의 일반 출력(st.*)은 모두 우측 결과 열에 표시된다.
    (Streamlit 은 매 실행마다 출력 위치 스택을 초기화하므로 우측 열 진입 상태가 다음 실행에 남지 않는다)"""
    col_in, col_out = st.columns(list(ratio), gap="large")
    try:
        box = col_in.container(border=True)
    except TypeError:
        box = col_in.container()
    if title:
        box.markdown(f"#### {title}")
    col_out.__enter__()
    return box


def kit_css():
    """화면 공통 스타일 주입 (페이지 상단에서 1회 호출)"""
    try:
        st.markdown(KIT_CSS, unsafe_allow_html=True)
    except Exception:
        pass


# ---- 아래첨자 : 'H1/3' → H<sub>1/3</sub> 등 (표 머리·카드 라벨) ----------------------
KIT_SUB_RULES = [
    (r"(?<![A-Za-z])H_?\{?(1/3|1/10|1/250|max|0|b|s|d|t|i|r)\}?(?![A-Za-z0-9])", r"H<sub>\1</sub>"),
    (r"(?<![A-Za-z])T_?\{?(1/3|0|p|s|m)\}?(?![A-Za-z0-9])", r"T<sub>\1</sub>"),
    (r"(?<![A-Za-z])L_?\{?(0|s)\}?(?![A-Za-z0-9])", r"L<sub>\1</sub>"),
    (r"(?<![A-Za-z])K_?\{?(s|r|d|D|t|a|p|ai|ah|0)\}?(?![A-Za-z0-9])", r"K<sub>\1</sub>"),
    (r"γ_?\{?(sat|t|w|r|c|b|a|s|m)\}?(?![A-Za-z])", r"γ<sub>\1</sub>"),
    (r"Σ([PM])([hvw])(?![A-Za-z])", r"Σ\1<sub>\2</sub>"),
]


def kit_sub(s, rules=None):
    """HTML 이스케이프 후 아래첨자 변환. 이미 <sub>가 있는 문자열은 그대로 둔다."""
    s = str(s)
    if "<sub>" in s or "<sup>" in s or "<span" in s or "<b>" in s:
        return s
    t = _kit_html.escape(s, quote=False)
    for a, b in (rules if rules is not None else KIT_SUB_RULES):
        t = _kit_re.sub(a, b, t)
    return t


# ---- st.table 셀 아래첨자 : 셀이 마크다운으로 렌더링되므로 'E_D'·'H1/3'·'γw' → $E_{D}$ 등 수식 표기 ----
KIT_TEX_RULES = [
    (r"(?<![A-Za-z0-9$\\{])([A-Za-z])_\{?([A-Za-z0-9/.]+)\}?(?![A-Za-z0-9])", r"$\1_{\2}$"),
    (r"(?<![A-Za-z$\\{])H(1/3|1/10|1/250|max|0)(?![A-Za-z0-9])", r"$H_{\1}$"),
    (r"(?<![A-Za-z$\\{])T(1/3|0)(?![A-Za-z0-9])", r"$T_{\1}$"),
    (r"(?<![A-Za-z$\\{])L0(?![A-Za-z0-9])", r"$L_{0}$"),
    (r"(?<![A-Za-z$\\{])K(s|r|d|D|ai|ah)(?![A-Za-z0-9])", r"$K_{\1}$"),
    (r"γ(sat|t|w|r|c)(?![A-Za-z])", r"$\\gamma_{\1}$"),
]


def kit_tex(s):
    if not isinstance(s, str) or "$" in s or "<" in s:
        return s
    for a, b in KIT_TEX_RULES:
        s = _kit_re.sub(a, b, s)
    s = _kit_re.sub(r"([α-ωΔΣΦΨ])_\{?([A-Za-z0-9/.]+)\}?(?![A-Za-z0-9])",
                    lambda m: f"$\\{_KIT_GREEK.get(m.group(1), 'alpha')}_{{{m.group(2)}}}$", s)
    return s


_KIT_GREEK = {"α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon", "ζ": "zeta", "η": "eta",
              "θ": "theta", "λ": "lambda", "μ": "mu", "ξ": "xi", "ρ": "rho", "σ": "sigma", "τ": "tau", "φ": "phi",
              "ψ": "psi", "ω": "omega", "Δ": "Delta", "Σ": "Sigma", "Φ": "Phi", "Ψ": "Psi"}


def _kit_df_tex(data):
    try:
        import pandas as _pd
        if not isinstance(data, _pd.DataFrame):
            return data
        d = data.copy()
        d.columns = [kit_tex(c) for c in d.columns]
        if d.index.dtype == object:
            d.index = [kit_tex(i) for i in d.index]
        f = getattr(d, "map", None) or d.applymap
        return f(kit_tex)
    except Exception:
        return data


if not getattr(st.table, "_kit", False):
    _kit_orig_table = st.table

    def _kit_table_patch(data=None, *a, **kw):
        return _kit_orig_table(_kit_df_tex(data), *a, **kw)

    _kit_table_patch._kit = True
    st.table = _kit_table_patch

# ---- [공통] 마크다운 물결표(~) 취소선 방지 : 수식($…$)·코드·<style> 밖의 '~' 는 글자 그대로 표시 ----
#      예) "0.7~0.9", "(3.155)~(3.156)" 처럼 '~' 가 두 번 나오면 그 사이가 취소선으로 그어지는 현상 방지
def _kit_tilde(s):
    if not isinstance(s, str) or "~" not in s:
        return s
    parts = _kit_re.split(r"(\$\$.*?\$\$|\$[^$\n]+\$|<style.*?</style>|`[^`]*`|~~)", s, flags=_kit_re.S)
    return "".join(p if i % 2 else p.replace("~", "&#126;") for i, p in enumerate(parts))


def _kit_tilde_install():
    from streamlit.delta_generator import DeltaGenerator as _KitDG

    def _mk_m(f):
        def w(self, body="", *a, **k):
            return f(self, _kit_tilde(body), *a, **k)
        w._kit_tilde = True
        return w

    def _mk_f(f):
        def w(body="", *a, **k):
            return f(_kit_tilde(body), *a, **k)
        w._kit_tilde = True
        return w

    for _n in ("markdown", "info", "warning", "success", "error", "caption"):
        if not getattr(getattr(_KitDG, _n), "_kit_tilde", False):
            setattr(_KitDG, _n, _mk_m(getattr(_KitDG, _n)))
        if not getattr(getattr(st, _n), "_kit_tilde", False):
            setattr(st, _n, _mk_f(getattr(st, _n)))


_kit_tilde_install()



# ---- 한눈에 보기 카드 -----------------------------------------------------------------
def kit_hero(head, sub, cards, report=False):
    """cards: [dict(icon,label,value,unit,lines,accent,pill)] — 10번 '설계 한눈에 보기'와 동일한 형식"""
    def inner(c):
        acc = c.get("accent", KIT_BLUE)
        pill = (f"<div style='margin-top:8px'><span style='display:inline-block;background:{c.get('pill_bg', acc)};color:#fff;"
                f"border-radius:12px;padding:3px 10px;font-size:12px;font-weight:700'>{c['pill']}</span></div>"
                if c.get("pill") else "")
        lines = "".join(f"<div style='font-size:12.5px;color:#334155;line-height:1.5'>{x}</div>" for x in c.get("lines", []))
        return (f"<div style='font-size:14px;font-weight:700;color:{KIT_INK}'>{c.get('icon', '')} {c['label']}</div>"
                f"<div style='margin:6px 0 4px;color:{acc}'><span style='font-size:28px;font-weight:800;"
                f"letter-spacing:-0.5px'>{c['value']}</span> <span style='font-size:14px;font-weight:700;color:#334155'>"
                f"{c.get('unit', '')}</span></div>{lines}{pill}")

    for i, c in enumerate(cards):
        c.setdefault("accent", KIT_ACCENT[i % len(KIT_ACCENT)])
    top = (f"<div style='background:linear-gradient(90deg,#1e3a8a,#2563eb);background-color:#1e3a8a;color:#fff;"
           f"padding:11px 16px;font-size:16px;font-weight:800'>📌 {head} <span style='font-size:13px;font-weight:600;"
           f"opacity:0.95;margin-left:8px'>{sub}</span></div>")
    if report:
        w = int(100 / max(1, len(cards)))
        cells = "".join(f"<td style='width:{w}%;vertical-align:top;background:#fff;border:1px solid {KIT_LINE};"
                        f"border-top:4px solid {c['accent']};padding:10px 12px'>{inner(c)}</td>" for c in cards)
        return (f"<div style='border:1px solid #93c5fd;margin:10px 0 18px'>{top}"
                f"<table style='border-collapse:separate;border-spacing:8px;width:100%;background:#eff6ff'><tr>{cells}"
                f"</tr></table></div>")
    cells = "".join(f"<div style='flex:1 1 200px;min-width:190px;background:#fff;border-radius:10px;border:1px solid #e2e8f0;"
                    f"border-top:4px solid {c['accent']};padding:12px 14px;box-shadow:0 1px 3px rgba(15,23,42,.08)'>"
                    f"{inner(c)}</div>" for c in cards)
    return (f"<div style='border:1px solid #bfdbfe;border-radius:12px;overflow:hidden;margin:4px 0 18px;"
            f"background:#eff6ff'>{top}<div style='display:flex;flex-wrap:wrap;gap:12px;padding:14px'>{cells}</div></div>")


def kit_show_hero(head, sub, cards):
    st.markdown(kit_hero(head, sub, cards), unsafe_allow_html=True)


# ---- 컬러 계산표 (DataFrame / 행 목록 → HTML) -------------------------------------------
KIT_GROUP = {"id": "#1e3a8a", "geo": "#334155", "seis": "#6d28d9", "ang": "#0e7490", "coef": "#047857",
             "str": "#b45309", "force": "#1d4ed8", "mom": "#9d174d", "res": "#0f766e", "ok": "#15803d", "ng": "#b91c1c"}
KIT_OK = ("O.K", "OK", "만족", "적합", "안전")
KIT_NG = ("N.G", "NG", "불만족", "부적합", "위험")


def _kit_judge(v):
    s = str(v)
    if any(k in s for k in KIT_NG):
        return f"<span style='background:#fee2e2;color:#991b1b;border-radius:10px;padding:1px 9px;font-weight:800'>{s}</span>"
    if any(k in s for k in KIT_OK):
        return f"<span style='background:#dcfce7;color:#166534;border-radius:10px;padding:1px 9px;font-weight:800'>{s}</span>"
    return None


def kit_table(df, groups=None, total_last=False, hi_rows=(), font="12.5px", bold_cols=(), judge=True, wrap=False):
    """inline-style HTML 표 (화면·HTML·Word 공통) — 열 그룹별 머리 색, 줄무늬, 합계·지배 행 강조, 아래첨자, O.K/N.G 칩"""
    groups = groups or {}
    cols = list(df.columns)
    ws_ = "normal" if wrap else "nowrap"
    th = "".join(f"<th style='background:{KIT_GROUP.get(groups.get(c, 'id'), KIT_NAVY)};color:#ffffff;font-weight:700;"
                 f"padding:7px 8px;border:1px solid #94a3b8;text-align:center;white-space:{ws_}'>{kit_sub(c)}</th>"
                 for c in cols)
    body, n = [], len(df)
    for i, (_, row) in enumerate(df.iterrows()):
        is_tot, is_hi = total_last and i == n - 1, i in hi_rows
        bg = "#dbeafe" if is_tot else "#fef3c7" if is_hi else ("#f8fafc" if i % 2 else "#ffffff")
        tds = []
        for j, c in enumerate(cols):
            v = row[c]
            v = "-" if v is None or (isinstance(v, float) and v != v) else v
            if isinstance(v, float) or type(v).__name__.startswith("float"):
                s_ = f"{float(v):,.4f}"
                while s_.endswith("0") and len(s_.split(".")[1]) > 2:
                    s_ = s_[:-1]
                v = s_
            cell = (_kit_judge(v) if judge else None) or kit_sub(v)
            fw = "700" if (is_tot or j == 0 or c in bold_cols) else "400"
            col = KIT_NAVY if (is_tot or j == 0) else KIT_INK
            bt = "border-top:2px solid #1e3a8a;" if is_tot else ""
            bl = "border-left:4px solid #f59e0b;" if (is_hi and j == 0) else ""
            tds.append(f"<td style='background:{bg};color:{col};font-weight:{fw};padding:6px 8px;border:1px solid {KIT_LINE};"
                       f"{bt}{bl}text-align:center;white-space:{ws_}'>{cell}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    return (f"<div class='kit-wrap' style='overflow-x:auto;margin:6px 0 16px'>"
            f"<table style='border-collapse:collapse;width:100%;font-size:{font};font-family:inherit'>"
            f"<thead><tr>{th}</tr></thead><tbody>{''.join(body)}</tbody></table></div>")


def kit_show_table(df, fmt=None, na_rep="-", **kw):
    """fmt: {열이름: '{:.2f}'} — Styler.format 과 같은 서식 지정 후 컬러 표로 출력"""
    if fmt:
        df = df.copy()
        for c, f in fmt.items():
            if c in df.columns:
                df[c] = [na_rep if (x is None or (isinstance(x, float) and x != x)) else
                         (f.format(x) if not isinstance(x, str) else x) for x in df[c]]
    st.markdown(kit_table(df, **kw), unsafe_allow_html=True)


def kit_bars_html(title, items, unit="", vmax=None, limit=None, limit_label="허용치"):
    """비교 막대 — items: [(이름, 값, 강조여부)] / limit 가 있으면 기준선 표시"""
    vals = [abs(float(v)) for _, v, *_ in items] + ([abs(float(limit))] if limit else [])
    vmax = vmax or (max(vals) if vals else 1.0) or 1.0
    rows = []
    for i, it in enumerate(items):
        nm, v = it[0], float(it[1])
        on = bool(it[2]) if len(it) > 2 else False
        w = max(1.0, 100 * abs(v) / vmax)
        col = "#1d4ed8" if on else "#93c5fd"
        tag = (" <span style='background:#1d4ed8;color:#fff;border-radius:8px;padding:0 7px;font-size:11px'>적용</span>"
               if on else "")
        lim = (f"<div style='position:absolute;left:{100 * abs(float(limit)) / vmax:.1f}%;top:-3px;height:20px;"
               f"border-left:2px dashed #dc2626'></div>" if limit else "")
        vs = f"{v:,.1f}" if abs(v) >= 100 else f"{v:,.3f}"
        rows.append(f"<div style='display:flex;align-items:center;gap:8px;padding:5px 12px;border-bottom:1px solid #e2e8f0'>"
                    f"<span style='width:190px;font-size:12.5px;color:#0f172a;font-weight:700'>{kit_sub(nm)}{tag}</span>"
                    f"<div style='flex:1;background:#e2e8f0;border-radius:6px;height:14px;position:relative'>"
                    f"<div style='width:{w:.1f}%;background:{col};height:14px;border-radius:6px'></div>{lim}</div>"
                    f"<span style='width:110px;text-align:right;font-weight:800;color:{KIT_INK};font-size:13px'>"
                    f"{vs} {unit}</span></div>")
    lv = (f"{float(limit):,.1f}" if abs(float(limit)) >= 100 else f"{float(limit):,.3f}") if limit else ""
    leg = (f"<div style='padding:4px 12px;font-size:11.5px;color:#991b1b'>┆ 붉은 점선 = {limit_label} {lv} {unit}</div>"
           if limit else "")
    return (f"<div style='border:1px solid #e2e8f0;border-radius:10px;background:#fff;margin:4px 0 16px'>"
            f"<div style='padding:8px 12px;font-weight:800;color:{KIT_NAVY};border-bottom:2px solid #1d4ed8'>"
            f"{kit_sub(title)}</div>{''.join(rows)}{leg}</div>")


def kit_bars(title, items, unit="", vmax=None, limit=None, limit_label="허용치"):
    st.markdown(kit_bars_html(title, items, unit, vmax, limit, limit_label), unsafe_allow_html=True)


def kit_strip(tag, items, accent="#047857"):
    """결과 한 줄 카드 — items: [(라벨, 값, 단위)]"""
    cells = "".join(f"<td style='padding:8px 10px;border:1px solid #bbf7d0;background:#fff;text-align:center'>"
                    f"<div style='font-size:12px;color:#334155;font-weight:700'>{kit_sub(l)}</div>"
                    f"<div style='font-size:17px;font-weight:800;color:{accent}'>{v}"
                    f" <span style='font-size:11.5px;color:#334155;font-weight:600'>{u}</span></div></td>"
                    for l, v, u in items)
    return (f"<div class='kit-wrap' style='margin:4px 0 18px'><table style='border-collapse:collapse;width:100%;"
            f"border:2px solid {accent}'><tr><td style='background:{accent};color:#fff;font-weight:800;padding:8px 12px;"
            f"white-space:nowrap;text-align:center'>✔ {_kit_html.escape(tag)}</td>{cells}</tr></table></div>")


def kit_metrics_html(items):
    """핵심 수치 한 줄 카드 — items: [(라벨, 값)] 또는 [(라벨, 값, 보조문)] (라벨 아래첨자 자동)"""
    cells = []
    for i, it in enumerate(items):
        lab, val = it[0], it[1]
        note = it[2] if len(it) > 2 else ""
        acc = KIT_ACCENT[i % len(KIT_ACCENT)]
        cells.append(f"<div style='flex:1 1 140px;min-width:130px;background:#fff;border:1px solid #e2e8f0;border-top:4px solid {acc};"
                     f"border-radius:10px;padding:8px 12px;box-shadow:0 1px 3px rgba(15,23,42,.08)'>"
                     f"<div style='font-size:12.5px;font-weight:700;color:#334155'>{kit_sub(lab)}</div>"
                     f"<div style='font-size:21px;font-weight:800;color:{acc};margin-top:2px'>{kit_sub(val)}</div>"
                     + (f"<div style='font-size:11.5px;color:#334155'>{kit_sub(note)}</div>" if note else "") + "</div>")
    return f"<div style='display:flex;flex-wrap:wrap;gap:10px;margin:6px 0 14px'>{''.join(cells)}</div>"


def kit_metrics(items):
    st.markdown(kit_metrics_html(items), unsafe_allow_html=True)


def kit_basis(text):
    """근거 표기 (흐린 캡션 대신 선명한 근거 띠)"""
    st.markdown(f"<div style='background:#eff6ff;border-left:4px solid #1d4ed8;padding:6px 12px;margin:4px 0 12px;"
                f"border-radius:0 6px 6px 0;color:#1e293b;font-size:0.88rem'>📌 <b style='color:#1e3a8a'>근거</b> : "
                f"{kit_sub(text)}</div>", unsafe_allow_html=True)


# ---- 납품용 Excel 마감 (모든 시트 공통) ---------------------------------------------------
def _kit_fix_rich(v):
    """공백만 있는 리치텍스트 조각은 openpyxl 이 xml:space='preserve' 없이 기록 → Excel 이 파일을 열지 못함.
    공백 조각을 다음 조각 앞에 붙여 제거한다."""
    try:
        from openpyxl.cell.rich_text import CellRichText, TextBlock
    except Exception:
        return v
    if not isinstance(v, CellRichText):
        return v
    out, carry = [], ""
    for p in list(v):
        t = p.text if isinstance(p, TextBlock) else str(p)
        if t.strip() == "":
            carry += t
            continue
        if carry:
            p = TextBlock(p.font, carry + t) if isinstance(p, TextBlock) else carry + t
            carry = ""
        out.append(p)
    if carry and out:
        p = out[-1]
        out[-1] = TextBlock(p.font, p.text + carry) if isinstance(p, TextBlock) else p + carry
    return CellRichText(out) if out else carry


KIT_XL_GREY_HEAD = {"D9D9D9", "BFBFBF", "E7E6E6", "D0CECE", "DDDDDD", "D8D8D8"}


def kit_xl_cover(wb, title, proj="", author="다온기술"):
    """표지 시트가 없는 계산서에 공통 표지 추가 : 계산서명 · 공사명 · 작성일 · 목차(시트 링크) · 결재란"""
    import datetime as _dt
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    if any("표지" in w.title for w in wb.worksheets):
        return
    sheets = [w.title for w in wb.worksheets]
    ws = wb.create_sheet("표지", 0)
    ws.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGH", (3, 16, 16, 16, 16, 16, 16, 3)):
        ws.column_dimensions[col].width = w
    navy = PatternFill("solid", fgColor="1E3A8A")
    thin = Side(style="thin", color="94A3B8")
    box = Border(left=thin, right=thin, top=thin, bottom=thin)

    def put(r, text, size=11, bold=False, color="0F172A", h="center"):
        ws.merge_cells(f"B{r}:G{r}")
        c = ws[f"B{r}"]
        c.value = text
        c.font = Font(name="맑은 고딕", size=size, bold=bold, color=color)
        c.alignment = Alignment(horizontal=h, vertical="center", wrap_text=True)

    put(3, proj or "○○ 공사 (공사명)", 13, True, "334155")
    for col in "BCDEFG":
        ws[f"{col}6"].fill = navy
        ws[f"{col}9"].fill = navy
    ws.row_dimensions[6].height = ws.row_dimensions[9].height = 5
    put(7, title, 24, True, "1E3A8A")
    ws.row_dimensions[7].height = 46
    put(8, "구 조 계 산 서", 13, False, "1E293B")
    put(12, "■ 목 차", 12, True, "1E3A8A", "left")
    r = 13
    for i, nm in enumerate(sheets, 1):
        ws.merge_cells(f"B{r}:G{r}")
        c = ws[f"B{r}"]
        c.value = f"  {i}. {nm}"
        c.hyperlink = f"#'{nm}'!A1"
        c.font = Font(name="맑은 고딕", size=11, color="1D4ED8", underline="single")
        r += 1
    r += 2
    for j, t in enumerate(("작 성", "검 토", "승 인")):
        c = ws.cell(r, 5 + j, t)
        c.font, c.fill, c.border = Font(name="맑은 고딕", bold=True, color="FFFFFF"), navy, box
        c.alignment = Alignment(horizontal="center")
        ws.cell(r + 1, 5 + j).border = box
    ws.row_dimensions[r + 1].height = 46
    put(r + 4, _dt.date.today().strftime("%Y. %m. %d."), 13, True)
    put(r + 5, author, 12, False, "334155")
    ws.page_setup.paperSize = 9
    ws.page_setup.orientation = "portrait"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    wb.active = 0
    for w in wb.worksheets:
        w.sheet_view.tabSelected = w.title == "표지"


def kit_xl_finish(wb, title, proj="", font_name="맑은 고딕", cover=True):
    """A4·폭 맞춤 인쇄, 머리글(계산서명/공사명)·바닥글(쪽번호), 여백, 전 셀 글꼴 통일, 눈금선 숨김(인쇄), 표지 없으면 공통 표지"""
    if cover:
        try:
            kit_xl_cover(wb, title, proj)
        except Exception:
            pass
    try:
        from copy import copy as _cp
    except Exception:
        _cp = None
    for w in wb.worksheets:
        try:
            if getattr(w, "sheet_state", "visible") != "visible":
                continue
            ps = w.page_setup
            ps.paperSize = 9
            if not ps.orientation:
                ps.orientation = "landscape" if (w.max_column or 0) > 9 else "portrait"
            pr = w.sheet_properties.pageSetUpPr
            if pr is None:
                from openpyxl.worksheet.properties import PageSetupProperties
                w.sheet_properties.pageSetUpPr = pr = PageSetupProperties()
            if not pr.fitToPage:                       # 앱에서 이미 지정한 인쇄배율은 존중
                pr.fitToPage = True
                ps.fitToWidth = 1
                ps.fitToHeight = 0
            w.print_options.horizontalCentered = True
            w.print_options.gridLines = False
            m = w.page_margins
            if m.left is None or m.left > 0.7:
                m.left = m.right = 0.45
                m.top, m.bottom, m.header, m.footer = 0.65, 0.6, 0.3, 0.3
            if not (w.oddHeader.left.text or w.oddHeader.center.text):
                w.oddHeader.left.text = title
                w.oddHeader.left.size = 8
                w.oddHeader.right.text = proj or ""
                w.oddHeader.right.size = 8
            if not w.oddFooter.center.text:
                w.oddFooter.center.text = "&P / &N"
                w.oddFooter.center.size = 8
            if _cp is not None and font_name:
                from openpyxl.styles import PatternFill as _PF
                for row in w.iter_rows():
                    for c in row:
                        if type(c.value).__name__ == "CellRichText":
                            c.value = _kit_fix_rich(c.value)
                        f = c.font
                        # 회색 표 머리 → 남색 머리·흰 글씨 (10번 계산서와 같은 색 체계)
                        try:
                            fl = c.fill
                            if (fl is not None and fl.fill_type == "solid" and f is not None and f.b
                                    and str(fl.fgColor.rgb)[-6:].upper() in KIT_XL_GREY_HEAD):
                                c.fill = _PF("solid", fgColor="1E3A8A")
                                nf = _cp(f)
                                nf.color = "FFFFFF"
                                c.font = nf
                                f = c.font
                        except Exception:
                            pass
                        if f is not None and f.name in (None, "Calibri", "Arial", "돋움", "굴림", "Cambria Math"):
                            nf = _cp(f)
                            # Cambria Math 는 Excel 에서 행 높이를 비정상적으로 키우므로 Cambria 로 대체
                            nf.name = "Cambria" if f.name == "Cambria Math" else font_name
                            c.font = nf
        except Exception:
            continue
    return wb


import requests
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
import concurrent.futures
from io import BytesIO
import time
from pathlib import Path
import base64

# Word(.docx) 생성을 위한 라이브러리 임포트
try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# =====================================================================
# ★ 페이지 기본 설정
# =====================================================================
st.set_page_config(page_title="인허가 법령 자동 업데이트 시스템", page_icon="⚖️", layout="wide")


# ==== [공통블록 v2 · 2026-10-20] 💾 입력 저장/불러오기 · 🧾 계산 정보(QA/QC) · 📚 적용 기준 ====
#   _공통블록/inject.py 가 앱마다 넣는 블록 (직접 고치지 말 것 — 고칠 때는 _공통블록/block_template.py 를 고친 뒤 inject.py 다시 실행)
#   · 💾 이름표(key)가 붙은 입력란 값을 JSON 으로 저장 · 불러오기 (사이드바)
#   · 🧾 내려받는 Excel · Word · HTML · JSON 에 '계산 정보'(프로그램 판 · 계산 일시 · 입력 지문 · 적용 기준)를 자동으로 붙임
#   · 📚 이 앱이 인용한 KDS 조항 목록 (확정본 고시 후 점검용 — _기준점검/kds_scan.py)
_PJ = {'app': '인허가 관련 법령 자동 업데이트', 'no': 23, 'save': True, 'keys': {'scope_mode': 'radio', 'scope_hide': 'checkbox', 'sc_sch_start': 'date_input', 'sc_sch_b': 'number_input', 'sc_sch_d': 'number_input', 'sc_sch_done': 'multiselect', 'in_시스템_설정_법제처_API_키_OC_필수': 'text_input'}, 'kds': [], 'basis': '앱 화면의 근거 표기 참조', 'tables': {'tb_edited_df': None}, 'credit': '김창보 @ 다온기술', 'lib': True, 'short': None}
_PJ_VER = "pj-10"


def _pj_kst():
    """[2026-10-26] 서버(Streamlit Cloud)는 세계 표준시(UTC) — 프로세스 시각을 한국 시간으로 맞춤
    (보관함 날짜 · 계산 일시 · 저장 파일 이름 · 각 앱 보고서 작성 시각). 'KST-9' 는 시간대 자료 없이도 되는 표기, 윈도우 PC 는 원래 한국 시간"""
    import os as _os, time as _tm
    if hasattr(_tm, "tzset") and _os.environ.get("TZ") != "KST-9":
        _os.environ["TZ"] = "KST-9"
        _tm.tzset()


_pj_kst()


def _pj_k(k, *sig):
    """이름표(key)를 붙인 입력란 중 기본값 · 범위 · 선택지가 계산으로 정해지는 것 — 그 값이 바뀌면 이름표 없을 때처럼
    새 기본값으로 다시 시작 (Streamlit 은 이름표가 있으면 예전 값을 계속 씀). 불러온 직후에는 불러온 값을 그대로 둠"""
    try:
        ss = st.session_state
        parts = []
        for x in sig:                     # 함수 · 반복자처럼 실행마다 주소가 바뀌는 값은 형식 이름만 비교
            r = repr(x)
            parts.append(type(x).__name__ if " at 0x" in r else r)
        h = "|".join(parts)
        memo = ss.setdefault("_pj_sig", {})
        if k in memo and memo[k] != h and not ss.get("_pj_loaded") and k in ss:
            del ss[k]
        memo[k] = h
    except Exception:  # noqa: BLE001
        pass
    return k


def _pj_thash(v):
    import hashlib as _hl
    try:
        s = v.to_json() if hasattr(v, "to_json") else repr(v)
    except Exception:  # noqa: BLE001
        s = repr(v)
    return _hl.md5(s.encode("utf-8", "replace")).hexdigest()


def _pj_tbl(t, data):
    """표 편집기(data_editor)의 바탕 표 — 불러온 표가 있으면 그것을, 앱이 만든 바탕 표가 그 뒤 바뀌면(다른 입력을 고침) 앱 것을"""
    try:
        base = st.session_state.get("_pj_tbase") or {}
        if t not in base:
            return data
        b, h = base[t]
        cur = _pj_thash(data)
        if h is None:                     # 불러온 첫 실행 — 이때 앱이 만든 바탕 표를 기억
            base[t] = (b, cur)
            return b
        if h != cur:
            base.pop(t, None)
            return data
        return b
    except Exception:  # noqa: BLE001
        return data


def _pj_tset(t, v):
    """표 편집기 결과(고친 표)를 기억 → 💾 입력 저장 때 함께 저장"""
    try:
        st.session_state.setdefault("_pj_tv", {})[t] = v
    except Exception:  # noqa: BLE001
        pass
    return v


def _pj_tenc(v):
    import json as _js
    try:
        import pandas as _pd
        if isinstance(v, _pd.DataFrame):
            d = _js.loads(v.to_json(orient="split", date_format="iso", force_ascii=False))
            return {"kind": "df", "data": d, "dtypes": {str(c): str(t) for c, t in v.dtypes.items()}}
    except Exception:  # noqa: BLE001
        return None
    try:
        _js.dumps(v)
        return {"kind": "raw", "data": v}
    except Exception:  # noqa: BLE001
        return None


def _pj_tdec(p):
    if not isinstance(p, dict):
        return None
    if p.get("kind") == "df":
        import pandas as _pd
        d = p.get("data") or {}
        df = _pd.DataFrame(d.get("data"), columns=d.get("columns"), index=d.get("index"))
        for c in df.columns:
            t = (p.get("dtypes") or {}).get(str(c))
            if t and t != "object":
                try:
                    df[c] = df[c].astype(t)
                except Exception:  # noqa: BLE001
                    pass
        return df
    return p.get("data")


_PJ_SKIP_VT = (None, "trigger_value", "string_trigger_value", "chat_input_value", "file_uploader_state_value")


def _pj_S():
    """이 접속(세션)의 상태 객체 — 앱 실행 밖(내려받기 단추를 누르는 순간)에서도 읽을 수 있음"""
    try:
        from streamlit.runtime.state import get_session_state as _gss
        return _gss()
    except Exception:  # noqa: BLE001
        return st.session_state


def _pj_widget_keys(S):
    """저장 대상 입력란 = 글자로 찾은 이름표(_PJ['keys']) + Streamlit 이 기억한 값 입력란
    (버튼 · 내려받기 · 파일 올리기 제외 — 이름표가 변수로 만들어진 앱도 포함)"""
    out = dict(_PJ["keys"])
    try:
        s = S
        for _i in range(4):                      # 감싼 겹수가 Streamlit 판마다 달라도 찾도록
            if hasattr(s, "_key_id_mapper"):
                break
            s = getattr(s, "_state", None)
        meta = s._new_widget_state.widget_metadata
        for wid, k in list(s._key_id_mapper.id_key_mapping.items()):
            if not isinstance(k, str) or k.startswith(("_", "$$")):
                continue
            vt = getattr(meta.get(wid), "value_type", None)
            if vt not in _PJ_SKIP_VT:
                out.setdefault(k, vt)
    except Exception:  # noqa: BLE001 — Streamlit 판이 바뀌어 내부 구조가 다르면 글자로 찾은 이름표만
        pass
    return out


def _pj_enc(v):
    """입력값 → (JSON 값, 형식) — 날짜 · 시각 · 범위(튜플)는 형식을 기억해 되살림"""
    import datetime as _dt
    if isinstance(v, _dt.datetime):
        return v.isoformat(), "datetime"
    if isinstance(v, _dt.date):
        return v.isoformat(), "date"
    if isinstance(v, _dt.time):
        return v.isoformat(), "time"
    if isinstance(v, tuple):
        vals = [_pj_enc(x) for x in v]
        if any(t is None for _x, t in vals) or not vals and False:
            return None, None
        tags = {t for _x, t in vals}
        return [x for x, _t in vals], ("tuple_date" if tags == {"date"} else "tuple")
    if isinstance(v, list):
        vals = [_pj_enc(x) for x in v]
        return ([x for x, _t in vals], "list") if all(t in ("", "list") for _x, t in vals) else (None, None)
    if isinstance(v, bool) or v is None or isinstance(v, (str, int, float)):
        return v, ""
    try:
        import numpy as _np
        if isinstance(v, _np.generic):
            return v.item(), ""
    except Exception:  # noqa: BLE001
        pass
    return None, None          # 표 편집 상태 · 파일 등은 저장하지 않음


def _pj_dec(v, t):
    import datetime as _dt
    if t == "date":
        return _dt.date.fromisoformat(str(v)[:10])
    if t == "datetime":
        return _dt.datetime.fromisoformat(str(v))
    if t == "time":
        return _dt.time.fromisoformat(str(v))
    if t == "tuple_date":
        return tuple(_dt.date.fromisoformat(str(x)[:10]) for x in v)
    if t == "tuple":
        return tuple(v)
    return v


def _pj_snapshot(S):
    vals, types = {}, {}
    for k in _pj_widget_keys(S):
        try:
            if k not in S:
                continue
            v, t = _pj_enc(S[k])
        except Exception:  # noqa: BLE001
            continue
        if t is not None:
            vals[k] = v
            if t and t != "list":
                types[k] = t
    return vals, types


def _pj_finger(vals):
    import hashlib as _hl, json as _js
    return _hl.md5(_js.dumps(vals, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()[:10]


def _pj_stamp_lines(S=None):
    """계산 정보 — 입력 지문은 부르는 순간의 입력값으로 (파일을 만드는 시점 = 계산한 입력)"""
    S = S if S is not None else _pj_S()
    try:
        ctx = S["_pj_ctx"] if "_pj_ctx" in S else {}
    except Exception:  # noqa: BLE001
        ctx = {}
    if not ctx:
        return []
    import datetime as _dt
    return [("프로그램", ctx.get("app", "-")), ("프로그램 판", ctx.get("ver", "-")),
            ("계산 일시", _dt.datetime.now().strftime("%Y-%m-%d %H:%M")),
            ("입력 지문", f"{_pj_finger(_pj_snapshot(S)[0])} (같은 입력이면 같은 값 — 저장한 입력 JSON 과 대조)"),
            ("적용 기준", ctx.get("basis", "-")), ("인용 기준", ctx.get("kds", "-") or "-")]


def _pj_stamp_xlsx(b, lines):
    import io as _io, re as _re, zipfile as _zf
    from xml.sax.saxutils import escape as _esc
    zin = _zf.ZipFile(_io.BytesIO(b))
    names = zin.namelist()
    if "xl/workbook.xml" not in names or "xl/_rels/workbook.xml.rels" not in names:
        return b
    wb = zin.read("xl/workbook.xml").decode("utf-8")
    if 'name="계산정보"' in wb:
        return b
    rels = zin.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    ct = zin.read("[Content_Types].xml").decode("utf-8")
    sid = max([int(x) for x in _re.findall(r'sheetId="(\d+)"', wb)] or [0]) + 1
    sp = _re.search(r"<(\w+:)?sheets>", wb)
    sp = (sp.group(1) or "") if sp else ""
    # r: 이름공간은 새 줄에 직접 선언 (openpyxl 은 sheet 줄마다 따로 선언함)
    wb = wb.replace(f"</{sp}sheets>", f'<{sp}sheet xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                                      f'name="계산정보" sheetId="{sid}" r:id="rIdPJ1"/></{sp}sheets>', 1)
    rels = rels.replace("</Relationships>", '<Relationship Id="rIdPJ1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                        'relationships/worksheet" Target="/xl/worksheets/sheet_pj.xml"/></Relationships>', 1)
    ct = ct.replace("</Types>", '<Override PartName="/xl/worksheets/sheet_pj.xml" ContentType="application/vnd.openxmlformats-'
                    'officedocument.spreadsheetml.worksheet+xml"/></Types>', 1)
    rows = [("🧾 계산 정보 (QA/QC)", "")] + list(lines)
    cells = "".join(f'<row r="{i}"><c r="A{i}" t="inlineStr"><is><t>{_esc(str(a))}</t></is></c>'
                    f'<c r="B{i}" t="inlineStr"><is><t>{_esc(str(v))}</t></is></c></row>' for i, (a, v) in enumerate(rows, 1))
    sheet = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/'
             'spreadsheetml/2006/main"><cols><col min="1" max="1" width="16" customWidth="1"/><col min="2" max="2" width="100" '
             f'customWidth="1"/></cols><sheetData>{cells}</sheetData></worksheet>')
    out = _io.BytesIO()
    with _zf.ZipFile(out, "w", _zf.ZIP_DEFLATED) as zo:
        for it in zin.infolist():
            data = {"xl/workbook.xml": wb.encode("utf-8"), "xl/_rels/workbook.xml.rels": rels.encode("utf-8"),
                    "[Content_Types].xml": ct.encode("utf-8")}.get(it.filename)
            zo.writestr(it, data if data is not None else zin.read(it.filename))
        zo.writestr("xl/worksheets/sheet_pj.xml", sheet)
    return out.getvalue()


def _pj_stamp_docx(b, lines):
    import io as _io, zipfile as _zf
    from xml.sax.saxutils import escape as _esc
    zin = _zf.ZipFile(_io.BytesIO(b))
    if "word/document.xml" not in zin.namelist():
        return b
    doc = zin.read("word/document.xml").decode("utf-8")
    if "🧾 계산 정보" in doc:
        return b

    def para(t, bold=False):
        rpr = f"<w:rPr>{'<w:b/>' if bold else ''}<w:sz w:val=\"16\"/></w:rPr>"
        return f'<w:p><w:r>{rpr}<w:t xml:space="preserve">{_esc(t)}</w:t></w:r></w:p>'
    add = para("🧾 계산 정보 (QA/QC)", True) + "".join(para(f"{a} : {v}") for a, v in lines)
    i = doc.rfind("<w:sectPr")
    i = i if i > doc.rfind("</w:p>") else doc.rfind("</w:body>")
    if i < 0:
        return b
    doc = doc[:i] + add + doc[i:]
    out = _io.BytesIO()
    with _zf.ZipFile(out, "w", _zf.ZIP_DEFLATED) as zo:
        for it in zin.infolist():
            zo.writestr(it, doc.encode("utf-8") if it.filename == "word/document.xml" else zin.read(it.filename))
    return out.getvalue()


_PJ_MJ_NAME = "mathjax-3.2.2-tex-svg.js"


def _pj_mathjax_js():
    """[2026-11-10] HTML 보고서에 넣을 MathJax 3.2.2 (SVG 판 — 글꼴 파일 없이 인터넷 없어도 수식 표시, 검증보고서 R-2).
    찾는 곳 : 앱 폴더 · 그 아래 _lib · 작업 폴더 pages/_lib · _공통블록/lib. 프로세스에 한 번 읽음."""
    import sys as _sy, os as _o
    if hasattr(_sy, "_pj_mj_js"):
        return _sy._pj_mj_js
    js = None
    try:
        here = _o.path.dirname(_o.path.abspath(__file__))
    except Exception:  # noqa: BLE001
        here = _o.getcwd()
    for d in (here, _o.path.join(here, "_lib"), _o.path.join(_o.getcwd(), "pages", "_lib"), _o.path.join(_o.getcwd(), "_lib"),
              _o.path.join(_o.path.dirname(here), "_공통블록", "lib"), _o.path.join(_o.getcwd(), "_공통블록", "lib")):
        p = _o.path.join(d, _PJ_MJ_NAME)
        if _o.path.exists(p):
            try:
                js = open(p, encoding="utf-8").read().replace("</script", "<\\/script")
                break
            except Exception:  # noqa: BLE001
                js = None
    _sy._pj_mj_js = js
    return js


def _pj_inline_mathjax(s):
    """인터넷에서 MathJax 를 부르는 <script src=…mathjax@3…> 를 파일 안에 넣은 스크립트로 바꿈 (파일이 없으면 그대로)"""
    import re as _re
    rx = _re.compile(r"""<script\b[^>]*\bsrc\s*=\s*["']https?://cdn\.jsdelivr\.net/npm/mathjax@3[^"']*["'][^>]*>\s*</script>""", _re.I)
    if not rx.search(s):
        return s
    js = _pj_mathjax_js()
    if not js:
        return s
    return rx.sub(lambda m: "<script id=\"MathJax-script\">/* MathJax 3.2.2 tex-svg (내장 — 인터넷 없이 수식 표시) */\n" + js + "\n</script>", s, count=1)


def _pj_stamp_html(s, lines, inline_mj=False):
    import html as _h
    if inline_mj:
        try:
            s = _pj_inline_mathjax(s)
        except Exception:  # noqa: BLE001
            pass
    if "🧾 계산 정보" in s or not any(t in s.lower() for t in ("<html", "<body", "<table", "<div")):
        return s
    foot = ("<div style='margin-top:24px;padding:8px 12px;border-top:2px solid #94a3b8;font-size:10pt;color:#334155'>"
            "<b>🧾 계산 정보 (QA/QC)</b><br>" + "<br>".join(f"{_h.escape(a)} : {_h.escape(str(v))}" for a, v in lines) + "</div>")
    j = s.lower().rfind("</body>")
    return s[:j] + foot + s[j:] if j >= 0 else s + foot


_PJ_SUB_RX = None


def _pj_xl_sub(b):
    """[2026-11-10] 내려받는 Excel 의 글자 칸 기호를 아랫첨자로 (H₁/₃ · T₁/₃ · H₀′ · L₀ · Hₘₐₓ · Kₛ …, 메모 subscripts-always).
    파일 XML (sharedStrings) 만 고침 — 차트 · 그림 · 수식 그대로, 글자 자체는 같아 MATCH 등도 그대로. 칸 글꼴(이름 · 크기 · 굵기 · 색) 유지.
    이미 서식 글자(rich text)인 칸 · 수식 칸은 손대지 않음. 실패하면 원래 파일."""
    import io as _io, re as _re, zipfile as _zf
    from xml.sax.saxutils import escape as _esc, unescape as _unesc
    global _PJ_SUB_RX
    try:
        if _PJ_SUB_RX is None:
            _PJ_SUB_RX = _re.compile(r"(?<![A-Za-z0-9_])(H1/250|H1/10|H1/3|T1/3|H2%|Hmax|H0[′']|Ru2%|Dn50|L0|Ks|Kr|"
                                     r"Lpp|Hs|HD|Hb|hb|hc|hs|kh|Rc|Sr|C0|Cf|Fs|Fd|Ph|Pw|Pu|Pv|Vc|Uc|Tm|Tp|Ts|T0|H0|Ka|Mv|Mh|Dn|Cb|Cr|Cm|Ce|Ns|Lm)(?![A-Za-z0-9_])")   # [2026-11-16] 기호 넓힘 (Excel 15개 점검)
        import html as _html
        _unesc = _html.unescape                      # &#44284; 같은 숫자 참조까지
        zin = _zf.ZipFile(_io.BytesIO(b))
        names = zin.namelist()
        if "xl/styles.xml" not in names:
            return b
        sst = zin.read("xl/sharedStrings.xml").decode("utf-8") if "xl/sharedStrings.xml" in names else ""
        items = list(_re.finditer(r"<si\b[^>]*?(?:/>|>(.*?)</si>)", sst, _re.S))
        plain = {}
        for i, m in enumerate(items):
            body = m.group(1) or ""
            if _re.search(r"<r\b", body):
                continue
            t = "".join(_unesc(x) for x in _re.findall(r"<t\b[^>]*>(.*?)</t>", body, _re.S))
            if _PJ_SUB_RX.search(t):
                plain[i] = t
        stx = zin.read("xl/styles.xml").decode("utf-8")
        fm = _re.search(r"<fonts\b[^>]*>(.*?)</fonts>", stx, _re.S)
        fonts = _re.findall(r"<font\b[^>]*/>|<font\b[^>]*>.*?</font>", fm.group(1), _re.S) if fm else []
        cx = _re.search(r"<cellXfs\b[^>]*>(.*?)</cellXfs>", stx, _re.S)
        xfs = _re.findall(r"<xf\b[^>]*/>|<xf\b[^>]*>.*?</xf>", cx.group(1), _re.S) if cx else []
        xf_font = [int((_re.search(r'\bfontId="(\d+)"', x) or [0, "0"])[1]) for x in xfs]

        def rpr(fid, sub):
            f = fonts[fid] if 0 <= fid < len(fonts) else ""
            g = lambda tag: (_re.search(rf"<{tag}\b[^>]*/>", f) or [None])[0]
            parts = []
            nm = _re.search(r'<name\b[^>]*\bval="([^"]*)"', f)
            if nm:
                parts.append(f'<rFont val="{nm.group(1)}"/>')
            for tag in ("charset", "family", "b", "i", "strike", "outline", "shadow", "condense", "extend", "color", "sz", "u"):
                v = g(tag)
                if v:
                    parts.append(v)
            if sub:
                parts.append('<vertAlign val="subscript"/>')
            sc = g("scheme")
            if sc:
                parts.append(sc)
            return "<rPr>" + "".join(parts) + "</rPr>" if parts else ""

        def runs(text, fid):
            out, k = [], 0
            for m in _PJ_SUB_RX.finditer(text):
                if m.start() > k:
                    out.append((text[k:m.start()], 0))
                s = m.group(1)
                if s.startswith("H0"):
                    out += [("H", 0), ("0", 1), (s[2:], 0)]
                else:
                    out += [(s[0], 0), (s[1:], 1)]
                k = m.end()
            if k < len(text):
                out.append((text[k:], 0))
            return "".join(f'<r>{rpr(fid, sb)}<t xml:space="preserve">{_esc(tx)}</t></r>' for tx, sb in out if tx)
        new_si, key2idx = [], {}
        n0 = len(items)
        rxc = _re.compile(r'<c\b([^>]*?)>\s*<v>(\d+)</v>\s*</c>', _re.S)
        rxi = _re.compile(r'<c\b([^>]*?\bt="inlineStr"[^>]*)>\s*<is>(.*?)</is>\s*</c>', _re.S)
        sheets = [n for n in names if n.startswith("xl/worksheets/") and n.endswith(".xml")]
        new_sheets = {}

        def _fid(attrs):
            sm = _re.search(r'\bs="(\d+)"', attrs)
            return xf_font[int(sm.group(1))] if sm and int(sm.group(1)) < len(xf_font) else 0
        for sn in sheets:
            x = zin.read(sn).decode("utf-8")
            changed = [False]

            def _cell(m):
                attrs, idx = m.group(1), int(m.group(2))
                if 't="s"' not in attrs or idx not in plain:
                    return m.group(0)
                fid = _fid(attrs)
                kk = (idx, fid)
                if kk not in key2idx:
                    key2idx[kk] = n0 + len(new_si)
                    new_si.append("<si>" + runs(plain[idx], fid) + "</si>")
                changed[0] = True
                return f"<c{attrs}><v>{key2idx[kk]}</v></c>"

            def _inl(m):
                attrs, body = m.group(1), m.group(2)
                if _re.search(r"<r\b", body):
                    return m.group(0)
                t = "".join(_unesc(q) for q in _re.findall(r"<t\b[^>]*>(.*?)</t>", body, _re.S))
                if not _PJ_SUB_RX.search(t):
                    return m.group(0)
                changed[0] = True
                return f"<c{attrs}><is>{runs(t, _fid(attrs))}</is></c>"
            y = rxi.sub(_inl, rxc.sub(_cell, x) if plain else x)
            if changed[0]:
                new_sheets[sn] = y
        if not new_sheets:
            return b
        sst2 = sst
        if new_si:
            sst2 = sst.replace("</sst>", "".join(new_si) + "</sst>", 1)
            sst2 = _re.sub(r'\buniqueCount="\d+"', f'uniqueCount="{n0 + len(new_si)}"', sst2, 1)
        out = _io.BytesIO()
        with _zf.ZipFile(out, "w", _zf.ZIP_DEFLATED) as zo:
            for it in zin.infolist():
                if it.filename == "xl/sharedStrings.xml" and new_si:
                    zo.writestr(it, sst2.encode("utf-8"))
                elif it.filename in new_sheets:
                    zo.writestr(it, new_sheets[it.filename].encode("utf-8"))
                else:
                    zo.writestr(it, zin.read(it.filename))
        return out.getvalue()
    except Exception:  # noqa: BLE001
        return b


def _pj_xl_cache(b):
    """[2026-11-10] 내려받는 Excel 에 수식 계산값도 함께 (미리보기 빈칸 방지) — 실패하거나 너무 크면 원래 파일 그대로"""
    try:
        if len(b) > 12_000_000:
            return b
        return _pjx().xl_cache(b)
    except Exception:  # noqa: BLE001
        return b


def _pj_xl_view(b):
    """[2026-11-11] 내려받는 Excel 을 열면 '페이지 나누기 미리보기' (인쇄 영역 · 쪽 경계가 보이게).
    시트 XML 의 sheetView 만 고침 — 차트 · 그림 · 수식 그대로. 앱이 정한 확대가 있으면 그 값, 없으면 85 %. 실패하면 원래 파일."""
    import io as _io, re as _re, zipfile as _zf
    try:
        zin = _zf.ZipFile(_io.BytesIO(b))
        names = [n for n in zin.namelist() if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")]
        if not names:
            return b
        rx = _re.compile(r"<sheetView\b([^>]*?)(/?)>")

        def _sv(m):
            a = m.group(1)
            zs = _re.search(r'\bzoomScale="(\d+)"', a)
            z = zs.group(1) if zs and zs.group(1) != "100" else "85"
            a = _re.sub(r'\s(?:view|zoomScale|zoomScaleSheetLayoutView)="[^"]*"', "", a)
            if "zoomScaleNormal=" not in a:
                a += ' zoomScaleNormal="100"'
            return f'<sheetView{a} view="pageBreakPreview" zoomScale="{z}" zoomScaleSheetLayoutView="{z}"{m.group(2)}>'
        new = {}
        for n in names:
            x = zin.read(n).decode("utf-8")
            y = rx.sub(_sv, x, count=1)
            if y == x and "<sheetView" not in x:          # 보기 설정이 없는 시트 (계산정보 등) — 넣음
                mm = _re.search(r"<(?:sheetFormatPr|cols|sheetData)\b", x)
                if mm:
                    y = (x[:mm.start()] + '<sheetViews><sheetView workbookViewId="0" zoomScaleNormal="100" view="pageBreakPreview" '
                         'zoomScale="85" zoomScaleSheetLayoutView="85"/></sheetViews>' + x[mm.start():])
            if y != x:
                new[n] = y
        if not new:
            return b
        out = _io.BytesIO()
        with _zf.ZipFile(out, "w", _zf.ZIP_DEFLATED) as zo:
            for it in zin.infolist():
                zo.writestr(it, new[it.filename].encode("utf-8") if it.filename in new else zin.read(it.filename))
        return out.getvalue()
    except Exception:  # noqa: BLE001
        return b


def _pj_stamp(data, fname, S=None):
    """내려받는 파일에 계산 정보 붙이기 — 실패하면 원래 파일 그대로"""
    try:
        lines = _pj_stamp_lines(S)
        ext = str(fname or "").lower().rsplit(".", 1)[-1]
        if not lines or ext not in ("xlsx", "xlsm", "docx", "html", "htm", "doc", "json"):
            return data
        raw = data.getvalue() if hasattr(data, "getvalue") else data
        if ext in ("xlsx", "xlsm") and isinstance(raw, (bytes, bytearray)):
            return _pj_xl_view(_pj_stamp_xlsx(_pj_xl_sub(_pj_xl_cache(bytes(raw))), lines))
        if ext == "docx" and isinstance(raw, (bytes, bytearray)):
            return _pj_stamp_docx(bytes(raw), lines)
        if ext in ("html", "htm", "doc"):
            _mj = ext in ("html", "htm")          # [2026-11-10] HTML 만 MathJax 내장 (Word 는 스크립트 안 돌림)
            if isinstance(raw, str):
                return _pj_stamp_html(raw, lines, _mj)
            if isinstance(raw, (bytes, bytearray)) and not bytes(raw[:8]).startswith(b"\xd0\xcf\x11\xe0"):
                pre = b"\xef\xbb\xbf" if bytes(raw[:3]) == b"\xef\xbb\xbf" else b""
                t = bytes(raw[len(pre):]).decode("utf-8")
                return pre + _pj_stamp_html(t, lines, _mj).encode("utf-8")
        if ext == "json":
            import json as _js
            t = raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else raw
            d = _js.loads(t)
            if isinstance(d, dict) and "_계산정보" not in d:
                d["_계산정보"] = dict(lines)
                o = _js.dumps(d, ensure_ascii=False, indent=1, default=str)
                return o.encode("utf-8") if isinstance(raw, (bytes, bytearray)) else o
    except Exception:  # noqa: BLE001 — 계산 정보를 못 붙여도 파일은 그대로 내려받기
        pass
    return data


class _PjSheet:
    """[2026-11-10] 납품용 Excel 계산서 모눈 시트 (16번 블록식 · 29번과 같은 양식) — 42열 모눈 · A4 세로 · 쪽 번호
    h1 (남색 밑줄 제목) · h2 · h3 · note · panel (공식 / 기호 설명 / 근거 상자) · result (초록 결과 상자) ·
    inp (노란 바탕 · 파란 글씨 입력 칸 + 이름) · header · box · page_break · finish · png (그림)"""
    NCOL = 42

    def __init__(self, wb, name, head=""):
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
        from openpyxl.utils import get_column_letter
        from openpyxl.worksheet.properties import PageSetupProperties
        self.A, self.B, self.F, self.P, self.S, self.CL = Alignment, Border, Font, PatternFill, Side, get_column_letter
        self.wb, self.name = wb, name
        self.ws = ws = wb.create_sheet(name)
        self.r = 1
        self.GRAY, self.INF = PatternFill("solid", fgColor="D9D9D9"), PatternFill("solid", fgColor="FFF2CC")
        self.FH, self.FB = PatternFill("solid", fgColor="DCE6F2"), PatternFill("solid", fgColor="F7F9FC")
        self.RES, self.HI = PatternFill("solid", fgColor="E2EFDA"), PatternFill("solid", fgColor="FCE4D6")
        self.THIN, self.HAIR = Side(style="thin"), Side(style="hair")
        self.MED, self.NAV = Side(style="medium", color="1E3A8A"), Side(style="thin", color="1E3A8A")
        ws.sheet_format.defaultRowHeight = 16.5
        ws.sheet_format.customHeight = True
        ws.column_dimensions["A"].width = 1.3
        for c in range(2, self.NCOL + 1):
            ws.column_dimensions[get_column_letter(c)].width = 2.35
        for c in range(self.NCOL + 1, self.NCOL + 20):
            ws.column_dimensions[get_column_letter(c)].width = 10
        ws.sheet_view.showGridLines = False
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.page_setup.orientation = "portrait"
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
        ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
        ws.page_margins.left = ws.page_margins.right = 0.5
        ws.page_margins.top = ws.page_margins.bottom = 0.6
        ws.oddFooter.center.text = "- &P / &N -"
        ws.oddFooter.center.size = 9
        if head:
            ws.oddHeader.right.text = head
            ws.oddHeader.right.size = 8

    def font(self, size=9, bold=False, color="000000"):
        return self.F(name="맑은 고딕", size=size, bold=bold, color=color)

    def ref(self, c, r):
        return f"'{self.name}'!${self.CL(c)}${r}"

    def put(self, r, c1, c2, v, fmt=None, bold=False, h="center", fill=None, color="000000", size=9, wrap=False, r2=None):
        ws = self.ws
        c2, r2 = c2 or c1, r2 or r
        if c2 > c1 or r2 > r:
            ws.merge_cells(start_row=r, start_column=c1, end_row=r2, end_column=c2)
        cell = ws.cell(r, c1, v)
        cell.font = self.font(size, bold, color)
        cell.alignment = self.A(horizontal=h, vertical="center", wrap_text=wrap)
        if fmt:
            cell.number_format = fmt
        if fill:
            for rr in range(r, r2 + 1):
                for cc in range(c1, c2 + 1):
                    ws.cell(rr, cc).fill = fill
        return cell

    def dname(self, nm, c, r):
        from openpyxl.workbook.defined_name import DefinedName
        self.wb.defined_names[nm] = DefinedName(nm, attr_text=self.ref(c, r))

    def inp(self, r, c1, c2, v, fmt="0.000", name=None, h="center"):
        self.put(r, c1, c2, v, fmt=fmt, bold=True, color="0000FF", fill=self.INF, h=h)
        if name:
            self.dname(name, c1, r)
        return self.ref(c1, r)

    def h1(self, t):
        self.put(self.r, 2, self.NCOL, t, size=13, bold=True, color="1E3A8A", h="left")
        for c in range(2, self.NCOL + 1):
            self.ws.cell(self.r, c).border = self.B(bottom=self.MED)
        self.ws.row_dimensions[self.r].height = 24
        self.r += 2

    def h2(self, t):
        self.put(self.r, 2, self.NCOL, t, size=10.5, bold=True, h="left")
        self.ws.row_dimensions[self.r].height = 19
        self.r += 1

    def h3(self, t):
        self.put(self.r, 3, self.NCOL, t, size=9.5, bold=True, color="595959", h="left")
        self.r += 1

    def note(self, t, c=3, color="595959", size=8.5, bold=False):
        import math as _m
        units = sum(1.75 if ord(ch) > 0x2E80 else 0.9 for ch in str(t)) * size / 9.0
        lines = max(1, _m.ceil(units / ((self.NCOL - c + 1) * 2.35)))
        self.put(self.r, c, self.NCOL, t, h="left", color=color, size=size, wrap=lines > 1, bold=bold)
        if lines > 1:
            self.ws.row_dimensions[self.r].height = 13.5 * lines + 2
        self.r += 1

    def gap(self, n=1):
        self.r += n

    def box(self, r1, r2, c1, c2, hdr_rows=0):
        o, i_ = self.THIN, self.HAIR
        for rr in range(r1, r2 + 1):
            for cc in range(c1, c2 + 1):
                self.ws.cell(rr, cc).border = self.B(
                    left=o if cc == c1 else i_, right=o if cc == c2 else i_,
                    top=o if (rr == r1 or (hdr_rows and rr == r1 + hdr_rows)) else i_,
                    bottom=o if (rr == r2 or (hdr_rows and rr == r1 + hdr_rows - 1)) else i_)

    def header(self, r, spans, h=None):
        for c1, c2, t in spans:
            self.put(r, c1, c2, t, bold=True, fill=self.GRAY, wrap=True)
        if h:
            self.ws.row_dimensions[r].height = h

    def panel(self, title, lines):
        """공식 · 기호 · 근거 상자 — lines : 문자열 (▶ 로 시작하면 굵게) 또는 (기호, 설명) 튜플"""
        import math as _m
        N, r0 = self.NCOL, self.r
        self.put(r0, 3, N - 1, "■ " + title, bold=True, color="1E3A8A", fill=self.FH, h="left", size=9.5)
        r = r0 + 1
        for ln in lines:
            if isinstance(ln, tuple):
                sym, desc = ln
                self.put(r, 4, 11, sym, fill=self.FB, bold=True, h="left")
                self.put(r, 12, N - 1, desc, fill=self.FB, h="left", wrap=len(desc) > 52)
                if len(desc) > 52:
                    self.ws.row_dimensions[r].height = 13.5 * _m.ceil(len(desc) / 52) + 3
            else:
                self.put(r, 4, N - 1, ln, fill=self.FB, h="left", bold=ln.startswith("▶"), wrap=len(ln) > 78)
                if len(ln) > 78:
                    self.ws.row_dimensions[r].height = 13.5 * _m.ceil(len(ln) / 78) + 3
            r += 1
        for rr in range(r0, r):
            for cc in range(3, N):
                self.ws.cell(rr, cc).border = self.B(
                    left=self.NAV if cc == 3 else None, right=self.NAV if cc == N - 1 else None,
                    top=self.NAV if rr == r0 else (self.HAIR if rr == r0 + 1 else None), bottom=self.NAV if rr == r - 1 else None)
        self.r = r + 1

    def result(self, v, c1=3, h=22):
        N = self.NCOL
        self.put(self.r, c1, N - 1, v, bold=True, fill=self.RES, h="left", size=10 if c1 == 3 else 9)
        if c1 > 3:
            self.ws.cell(self.r, c1).alignment = self.A(horizontal="left", vertical="center", shrink_to_fit=True)
        for cc in range(c1, N):
            self.ws.cell(self.r, cc).border = self.B(top=self.THIN, bottom=self.THIN, left=self.THIN if cc == c1 else None,
                                                     right=self.THIN if cc == N - 1 else None)
        if c1 == 3 and h:
            self.ws.row_dimensions[self.r].height = h
        self.r += 2

    def png(self, data, col=3, w=560, h=280, row=None):
        """그림 넣기 → 차지한 행 수 (못 넣으면 0)"""
        try:
            import io as _io
            from openpyxl.drawing.image import Image as _XI
            im = _XI(_io.BytesIO(data))
            im.width, im.height = w, h
            self.ws.add_image(im, f"{self.CL(col)}{row or self.r}")
            n = int(h / 21) + 1
            if row is None:
                self.r += n + 1
            return n
        except Exception:  # noqa: BLE001
            return 0

    def page_break(self):
        from openpyxl.worksheet.pagebreak import Break
        self.ws.row_breaks.append(Break(id=self.r - 1))

    def finish(self):
        self.ws.print_area = f"A1:{self.CL(self.NCOL)}{max(self.r, 2)}"


# [2026-10-23] Excel 수식 계산기 (Excel 없이 수식 값을 구함 — 일반 판 고정값 · 계산값 저장용)
_PJX_SRC = r'''# -*- coding: utf-8 -*-
"""작은 Excel 수식 계산기 — openpyxl 로 만든 계산서의 수식을 Excel 없이 계산해 '값만 박힌 판'을 만든다.
xl_values(bytes) -> bytes  (수식 칸을 값으로 바꾼 xlsx, 그림 · 서식 · 차트는 그대로)"""
import io as _io
import math as _m
import re as _re


class _XE(Exception):
    def __init__(self, code="#VALUE!"):
        super().__init__(code)
        self.code = code


class _ErrV:
    __slots__ = ("code",)

    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return self.code


def _col2n(s):
    n = 0
    for ch in s:
        n = n * 26 + ord(ch) - 64
    return n


def _n2col(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


class _Arr:
    """2차원 값 배열 (범위 · 배열 연산 결과)"""
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v

    @property
    def nr(self):
        return len(self.v)

    @property
    def nc(self):
        return len(self.v[0]) if self.v else 0

    def flat(self):
        return [x for row in self.v for x in row]


class _Rng:
    __slots__ = ("bk", "sh", "r1", "c1", "r2", "c2")

    def __init__(self, bk, sh, r1, c1, r2, c2):
        self.bk, self.sh = bk, sh
        self.r1, self.c1, self.r2, self.c2 = min(r1, r2), min(c1, c2), max(r1, r2), max(c1, c2)

    @property
    def nr(self):
        return self.r2 - self.r1 + 1

    @property
    def nc(self):
        return self.c2 - self.c1 + 1

    def cell(self, i, j):          # 0 기준
        return self.bk.get(self.sh, self.r1 + i, self.c1 + j)

    def arr(self):
        return _Arr([[self.bk.get(self.sh, r, c, soft=True) for c in range(self.c1, self.c2 + 1)]
                     for r in range(self.r1, self.r2 + 1)])

    def flat(self):
        return self.arr().flat()


# ── 값 변환 ──
def _num(x):
    if isinstance(x, _ErrV):
        raise _XE(x.code)
    if x is None:
        return 0.0
    if isinstance(x, bool):
        return 1.0 if x else 0.0
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        t = x.strip()
        if t == "":
            raise _XE("#VALUE!")
        try:
            return float(t.replace(",", ""))
        except ValueError:
            raise _XE("#VALUE!")
    if isinstance(x, (_Rng, _Arr)):
        a = x.arr() if isinstance(x, _Rng) else x
        if a.nr == 1 and a.nc == 1:
            return _num(a.v[0][0])
        raise _XE("#VALUE!")
    raise _XE("#VALUE!")


def _n2s(v):
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, float):
        if v == int(v) and abs(v) < 1e15:
            return str(int(v))
        s = format(v, ".15g")
        if "e" in s:
            mant, ex = s.split("e")
            s = f"{mant}E{'+' if int(ex) >= 0 else '-'}{abs(int(ex)):02d}"
        return s
    if isinstance(v, int):
        return str(v)
    return "" if v is None else str(v)


def _str(x):
    if isinstance(x, _ErrV):
        raise _XE(x.code)
    if isinstance(x, (_Rng, _Arr)):
        a = x.arr() if isinstance(x, _Rng) else x
        return _str(a.v[0][0])
    return _n2s(x)


def _bool(x):
    if isinstance(x, _ErrV):
        raise _XE(x.code)
    if isinstance(x, (_Rng, _Arr)):
        a = x.arr() if isinstance(x, _Rng) else x
        return _bool(a.v[0][0])
    if isinstance(x, bool):
        return x
    if x is None:
        return False
    if isinstance(x, (int, float)):
        return x != 0
    if isinstance(x, str):
        if x.upper() == "TRUE":
            return True
        if x.upper() == "FALSE":
            return False
    raise _XE("#VALUE!")


def _scalar(x):
    if isinstance(x, _Rng):
        if x.nr == 1 and x.nc == 1:
            return x.cell(0, 0)
        return x
    return x


def _chk(x):
    if isinstance(x, _ErrV):
        raise _XE(x.code)
    return x


def _cmp(a, b, op):
    a, b = _chk(a), _chk(b)
    if a is None:
        a = "" if isinstance(b, str) else (False if isinstance(b, bool) else 0.0)
    if b is None:
        b = "" if isinstance(a, str) else (False if isinstance(a, bool) else 0.0)

    def rank(v):
        return 2 if isinstance(v, bool) else (1 if isinstance(v, str) else 0)
    ra, rb = rank(a), rank(b)
    if ra != rb:
        d = (ra > rb) - (ra < rb)
    elif ra == 1:
        x, y = a.lower(), b.lower()
        d = (x > y) - (x < y)
    else:
        x, y = float(a), float(b)
        d = (x > y) - (x < y)
    return {"=": d == 0, "<>": d != 0, "<": d < 0, ">": d > 0, "<=": d <= 0, ">=": d >= 0}[op]


def _arith(a, b, op):
    x, y = _num(a), _num(b)
    if op == "+":
        return x + y
    if op == "-":
        return x - y
    if op == "*":
        return x * y
    if op == "/":
        if y == 0:
            raise _XE("#DIV/0!")
        return x / y
    if op == "^":
        if x == 0 and y < 0:
            raise _XE("#DIV/0!")
        if x < 0 and y != int(y):
            raise _XE("#NUM!")
        try:
            r = x ** y
        except OverflowError:
            raise _XE("#NUM!")
        if isinstance(r, complex) or r != r or r in (float("inf"), float("-inf")):
            raise _XE("#NUM!")
        return float(r)
    raise _XE()


def _binop(a, b, op):
    """배열이면 원소별"""
    A_, B_ = isinstance(a, (_Rng, _Arr)), isinstance(b, (_Rng, _Arr))
    if A_ or B_:
        aa = (a.arr() if isinstance(a, _Rng) else a) if A_ else None
        bb = (b.arr() if isinstance(b, _Rng) else b) if B_ else None
        if aa is not None and aa.nr == 1 and aa.nc == 1 and not B_:
            aa, A_ = None, False
            a = (a.arr() if isinstance(a, _Rng) else a).v[0][0]
        if A_ or B_:
            nr = max(aa.nr if aa else 1, bb.nr if bb else 1)
            nc = max(aa.nc if aa else 1, bb.nc if bb else 1)

            def g(M, s, i, j):
                if M is None:
                    return s
                return M.v[i if M.nr > 1 else 0][j if M.nc > 1 else 0]
            out = []
            for i in range(nr):
                row = []
                for j in range(nc):
                    try:
                        row.append(_binop(g(aa, a, i, j), g(bb, b, i, j), op))
                    except _XE as e:
                        row.append(_ErrV(e.code))
                row = row
                out.append(row)
            return _Arr(out)
    if op == "&":
        return _str(a) + _str(b)
    if op in ("=", "<>", "<", ">", "<=", ">="):
        return _cmp(a, b, op)
    return _arith(a, b, op)


# ── 함수 ── (인자는 지연 계산 thunk)
def _vals(args, keep_text=False):
    """MAX · MIN · SUM 등 : 범위의 숫자만, 직접 인자는 숫자로 변환"""
    out = []
    for t in args:
        v = t()
        if isinstance(v, (_Rng, _Arr)):
            for x in v.flat():
                if isinstance(x, _ErrV):
                    raise _XE(x.code)
                if isinstance(x, (int, float)) and not isinstance(x, bool):
                    out.append(float(x))
        else:
            out.append(_num(v))
    return out


def _round(x, n):
    x, n = _num(x), int(_num(n))
    # Excel ROUND : half away from zero (부동소수 보정)
    from decimal import Decimal, ROUND_HALF_UP
    d = Decimal(repr(abs(x))).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP) if n >= 0 else \
        (Decimal(repr(abs(x))) / Decimal(10) ** (-n)).quantize(Decimal(1), rounding=ROUND_HALF_UP) * Decimal(10) ** (-n)
    return float(d) * (1 if x >= 0 else -1)


def _text(v, fmt):
    v = _chk(v)
    if isinstance(v, str):
        try:
            v = float(v)
        except ValueError:
            return v
    x = _num(v)
    f = _str(fmt)
    if ";" in f:                       # 양수;음수;0 구역
        secs = f.split(";")
        if x < 0 and len(secs) > 1:
            f, x = secs[1], -x
        elif x == 0 and len(secs) > 2:
            f = secs[2]
        else:
            f = secs[0]
    mm = _re.match(r"^([^0#,.]*)(.*?)([^0#,.]*)$", f)
    pre, f, suf = (mm.group(1), mm.group(2), mm.group(3)) if mm else ("", f, "")
    _pct = _re.sub(r'"[^"]*"', "", pre + suf).count("%")     # [2026-11-10] 따옴표 밖 % = 100 배 (Excel 퍼센트 서식)
    if _pct:
        x = x * 100.0 ** _pct
    pre, suf = pre.replace(chr(34), ""), suf.replace(chr(34), "")
    if pre or suf:
        return pre + _text(x, f) + suf
    m = _re.fullmatch(r"([#,0]*)(?:\.([0#]*))?", f)
    if not m:
        m2 = _re.fullmatch(r"0(?:\.(0+))?E\+00", f)
        if m2:
            nd = len(m2.group(1) or "")
            s = f"{x:.{nd}E}"
            mant, ex = s.split("E")
            return f"{mant}E{'+' if int(ex) >= 0 else '-'}{abs(int(ex)):02d}"
        return _n2s(x)
    ip, dp = m.group(1) or "", m.group(2) or ""
    nmin, nmax = dp.count("0"), len(dp)
    s = f"{_round(x, nmax):.{nmax}f}"
    if nmax > nmin:
        whole, frac = s.split(".")
        frac = frac.rstrip("0")
        if len(frac) < nmin:
            frac = frac + "0" * (nmin - len(frac))
        s = whole + ("." + frac if frac else ("" if nmin == 0 else ""))
        if not frac and "." in f and nmin == 0:
            s = whole + "."
    if "," in ip:
        neg = s.startswith("-")
        s = s.lstrip("-")
        whole, _, frac = s.partition(".")
        whole = f"{int(whole):,}"
        s = ("-" if neg else "") + whole + ("." + frac if _ else "")
    if ip and ip.replace(",", "") .strip("#") == "" and s.startswith("0") and "." in s:
        s = s[1:]
    return s


def _gammainc(a, x):
    try:
        from scipy.special import gammainc
        return float(gammainc(a, x))
    except ImportError:
        # 급수 / 연분수 (Numerical Recipes)
        if x <= 0:
            return 0.0
        if x < a + 1:
            ap, s, d = a, 1.0 / a, 1.0 / a
            for _ in range(500):
                ap += 1
                d *= x / ap
                s += d
                if abs(d) < abs(s) * 1e-15:
                    break
            return s * _m.exp(-x + a * _m.log(x) - _m.lgamma(a))
        b, c, d = x + 1 - a, 1e300, 1 / (x + 1 - a)
        h = d
        for i in range(1, 500):
            an = -i * (i - a)
            b += 2
            d = an * d + b
            d = 1e-300 if abs(d) < 1e-300 else d
            c = b + an / c
            c = 1e-300 if abs(c) < 1e-300 else c
            d = 1 / d
            de = d * c
            h *= de
            if abs(de - 1) < 1e-15:
                break
        return 1 - _m.exp(-x + a * _m.log(x) - _m.lgamma(a)) * h


def _as_arr(v):
    v = v if not callable(v) else v()
    if isinstance(v, _Rng):
        return v.arr()
    if isinstance(v, _Arr):
        return v
    return _Arr([[v]])


def _index(bk, args):
    ref = args[0]()
    r = int(_num(args[1]())) if len(args) > 1 else 0
    c = int(_num(args[2]())) if len(args) > 2 and args[2] is not None else 0
    if isinstance(ref, _Rng):
        if ref.nr == 1 and len(args) == 2:
            r, c = 1, r
        if r == 0 and c == 0:
            return ref
        if r == 0:
            return _Rng(bk, ref.sh, ref.r1, ref.c1 + c - 1, ref.r2, ref.c1 + c - 1)
        if c == 0:
            if ref.nc == 1:
                c = 1
            else:
                return _Rng(bk, ref.sh, ref.r1 + r - 1, ref.c1, ref.r1 + r - 1, ref.c2)
        if r < 1 or c < 1 or r > ref.nr or c > ref.nc:
            raise _XE("#REF!")
        return ref.cell(r - 1, c - 1)
    a = _as_arr(ref)
    if a.nr == 1 and len(args) == 2:
        r, c = 1, r
    if r == 0:
        if c == 0:
            return a
        return _Arr([[row[c - 1]] for row in a.v])
    if c == 0:
        c = 1 if a.nc == 1 else 0
        if c == 0:
            return _Arr([a.v[r - 1]])
    if r < 1 or c < 1 or r > a.nr or c > a.nc:
        raise _XE("#REF!")
    return _chk_soft(a.v[r - 1][c - 1])


def _chk_soft(x):
    if isinstance(x, _ErrV):
        raise _XE(x.code)
    return x


def _match(args):
    look = _chk(_scalar(args[0]()))
    arr = _as_arr(args[1])
    mt = int(_num(args[2]())) if len(args) > 2 else 1
    seq = arr.flat()
    if mt == 0:
        for i, x in enumerate(seq):
            if isinstance(x, _ErrV):
                continue
            try:
                if _cmp(x, look, "="):
                    return float(i + 1)
            except _XE:
                continue
        raise _XE("#N/A")
    # 이진 탐색 (Excel 과 같이 정렬 가정) — 빈 칸 · 형식 다른 값 건너뜀
    lo, hi, best = 0, len(seq) - 1, None
    nums = isinstance(look, (int, float)) and not isinstance(look, bool)
    while lo <= hi:
        mid = (lo + hi) // 2
        x = seq[mid]
        if x is None or isinstance(x, _ErrV) or (nums != (isinstance(x, (int, float)) and not isinstance(x, bool))):
            # 앞쪽 유효값 찾기
            k = mid - 1
            while k >= lo and (seq[k] is None or isinstance(seq[k], _ErrV) or
                               nums != (isinstance(seq[k], (int, float)) and not isinstance(seq[k], bool))):
                k -= 1
            if k < lo:
                lo = mid + 1
                continue
            mid, x = k, seq[k]
        c = _cmp(x, look, "<=") if mt == 1 else _cmp(x, look, ">=")
        if c:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    if best is None:
        raise _XE("#N/A")
    return float(best + 1)


def _countif(args):
    a = _as_arr(args[0])
    crit = _chk(_scalar(args[1]()))
    op, val = "=", crit
    if isinstance(crit, str):
        mm = _re.match(r"(<=|>=|<>|<|>|=)?(.*)$", crit, _re.S)
        op = mm.group(1) or "="
        val = mm.group(2)
        try:
            val = float(val)
        except ValueError:
            pass
    n = 0
    for x in a.flat():
        if isinstance(x, _ErrV) or x is None:
            continue
        if isinstance(val, str) and op == "=" and ("*" in val or "?" in val):
            pat = "^" + _re.escape(val).replace(r"\*", ".*").replace(r"\?", ".") + "$"
            if isinstance(x, str) and _re.match(pat, x, _re.I | _re.S):
                n += 1
            continue
        if isinstance(val, float) and not (isinstance(x, (int, float)) and not isinstance(x, bool)):
            continue
        if isinstance(val, str) and not isinstance(x, str):
            continue
        if _cmp(x, val, op):
            n += 1
    return float(n)


def _aggregate(args):
    fn = int(_num(args[0]()))
    opt = int(_num(args[1]()))
    a = args[2]()
    vals = []
    for x in (a.flat() if isinstance(a, (_Rng, _Arr)) else [a]):
        if isinstance(x, _ErrV):
            if opt in (2, 3, 6, 7):
                continue
            raise _XE(x.code)
        if isinstance(x, (int, float)) and not isinstance(x, bool):
            vals.append(float(x))
    k = int(_num(args[3]())) if len(args) > 3 else None
    vals.sort()
    if fn == 15:
        if not k or k > len(vals):
            raise _XE("#NUM!")
        return vals[k - 1]
    if fn == 14:
        if not k or k > len(vals):
            raise _XE("#NUM!")
        return vals[-k]
    if fn == 4:
        return max(vals) if vals else 0.0
    if fn == 5:
        return min(vals) if vals else 0.0
    if fn == 9:
        return sum(vals)
    raise _XE("#VALUE!")


def _offset(bk, args):
    ref = args[0]()
    if not isinstance(ref, _Rng):
        raise _XE("#VALUE!")
    dr, dc = int(_num(args[1]())), int(_num(args[2]()))
    h = int(_num(args[3]())) if len(args) > 3 and args[3] is not None else ref.nr
    w = int(_num(args[4]())) if len(args) > 4 and args[4] is not None else ref.nc
    if h < 1 or w < 1:
        raise _XE("#REF!")
    r1, c1 = ref.r1 + dr, ref.c1 + dc
    if r1 < 1 or c1 < 1:
        raise _XE("#REF!")
    return _Rng(bk, ref.sh, r1, c1, r1 + h - 1, c1 + w - 1)


def _ceiling(x, s=1.0):
    x, s = _num(x), _num(s)
    if s == 0:
        return 0.0
    if x > 0 and s < 0:
        raise _XE("#NUM!")
    q = x / s
    k = _m.ceil(q - 1e-12) if x >= 0 else -_m.floor(-q + 1e-12)
    return float(k * s)


def _fn(bk, name, args):
    N = name.upper().replace("_XLFN.", "").replace("_XLWS.", "")
    a = args
    if N == "IF":
        c = _bool(a[0]())
        if c:
            return a[1]() if len(a) > 1 and a[1] is not None else True
        return a[2]() if len(a) > 2 and a[2] is not None else False
    if N in ("IFERROR", "IFNA"):
        try:
            v = a[0]()
            v = _scalar(v) if isinstance(v, _Rng) and v.nr == 1 and v.nc == 1 else v
            if isinstance(v, _ErrV) and (N == "IFERROR" or v.code == "#N/A"):
                return a[1]()
            return v
        except _XE as e:
            if N == "IFERROR" or e.code == "#N/A":
                return a[1]()
            raise
    if N in ("ISNUMBER", "ISTEXT", "ISERROR", "ISBLANK", "ISNA"):
        try:
            v = _scalar(a[0]())
        except _XE as e:
            return N == "ISERROR" or (N == "ISNA" and e.code == "#N/A")
        if isinstance(v, _ErrV):
            return N == "ISERROR" or (N == "ISNA" and v.code == "#N/A")
        if N == "ISNUMBER":
            return isinstance(v, (int, float)) and not isinstance(v, bool)
        if N == "ISTEXT":
            return isinstance(v, str)
        if N == "ISBLANK":
            return v is None
        return False
    if N == "AND":
        r = True
        for t in a:
            v = t()
            for x in (v.flat() if isinstance(v, (_Rng, _Arr)) else [v]):
                if x is None and isinstance(v, (_Rng, _Arr)):
                    continue
                r = r and _bool(x)
        return r
    if N == "OR":
        r = False
        for t in a:
            v = t()
            for x in (v.flat() if isinstance(v, (_Rng, _Arr)) else [v]):
                if x is None and isinstance(v, (_Rng, _Arr)):
                    continue
                r = r or _bool(x)
        return r
    if N == "NOT":
        return not _bool(a[0]())
    if N == "TRUE":
        return True
    if N == "FALSE":
        return False
    if N == "CHOOSE":
        i = int(_num(a[0]()))
        if i < 1 or i >= len(a):
            raise _XE("#VALUE!")
        return a[i]()
    if N == "INDEX":
        return _index(bk, a)
    if N == "MATCH":
        return _match(a)
    if N == "OFFSET":
        return _offset(bk, a)
    if N == "INDIRECT":
        return bk.ref_text(_str(a[0]()))
    if N == "ROWS":
        v = a[0]()
        return float(v.nr if isinstance(v, (_Rng, _Arr)) else 1)
    if N == "COLUMNS":
        v = a[0]()
        return float(v.nc if isinstance(v, (_Rng, _Arr)) else 1)
    if N == "COUNTIF":
        return _countif(a)
    if N == "COUNT":
        n = 0
        for t in a:
            v = t()
            for x in (v.flat() if isinstance(v, (_Rng, _Arr)) else [v]):
                if isinstance(x, (int, float)) and not isinstance(x, bool):
                    n += 1
        return float(n)
    if N == "AGGREGATE":
        return _aggregate(a)
    if N == "PI":
        return _m.pi
    if N in ("MAX", "MIN", "SUM", "AVERAGE"):
        v = _vals(a)
        if N == "SUM":
            return sum(v)
        if N == "AVERAGE":
            if not v:
                raise _XE("#DIV/0!")
            return sum(v) / len(v)
        if not v:
            return 0.0
        return max(v) if N == "MAX" else min(v)
    if N == "SUMPRODUCT":
        arrs = [_as_arr(t) for t in a]
        tot = 0.0
        for k_ in range(len(arrs[0].flat())):
            p = 1.0
            for A_ in arrs:
                x = A_.flat()[k_]
                p *= _num(x) if isinstance(x, (int, float, bool)) and x is not None else 0.0
            tot += p
        return tot
    one = {"ABS": abs, "SQRT": None, "EXP": None, "LN": None, "LOG10": None, "SIN": _m.sin, "COS": _m.cos, "TAN": _m.tan,
           "TANH": _m.tanh, "SINH": None, "COSH": None, "RADIANS": _m.radians, "DEGREES": _m.degrees, "INT": None,
           "SIGN": None, "ATAN": _m.atan, "ASIN": None, "ACOS": None, "GAMMA": None, "EVEN": None, "ODD": None}
    if N in one:
        x = _num(_scalar(a[0]()))
        try:
            if N == "SQRT":
                if x < 0:
                    raise _XE("#NUM!")
                return _m.sqrt(x)
            if N == "EXP":
                return _m.exp(x)
            if N in ("LN", "LOG10"):
                if x <= 0:
                    raise _XE("#NUM!")
                return _m.log(x) if N == "LN" else _m.log10(x)
            if N == "SINH":
                return _m.sinh(x)
            if N == "COSH":
                return _m.cosh(x)
            if N == "INT":
                return float(_m.floor(x))
            if N == "SIGN":
                return float((x > 0) - (x < 0))
            if N == "ASIN":
                return _m.asin(x)
            if N == "ACOS":
                return _m.acos(x)
            if N == "GAMMA":
                if x <= 0 and x == int(x):
                    raise _XE("#NUM!")
                return _m.gamma(x)
            return float(one[N](x))
        except OverflowError:
            raise _XE("#NUM!")
        except ValueError:
            raise _XE("#NUM!")
    if N == "ATAN2":
        return _m.atan2(_num(a[1]()), _num(a[0]()))
    if N == "POWER":
        return _arith(a[0](), a[1](), "^")
    if N == "MOD":
        x, y = _num(a[0]()), _num(a[1]())
        if y == 0:
            raise _XE("#DIV/0!")
        return x - y * _m.floor(x / y)
    if N == "ROUND":
        return _round(a[0](), a[1]())
    if N in ("ROUNDDOWN", "ROUNDUP"):
        x, n = _num(a[0]()), int(_num(a[1]()))
        f = 10.0 ** n
        y = abs(x) * f
        y = _m.floor(y + 1e-9) if N == "ROUNDDOWN" else _m.ceil(y - 1e-9)
        return (y / f) * (1 if x >= 0 else -1)
    if N == "CEILING":
        return _ceiling(a[0](), a[1]() if len(a) > 1 else 1.0)
    if N == "FLOOR":
        x, s = _num(a[0]()), _num(a[1]())
        return float(_m.floor(x / s + 1e-12) * s) if s else 0.0
    if N == "TEXT":
        return _text(_scalar(a[0]()), a[1]())
    if N == "SUBSTITUTE":
        return _str(a[0]()).replace(_str(a[1]()), _str(a[2]()))
    if N == "LEFT":
        n = int(_num(a[1]())) if len(a) > 1 else 1
        return _str(a[0]())[:n]
    if N == "RIGHT":
        n = int(_num(a[1]())) if len(a) > 1 else 1
        s = _str(a[0]())
        return s[-n:] if n else ""
    if N == "MID":
        s, i, n = _str(a[0]()), int(_num(a[1]())), int(_num(a[2]()))
        return s[i - 1:i - 1 + n]
    if N == "LEN":
        return float(len(_str(a[0]())))
    if N == "CHAR":
        return chr(int(_num(a[0]())))
    if N == "CONCATENATE":
        return "".join(_str(t()) for t in a)
    if N == "VALUE":
        return _num(a[0]())
    if N == "NA":
        raise _XE("#N/A")
    if N == "GAMMA.DIST":
        x, al, be, cum = _num(a[0]()), _num(a[1]()), _num(a[2]()), _bool(a[3]())
        if x < 0 or al <= 0 or be <= 0:
            raise _XE("#NUM!")
        if cum:
            return _gammainc(al, x / be)
        return x ** (al - 1) * _m.exp(-x / be) / (be ** al * _m.gamma(al))
    raise _XE("#NAME?")


# ── 수식 해석 (openpyxl Tokenizer → 구문 나무 → 닫힌 함수) ──
_PREC = {":": 8, "%": 7, "^": 6, "*": 5, "/": 5, "+": 4, "-": 4, "&": 3, "=": 2, "<>": 2, "<": 2, ">": 2, "<=": 2, ">=": 2}
_RX_REF = _re.compile(r"^(?:(?P<sh>'(?:[^']|'')+'|[^!:]+)!)?(?P<a>\$?[A-Z]{1,3}\$?\d+|\$?[A-Z]{1,3}:\$?[A-Z]{1,3}|\$?\d+:\$?\d+)"
                      r"(?::(?P<b>\$?[A-Z]{1,3}\$?\d+))?$")


class _Book:
    def __init__(self, wb):
        self.wb = wb
        self.cells = {}            # (sheet, r, c) → 값 또는 수식 함수
        self.memo = {}
        self.names = {}
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if v is None:
                        continue
                    if c.data_type != "f" and isinstance(v, str) and v.startswith("="):
                        v = " " + v
                    if hasattr(v, "__class__") and v.__class__.__name__ == "CellRichText":
                        v = str(v)
                    self.cells[(ws.title, c.row, c.column)] = v
        try:
            items = wb.defined_names.items()
        except Exception:  # noqa: BLE001
            items = [(d.name, d) for d in getattr(wb.defined_names, "definedName", [])]
        for nm, d in items:
            self.names[nm.upper()] = d.attr_text
        self.compiled = {}
        self.cur_sheet = None

    def get(self, sh, r, c, soft=False):
        k = (sh, r, c)
        if k in self.memo:
            v = self.memo[k]
        else:
            v = self.cells.get(k)
            if isinstance(v, str) and v.startswith("="):
                v = self.eval_cell(k)
        if isinstance(v, _ErrV) and not soft:
            raise _XE(v.code)
        return v

    def eval_cell(self, k):
        if k in self.memo:
            return self.memo[k]
        self.memo[k] = _ErrV("#CIRC!")
        f = self.cells[k]
        try:
            fn = _compile(self, f, k[0])
            v = fn()
            v = _deref(v)
        except _XE as e:
            v = _ErrV(e.code)
        except (ZeroDivisionError,):
            v = _ErrV("#DIV/0!")
        except (OverflowError, ValueError):
            v = _ErrV("#NUM!")
        except RecursionError:
            raise
        self.memo[k] = v
        return v

    def ref_text(self, t, sheet=None):
        t = t.strip()
        if t.upper() in self.names:
            return self.ref_text(self.names[t.upper()], sheet)
        m = _RX_REF.match(t.replace("$", "") if False else t)
        if not m:
            raise _XE("#REF!")
        sh = m.group("sh")
        sh = sh[1:-1].replace("''", "'") if sh and sh.startswith("'") else (sh or sheet or self.cur_sheet)
        a = m.group("a").replace("$", "")
        b = (m.group("b") or "").replace("$", "")
        if ":" in a:                      # 열 · 행 전체
            x, y = a.split(":")
            if x.isdigit():
                return _Rng(self, sh, int(x), 1, int(y), 16384)
            return _Rng(self, sh, 1, _col2n(x), 1048576, _col2n(y))
        ma = _re.match(r"([A-Z]+)(\d+)", a)
        r1, c1 = int(ma.group(2)), _col2n(ma.group(1))
        if b:
            mb = _re.match(r"([A-Z]+)(\d+)", b)
            r2, c2 = int(mb.group(2)), _col2n(mb.group(1))
        else:
            r2, c2 = r1, c1
        return _Rng(self, sh, r1, c1, r2, c2)


def _deref(v):
    if isinstance(v, _Rng):
        if v.nr == 1 and v.nc == 1:
            x = v.cell(0, 0)
            return 0.0 if x is None else x
        return _ErrV("#VALUE!")
    if isinstance(v, _Arr):
        x = v.v[0][0]
        return 0.0 if x is None else x
    return v


def _compile(bk, f, sheet):
    key = (sheet, f)
    if key in bk.compiled:
        return bk.compiled[key]
    from openpyxl.formula.tokenizer import Tokenizer, Token
    tok = Tokenizer(f)
    items = [t for t in tok.items if t.type != Token.WSPACE]
    pos = [0]

    def peek():
        return items[pos[0]] if pos[0] < len(items) else None

    def take():
        t = items[pos[0]]
        pos[0] += 1
        return t

    def primary():
        t = take()
        if t.type == Token.OPERAND:
            if t.subtype == Token.NUMBER:
                v = float(t.value)
                return lambda v=v: v
            if t.subtype == Token.TEXT:
                s_ = t.value[1:-1].replace('""', '"')
                return lambda s_=s_: s_
            if t.subtype == Token.LOGICAL:
                b_ = t.value.upper() == "TRUE"
                return lambda b_=b_: b_
            if t.subtype == Token.ERROR:
                e_ = t.value
                return lambda e_=e_: (_ for _ in ()).throw(_XE(e_))
            # RANGE
            txt = t.value
            if txt.upper() in bk.names:
                return lambda txt=txt: bk.ref_text(bk.names[txt.upper()], sheet)
            rg = bk.ref_text(txt, sheet)
            return lambda rg=rg: rg
        if t.type == Token.FUNC and t.subtype == Token.OPEN:
            name = t.value[:-1]
            args = []
            if peek() is not None and peek().type == Token.FUNC and peek().subtype == Token.CLOSE:
                take()
            else:
                while True:
                    nx = peek()
                    if nx.type == Token.SEP and nx.subtype == Token.ARG:
                        args.append(None)
                        take()
                        continue
                    if nx.type == Token.FUNC and nx.subtype == Token.CLOSE:
                        args.append(None)
                        take()
                        break
                    args.append(expr(0))
                    nx = take()
                    if nx.type == Token.FUNC and nx.subtype == Token.CLOSE:
                        break
            return lambda name=name, args=args: _fn(bk, name, args)
        if t.type == Token.ARRAY and t.subtype == Token.OPEN:
            rows_, row_ = [], []
            while True:
                x = take()
                if x.type == Token.ARRAY and x.subtype == Token.CLOSE:
                    break
                if x.type == Token.SEP:
                    if x.subtype == Token.ROW:
                        rows_.append(row_)
                        row_ = []
                    continue
                if x.type == Token.ARRAY:
                    continue
                if x.subtype == Token.NUMBER:
                    row_.append(float(x.value))
                elif x.subtype == Token.TEXT:
                    row_.append(x.value[1:-1].replace(chr(34) * 2, chr(34)))
                elif x.subtype == Token.LOGICAL:
                    row_.append(x.value.upper() == "TRUE")
            rows_.append(row_)
            arr_ = _Arr([r_ for r_ in rows_ if r_])
            return lambda arr_=arr_: arr_
        if t.type == Token.PAREN and t.subtype == Token.OPEN:
            e = expr(0)
            take()
            return e
        if t.type == Token.OP_PRE:
            sub = expr(7)                 # 단항 부호 : ^ 보다 먼저 (Excel)
            if t.value == "-":
                return lambda sub=sub: _binop(-1.0, _val(sub()), "*")
            return sub
        if t.type == Token.OPERAND and False:
            pass
        raise _XE("#NAME?")

    def expr(minp):
        lhs = primary()
        while True:
            t = peek()
            if t is None:
                break
            if t.type == Token.OP_POST:
                take()
                lhs = (lambda l=lhs: _num(l()) / 100.0)
                continue
            if t.type != Token.OP_IN:
                break
            op = t.value
            p = _PREC.get(op, 0)
            if p < minp or (p == minp and op != "^" and False):
                break
            if p <= minp - 1:
                break
            take()
            rhs = expr(p + 1)       # 좌결합 (^ 도 Excel 은 좌결합)
            if op == ":":
                lhs = (lambda l=lhs, r=rhs: _union(bk, l(), r()))
            else:
                lhs = (lambda l=lhs, r=rhs, op=op: _binop(_val(l()), _val(r()), op))
        return lhs
    e = expr(0)
    bk.compiled[key] = e
    return e


def _union(bk, a, b):
    if isinstance(a, _Rng) and isinstance(b, _Rng):
        return _Rng(bk, a.sh, min(a.r1, b.r1), min(a.c1, b.c1), max(a.r2, b.r2), max(a.c2, b.c2))
    raise _XE("#REF!")


def _val(v):
    if isinstance(v, _Rng) and v.nr == 1 and v.nc == 1:
        x = v.cell(0, 0)
        return x
    return v


def evaluate(xlsx_bytes):
    """→ (openpyxl 워크북, {(시트, 행, 열): 값})"""
    import sys as _sys
    import threading as _th
    import openpyxl
    wb = openpyxl.load_workbook(_io.BytesIO(xlsx_bytes))
    bk = _Book(wb)
    res, err = {}, []

    def run():
        try:
            for k, v in list(bk.cells.items()):
                if isinstance(v, str) and v.startswith("="):
                    res[k] = bk.eval_cell(k)
        except BaseException as e:  # noqa: BLE001
            err.append(e)
    old = _sys.getrecursionlimit()
    _sys.setrecursionlimit(200000)
    try:
        _th.stack_size(512 * 1024 * 1024)
    except Exception:  # noqa: BLE001
        pass
    t = _th.Thread(target=run)
    t.start()
    t.join()
    _sys.setrecursionlimit(old)
    try:
        _th.stack_size(0)
    except Exception:  # noqa: BLE001
        pass
    if err:
        raise err[0]
    wb._pjx_book = bk
    return wb, res


def _refs(bk, f, sheet):
    """수식이 참조하는 범위들 (이름 포함)"""
    from openpyxl.formula.tokenizer import Tokenizer, Token
    out = []
    try:
        for t in Tokenizer(f).items:
            if t.type == Token.OPERAND and t.subtype == Token.RANGE:
                try:
                    v = bk.ref_text(bk.names.get(t.value.upper(), t.value), sheet)
                    out.append(v)
                except _XE:
                    pass
    except Exception:  # noqa: BLE001
        pass
    return out


def _sheet_files(zin):
    """xl/worksheets/*.xml → 시트 이름"""
    wbx = zin.read("xl/workbook.xml").decode("utf-8")
    rels = zin.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    rid2t = {}
    for m in _re.finditer(r"<Relationship\b([^>]*)/?>", rels):
        a = m.group(1)
        i_, t_ = _re.search(r'\bId="([^"]+)"', a), _re.search(r'\bTarget="([^"]+)"', a)
        if i_ and t_:
            rid2t[i_.group(1)] = t_.group(1)
    out = {}
    for m in _re.finditer(r"<(?:\w+:)?sheet\b([^>]*)/?>", wbx):
        a = m.group(1)
        nm, rid = _re.search(r'\bname="([^"]+)"', a), _re.search(r'\br:id="([^"]+)"', a)
        if not (nm and rid):
            continue
        tgt = rid2t.get(rid.group(1), "").lstrip("/")
        tgt = tgt if tgt.startswith("xl/") else "xl/" + tgt
        out[tgt] = (nm.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                    .replace("&quot;", '"').replace("&apos;", "'"))
    return out


def _is_input_fill(rgb):
    """입력칸 바탕 (연한 노랑 계열) — 잠금 풀 칸"""
    rgb = (rgb or "")[-6:].upper()
    if len(rgb) != 6:
        return False
    r, g, b = int(rgb[0:2], 16), int(rgb[2:4], 16), int(rgb[4:6], 16)
    return r >= 0xF0 and g >= 0xEF and b <= 0xE0 and b < g


def freeze_picker(wb, spec):
    """spec = [(시트 이름 또는 '*', 시작 열, 시작 행 또는 '그 행 글자로 시작')] → pick(시트, 행, 열)"""
    rules = []
    for sh, c0, r0 in spec or []:
        names = [ws.title for ws in wb.worksheets] if sh == "*" else [sh]
        for nm in names:
            if nm not in wb.sheetnames:
                continue
            rr = r0
            if isinstance(r0, str):
                rr = None
                for row in wb[nm].iter_rows():
                    for c in row:
                        if isinstance(c.value, str) and c.value.startswith(r0):
                            rr = c.row
                            break
                    if rr:
                        break
                if rr is None:
                    continue
            rules.append((nm, int(c0), int(rr)))
    return lambda sh, r, c: any(sh == a and c >= b and r >= d for a, b, d in rules)


def xl_rewrite(xlsx_bytes, freeze=None, protect=False, hide=()):
    """계산기로 모든 수식 값을 구해
    · freeze 구역(spec) 칸 = 수식을 지우고 값만 (기본 판 : 도표 판독 · 반복 계산을 내려받을 때 값으로 고정)
    · 나머지 수식 칸 = 수식 그대로 + 계산값 저장 (미리보기에서도 값이 보임)
    · protect = 수식 칸 잠금(비밀번호 없음, 입력칸만 열림) · hide = 숨길 시트 이름"""
    import zipfile as _zf
    from xml.sax.saxutils import escape as _esc
    wb, res = evaluate(xlsx_bytes)
    pick0 = freeze_picker(wb, freeze) if freeze else (lambda sh, r, c: False)
    bk = wb._pjx_book
    frz = set()
    if freeze:
        for (sh, r, c) in res:
            if pick0(sh, r, c):
                frz.add((sh, r, c))
            else:                       # 고정 구역을 참조하는 칸도 값으로 (자동 판독값을 이어받는 칸)
                f_ = bk.cells.get((sh, r, c))
                for rg in _refs(bk, f_, sh):
                    if pick0(rg.sh, rg.r1, rg.c1) or pick0(rg.sh, rg.r2, rg.c2):
                        frz.add((sh, r, c))
                        break
    pick = lambda sh, r, c: (sh, r, c) in frz
    zin = _zf.ZipFile(_io.BytesIO(xlsx_bytes))
    sheets = _sheet_files(zin)
    by_sheet = {}
    for (sh, r, c), v in res.items():
        by_sheet.setdefault(sh, {})[f"{_n2col(c)}{r}"] = (v, pick(sh, r, c))

    def vxml(v):
        if isinstance(v, _ErrV):
            return ' t="e"', f"<v>{_esc(v.code if v.code != '#CIRC!' else '#REF!')}</v>"
        if isinstance(v, bool):
            return ' t="b"', f"<v>{1 if v else 0}</v>"
        if isinstance(v, (int, float)):
            return "", f"<v>{repr(float(v))}</v>"
        if v is None:
            return "", ""
        return ' t="str"', f"<v>{_esc(str(v))}</v>"

    def cellxml(m, vals):
        attrs, body = m.group(1), m.group(2)
        mr = _re.search(r'\br="([A-Z]+\d+)"', attrs)
        if not mr or "<f" not in body or mr.group(1) not in vals:
            return m.group(0)
        v, frz = vals[mr.group(1)]
        attrs = _re.sub(r'\s+t="[^"]*"', "", attrs)
        t_, vx = vxml(v)
        if frz:
            if t_ == ' t="str"':
                return f'<c{attrs} t="inlineStr"><is><t xml:space="preserve">{_esc(str(v))}</t></is></c>'
            return f"<c{attrs}{t_}>{vx}</c>" if vx else f"<c{attrs}/>"
        fm = _re.search(r"<f\b[^>]*>.*?</f>|<f\b[^>]*/>", body, _re.S)
        return f"<c{attrs}{t_}>{fm.group(0) if fm else ''}{vx}</c>"
    unlock = set()
    if protect and "xl/styles.xml" in zin.namelist():
        st = zin.read("xl/styles.xml").decode("utf-8")
        fills = _re.search(r"<fills\b[^>]*>(.*?)</fills>", st, _re.S)
        fl = _re.findall(r"<fill\b.*?</fill>|<fill\b[^>]*/>", fills.group(1), _re.S) if fills else []
        inp_fill = {i for i, x in enumerate(fl) if _is_input_fill((_re.search(r'<fgColor\b[^>]*rgb="([0-9A-Fa-f]{6,8})"', x) or [None, ""])[1])}
        cx = _re.search(r"(<cellXfs\b[^>]*>)(.*?)(</cellXfs>)", st, _re.S)
        if cx:
            xfs = _re.findall(r"<xf\b[^>]*/>|<xf\b[^>]*>.*?</xf>", cx.group(2), _re.S)
            new = []
            for x in xfs:
                fid = _re.search(r'\bfillId="(\d+)"', x)
                if fid and int(fid.group(1)) in inp_fill:
                    x = _re.sub(r"<protection\b[^>]*/>", "", x)
                    if x.endswith("/>"):
                        x = x[:-2] + '><protection locked="0"/></xf>'
                    else:
                        x = x.replace("</xf>", '<protection locked="0"/></xf>')
                    if "applyProtection" not in x:
                        x = x.replace("<xf ", '<xf applyProtection="1" ', 1)
                new.append(x)
            st = st[:cx.start(2)] + "".join(new) + st[cx.end(2):]
        unlock = {"xl/styles.xml": st}
    out = _io.BytesIO()
    rx = _re.compile(r"<c\b([^>]*?)(?:/>|>(.*?)</c>)", _re.S)
    with _zf.ZipFile(out, "w", _zf.ZIP_DEFLATED) as zo:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename in sheets:
                vals = by_sheet.get(sheets[it.filename], {})
                x = data.decode("utf-8")
                if vals:
                    x = rx.sub(lambda m: cellxml(m, vals) if m.group(2) is not None else m.group(0), x)
                if protect and sheets[it.filename] not in hide and "<sheetProtection" not in x:
                    x = x.replace("</sheetData>", '</sheetData><sheetProtection sheet="1" objects="1" scenarios="1" '
                                  'formatColumns="0" formatRows="0" selectLockedCells="0" selectUnlockedCells="0"/>', 1)
                data = x.encode("utf-8")
            elif it.filename == "xl/workbook.xml":
                x = data.decode("utf-8")
                x = _re.sub(r'\s+fullCalcOnLoad="[^"]*"', "", x)
                for nm in hide:
                    def _h(m, nm=nm):
                        t = m.group(0)
                        if f'name="{_esc(nm)}"' not in t:
                            return t
                        t = _re.sub(r'\s+state="[^"]*"', "", t)
                        return t.replace("<sheet ", '<sheet state="hidden" ', 1) if "<sheet " in t else t
                    x = _re.sub(r"<(?:\w+:)?sheet\b[^>]*/>", _h, x)
                data = x.encode("utf-8")
            elif it.filename in unlock:
                data = unlock[it.filename].encode("utf-8")
            elif it.filename == "xl/calcChain.xml":
                continue
            zo.writestr(it, data)
    return out.getvalue()


def xl_cache(xlsx_bytes):
    """[2026-11-10] 수식은 그대로 두고 계산값만 함께 저장 (미리보기 · 휴대폰 뷰어에서 빈칸 방지, 검증보고서 R-1).
    계산기가 못 푼 칸(오류)은 값을 넣지 않음 (그 칸만 지금처럼 빈칸), Excel 로 열면 원래대로 전체 재계산 (fullCalcOnLoad)."""
    import zipfile as _zf
    from xml.sax.saxutils import escape as _esc
    zin = _zf.ZipFile(_io.BytesIO(xlsx_bytes))
    sheets = _sheet_files(zin)
    for fn in sheets:                       # 이미 계산값이 들어 있으면 (두 판 Excel 등) 그대로
        if _re.search(r"</f>\s*<v>[^<]", zin.read(fn).decode("utf-8", "ignore")):   # 빈 <v></v> 는 값 없음
            return xlsx_bytes
    wb, res = evaluate(xlsx_bytes)
    by_sheet = {}
    for (sh, r, c), v in res.items():
        if isinstance(v, _ErrV) or v is None:
            continue
        by_sheet.setdefault(sh, {})[f"{_n2col(c)}{r}"] = v

    def vxml(v):
        if isinstance(v, bool):
            return ' t="b"', f"<v>{1 if v else 0}</v>"
        if isinstance(v, (int, float)):
            return "", f"<v>{repr(float(v))}</v>"
        return ' t="str"', f"<v>{_esc(str(v))}</v>"

    def cellxml(m, vals):
        attrs, body = m.group(1), m.group(2)
        mr = _re.search(r'\br="([A-Z]+\d+)"', attrs)
        if not mr or "<f" not in body or mr.group(1) not in vals or _re.search(r"<v>[^<]", body):
            return m.group(0)
        attrs = _re.sub(r'\s+t="[^"]*"', "", attrs)
        t_, vx = vxml(vals[mr.group(1)])
        fm = _re.search(r"<f\b[^>]*>.*?</f>|<f\b[^>]*/>", body, _re.S)
        return f"<c{attrs}{t_}>{fm.group(0) if fm else ''}{vx}</c>"
    out = _io.BytesIO()
    rx = _re.compile(r"<c\b([^>]*?)(?:/>|>(.*?)</c>)", _re.S)
    with _zf.ZipFile(out, "w", _zf.ZIP_DEFLATED) as zo:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename in sheets and by_sheet.get(sheets[it.filename]):
                vals = by_sheet[sheets[it.filename]]
                data = rx.sub(lambda m: cellxml(m, vals) if m.group(2) is not None else m.group(0),
                              data.decode("utf-8")).encode("utf-8")
            elif it.filename == "xl/workbook.xml":
                x = data.decode("utf-8")
                if "fullCalcOnLoad" not in x:
                    if _re.search(r"<(?:\w+:)?calcPr\b", x):
                        x = _re.sub(r"<((?:\w+:)?calcPr)\b", r'<\1 fullCalcOnLoad="1"', x, 1)
                    else:
                        x = _re.sub(r"</(\w+:)?workbook>", lambda m: f'<{m.group(1) or ""}calcPr fullCalcOnLoad="1"/></{m.group(1) or ""}workbook>', x, 1)
                data = x.encode("utf-8")
            elif it.filename == "xl/calcChain.xml":
                continue
            zo.writestr(it, data)
    return out.getvalue()'''
_PJX_NS = {}


def _pjx():
    if "m" not in _PJX_NS:
        import types as _ty
        m = _ty.ModuleType("_pj_xleval")
        exec(compile(_PJX_SRC, "_pj_xleval", "exec"), m.__dict__)
        _PJX_NS["m"] = m
    return _PJX_NS["m"]


def _pj_xl_dual(label, make_basic, make_full, file_name, key, basic_post=None, dg=None, **kw):
    """[2026-10-23] Excel 계산서 두 판 (사용자 결정)
    · 일반 판 (모두) : 기본 산식은 살아 있고, 도표 독취 · 시산(반복)은 사람이 — 도표 그림은 그대로, 자동 판독 구역은 값으로 고정 · 숨김
    · 전부 자동 판 (매니저) : 앱과 같은 자동 독취 · 반복 계산 (입력만 바꾸면 전부 다시 계산)"""
    import os as _os
    dg = dg or st

    def _basic():
        b = make_basic()
        try:
            b = _pjx().xl_rewrite(b, **(basic_post or {}))
        except Exception:  # noqa: BLE001 — 고정 처리 실패 시 일반 판 원본 그대로
            pass
        return b

    def _full():
        b = make_full()
        try:
            b = _pjx().xl_rewrite(b)                 # 수식 그대로 + 계산값 저장 (미리보기에서도 값)
        except Exception:  # noqa: BLE001
            pass
        return b
    dg.download_button(label, _basic, file_name=file_name, key=key, **kw)
    stem, ext = _os.path.splitext(file_name)
    if st.session_state.get("_mgr_ok"):
        dg.download_button("🧮 전부 자동 판 (앱과 같은 자동 독취 · 반복)", _full, file_name=f"{stem}_전부자동{ext}", key=key + "_full", **kw)
    elif _pj_mgr_key() and _pj_mgr_door():
        with dg.expander("🧮 전부 자동 판", expanded=False):
            st.caption("도표 자동 독취 · 반복 계산까지 앱과 같은 Excel")
            _pj_mgr_ok(key=key + "_pw")



def _pj_pname_from(fname, app=None):
    """저장 파일 이름 '프로그램명-프로젝트명(YYYY-MM-DD).json' 에서 프로젝트명 (없으면 '').
    app = 지금 그리는 앱 이름 (다운로드 감싸기는 프로세스에 한 번 만들어져 _PJ 가 처음 앱 것이므로 세션의 _pj_ctx 로 넘김)"""
    import re as _re
    f = str(fname or "")
    m = _re.fullmatch(r"(.*)\(\d{4}-\d{2}-\d{2}\)\.json", f, _re.I)
    if not m:
        return ""
    s = m.group(1)
    app = _re.sub(r'[\\/:*?"<>|]+', " ", str(app if app is not None else (_PJ.get("app") or ""))).strip()
    if app and s.startswith(app + "-"):
        return s[len(app) + 1:].strip()
    return ""


def _pj_own_put(hook, project, data):
    """앱 자체 저장 파일을 보관함에 (프로젝트명 · 파일 전체) — 실패해도 내려받기는 그대로. data 를 그대로 돌려줌"""
    try:
        hook(project=project or None, own=data)
    except TypeError:                  # 예전 보관 함수(인자 없음)
        try:
            hook()
        except Exception:  # noqa: BLE001
            pass
    except Exception:  # noqa: BLE001
        pass
    return data


def _pj_keep_deferred(mm, items):
    """[2026-11-09] 💾 저장 단추의 지연 다운로드 등록을 프로세스에 잠깐 보관.
    Streamlit 은 상자가 다시 그려질 때 옛 등록을 지움 → 느린 서버(Cloud)에서 다시 그려지는 사이에 누른 첫 누름이
    '등록 없음'으로 사라짐. 실행 때 등록이 없으면 보관본을 되넣어 그대로 저장되게 함 (내용 · 파일 이름은 누르는 순간 값).
    [2026-11-24] 보관 = 최근 2 개 · 2 분까지만. 등록 하나 (저장 함수) 가 그 화면 실행의 모든 자료 (그림 · 표 · 3D 모양) 를 붙잡고 있어,
    300 개씩 보관하니 화면을 다시 그릴 때마다 메모리가 쌓였음 (32번 울산 2-2 예제 : 한 번에 +50 MB → Cloud 'Oh no')."""
    import sys as _sy, collections as _co, time as _tm
    keep = getattr(_sy, "_pj_dl_keep", None)
    if keep is None:
        keep = _co.OrderedDict()
        _sy._pj_dl_keep = keep
    now = _tm.time()
    for k, e in items:
        keep[k] = (now, e)
        keep.move_to_end(k)
    for k in [k_ for k_, v_ in keep.items() if not isinstance(v_, tuple) or now - v_[0] > 120.0]:
        keep.pop(k, None)
    while len(keep) > 2:
        keep.popitem(last=False)
    if getattr(mm, "_pj_keep_patched", False):
        return
    orig = mm.execute_deferred

    def ex(file_id, _o=orig, _m=mm):
        try:
            with _m._lock:
                _v = _sy._pj_dl_keep.get(file_id)
                if file_id not in _m._deferred_callables and isinstance(_v, tuple):
                    _m._deferred_callables[file_id] = _v[1]
        except Exception:  # noqa: BLE001
            pass
        return _o(file_id)
    mm.execute_deferred = ex
    mm._pj_keep_patched = True


def _pj_patch_download():
    """st.download_button (컬럼 · 사이드바 포함) 이 내려주는 파일에 계산 정보를 붙이도록 감쌈 — 프로세스에 한 번"""
    from streamlit.delta_generator import DeltaGenerator as _DG
    cur = _DG.download_button
    if getattr(cur, "_pj_ver", None) == _PJ_VER:
        return
    orig = getattr(cur, "_pj_orig", cur)

    def wrap(self, *a, **k):
        a = list(a)
        fname = k.get("file_name") if "file_name" in k else (a[2] if len(a) > 2 else None)
        if "data" in k:
            d, put = k["data"], lambda x: k.__setitem__("data", x)
        elif len(a) > 1:
            d, put = a[1], lambda x: a.__setitem__(1, x)
        else:
            return orig(self, *a, **k)
        S = _pj_S()                    # 누르는 순간 만들어지는 파일(함수로 넘긴 data)도 이 접속의 입력값으로
        try:                           # [2026-10-22] 🗄 보관함 앱 : 앱 자체 JSON 저장을 누르면 그때 입력제원 보관
            hook = S["_pj_lib_hook"] if "_pj_lib_hook" in S else None
            ctx_ = S["_pj_ctx"] if "_pj_ctx" in S else {}
            pn_ = _pj_pname_from(fname, ctx_.get("app", ""))   # [2026-10-26] 앱 자체 저장(14 · 29 · 30)의 프로젝트명 = 저장 파일 이름에서
            if hook and str(fname or "").lower().endswith(".json") and not str(k.get("key") or "").startswith("_pj_dl"):
                # [2026-10-26] 앱 자체 저장(14 · 29 · 30) : 이 앱이 만든 보관 함수에 프로젝트명 + 내려주는 프로젝트 파일 전체를 넘김
                #   (보관함에서 고르면 그 파일을 앱 자체 불러오기로 되살림 — 기준점 · 관측소 · 표 등 입력칸 밖 상태까지)
                if callable(d):          # 누르는 순간 파일을 만드는 경우 — 만들 때 보관
                    d = (lambda _f=d, _h=hook, _p=pn_: _pj_own_put(_h, _p, _f()))
                else:
                    h2 = (lambda *x, _h=hook, _p=pn_, _d=d, **y: _pj_own_put(_h, _p, _d))
                    oc = k.get("on_click")
                    if oc is None:
                        k["on_click"] = h2
                    elif callable(oc):
                        def _both(*x, _o=oc, _h=h2, **y):
                            _h()
                            return _o(*x, **y)
                        k["on_click"] = _both
        except Exception:  # noqa: BLE001
            pass
        if callable(d):
            put(lambda _f=d, _S=S: _pj_stamp(_f(), fname, _S))
        elif str(fname or "").lower().rsplit(".", 1)[-1] in ("html", "htm", "doc", "xlsx", "xlsm", "docx"):
            # [2026-11-20] 미리 만든 보고서도 계산 정보 · 수식 스크립트 (MathJax 약 2 MB) 는 누르는 순간 붙임 —
            #  전에는 화면을 그릴 때마다 붙여 접속마다 서버 메모리에 2 MB 넘게 더 잡혔음 (Streamlit Cloud 'Oh no')
            put(lambda _d=d, _S=S: _pj_stamp(_d, fname, _S))
        else:
            put(_pj_stamp(d, fname, S))
        return orig(self, *a, **k)

    wrap._pj_ver, wrap._pj_orig = _PJ_VER, orig
    _DG.download_button = wrap
    try:
        st.download_button = st._main.download_button
    except Exception:  # noqa: BLE001
        pass


def _pj_block():
    import datetime as _dt, hashlib as _hl, json as _js, os as _os
    ss, S = st.session_state, _pj_S()
    # (1) 불러온 값 적용 — 입력란이 만들어지기 전
    p = ss.pop("_pj_pending", None)
    ss["_pj_loaded"] = bool(p)          # 불러온 실행에서는 _pj_k 가 값을 지우지 않음
    if p:
        n, ok_keys, types = 0, _pj_widget_keys(S), p.get("types") or {}
        for k, v in (p.get("inputs") or {}).items():
            if k not in ok_keys or v is None:
                continue
            try:
                ss[k] = _pj_dec(v, types.get(k, ""))
                n += 1
            except Exception:  # noqa: BLE001
                pass
        nt = 0
        for t, pl in (p.get("tables") or {}).items():          # 표 — 바탕 표로 넣고 편집 기록은 비움
            if t not in (_PJ.get("tables") or {}):
                continue
            v = _pj_tdec(pl)
            if v is None:
                continue
            ss.setdefault("_pj_tbase", {})[t] = (v, None)
            if _PJ["tables"][t]:
                ss.pop(_PJ["tables"][t], None)
            nt += 1
        if p.get("project"):
            ss["_pj_pname"] = str(p["project"])
        ss["_pj_msg"] = (f"불러왔습니다 (저장 {p.get('saved', '-')}) — 입력 {n}개" + (f" · 표 {nt}개" if nt else "") + " 반영")
    # (2) 계산 정보 (프로그램 판 = 파일 수정일 + 코드 지문, 입력 지문 = 저장 대상 입력값 지문)
    try:
        src = _os.path.abspath(__file__)
        mt = _os.path.getmtime(src)
        cache = st.session_state.setdefault("_pj_hash", {})
        if cache.get(src, (None,))[0] != mt:
            with open(src, "rb") as f:
                cache[src] = (mt, _hl.md5(f.read()).hexdigest()[:8])
        ver = f"{_dt.datetime.fromtimestamp(mt):%Y-%m-%d} 수정 · 코드 {cache[src][1]}"
    except Exception:  # noqa: BLE001
        ver = "-"
    ss["_pj_ctx"] = {"app": _PJ["app"], "ver": ver, "basis": _PJ["basis"],
                     "kds": ", ".join(c for c, _y, _n in _PJ["kds"][:8]) + (" 외" if len(_PJ["kds"]) > 8 else "")}
    if _PJ.get("lib"):
        ss["_pj_lib_hook"] = lambda project=None, own=None: _pj_lib_put(dict(
            _pj_body(_pj_S()), **({"project": project} if project else {}), **({"own": own} if own is not None else {})))
    else:
        ss.pop("_pj_lib_hook", None)
    _pj_patch_download()
    ss["_pj_ver_txt"] = ver
    # (3) 💾 · 🧾 · 📚 는 입력란 맨 아래(입력 상자가 없는 앱은 화면 맨 아래)에 — _pj_end() 가 그림 (사이드바는 페이지 목록만)
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx as _ctx
        ss["_pj_on_stop"] = (getattr(_ctx(), "page_script_hash", None), _pj_end)
    except Exception:  # noqa: BLE001
        pass
    _pj_patch_stop()
    _pj_patch_eqimg()
    _pj_patch_mpl_lock()
    _pj_patch_latex()
    _pj_mpl_cache_clear()


def _pj_mpl_cache_clear():
    """[2026-11-20] matplotlib 글꼴 · 수식 캐시 비우기 (실행마다 처음 · 끝) — 캐시 열쇠에 스레드 번호가 들어가
    (font_manager.get_font 의 thread_id), Streamlit 이 다시 그릴 때마다 새 스레드라 글꼴 · 수식 글꼴 덩어리가 계속 쌓임
    → 서버 메모리 한도 초과 ('Oh no'). 13번 시험 : 다시 그릴 때마다 +85 MB → +8 MB. 쓰는 중인 그림은 자기 참조가 있어 안전"""
    try:
        import matplotlib.font_manager as _fm
        import matplotlib.mathtext as _mmt
        _fm._get_font.cache_clear()
        _mmt.MathTextParser._parse_cached.cache_clear()
    except Exception:  # noqa: BLE001
        pass


def _pj_tex_split(s, lim=60):
    """[2026-11-17] 긴 수식을 위아래 줄로 (좁은 화면 잘림 방지) — 맨 바깥(중괄호 · \\left…\\right 밖)에서
    ① \\qquad · ',\\quad' · ',\\ ' · '\\quad (' 로 나누고 ② 그래도 긴 조각이 '=' 를 둘 넘게 이으면 '=' 앞에서 나눠 맞춤.
    이미 여러 줄(\\\\ · \\begin)인 식 · 짧은 식 · 나눌 곳이 없는 식은 그대로"""
    return s          # [2026-11-18] 사용자 '원래대로 — 줄을 나누니 여백이 많아 화면 구성이 안 좋음' → 나누지 않음 (아래 코드는 남겨 둠)
    if not isinstance(s, str) or len(s) < lim or "\\\\" in s or "\\begin" in s:
        return s

    def scan(x, at_eq=False):
        parts, cur, dep, lr, i, n = [], [], 0, 0, 0, len(x)
        while i < n:
            c = x[i]
            if c == "\\":
                m = i + 1
                while m < n and x[m].isalpha():
                    m += 1
                w = x[i + 1:m]
                top = dep == 0 and lr == 0
                if m == i + 1:                         # \{ \, \; \  같은 한 글자 명령
                    if (not at_eq and top and x[i + 1:i + 2] == " " and "".join(cur).rstrip().endswith(",")):
                        parts.append("".join(cur))
                        cur = []
                        i += 2
                        continue
                    cur.append(x[i:i + 2])
                    i += 2
                    continue
                if w == "left":
                    lr += 1
                elif w == "right":
                    lr -= 1
                if not at_eq and top and w in ("qquad", "quad"):
                    prev = "".join(cur).rstrip()
                    nxt = x[m:].lstrip()
                    if w == "qquad" or prev.endswith(",") or nxt.startswith("("):
                        parts.append(prev)
                        cur = []
                        i = m
                        continue
                cur.append(x[i:m])
                i = m
                continue
            if c == "{":
                dep += 1
            elif c == "}":
                dep -= 1
            elif at_eq and c == "=" and dep == 0 and lr == 0:
                parts.append("".join(cur))
                cur = []
                i += 1
                continue
            cur.append(c)
            i += 1
        parts.append("".join(cur))
        return parts, dep == 0 and lr == 0

    parts, ok = scan(s)
    if not ok:
        return s
    parts = [p.strip().rstrip(",").rstrip() for p in parts if p.strip().strip(",").strip()]
    out = []
    for p in parts:
        q, ok2 = scan(p, at_eq=True)
        q = [y.strip() for y in q]
        if ok2 and len(p) > lim and len(q) >= 3 and all(q):
            out.append("\\begin{aligned}" + q[0] + " &= " + q[1] + "".join(" \\\\ &= " + y for y in q[2:]) + "\\end{aligned}")
        else:
            out.append(p)
    if len(out) == 1 and out[0] == s.strip():
        return s
    if len(out) == 1:
        return out[0]
    return "\\begin{gathered}" + " \\\\ ".join(out) + "\\end{gathered}"


def _pj_patch_latex():
    """[2026-11-17] 좁은 화면(휴대폰)에서 긴 수식이 잘려 보이던 것 — st.latex 를 감싸 \\qquad · ',\\quad' 로 이은 긴 식을 위아래 줄로 (프로세스에 한 번)"""
    try:
        from streamlit.delta_generator import DeltaGenerator as _DG
    except Exception:  # noqa: BLE001
        return
    _DG._pj_split = staticmethod(_pj_tex_split)          # 늘 이번 실행의 최신 함수 (프로세스에 남은 옛 감싸기도 이것을 씀)
    cur = _DG.latex
    if getattr(cur, "_pj_ver", None) == _PJ_VER:
        return
    orig = getattr(cur, "_pj_orig", cur)

    def latex(self, body, *a, **k):
        try:
            body = _DG._pj_split(body)
        except Exception:  # noqa: BLE001
            pass
        return orig(self, body, *a, **k)
    latex._pj_ver, latex._pj_orig = _PJ_VER, orig
    _DG.latex = latex
    try:
        st.latex = lambda body, *a, **k: latex(st._main, body, *a, **k)
    except Exception:  # noqa: BLE001
        pass


_PJ_TEX_CSS = ("<style>.katex-display{overflow-x:auto;overflow-y:hidden;padding-bottom:2px}"
               ".katex-display::-webkit-scrollbar{height:6px}.katex-display::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:3px}"
               "@media (max-width:640px){.katex-display>.katex{font-size:1.0em}}</style>")


def _pj_patch_mpl_lock():
    """[2026-10-26] Streamlit Cloud 는 모든 앱 · 접속이 한 프로세스의 여러 스레드 — matplotlib 수식 해석기(전역 1개) ·
    Agg 그리기는 동시 사용에 안전하지 않아 'ValueError (mathtext)' · 프로세스 중단이 남 (12번 plot_q_crest 오류).
    해석 · 배치 맞추기 · 그리기 · 저장을 프로세스 공용 잠금 하나로 한 번에 하나씩 (프로세스에 한 번, 앱끼리 같은 잠금)"""
    try:
        import functools as _ft
        import threading as _th
        import matplotlib as _m
        import matplotlib.mathtext as _mt
        import matplotlib.figure as _mf
        from matplotlib.backends import backend_agg as _ba
    except Exception:  # noqa: BLE001
        return
    lk = getattr(_m, "_pj_lock", None)
    if lk is None:
        lk = _m._pj_lock = _th.RLock()
    for cls, name in ((_mt.MathTextParser, "parse"), (_ba.FigureCanvasAgg, "draw"), (_ba.FigureCanvasAgg, "print_figure"),
                      (_mf.Figure, "tight_layout"), (_mf.Figure, "savefig")):
        f = getattr(cls, name, None)
        if f is None or getattr(f, "_pj_lock", False):
            continue

        @_ft.wraps(f)                     # __qualname__ 등 원래 그대로 — pyplot 불러올 때 'Wrapped method from unexpected class' 방지
        def g(*a, _f=f, **k):
            with lk:
                return _f(*a, **k)
        g._pj_lock = True
        setattr(cls, name, g)


_PJ_PANEL ={"c": None, "done": False}        # 이 실행의 입력 상자 · 그렸는지 (실행마다 새로 만들어짐)


def _pj_in(c):
    """입력 상자(컨테이너)를 기억 → 실행 끝에 그 아래에 💾 · 🧾 · 📚 를 붙임"""
    _PJ_PANEL["c"] = c
    return c


def _pj_credit(extra=None):
    """제작자 표시 — 제목 바로 밑 (모든 앱 같은 모양 : Made by 이름 @ 소속 · 판 · ©)"""
    import html as _h
    cr = _PJ.get("credit")
    try:
        pass                                                   # [2026-11-18] 긴 수식 CSS 도 원래대로 (사용자)
    except Exception:  # noqa: BLE001
        pass
    if cr:
        tail = (f" · {_h.escape(str(extra))}" if extra else "") + " · © 2026 All rights reserved."
        st.markdown(f"<div style='font-size:0.82rem;color:#5A6B7D;margin:-0.4rem 0 0.6rem'>Made by "
                    f"<b style='color:#14263A'>{_h.escape(cr)}</b>{tail}</div>", unsafe_allow_html=True)


def _pj_patch_eqimg():
    """[2026-10-22] 검증보고서 참고 항목 (5-3 · 7-3 등) : 보고서 수식 그림을 외부 서버(latex.codecogs.com)로 보내지 않고
    앱 안에서 matplotlib 로 그림 — urllib.request.urlopen 의 codecogs 요청만 가로챔 (프로세스에 한 번)"""
    import urllib.request as _ur
    cur = _ur.urlopen
    if getattr(cur, "_pj_ver", None) == _PJ_VER:
        return
    orig = getattr(cur, "_pj_orig", cur)

    def _render(url):
        import io as _io, re as _re, urllib.parse as _up
        from matplotlib.figure import Figure
        q = url.split("?", 1)[1] if "?" in url else url
        tex = _up.unquote(q.replace("&space;", " "))
        m = _re.search(r"\\dpi\{(\d+)\}", tex)
        dpi = int(m.group(1)) if m else 120
        tex = _re.sub(r"\\dpi\{\d+\}|\\bg_white|\\bg\{[^}]*\}|\\inline|\\large|\\Large|\\normalsize", " ", tex).strip()
        tex = tex.replace(r"\dfrac", r"\frac").replace(r"\tfrac", r"\frac").replace(r"\therefore", r"\Rightarrow")
        tex = _re.sub(r"\\text\{([^}]*)\}", r"\\mathrm{\1}", tex)
        tex = _re.sub(r"\\(le|ge|ne)(?![a-zA-Z])", r"\\\1q", tex).replace(r"\fallingdotseq", r"\approx").replace(r"\coloneqq", "=")
        for cand in (tex, tex.replace(r"\left", "").replace(r"\right", ""), _re.sub(r"\\mathrm\{[^}]*[가-힣][^}]*\}", "", tex)):
            try:
                fig = Figure(figsize=(0.1, 0.1))
                fig.text(0, 0, f"${cand}$", fontsize=12)
                buf = _io.BytesIO()
                fig.savefig(buf, format="png", dpi=max(80, min(dpi, 200)), bbox_inches="tight", pad_inches=0.03, facecolor="white")
                return buf.getvalue()
            except Exception:  # noqa: BLE001
                continue
        return None

    class _Resp:
        def __init__(self, data):
            self._b, self.status, self.code = data, 200, 200
        def read(self, *a): return self._b
        def getcode(self): return 200
        def close(self): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False

    def urlopen(url, *a, **k):
        u = getattr(url, "full_url", url)
        if isinstance(u, str) and "latex.codecogs.com" in u:
            data = _render(u)
            if data is None:
                import urllib.error as _ue
                raise _ue.URLError("수식 그림 생성 실패 (외부 서버 미사용)")
            return _Resp(data)
        return orig(url, *a, **k)
    urlopen._pj_ver, urlopen._pj_orig = _PJ_VER, orig
    _ur.urlopen = urlopen


def _pj_patch_stop():
    """st.stop() 으로 실행이 중간에 끝나도 💾 · 🧾 · 📚 가 그려지도록 — 프로세스에 한 번"""
    cur = st.stop
    if getattr(cur, "_pj_ver", None) == _PJ_VER:
        return
    orig = getattr(cur, "_pj_orig", cur)

    def stop(*a, **k):
        try:
            import sys as _sys
            fr, in_cache = _sys._getframe(1), False
            while fr is not None:                  # @st.cache_* 함수 안의 st.stop() 이면 그리지 않음 (캐시 안 위젯 경고)
                if "caching" in fr.f_code.co_filename.replace("\\", "/").split("streamlit/runtime/")[-1][:8]:
                    in_cache = True
                    break
                fr = fr.f_back
            from streamlit.runtime.scriptrunner import get_script_run_ctx as _ctx
            h, f = st.session_state.get("_pj_on_stop") or (None, None)
            if f is not None and not in_cache and h == getattr(_ctx(), "page_script_hash", None):
                f()
        except Exception:  # noqa: BLE001
            pass
        return orig(*a, **k)
    stop._pj_ver, stop._pj_orig = _PJ_VER, orig
    st.stop = stop


def _pj_end():
    if _PJ_PANEL["done"]:
        return
    _PJ_PANEL["done"] = True
    _pj_mpl_cache_clear()
    try:
        _pj_panel(_PJ_PANEL["c"])
    except Exception as e:  # noqa: BLE001
        try:
            st.caption(f"공통블록 오류 : {e}")
        except Exception:  # noqa: BLE001
            pass


def _pj_gh_cfg():
    """[2026-10-22] 보관 자료 영구 저장소 — Streamlit Cloud Secrets : DATA_REPO = "아이디/저장소", DATA_TOKEN = "github_pat_…",
    (선택) DATA_BRANCH = "main". 앱 저장소와 다른 비공개 저장소여야 함 (같으면 저장할 때마다 앱이 다시 배포됨). 없으면 서버 폴더만 사용"""
    import os as _os
    repo = tok = ""
    br = "main"
    try:
        src = st.secrets
        if not src.get("DATA_REPO"):           # [2026-10-26] [섹션] 아래에 들어간 경우도 찾음 (TOML 은 [섹션] 뒤의 줄이 그 섹션 소속)
            src = next((v for v in st.secrets.values() if hasattr(v, "get") and v.get("DATA_REPO")), src)
        repo = str(src.get("DATA_REPO", "") or "")
        tok = str(src.get("DATA_TOKEN", "") or "")
        br = str(src.get("DATA_BRANCH", "main") or "main")
    except Exception:  # noqa: BLE001 — 로컬에 secrets 파일이 없을 때
        pass
    repo = repo or _os.environ.get("DATA_REPO", "")
    tok = tok or _os.environ.get("DATA_TOKEN", "")
    repo = repo.strip().split("github.com/")[-1].strip("/")       # 주소 통째로 넣어도 '아이디/저장소' 로
    repo = repo[:-4] if repo.endswith(".git") else repo
    return (repo.strip(), tok.strip(), br.strip()) if repo.strip() and tok.strip() else None


def _pj_gh_call(cfg, method, path, body=None, raw=False):
    import json as _js, urllib.parse as _up, urllib.request as _ur
    repo, tok, br = cfg
    url = f"https://api.github.com/repos/{repo}/contents/{_up.quote(path)}"
    if method == "GET":
        url += f"?ref={_up.quote(br)}"
    hd = {"Authorization": f"Bearer {tok}", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "harbor-apps",
          "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json"}
    data = _js.dumps(body).encode("utf-8") if body is not None else None
    if data is not None:
        hd["Content-Type"] = "application/json"
    req = _ur.Request(url, data=data, method=method, headers=hd)
    with _ur.urlopen(req, timeout=120) as r:
        return r.read()



_PJ_PKL_MODS = ("numpy", "pandas", "datetime", "collections", "decimal", "zoneinfo", "pytz", "dateutil", "uuid", "pathlib", "fractions")
_PJ_PKL_BUILTINS = {"list", "dict", "set", "frozenset", "tuple", "bytearray", "bytes", "slice", "complex", "range", "object",
                    "int", "float", "str", "bool", "NoneType", "Ellipsis", "NotImplemented"}
_PJ_PKL_BAD = ("Store", "Writer", "Reader", "File", "memmap", "IO", "Popen", "eval", "exec", "load", "read", "save", "system")


def _pj_pkl_global_ok(mod, name):
    """[2026-11-06] pickle 안 전역 이름 허용 목록 — 표 · 숫자 자료(numpy · pandas · 날짜 등)의 클래스와 내부 복원 함수만"""
    import importlib as _il
    mod, name = str(mod or ""), str(name or "")
    if not mod or not name or any(b in name for b in _PJ_PKL_BAD):
        return False
    if mod in ("builtins", "__builtin__"):          # __builtin__ = pickle 2 판의 옛 이름
        return name in _PJ_PKL_BUILTINS
    if mod == "pyarrow.lib":                         # pandas 문자열 열 (pyarrow) 복원
        return name in ("_restore_array", "type_for_alias", "py_buffer", "schema", "field")
    if mod == "copyreg":
        return name in ("_reconstructor", "__newobj__", "__newobj_ex__")
    if mod == "_codecs":
        return name == "encode"
    if mod.split(".")[0] not in _PJ_PKL_MODS or any(x in mod for x in (".io", "npyio", "testing", "f2py", "distutils", "plotting")):
        return False
    try:
        obj = _il.import_module(mod)
        for p in name.split("."):
            obj = getattr(obj, p)
    except Exception:  # noqa: BLE001
        return False
    return isinstance(obj, type) or name.split(".")[-1].startswith("_") or name in ("scalar", "dtype")


def _pj_pkl_safe(b):
    """pickle 을 실행하지 않고 명령(opcode)만 훑어, 허용 목록 밖 함수 · 클래스를 부르면 False"""
    import io as _io, pickletools as _pt
    memo, strs = {}, []
    try:
        for op, arg, _pos in _pt.genops(_io.BytesIO(b)):
            nm = op.name
            if nm in ("GLOBAL", "INST"):
                m_, n_ = (str(arg).split(" ", 1) + [""])[:2]
                if not _pj_pkl_global_ok(m_, n_):
                    return False
            elif nm == "STACK_GLOBAL":
                if len(strs) < 2 or not _pj_pkl_global_ok(strs[-2], strs[-1]):
                    return False
            elif nm in ("SHORT_BINUNICODE", "BINUNICODE", "BINUNICODE8", "UNICODE", "STRING", "BINSTRING", "SHORT_BINSTRING"):
                strs.append(arg)
            elif nm == "MEMOIZE":
                memo[len(memo)] = strs[-1] if strs else None
            elif nm in ("BINPUT", "LONG_BINPUT", "PUT"):
                memo[arg] = strs[-1] if strs else None
            elif nm in ("BINGET", "LONG_BINGET", "GET"):
                strs.append(memo.get(arg))
            elif nm == "STOP":
                break
            else:
                strs.append(None)
            if len(strs) > 64:
                del strs[:-8]
        return True
    except Exception:  # noqa: BLE001 — 깨진 pickle
        return False


def _pj_blob_safe(b, depth=0):
    """[2026-11-06] 저장소에서 받은 파일 검사 — gzip · tar · zip 은 풀어서 안까지, pickle 은 _pj_pkl_safe. 그 밖(CSV · JSON · 그림 · DXF)은 통과"""
    import gzip as _gz, io as _io, tarfile as _tar, zipfile as _zf
    if not b or depth > 4:
        return depth <= 4
    try:
        if b[:2] == b"\x1f\x8b":
            return _pj_blob_safe(_gz.decompress(b), depth + 1)
        if b[:2] == b"PK":
            with _zf.ZipFile(_io.BytesIO(b)) as z:
                return all(_pj_blob_safe(z.read(n), depth + 1) for n in z.namelist() if not n.endswith("/"))
        if len(b) > 262 and b[257:262] == b"ustar":
            with _tar.open(fileobj=_io.BytesIO(b)) as tf:
                return all(_pj_blob_safe(tf.extractfile(m).read(), depth + 1) for m in tf.getmembers() if m.isfile())
        if b[:1] == b"\x80" and len(b) > 2 and 2 <= b[1] <= 5:
            return _pj_pkl_safe(b)
        try:                                         # 옛 pickle (0 · 1판) : 끝까지 pickle 로 읽히면 같은 검사
            import pickletools as _pt
            for op, _a, _p in _pt.genops(_io.BytesIO(b)):
                if op.name == "STOP":
                    return _pj_pkl_safe(b)
        except Exception:  # noqa: BLE001 — pickle 아님 (CSV · DXF · 그림 등)
            pass
        return True
    except Exception:  # noqa: BLE001 — 풀다가 깨짐
        return False


def _pj_gh_get(path, cfg=None):
    """저장소 파일 내용 (없으면 None). [2026-11-06] pickle 묶음은 안을 검사해 실행 코드가 섞였으면 받지 않음 (토큰이 새어 누가 파일을 바꿔도 서버에서 실행 안 됨)"""
    import sys as _sys
    cfg = cfg or _pj_gh_cfg()
    if not cfg:
        return None
    try:
        b = _pj_gh_call(cfg, "GET", path, raw=True)
    except Exception:  # noqa: BLE001 — 없음(404) · 연결 실패
        return None
    if not str(path).lower().endswith(".json") and not _pj_blob_safe(b):
        rj = getattr(_sys, "_pj_gh_rejected", None)
        if rj is None:
            rj = _sys._pj_gh_rejected = []
        if path not in rj:
            rj.append(str(path))
        return None
    return b


def _pj_gh_list(path, cfg=None):
    """폴더 안 파일 이름 목록"""
    import json as _js
    cfg = cfg or _pj_gh_cfg()
    if not cfg:
        return []
    try:
        d = _js.loads(_pj_gh_call(cfg, "GET", path))
        return [x["name"] for x in d if isinstance(x, dict) and x.get("type") == "file"] if isinstance(d, list) else []
    except Exception:  # noqa: BLE001
        return []


def _pj_gh_sha(cfg, path):
    import json as _js
    try:
        return _js.loads(_pj_gh_call(cfg, "GET", path)).get("sha")
    except Exception:  # noqa: BLE001
        return None


def _pj_gh_put(path, data, cfg=None, msg=None, wait=False):
    """파일 올리기 (있으면 덮어씀) — 기본은 뒤에서(스레드) 올려 화면이 느려지지 않게"""
    cfg = cfg or _pj_gh_cfg()
    if not cfg:
        return False

    def _run():
        import base64 as _b64
        for _i in range(2):                       # 동시에 고쳐 sha 가 바뀌었으면 한 번 더
            try:
                body = {"message": msg or f"보관 {path}", "content": _b64.b64encode(data).decode("ascii"), "branch": cfg[2]}
                sha = _pj_gh_sha(cfg, path)
                if sha:
                    body["sha"] = sha
                _pj_gh_call(cfg, "PUT", path, body)
                try:                                  # [2026-11-06] 상태 점검용 : 이 서버가 최근 올린 것
                    import sys as _sys, time as _tm
                    lg = getattr(_sys, "_pj_gh_log", None)
                    if lg is None:
                        lg = _sys._pj_gh_log = []
                    lg.append((_tm.time(), str(path), len(data)))
                    del lg[:-30]
                except Exception:  # noqa: BLE001
                    pass
                return True
            except Exception:  # noqa: BLE001
                continue
        return False
    if wait:
        return _run()
    import threading as _th
    _th.Thread(target=_run, daemon=True).start()
    return True


def _pj_gh_del(path, cfg=None):
    cfg = cfg or _pj_gh_cfg()
    if not cfg:
        return False
    try:
        sha = _pj_gh_sha(cfg, path)
        if sha:
            _pj_gh_call(cfg, "DELETE", path, {"message": f"삭제 {path}", "sha": sha, "branch": cfg[2]})
        return True
    except Exception:  # noqa: BLE001
        return False


def _pj_gh_check():
    """[2026-10-26] 보관 저장소 연결 확인 (매니저) — Secrets 읽힘 · 저장소 보기 · 쓰기 시험 결과를 쉬운 말로. 토큰 값은 보여 주지 않음"""
    import datetime as _dt, json as _js, urllib.error as _ue, urllib.request as _ur
    out = []
    cfg = _pj_gh_cfg()
    if not cfg:
        return [(False, "Secrets 에서 DATA_REPO · DATA_TOKEN 을 찾지 못했습니다 — 두 줄이 있는지, 값이 비어 있지 않은지 확인하세요.")]
    repo, tok, br = cfg
    out.append((True, f"Secrets 읽음 : 저장소 '{repo}' · 가지 '{br}' · 토큰 {len(tok)}자 ({tok[:11]}…)"))
    try:
        req = _ur.Request(f"https://api.github.com/repos/{repo}", headers={"Authorization": f"Bearer {tok}", "User-Agent": "harbor-apps",
                                                                         "X-GitHub-Api-Version": "2022-11-28"})
        with _ur.urlopen(req, timeout=30) as r:
            info = _js.loads(r.read())
        out.append((True, f"저장소 보기 성공 : {info.get('full_name')} ({'비공개' if info.get('private') else '공개 — 비공개로 바꾸세요'})"))
    except _ue.HTTPError as e:
        out.append((False, {401: "토큰이 틀렸거나 만료되었습니다 — 토큰을 새로 만들어 DATA_TOKEN 에 넣으세요.",
                            404: f"저장소 '{repo}' 를 찾을 수 없습니다 — 이름(아이디/저장소) 오타이거나, 토큰의 Repository access 에 이 저장소가 없습니다."}
                    .get(e.code, f"저장소 보기 실패 (HTTP {e.code})")))
        return out
    except Exception as e:  # noqa: BLE001
        return out + [(False, f"GitHub 연결 실패 : {e}")]
    import base64 as _b64
    body = {"message": "연결 확인", "branch": br,
            "content": _b64.b64encode(f"연결 확인 {_dt.datetime.now():%Y-%m-%d %H:%M:%S}".encode("utf-8")).decode("ascii")}
    sha = _pj_gh_sha(cfg, "_연결확인.txt")
    if sha:
        body["sha"] = sha
    try:
        _pj_gh_call(cfg, "PUT", "_연결확인.txt", body)
        out.append((True, "쓰기 시험 성공 — 저장소에 '_연결확인.txt' 가 생겼습니다. 보관이 정상입니다."))
    except _ue.HTTPError as e:
        out.append((False, {403: "쓰기 권한이 없습니다 — 토큰 Permissions 의 Contents 를 'Read and write' 로 바꾸세요.",
                            404: "쓰기 권한이 없거나 가지 이름이 틀렸습니다 — 토큰 Contents 'Read and write', DATA_BRANCH(기본 main) 확인.",
                            409: f"가지 '{br}' 에 쓸 수 없습니다 — DATA_BRANCH 를 지우거나 저장소 가지 이름으로.",
                            422: f"가지 '{br}' 가 없습니다 — DATA_BRANCH 를 지우거나 저장소 가지 이름으로."}
                    .get(e.code, f"쓰기 실패 (HTTP {e.code})")))
    except Exception as e:  # noqa: BLE001
        out.append((False, f"쓰기 시험 실패 : {e}"))
    return out


def _pj_gh_status():
    """[2026-11-06] 보관 저장소 상태 (매니저) → (요약 줄 목록, 폴더별 표 DataFrame, 경고 목록)"""
    import datetime as _dt, json as _js, sys as _sys, time as _tm, urllib.parse as _up, urllib.request as _ur
    import pandas as _pd
    cfg = _pj_gh_cfg()
    if not cfg:
        return ["보관 저장소(DATA_REPO · DATA_TOKEN)가 설정되지 않았습니다 — 서버 폴더에만 보관됩니다."], None, []
    repo, tok, br = cfg

    def api(p):
        req = _ur.Request(f"https://api.github.com/repos/{repo}{p}", headers={"Authorization": f"Bearer {tok}", "User-Agent": "harbor-apps",
                                                                         "X-GitHub-Api-Version": "2022-11-28"})
        with _ur.urlopen(req, timeout=60) as r:
            return _js.loads(r.read())
    lines, warn = [], []
    try:
        info = api("")
        kb = float(info.get("size", 0) or 0)
        lines.append(f"저장소 {info.get('full_name')} ({'비공개' if info.get('private') else '공개 — 비공개로 바꾸세요'}) · 전체 용량 약 {kb / 1024:,.1f} MB")
        if not info.get("private"):
            warn.append("저장소가 공개입니다 — 보관 자료가 누구에게나 보입니다. GitHub 저장소 Settings 에서 Private 로 바꾸세요.")
        if kb > 900 * 1024:
            warn.append(f"저장소 용량이 {kb / 1024:,.0f} MB 입니다 — GitHub 권장 1 GB 에 가까움 (오래된 수집 자료 정리 필요)")
    except Exception as e:  # noqa: BLE001
        return [f"저장소 정보를 읽지 못했습니다 : {e} — '🔌 연결 확인' 을 먼저 눌러 보세요."], None, []
    try:
        c = api(f"/commits?sha={_up.quote(br)}&per_page=1")[0]
        t = _dt.datetime.fromisoformat(c["commit"]["committer"]["date"].replace("Z", "+00:00")).astimezone()
        lines.append(f"마지막 보관 : {t:%Y-%m-%d %H:%M} · '{c['commit']['message'][:40]}'")
        if (_dt.datetime.now(t.tzinfo) - t).days >= 14:
            warn.append(f"마지막 보관이 {(_dt.datetime.now(t.tzinfo) - t).days}일 전입니다 — 보관이 멈췄을 수 있습니다 (연결 확인).")
    except Exception:  # noqa: BLE001
        lines.append("마지막 보관 : (기록 없음)")
    tab = None
    try:
        tr = api(f"/git/trees/{_up.quote(br)}?recursive=1")
        rows = {}
        for x in tr.get("tree", []):
            if x.get("type") != "blob":
                continue
            p = x["path"].split("/")
            grp = "/".join(p[:2]) if len(p) > 2 else (p[0] if len(p) > 1 else "(맨 위)")
            r = rows.setdefault(grp, [0, 0, 0])
            r[0] += 1
            r[1] += int(x.get("size", 0) or 0)
            r[2] = max(r[2], int(x.get("size", 0) or 0))
            if int(x.get("size", 0) or 0) > 45 * 1024 * 1024:
                warn.append(f"큰 파일 {x['path']} ({int(x['size']) / 1048576:,.0f} MB) — 100 MB 가 넘으면 GitHub 에 올라가지 않습니다.")
        tab = _pd.DataFrame([{"폴더": k, "파일 수": v[0], "용량 (MB)": round(v[1] / 1048576, 2), "가장 큰 파일 (MB)": round(v[2] / 1048576, 2)}
                             for k, v in sorted(rows.items())])
        if tr.get("truncated"):
            warn.append("파일이 너무 많아 목록 일부만 셌습니다.")
    except Exception as e:  # noqa: BLE001
        lines.append(f"폴더 목록을 읽지 못했습니다 : {e}")
    rj = list(getattr(_sys, "_pj_gh_rejected", []) or [])
    if rj:
        warn.append("안전 검사에서 받지 않은 파일 (실행 코드가 섞였거나 깨진 파일) : " + ", ".join(rj[:10])
                    + " — 누가 저장소 파일을 바꿨을 수 있습니다. DATA_TOKEN 을 새로 만드세요.")
    else:
        lines.append("안전 검사 : 이 서버가 받은 파일 중 거부된 것 없음")
    lg = list(getattr(_sys, "_pj_gh_log", []) or [])
    if lg:
        lines.append("이 서버가 최근 올린 것 : " + " · ".join(f"{_tm.strftime('%m-%d %H:%M', _tm.localtime(t_))} {p_.split('/')[-1][:28]}"
                                                      for t_, p_, _n in lg[-5:][::-1]))
    reg = getattr(_sys, "_pj_mirror_reg", None)
    if reg and reg.get("dirs"):
        alive = reg.get("thread") is not None and reg["thread"].is_alive()
        lines.append(f"수집 자료 자동 보관 : 폴더 {len(reg['dirs'])}개 등록 · 뒤 작업 {'동작 중' if alive else '멈춤'}")
        if not alive:
            warn.append("수집 자료 자동 보관 뒤 작업이 멈춰 있습니다 — 앱을 다시 시작(Reboot)하면 다시 돕니다.")
    return lines, tab, warn


def _pj_mirror(local_dir, prefix, skip=(), only=()):
    """[2026-10-26] 수집 자료 폴더 영구 보관 (pj-9) — DATA_REPO 저장소 '<prefix>/' 에 폴더 맨 위 항목마다 하나씩 보관
    (하위 폴더 = 이름.tgz 묶음, 파일 = 이름.gz). 서버 프로세스가 처음 이 폴더를 쓸 때 저장소 → 서버로 되받고(저장소 우선),
    그 뒤 새로 생기거나 바뀐 항목은 뒤 스레드가 20초쯤 모아 올림 · 서버에서 지운 항목은 저장소에서도 지움.
    skip = 빼는 이름(따로 보관하는 파일 등), only = 이 무늬(fnmatch)에 맞는 이름만. DATA_REPO 없으면 아무것도 안 함"""
    import os as _os, sys as _sys, threading as _th
    cfg = _pj_gh_cfg()
    if not cfg:
        return
    reg = getattr(_sys, "_pj_mirror_reg", None)
    if reg is None:
        reg = _sys._pj_mirror_reg = {"lock": _th.Lock(), "dirs": {}, "thread": None}
    key = _os.path.abspath(str(local_dir))
    with reg["lock"]:
        if key in reg["dirs"]:
            return
        d = dict(prefix=prefix.strip("/"), skip=tuple(skip), only=tuple(only), cfg=cfg)
        try:
            _os.makedirs(key, exist_ok=True)
            _pj_mirror_restore(d, key)
        except Exception:  # noqa: BLE001 — 되받기 실패해도 앱은 그대로
            pass
        d["sig"] = _pj_mirror_sigs(d, key)
        reg["dirs"][key] = d
        if reg["thread"] is None or not reg["thread"].is_alive():
            reg["thread"] = _th.Thread(target=_pj_mirror_loop, args=(reg,), daemon=True)
            reg["thread"].start()


def _pj_mirror_names(d, key):
    import fnmatch as _fm, os as _os
    out = []
    for nm in (_os.listdir(key) if _os.path.isdir(key) else []):
        if nm.startswith(".") or nm.endswith(".tmp") or nm in d["skip"] or nm == "__pycache__":
            continue
        if d["only"] and not any(_fm.fnmatch(nm, p) for p in d["only"]):
            continue
        out.append(nm)
    return out


def _pj_mirror_sigs(d, key):
    """항목별 서명 (파일 : 크기 · 수정시각, 폴더 : 안의 파일 전부)"""
    import os as _os
    out = {}
    for nm in _pj_mirror_names(d, key):
        p = _os.path.join(key, nm)
        try:
            if _os.path.isdir(p):
                rows = []
                for r, _ds, fs in _os.walk(p):
                    for f in fs:
                        if not f.endswith(".tmp"):
                            st_ = _os.stat(_os.path.join(r, f))
                            rows.append((_os.path.relpath(_os.path.join(r, f), p), st_.st_size, st_.st_mtime_ns))
                out[nm] = tuple(sorted(rows))
            else:
                st_ = _os.stat(p)
                out[nm] = (st_.st_size, st_.st_mtime_ns)
        except OSError:
            continue
    return out


def _pj_mirror_restore(d, key):
    """저장소 → 서버 (저장소 우선 : 처음 실행 때 서버에 있는 것은 배포 묶음 · 옛 자료이므로)"""
    import fnmatch as _fm, gzip as _gz, io as _io, os as _os, tarfile as _tar
    for fn in _pj_gh_list(d["prefix"], d["cfg"]):
        if fn.endswith(".tgz"):
            nm, kind = fn[:-4], "dir"
        elif fn.endswith(".gz"):
            nm, kind = fn[:-3], "file"
        else:
            continue
        if nm in d["skip"] or (d["only"] and not any(_fm.fnmatch(nm, p) for p in d["only"])):
            continue
        b = _pj_gh_get(f"{d['prefix']}/{fn}", d["cfg"])
        if not b:
            continue
        raw = _gz.decompress(b)
        if kind == "file":
            tmp = _os.path.join(key, nm + ".tmp")
            with open(tmp, "wb") as f:
                f.write(raw)
            _os.replace(tmp, _os.path.join(key, nm))
            continue
        base = _os.path.abspath(_os.path.join(key, nm))
        with _tar.open(fileobj=_io.BytesIO(raw)) as tf:
            for m in tf.getmembers():
                dst = _os.path.abspath(_os.path.join(base, *m.name.split("/")))
                if not m.isfile() or not dst.startswith(base + _os.sep):
                    continue
                _os.makedirs(_os.path.dirname(dst), exist_ok=True)
                with open(dst, "wb") as f:
                    f.write(tf.extractfile(m).read())


def _pj_mirror_push(d, key, nm, gone):
    """항목 하나 올리기 (지워졌으면 저장소에서도 지움). 45 MB 넘는 묶음은 올리지 않음"""
    import gzip as _gz, io as _io, os as _os, tarfile as _tar
    p = _os.path.join(key, nm)
    if gone:
        _pj_gh_del(f"{d['prefix']}/{nm}.tgz", d["cfg"])
        _pj_gh_del(f"{d['prefix']}/{nm}.gz", d["cfg"])
        return True
    if _os.path.isdir(p):
        bio = _io.BytesIO()
        with _tar.open(fileobj=bio, mode="w") as tf:
            for r, _ds, fs in _os.walk(p):
                for f in sorted(fs):
                    if not f.endswith(".tmp"):
                        fp = _os.path.join(r, f)
                        tf.add(fp, arcname=_os.path.relpath(fp, p).replace(_os.sep, "/"))
        data, fn = _gz.compress(bio.getvalue(), 6), f"{nm}.tgz"
    else:
        with open(p, "rb") as f:
            data, fn = _gz.compress(f.read(), 6), f"{nm}.gz"
    if len(data) > 45 * 1024 * 1024:
        return True
    return _pj_gh_put(f"{d['prefix']}/{fn}", data, d["cfg"], msg=f"수집 자료 {d['prefix']}/{nm}", wait=True)


def _pj_mirror_loop(reg):
    """뒤 스레드 : 10초마다 등록 폴더를 살펴, 바뀐 뒤 한 번 더 그대로인(쓰기가 끝난) 항목만 올림"""
    import time as _tm
    pend = {}
    while True:
        _tm.sleep(10)
        for key, d in list(reg["dirs"].items()):
            try:
                cur = _pj_mirror_sigs(d, key)
                for nm in sorted(set(cur) | set(d["sig"])):
                    now, was = cur.get(nm), d["sig"].get(nm)
                    if now == was:
                        pend.pop((key, nm), None)
                        continue
                    if pend.get((key, nm), "∅") != now:
                        pend[(key, nm)] = now          # 아직 쓰는 중일 수 있음 → 다음 차례에 같으면 올림
                        continue
                    if _pj_mirror_push(d, key, nm, now is None):
                        if now is None:
                            d["sig"].pop(nm, None)
                        else:
                            d["sig"][nm] = now
                        pend.pop((key, nm), None)
                    _tm.sleep(1.5)                     # GitHub 쓰기 횟수 제한
            except Exception:  # noqa: BLE001 — 다음 차례에 다시
                continue


def _pj_lib_dir(make=False):
    """[2026-10-22] 입력제원 보관함 폴더 (앱 파일 옆 _입력보관/앱번호) — inject.py 의 LIB 앱만 사용"""
    import os as _os
    d = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "_입력보관", f"{int(_PJ.get('no') or 0):02d}")
    if make:
        _os.makedirs(d, exist_ok=True)
    return d


def _pj_lib_put(body):
    """입력제원 자동 보관 — 같은 입력(지문)이면 한 파일로 합쳐 날짜 · 횟수만 갱신"""
    import json as _js, os as _os, datetime as _dt
    try:
        own = body.pop("own", None)        # [2026-10-26] 앱 자체 저장 파일 전체 (14 · 29 · 30)
        if own is not None:
            try:
                own = _js.loads(own.decode("utf-8") if isinstance(own, (bytes, bytearray)) else str(own))
            except Exception:  # noqa: BLE001
                own = None
        if not _PJ.get("lib") or not (body.get("inputs") or body.get("tables") or own):
            return
        if isinstance(own, dict):
            body["own"] = own
            fp = _pj_finger({"o": {k: v for k, v in own.items() if k not in ("saved", "_계산정보")}})
        else:
            fp = _pj_finger({"i": body.get("inputs"), "t": body.get("tables")})
        d = _pj_lib_dir(True)
        # [2026-11-11] 파일 이름 = 프로젝트명 (예 '동방파제 두부.json', 같은 이름에 다른 입력이면 ' (2)') — 같은 입력인지는 파일 안 지문(finger)으로
        fn, old = None, {}
        for f_ in sorted(_os.listdir(d)):
            if f_.endswith(".json"):
                try:
                    with open(_os.path.join(d, f_), encoding="utf-8") as f:
                        r_ = _js.load(f)
                    if r_.get("finger") == fp:
                        fn, old = f_, r_
                        break
                except Exception:  # noqa: BLE001
                    pass
        if not old:
            b = _pj_gh_get(_pj_lib_ghdir() + f"/{fp}.json")          # 예전 이름 (지문.json) — 저장소에만 있을 때
            if b:
                old, fn = _js.loads(b.decode("utf-8")), f"{fp}.json"
        legacy = fn == f"{fp}.json"                                  # 예전 이름이면 새 이름으로 옮김
        now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        rec = dict(body, finger=fp, first=old.get("first", body.get("saved") or now), last=now,
                   count=int(old.get("count", 0)) + 1,
                   project=str(body.get("project") or old.get("project") or "").strip())
        if fn is None or legacy:
            import re as _re
            base = _re.sub(r'[\\/:*?"<>|\r\n\t]+', " ", rec["project"] or str(_PJ.get("short") or _PJ.get("app") or "입력")).strip()[:80] or "입력"
            gh_names = set()
            try:
                gh_names = set(_pj_gh_list(_pj_lib_ghdir()) or ())
            except Exception:  # noqa: BLE001
                pass
            k, new = 1, f"{base}.json"
            while _os.path.exists(_os.path.join(d, new)) or new in gh_names:
                k += 1
                new = f"{base} ({k}).json"
            if legacy:
                try:
                    _os.remove(_os.path.join(d, fn))
                except Exception:  # noqa: BLE001
                    pass
                _pj_gh_del(_pj_lib_ghdir() + f"/{fn}")
            fn = new
        path = _os.path.join(d, fn)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            _js.dump(rec, f, ensure_ascii=False, indent=1)
        _os.replace(tmp, path)
        _pj_gh_put(_pj_lib_ghdir() + f"/{fn}", _js.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8"))
    except Exception:  # noqa: BLE001 — 보관 실패로 저장 · 불러오기가 막히지 않게
        pass


def _pj_lib_put_bg(body):
    """[2026-11-06] 보관을 뒤 스레드에서 (저장소에서 옛 기록을 받아 오는 동안 저장 · 불러오기가 기다리지 않게)"""
    import copy as _cp, threading as _th
    if not _PJ.get("lib"):
        return
    _th.Thread(target=_pj_lib_put, args=(_cp.deepcopy(body),), daemon=True).start()


def _pj_lib_ghdir():
    return f"input_library/{int(_PJ.get('no') or 0):02d}"


def _pj_lib_sync():
    """저장소에만 있는 보관 파일을 서버 폴더로 내려받음 (서버를 다시 배포한 뒤 · 2분에 한 번)"""
    import os as _os, time as _tm
    ss = st.session_state
    key = f"_pj_lib_synced_{_PJ.get('no')}"
    if _tm.time() - ss.get(key, 0) < 120 or not _pj_gh_cfg():
        return
    ss[key] = _tm.time()
    d = _pj_lib_dir(True)
    for fn in _pj_gh_list(_pj_lib_ghdir()):
        fp = _os.path.join(d, fn)
        if fn.endswith(".json") and not _os.path.exists(fp):
            b = _pj_gh_get(_pj_lib_ghdir() + "/" + fn)
            if b:
                with open(fp, "wb") as f:
                    f.write(b)


def _pj_lib_list():
    import json as _js, os as _os
    out = []
    try:
        _pj_lib_sync()
    except Exception:  # noqa: BLE001
        pass
    try:
        d = _pj_lib_dir()
        for fn in (_os.listdir(d) if _os.path.isdir(d) else []):
            if fn.endswith(".json"):
                try:
                    with open(_os.path.join(d, fn), encoding="utf-8") as f:
                        out.append(dict(_js.load(f), _fn=fn))      # [2026-11-11] 파일 이름 (지우기용)
                except Exception:  # noqa: BLE001
                    pass
    except Exception:  # noqa: BLE001
        pass
    return sorted(out, key=lambda r: str(r.get("last", "")), reverse=True)


def _pj_mgr_key():
    import os as _os
    try:
        key = str(st.secrets.get("MANAGER_KEY", "") or "")
    except Exception:  # noqa: BLE001 — 로컬에 secrets 파일이 없을 때
        key = ""
    return key or _os.environ.get("MANAGER_KEY", "")


def _pj_mgr_door():
    """[2026-10-27] 매니저 칸(보관함 · 전부 자동 판 · 저장 자료 비우기)은 다른 사람에게 아예 안 보이게 (사용자 요청).
    보이는 때 : 이미 매니저 확인됨, 또는 주소 끝에 ?mgr 를 붙여 들어옴 (한 번 들어오면 이 창에서는 페이지를 옮겨도 유지)"""
    ss = st.session_state
    if ss.get("_mgr_ok") or ss.get("_mgr_door"):
        return True
    try:
        if "mgr" in st.query_params:
            ss["_mgr_door"] = True
            return True
    except Exception:  # noqa: BLE001
        pass
    return False


def _pj_mgr_ok(key="_pj_mgr_pw", force=False):
    """보관함 보기 · 불러오기 · 지우기는 매니저만 — 비밀번호는 Streamlit Cloud Secrets 'MANAGER_KEY' (코드에 적지 않음)"""
    import hmac as _hm
    ss = st.session_state
    if ss.get("_mgr_ok"):
        return True
    mk = _pj_mgr_key()                 # [2026-10-26] 검증보고서 30-1 : 예전엔 key(위젯 이름)를 비밀번호로 덮어써 중복 key 오류에 비밀번호가 보였음
    if not mk or not (force or _pj_mgr_door()):      # force = '🔐 매니저 관리' 상자처럼 사용자가 직접 연 곳
        return False
    pw = st.text_input("🔐 매니저 비밀번호", type="password", key=key)
    if pw:
        ok_, msg_ = _pj_pw_try(pw, mk)
        if ok_:
            ss["_mgr_ok"] = True
            st.rerun()
        st.error(msg_)
    return False


def _pj_pw_try(pw, mk):
    """[2026-11-06] 매니저 비밀번호 확인 + 연속 실패 잠금 → (맞음, 안내).
    한 창에서 5번 틀리면 그 창 10분 잠금, 모든 사용자 합쳐 10분 안에 20번 틀리면 전체 10분 잠금 (새 탭으로 계속 맞춰 보기 방지).
    같은 글자를 그대로 두고 화면만 새로 그려지면 다시 세지 않음. 틀릴 때마다 1초 기다림"""
    import hashlib as _hl, hmac as _hm, sys as _sys, threading as _th, time as _tm
    ss = st.session_state
    now = _tm.time()
    g = getattr(_sys, "_pj_pw_fail", None)
    if g is None:
        g = _sys._pj_pw_fail = {"t": [], "lock": 0.0, "mx": _th.Lock()}
    until = max(float(ss.get("_pj_pw_lock", 0.0)), float(g["lock"]))
    if now < until:
        return False, f"비밀번호를 여러 번 틀려 잠갔습니다 — {int((until - now) // 60) + 1}분 뒤 다시 넣어 주세요."
    if _hm.compare_digest(pw.encode("utf-8"), mk.encode("utf-8")):
        ss["_pj_pw_n"] = 0
        ss.pop("_pj_pw_last", None)
        return True, ""
    h = _hl.sha256(("pj|" + pw).encode("utf-8")).hexdigest()
    n = int(ss.get("_pj_pw_n", 0))
    if ss.get("_pj_pw_last") != h:             # 새로 넣은 값일 때만 셈
        ss["_pj_pw_last"] = h
        _tm.sleep(1.0)
        n += 1
        ss["_pj_pw_n"] = n
        with g["mx"]:
            g["t"] = [t for t in g["t"] if now - t < 600] + [now]
            if len(g["t"]) >= 20:
                g["lock"], g["t"] = now + 600, []
        if n >= 5:
            ss["_pj_pw_lock"], ss["_pj_pw_n"] = now + 600, 0
            return False, "비밀번호를 5번 틀려 10분 동안 잠갔습니다."
    return False, f"비밀번호가 다릅니다. ({n}/5 — 5번 틀리면 10분 잠금)"


def _pj_confirm(label, key, warn, **bkw):
    """[2026-10-23] 지우기 버튼 → '정말 지울까요?' 확인 한 번 더 (예 = True). 25번 비우기 버튼도 같이 씀"""
    ss = st.session_state
    fk = "_cf_" + key
    if not ss.get(fk):
        if st.button(label, key=key, **bkw):
            ss[fk] = True
            st.rerun()
        return False
    st.warning(f"⚠️ 정말 지울까요? {warn} — 지운 자료는 되돌릴 수 없습니다.")
    if st.button("🗑 예, 지웁니다", key=key + "_yes", type="primary"):
        ss[fk] = False
        return True
    if st.button("취소", key=key + "_no"):
        ss[fk] = False
        st.rerun()
    return False


def _pj_body(S):
    """지금 입력값 → 저장 내용 (💾 저장 · 보관함 공통)"""
    import datetime as _dt
    vals, tys = _pj_snapshot(S)
    try:
        pn = S["_pj_pname"] if "_pj_pname" in S else ""
    except Exception:  # noqa: BLE001
        pn = ""
    body = {"app": _PJ["app"], "project": str(pn or "").strip(),
            "saved": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "inputs": vals, "types": tys}
    try:
        tv = S["_pj_tv"] if "_pj_tv" in S else {}
    except Exception:  # noqa: BLE001
        tv = {}
    tabs = {t: _pj_tenc(v) for t, v in tv.items() if t in (_PJ.get("tables") or {})}
    tabs = {t: v for t, v in tabs.items() if v is not None}
    if tabs:
        body["tables"] = tabs
    return body


def _pj_lib_load_cb():
    """매니저가 목록에서 고르면 바로 그 입력제원으로 채움 (다음 실행 첫머리에 적용)"""
    ss = st.session_state
    fp = ss.get("_pj_lib_pick")
    if not fp or not ss.get("_mgr_ok"):
        return
    r = next((x for x in _pj_lib_list() if x.get("finger") == fp), None)
    if r and isinstance(r.get("own"), dict):        # [2026-10-26] 앱 자체 저장 파일 → 앱 자체 불러오기로 (14 · 29 · 30)
        ss["_pj_own_pending"] = r["own"]
    elif r:
        ss["_pj_pending"] = {k: r.get(k) for k in ("app", "project", "inputs", "types", "tables")}
        ss["_pj_pending"]["saved"] = r.get("last")
    ss["_pj_lib_pick"] = None


def _pj_lib_ui():
    """🗄 보관된 입력제원 — 목록 보기 · 고르면 바로 불러오기 · 지우기 모두 매니저만 (사용자 결정 10.22, 25번 현황 표는 공개)"""
    import os as _os
    import pandas as _pd
    ss = st.session_state
    if not _pj_mgr_ok(key="_pj_mgr_pw_lib", force=True):    # [2026-10-27] '🔐 매니저 관리' 상자 안 — 비밀번호를 넣어야 아래가 보임
        return
    st.markdown("**🗄 보관된 입력제원**")
    _c1, _c2 = st.columns(2)
    if _c1.button("🔌 보관 저장소 연결 확인", key="_pj_gh_chk", width="stretch"):
        for ok_, m_ in _pj_gh_check():
            (st.success if ok_ else st.error)(("✅ " if ok_ else "❌ ") + m_)
    if _c2.button("📊 보관 저장소 상태 점검", key="_pj_gh_stat", width="stretch"):
        _ln, _tb, _wn = _pj_gh_status()
        for w_ in _wn:
            st.warning("⚠ " + w_)
        st.markdown("\n".join(f"- {x}" for x in _ln))
        if _tb is not None and len(_tb):
            st.dataframe(_tb, hide_index=True, width="stretch")
    recs = _pj_lib_list()
    if not recs:
        st.caption("보관된 입력제원이 없습니다. 입력을 저장(💾 JSON)하거나 파일로 불러오면 여기에 자동으로 보관됩니다.")
    else:
        st.dataframe(_pd.DataFrame([{"프로젝트명": r.get("project") or "(없음)", "처음 보관": r.get("first", ""),
                                     "마지막 보관": r.get("last", ""), "저장 · 불러오기": f"{int(r.get('count', 1))}회",
                                     "입력 수": len(r.get("inputs") or {})} for r in recs]),
                     hide_index=True, width="stretch")
    st.caption("저장 · 불러오기 한 입력은 자동으로 보관됩니다 (같은 입력은 한 줄, 횟수만 늘어남).")
    if not recs:
        return
    lab = {r["finger"]: f"{r.get('project') or '(프로젝트명 없음)'} · {r.get('last', '')} · {int(r.get('count', 1))}회"
           for r in recs}
    st.selectbox("📥 불러올 입력제원 (고르면 바로 입력에 들어감) — 매니저", list(lab), index=None,
                 format_func=lab.get, key="_pj_lib_pick", on_change=_pj_lib_load_cb, placeholder="보관된 입력 선택")
    dl = st.selectbox("🗑 지울 입력제원 — 매니저", list(lab), index=None, format_func=lab.get, key="_pj_lib_delpick",
                      placeholder="지울 항목 선택")
    _fnm = {r["finger"]: (r.get("_fn") or f"{r['finger']}.json") for r in recs}      # [2026-11-11] 지문 → 파일 이름 (프로젝트명 · 예전 지문 이름)
    if _pj_confirm("🗑 고른 항목 지우기", "_pj_lib_del", f"'{lab.get(dl, '')}' 1건을 지웁니다", disabled=dl is None):
        try:
            _os.remove(_os.path.join(_pj_lib_dir(), _fnm.get(dl, f"{dl}.json")))
        except Exception:  # noqa: BLE001
            pass
        _pj_gh_del(_pj_lib_ghdir() + f"/{_fnm.get(dl, f'{dl}.json')}")
        st.rerun()
    if _pj_confirm("🗑 보관함 모두 지우기", "_pj_lib_clear", f"이 앱의 보관 입력제원 {len(recs)}건을 모두 지웁니다"):
        for x in recs:
            try:
                _os.remove(_os.path.join(_pj_lib_dir(), _fnm[x["finger"]]))
            except Exception:  # noqa: BLE001
                pass
            _pj_gh_del(_pj_lib_ghdir() + f"/{_fnm[x['finger']]}")
        st.rerun()


def _pj_fname(pn):
    """저장 파일 이름 : 프로그램명-프로젝트명(저장날짜).json — 파일 이름에 못 쓰는 글자는 뺌"""
    import datetime as _dt, re as _re
    pn = _re.sub(r'[\\/:*?"<>|\r\n\t]+', " ", str(pn or "")).strip()
    app = _re.sub(r'[\\/:*?"<>|]+', " ", str(_PJ.get("short") or _PJ["app"])).strip()      # [2026-11-03] 긴 이름은 짧은 이름 (예 : 블록식안벽(결정론))
    return f"{app}{'-' + pn if pn else ''}({_dt.date.today():%Y-%m-%d}).json"


def _pj_panel(c):
    import datetime as _dt, json as _js
    ss, S = st.session_state, _pj_S()
    msg = ss.pop("_pj_msg", None)
    ver = ss.get("_pj_ver_txt", "-")
    # [2026-10-27] 사용자 요청 : '🔐 매니저 관리' 상자 → 비밀번호 → 보관된 입력제원 (상자 안에는 비밀번호 칸만, 맞아야 내용)
    own_lib = bool(_PJ.get("lib")) and bool(_pj_mgr_key() or ss.get("_mgr_ok"))
    n = (1 if _PJ["save"] else 0) + (1 if own_lib else 0) + 1 + (1 if _PJ["kds"] else 0)
    if c is None:                                  # 입력 상자가 없는 앱 — 화면 맨 아래 한 줄
        st.divider()
        slots = list(st.columns(n))
    else:
        slots = [c] * n
    i = 0
    if _PJ["save"]:
        with slots[i].expander("💾 입력 저장 / 불러오기", expanded=bool(msg)):
            if msg:
                st.success(msg)
            _frag = getattr(st, "fragment", None) or (lambda f: f)

            @_frag
            def _pj_save_frag():
                """[2026-11-06] 이 상자 안 조작(프로젝트명 · 파일 고르기)은 상자만 다시 그림 — 무거운 앱도 바로 반응"""
                _fn_box = [None]

                def _save(_S=S):
                    """누르는 순간의 입력값으로 저장 파일을 만듦 (처음 열자마자 눌러도 빈 파일이 되지 않게)"""
                    import time as _tm
                    _tm.sleep(0.8)                    # [2026-11-03] 프로젝트명을 막 입력하고 바로 누르면 그 값이 서버에 닿기 전에 불림 → 잠깐 기다림
                    body = _pj_body(_S)
                    _pj_lib_put_bg(body)              # 🗄 보관함에도 자동 보관 (보관함을 켠 앱만, 뒤에서 — 저장이 기다리지 않게)
                    try:                              # [2026-11-03] 파일 이름도 누르는 순간의 프로젝트명으로 (전에는 화면 그릴 때 이름 → 두 번 눌러야 새 이름)
                        from streamlit import runtime as _rt
                        _m = _rt.get_instance().media_file_mgr
                        _nf = _pj_fname(body.get("project"))
                        for _e in _fn_box[1:]:            # 이 단추를 그릴 때 붙잡아 둔 등록 정보 (기다리는 사이 화면이 새로 그려져 목록에서 빠져도 그대로 씀)
                            _e["filename"] = _nf
                    except Exception:  # noqa: BLE001
                        pass
                    return _js.dumps(body, ensure_ascii=False, indent=1).encode("utf-8")
                pn = st.text_input("프로젝트명 (저장 파일 이름)", key="_pj_pname", placeholder="예 : 울산신항 8부두",
                                   help="저장 파일 이름 = 프로그램명-프로젝트명(저장날짜).json — 입력한 뒤 Enter (또는 칸 밖을 한 번 누름) 하고 저장")
                _fn = _pj_fname(pn)
                _fn_box[0] = _fn
                # [2026-11-09] 단추 key 고정 — 프로젝트명을 쓰고 바로 누르면 칸을 벗어나며 상자가 다시 그려지는데,
                #   key 가 파일 이름 따라 바뀌면 단추가 새것으로 바뀌어 첫 누름이 사라졌음 (두 번 눌러야 저장).
                #   파일 이름은 누르는 순간 _save 가 새 프로젝트명으로 바꾸므로 key 를 바꿀 필요 없음.
                st.download_button("💾 입력 저장 (JSON)", _save, file_name=_fn, mime="application/json",
                                   key="_pj_dl_save", width="stretch")
                try:                                  # [2026-11-03] 방금 등록된 이 단추의 지연 다운로드 정보를 붙잡아 둠 (누르는 순간 파일 이름을 바꾸려고)
                    from streamlit import runtime as _rt
                    _mm = _rt.get_instance().media_file_mgr
                    # [2026-11-24] 이번 실행의 등록만 붙잡음. 전에는 '파일 이름이 같은 등록' 을 모두 붙잡아 이전 실행의 등록까지 딸려 들어왔고,
                    #   그 등록 → 이전 저장 함수 → 그 이전 등록 … 으로 사슬이 이어져 실행마다 화면 자료 전체가 안 지워짐 (실제 서버에서만 — Cloud 'Oh no' 원인)
                    def _pj_own(_e, _S0=_save):
                        _c = _e.get("callable")
                        if _c is _S0:
                            return True
                        for _cl in (getattr(_c, "__closure__", None) or ()):
                            try:
                                if _cl.cell_contents is _S0:
                                    return True
                            except ValueError:
                                pass
                        return False
                    _all = list(getattr(_mm, "_deferred_callables", {}).items())
                    _mine = [(_k, _e) for _k, _e in _all if _pj_own(_e)]
                    if not _mine:
                        _mine = [(_k, _e) for _k, _e in _all if _e.get("filename") == _fn][-1:]
                    _fn_box += [_e for _k, _e in _mine]
                    _pj_keep_deferred(_mm, _mine)     # [2026-11-09] 다시 그려져 지워진 옛 단추를 눌러도 저장되게
                except Exception:  # noqa: BLE001
                    pass
                st.caption(f"저장될 파일 이름 : {_fn}")
                up = st.file_uploader("📂 저장한 입력 불러오기", type=["json"], key="_pj_up")
                if up is not None and ss.get("_pj_up_id") != up.file_id:
                    ss["_pj_up_id"] = up.file_id
                    try:
                        d = _js.loads(up.getvalue().decode("utf-8"))
                        if not isinstance(d, dict) or "inputs" not in d:
                            st.error("저장한 입력 파일(JSON)이 아닙니다.")
                        elif d.get("app") not in (None, _PJ["app"]):
                            st.error(f"다른 앱({d.get('app')})에서 저장한 파일입니다.")
                        else:
                            _pj_lib_put_bg(d)             # 🗄 불러온 입력제원도 보관 (뒤에서)
                            ss["_pj_pending"] = d
                            st.rerun()
                    except Exception as e:  # noqa: BLE001
                        st.error(f"불러오기 실패 : {e}")
            _pj_save_frag()
            nt = len(_PJ.get("tables") or {})
            st.caption(f"저장 대상 : 이름표가 있는 입력란 {len(_pj_widget_keys(S))}개" + (f" · 표 {nt}개" if nt else "")
                       + " (파일 · 이름표 없는 입력란 제외)")
        i += 1
    if own_lib:
        with slots[i].expander("🔐 매니저 관리", expanded=bool(msg) and not _PJ["save"]):
            if msg and not _PJ["save"]:
                st.success(msg)
            _pj_lib_ui()
        i += 1
    with slots[i].expander("🧾 계산 정보"):
        st.markdown("내려받는 Excel · Word · HTML 에 함께 들어갑니다 (프로그램 · 프로그램 판 · 계산 일시 · 입력 지문 · 적용 기준)")
        st.caption(f"프로그램 판 {ver} · 적용 기준 {_PJ['basis']}")
    i += 1
    if _PJ["kds"]:
        with slots[i].expander(f"📚 적용 기준 (KDS {len(_PJ['kds'])}종)"):
            st.caption(_PJ["basis"])
            st.markdown("\n".join(f"- {c_}" + (f" ({y})" if y else "") + f" · {k}곳" for c_, y, k in _PJ["kds"]))


try:
    _pj_block()
except Exception as _pj_e:  # noqa: BLE001 — 공통블록 문제로 앱이 멈추지 않도록
    st.caption(f"공통블록 오류 : {_pj_e}")
# ==== [공통블록 끝] ====




# =====================================================================
# ★ 기본 매핑 데이터 (신규 3종 추가 완료)
# =====================================================================
DEFAULT_MAPPING = [
    {"인허가명": "전략환경영향평가", "검색 법령명": "환경영향평가법"},
    {"인허가명": "환경영향평가", "검색 법령명": "환경영향평가법"},
    {"인허가명": "소규모 환경영향평가", "검색 법령명": "환경영향평가법"},
    {"인허가명": "기후영향평가", "검색 법령명": "기후위기 대응을 위한 탄소중립·녹색성장 기본법"},   # [2026-10-23 검증보고서 23-5] 판정 근거(제23조)와 같은 법
    {"인허가명": "사후환경영향조사", "검색 법령명": "환경영향평가법"},
    {"인허가명": "일반 및 간이해양 이용협의", "검색 법령명": "해양이용영향평가법"},
    {"인허가명": "해양이용영향평가", "검색 법령명": "해양이용영향평가법"},
    {"인허가명": "해양환경영향조사", "검색 법령명": "해양이용영향평가법"},
    {"인허가명": "해양공간적합성협의", "검색 법령명": "해양공간계획 및 관리에 관한 법률"},
    {"인허가명": "공유수면 점용·사용허가", "검색 법령명": "공유수면 관리 및 매립에 관한 법률"},
    {"인허가명": "공유수면 매립", "검색 법령명": "공유수면 관리 및 매립에 관한 법률"},
    {"인허가명": "재해영향성검토", "검색 법령명": "자연재해대책법"},
    {"인허가명": "재해영향평가", "검색 법령명": "자연재해대책법"},
    {"인허가명": "소규모 재해영향평가", "검색 법령명": "자연재해대책법"},
    {"인허가명": "교통영향평가", "검색 법령명": "도시교통정비 촉진법"},
    {"인허가명": "도시계획시설결정", "검색 법령명": "국토의 계획 및 이용에 관한 법률"},
    {"인허가명": "에너지사용계획 협의", "검색 법령명": "에너지이용 합리화법"},
    {"인허가명": "지하안전평가", "검색 법령명": "지하안전관리에 관한 특별법"},
    {"인허가명": "설계안전성검토(DFS)", "검색 법령명": "건설기술 진흥법"},
    {"인허가명": "안전관리계획 수립", "검색 법령명": "건설기술 진흥법"},
    {"인허가명": "유해위험방지계획서", "검색 법령명": "산업안전보건법"},
    {"인허가명": "해상교통안전진단", "검색 법령명": "해상교통안전법"},
    {"인허가명": "해상풍력발전 인허가", "검색 법령명": "해상풍력 보급 촉진 및 산업 육성에 관한 특별법"},
    {"인허가명": "어업피해영향 조사", "검색 법령명": "수산업법"},
    {"인허가명": "문화재 지표조사", "검색 법령명": "매장유산 보호 및 조사에 관한 법률"},
    {"인허가명": "문화재 현상변경 허가", "검색 법령명": "문화유산의 보존 및 활용에 관한 법률"},
    {"인허가명": "수저준설토사 유효활용", "검색 법령명": "해양환경관리법"},
    {"인허가명": "설계의 경제성(VE) 검토", "검색 법령명": "건설기술 진흥법"},
    {"인허가명": "경관심의", "검색 법령명": "경관법"},
    {"인허가명": "공공디자인 심의", "검색 법령명": "공공디자인의 진흥에 관한 법률"},
    {"인허가명": "항만공간 공공디자인 협의", "검색 법령명": "항만공간의 공공디자인 가이드라인"}
]

if 'mapping_df' not in st.session_state:
    st.session_state['mapping_df'] = pd.DataFrame(DEFAULT_MAPPING)

if 'result_df' not in st.session_state:
    st.session_state['result_df'] = pd.DataFrame()

# =====================================================================
# ★ 국가법령정보 통신 엔진
# =====================================================================
_LAW_DENY = "⛔ 법제처 거부"


def _law_api_err(root):
    """[2026-10-30] 법제처가 키 · 서버 주소를 거부하면 <Response><result>…</result><msg>…</msg></Response> 로 답함
    (예 : '사용자 정보 검증에 실패하였습니다.') — 전에는 이것을 '검색 결과 없음'으로 보였음 → 거부 사유를 그대로 돌려줌"""
    em = root.findtext('.//errMsg')
    if em:
        return f"{_LAW_DENY} : {em.strip()}"
    if root.tag == 'Response' and root.find('.//totalCnt') is None:
        r_, m_ = (root.findtext(k, default='').strip() for k in ('result', 'msg'))
        if r_ or m_:
            return f"{_LAW_DENY} : " + " — ".join(x for x in (r_, m_) if x)
    return None


def _law_oc_secret():
    """[2026-10-30] 관리자가 Streamlit Cloud Secrets 에 넣은 법제처 OC 키 (LAW_OC 등) — 화면 · 코드에는 키를 두지 않음.
    [섹션] 아래에 넣은 경우도 찾음. 없으면 '' """
    import os as _os
    names = ("LAW_OC", "LAW_API_KEY", "LAW_KEY", "OC", "law_oc")
    try:
        sec = st.secrets
        for n_ in names:
            if sec.get(n_):
                return str(sec.get(n_)).strip()
        for v_ in sec.values():
            if hasattr(v_, "get"):
                for n_ in names:
                    if v_.get(n_):
                        return str(v_.get(n_)).strip()
    except Exception:
        pass
    return next((_os.environ[n_].strip() for n_ in names if _os.environ.get(n_)), "")


def fetch_law_info(api_key, law_name):
    url = "https://www.law.go.kr/DRF/lawSearch.do"
    oc_key = api_key.strip() if api_key.strip() else "test"
    params = {'OC': oc_key, 'target': 'law', 'type': 'XML', 'query': law_name.strip(), 'display': 100}
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    result = {"검색 법령명": law_name, "실제 법령명": "검색 실패", "시행일자": "-", "공포일자": "-", "제개정구분": "-", "상세링크": "-"}
    try:
        res = requests.get(url, params=params, headers=headers, timeout=10)
        res.raise_for_status()
        root = ET.fromstring(res.text)

        err_msg = _law_api_err(root)
        if err_msg:
            result["실제 법령명"] = err_msg
            return result
            
        total_cnt = root.findtext('.//totalCnt', default='0')
        if total_cnt == '0':
            # [2026-10-20] 법령(법률·시행령·시행규칙)에 없으면 행정규칙(훈령·예규·고시)에서 다시 찾음
            #   예) 항만공간의 공공디자인 가이드라인 = 해양수산부 예규 제122호
            return fetch_admrul_info(oc_key, law_name, result)
            
        # [2026-10-23 검증보고서 23-1] 검색 결과의 첫 항목이 아니라 법령명이 완전히 같은 항목을 채택
        #   (예 : 해상교통안전법 → 해사안전기본법, 수산업법 → 농림수산업자 신용보증법 으로 잘못 붙던 문제)
        def _norm(t):
            return _kit_re.sub(r"[\s·ㆍ・\.]", "", str(t or ""))
        nodes = root.findall('.//law')
        law_node = next((n_ for n_ in nodes if _norm(n_.findtext('법령명한글')) == _norm(law_name)), None)
        exact = law_node is not None
        if law_node is None and nodes:
            law_node = nodes[0]
        if law_node is not None:
            result["실제 법령명"] = law_node.findtext('법령명한글', default='-')
            if not exact:
                result["실제 법령명"] = f"⚠ 확인 필요 — 같은 이름 없음 (검색 첫 항목 : {result['실제 법령명']})"
            enf_date = law_node.findtext('시행일자', default='-')
            if len(enf_date) == 8:
                result["시행일자"] = f"{enf_date[:4]}-{enf_date[4:6]}-{enf_date[6:]}"
            pub_date = law_node.findtext('공포일자', default='-')
            if len(pub_date) == 8:
                result["공포일자"] = f"{pub_date[:4]}-{pub_date[4:6]}-{pub_date[6:]}"
            result["제개정구분"] = law_node.findtext('제개정구분명', default='-')
            link_uri = law_node.findtext('법령상세링크', default='')
            if link_uri:
                result["상세링크"] = f"https://www.law.go.kr{link_uri}"
    except Exception:
        result["실제 법령명"] = "서버 통신 에러"
    return result


def fetch_admrul_info(oc_key, law_name, result):
    """행정규칙(훈령 · 예규 · 고시 등) 검색 — 법령 검색 결과가 없을 때"""
    params = {'OC': oc_key, 'target': 'admrul', 'type': 'XML', 'query': law_name.strip()}
    try:
        res = requests.get("https://www.law.go.kr/DRF/lawSearch.do", params=params,
                           headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        res.raise_for_status()
        root = ET.fromstring(res.text)
        err_msg = _law_api_err(root)
        if err_msg:
            result["실제 법령명"] = err_msg
            return result
        node = root.find('.//admrul')
        if node is None:
            result["실제 법령명"] = "검색 결과 없음 (법령 · 행정규칙)"
            return result
        kind, no, dept = (node.findtext(k, default='') for k in ('행정규칙종류', '발령번호', '소관부처명'))
        result["실제 법령명"] = (node.findtext('행정규칙명', default='-')
                              + f" ({dept} {kind}" + (f" 제{no}호" if no else "") + ")")
        for k_out, k_in in (("시행일자", "시행일자"), ("공포일자", "발령일자")):
            d = node.findtext(k_in, default='-')
            if len(d) == 8:
                result[k_out] = f"{d[:4]}-{d[4:6]}-{d[6:]}"
        result["제개정구분"] = node.findtext('제개정구분명', default='-')
        link_uri = node.findtext('행정규칙상세링크', default='')
        if link_uri:
            result["상세링크"] = f"https://www.law.go.kr{link_uri}"
    except Exception:
        result["실제 법령명"] = "검색 결과 없음 (행정규칙 조회 실패)"
    return result

# =====================================================================
# ★ [v2.0] 인허가 절차 흐름도 (현행 법령 기준 도식화 · 2026.10 확인)
#    — 화면 · HTML · Word 보고서 공통 PNG, 기간은 법령 조문 확인값만 표기
# =====================================================================
import io as _fio
import os as _fos
import textwrap as _ftw
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as _fplt
import matplotlib.font_manager as _ffm
from matplotlib.patches import FancyBboxPatch as _FBP


@st.cache_resource
def _flow_font():
    import urllib.request as _ur
    fp = _fos.path.join(_fos.path.dirname(_fos.path.abspath(__file__)), "NanumGothic.ttf")
    if not _fos.path.exists(fp):
        try:
            _ur.urlretrieve("https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf", fp)
        except Exception:
            pass
    if _fos.path.exists(fp):
        _ffm.fontManager.addfont(fp)
        return _ffm.FontProperties(fname=fp).get_name()
    return "Malgun Gothic"


_FLOW_ACTORS = [("주민", "#15803d"), ("위원회", "#b45309"), ("심의", "#b45309"), ("검토기관", "#475569"), ("전문기관", "#475569"),
                ("공단", "#475569"), ("관리원", "#475569"), ("연구원", "#475569"), ("조사기관", "#475569"),
                ("장관", "#7c3aed"), ("청장", "#7c3aed"), ("협의기관", "#7c3aed"), ("유산청", "#7c3aed"),
                ("승인기관", "#0f766e"), ("처분기관", "#0f766e"), ("관리청", "#0f766e"), ("발주청", "#0f766e"), ("관청", "#0f766e"),
                ("입안권자", "#0f766e"), ("결정권자", "#0f766e"), ("허가권자", "#0f766e"), ("지자체", "#0f766e"), ("관계기관", "#0f766e")]


def _flow_col(actor):
    for k, c in _FLOW_ACTORS:
        if k in actor:
            return c
    return "#1d4ed8"


def _wrap(s, w):
    out = []
    for part in str(s).split("\n"):
        out += _ftw.wrap(part, w) or [""]
    return out


def flow_png(title, steps, basis=""):
    """steps : [dict(a=주체, t=단계, d=내용, day=법정기간)] / 리스트 원소는 병렬·분기 단계"""
    _fplt.rcParams["font.family"] = _flow_font()
    _fplt.rcParams["axes.unicode_minus"] = False
    W, X0, X1 = 10.0, 1.95, 8.15
    rows = []
    for st_ in steps:
        grp = st_ if isinstance(st_, list) else [st_]
        n = len(grp)
        wbox = (X1 - X0 - 0.2 * (n - 1)) / n
        cw_t, cw_d = max(8, int(wbox * 6.3)), max(10, int(wbox * 7.6))
        items, hmax = [], 0
        for g in grp:
            tl = _wrap(g.get("t", ""), cw_t)
            dl = _wrap(g.get("d", ""), cw_d) if g.get("d") else []
            if n > 1:
                tl = _wrap(g.get("a", ""), cw_d) + tl
            h = 0.26 + 0.235 * len(tl) + 0.19 * len(dl)
            hmax = max(hmax, h)
            items.append((g, tl, dl))
        rows.append((items, wbox, hmax, n))
    gap = 0.42
    H = 0.95 + sum(r[2] for r in rows) + gap * (len(rows) - 1) + (0.35 + 0.19 * len(_wrap(basis, 92)) if basis else 0) + 0.25
    fig = _fplt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    ax.add_patch(_FBP((0.12, 0.12), W - 0.24, 0.55, boxstyle="round,pad=0,rounding_size=0.08", fc="#1e3a8a", ec="none"))
    ax.text(0.35, 0.395, title, color="white", fontsize=12.5, fontweight="bold", va="center")
    y = 0.95
    prev = None
    for items, wbox, hmax, n in rows:
        cents = []
        for i, (g, tl, dl) in enumerate(items):
            x = X0 + i * (wbox + 0.2)
            col = _flow_col(g.get("a", ""))
            soft = g.get("opt", False)
            ax.add_patch(_FBP((x, y), wbox, hmax, boxstyle="round,pad=0,rounding_size=0.08", fc="#f8fafc" if not soft else "#ffffff",
                              ec=col, lw=1.6, ls="--" if soft else "-"))
            ax.add_patch(_FBP((x, y), 0.07, hmax, boxstyle="square,pad=0", fc=col, ec="none"))
            ty = y + 0.17
            for k, line in enumerate(tl):
                is_actor = n > 1 and k < len(_wrap(g.get("a", ""), max(10, int(wbox * 7.6))))
                ax.text(x + 0.18, ty + 0.1, line, fontsize=8.6 if is_actor else 10, fontweight="normal" if is_actor else "bold",
                        color=col if is_actor else "#0f172a", va="center")
                ty += 0.235
            for line in dl:
                ax.text(x + 0.18, ty + 0.06, line, fontsize=8.6, color="#334155", va="center")
                ty += 0.19
            if g.get("day") and n == 1:
                ax.add_patch(_FBP((X1 + 0.15, y + hmax / 2 - 0.24), W - X1 - 0.3, 0.48, boxstyle="round,pad=0,rounding_size=0.1",
                                  fc="#fff7ed", ec="#f97316", lw=1.3))
                dd = _wrap(g["day"], 13)
                for k, line in enumerate(dd[:2]):
                    ax.text((X1 + 0.15 + W - 0.15) / 2, y + hmax / 2 + (k - (len(dd[:2]) - 1) / 2) * 0.2, line, fontsize=8.6,
                            color="#c2410c", fontweight="bold", ha="center", va="center")
            elif g.get("day"):
                ax.text(x + wbox - 0.1, y + hmax - 0.16, g["day"], fontsize=8.2, color="#c2410c", fontweight="bold", ha="right", va="center",
                        bbox=dict(boxstyle="round,pad=0.18", fc="#fff7ed", ec="#f97316", lw=0.8))
            if n == 1:
                al = _wrap(g.get("a", ""), 10)[:3]
                hc = max(0.44, 0.17 * len(al) + 0.14)
                ax.add_patch(_FBP((0.2, y + hmax / 2 - hc / 2), 1.58, hc, boxstyle="round,pad=0,rounding_size=0.1", fc=col, ec="none"))
                for k, line in enumerate(al):
                    ax.text(0.99, y + hmax / 2 + (k - (len(al) - 1) / 2) * 0.17, line, fontsize=8.0 if len(al) > 2 else 8.3, color="white",
                            fontweight="bold", ha="center", va="center")
            cents.append((x + wbox / 2, y, y + hmax))
        if prev:
            for (px, _, pb) in prev:
                for (cx, ct, _) in cents:
                    if len(prev) > 1 and len(cents) > 1 and len(prev) == len(cents) and prev.index((px, _, pb)) != cents.index((cx, ct, _)):
                        continue
                    ax.annotate("", xy=(cx, ct - 0.02), xytext=(px, pb + 0.02),
                                arrowprops=dict(arrowstyle="-|>", color="#64748b", lw=1.3, mutation_scale=12, shrinkA=0, shrinkB=0))
        prev = cents
        y += hmax + gap
    if basis:
        bl = _wrap("근거 : " + basis, 92)
        hb = 0.2 + 0.19 * len(bl)
        y += -gap + 0.2
        ax.add_patch(_FBP((0.2, y), W - 0.4, hb, boxstyle="round,pad=0,rounding_size=0.06", fc="#eff6ff", ec="#bfdbfe"))
        for k, line in enumerate(bl):
            ax.text(0.35, y + 0.18 + k * 0.19, line, fontsize=8.3, color="#1e3a8a", va="center")
    buf = _fio.BytesIO()
    fig.savefig(buf, format="png", dpi=130)
    _fplt.close(fig)
    return buf.getvalue()


_MOE = "기후에너지환경부장관 (지방·유역 환경청)"
FLOWS = {
    1: [("전략환경영향평가 절차 — 개발기본계획", [
            dict(a="계획수립기관", t="평가준비서 작성", d="대안·평가항목·범위 등 검토"),
            dict(a="환경영향평가협의회", t="평가준비서 심의", d="평가항목·범위·대안 등 결정", day="30일 (시행령 제9조)"),
            dict(a="계획수립기관", t="평가항목 등 결정내용 공개", d="결정일부터 20일 이내 공개, 14일 이상 게시", day="20일 이내 공개"),
            dict(a="계획수립기관", t="전략환경영향평가서 초안 작성"),
            dict(a="주민 등", t="초안 의견수렴", d="제출일부터 10일 이내 공고 → 공람 20~40일 → 설명회(7일 전 공고) → 공람 종료 후 7일 이내 의견", day="공람 20~40일"),
            dict(a="계획수립기관", t="전략환경영향평가서 작성 · 협의 요청", d="주민 의견 반영 여부 포함, 계획 확정 전 협의"),
            dict(a=_MOE, t="검토 및 협의내용 통보", d="한국환경연구원 등 전문기관 검토, 보완기간·공휴일 제외", day="30일 (연장 40일)"),
            dict(a="계획수립기관", t="협의내용 반영 · 계획 확정", d="조치결과 통보, 미반영 시 사유 통보")],
         "환경영향평가법 제9~21조, 동법 시행령 제9·10·13~15·25조 (2026.09.18 시행본)"),
        ("전략환경영향평가 절차 — 정책계획", [
            dict(a="계획수립기관", t="평가준비서 작성"),
            dict(a="환경영향평가협의회", t="평가준비서 심의 · 평가항목 등 결정", day="30일"),
            dict(a="계획수립기관", t="결정내용 공개 (20일 이내, 14일 이상 게시)"),
            dict(a="계획수립기관", t="전략환경영향평가서 작성 · 협의 요청", d="정책계획은 초안 주민의견수렴 대상 아님 (개발기본계획만 해당)"),
            dict(a=_MOE, t="검토 및 협의내용 통보", day="30일 (연장 40일)"),
            dict(a="계획수립기관", t="협의내용 반영 · 계획 확정")],
         "환경영향평가법 제9~21조, 동법 시행령 제9·10·25조")],
    2: [("환경영향평가 절차", [
            dict(a="사업자", t="평가준비서 작성 · 제출", d="승인기관 경유"),
            dict(a="환경영향평가협의회", t="평가준비서 심의 · 평가항목 등 결정", d="사업자 보완기간·공휴일 제외", day="30일 (시행령 제32조)"),
            dict(a="승인기관", t="결정내용 공개", d="결정일부터 20일 이내 공개, 14일 이상 게시", day="20일 이내"),
            dict(a="사업자", t="환경영향평가서 초안 작성 · 제출"),
            dict(a="주민 등", t="초안 공고 · 공람 · 설명회 (필요 시 공청회)", d="접수 10일 이내 공고, 공람 20~60일, 설명회 7일 전 공고, 공람 종료 후 7일 이내 의견 제출", day="공람 20~60일"),
            dict(a="사업자", t="환경영향평가서(본안) 작성", d="주민 의견 반영 · 미반영 사유 포함"),
            dict(a="승인기관", t="협의 요청", d="사업계획 승인 전"),
            dict(a=_MOE, t="검토 및 협의내용 통보", d="한국환경연구원 등 검토, 보완기간·전문위원회 검토기간·공휴일 제외", day="45일 (연장 60일)"),
            dict(a="승인기관", t="협의내용 반영 · 사업계획 승인"),
            dict(a="사업자", t="협의내용 이행 · 사후환경영향조사", d="협의내용 관리책임자 지정, 조사결과 통보")],
         "환경영향평가법 제22~36조, 동법 시행령 제32·33·36·38·39·50조 (2026.09.18 시행본)")],
    3: [("소규모 환경영향평가 절차", [
            dict(a="사업자", t="소규모 환경영향평가서 작성", d="보전용도지역 등 개발사업 (시행령 별표 4)"),
            dict(a="승인기관", t="협의 요청", d="사업계획 승인 전"),
            dict(a="지방·유역환경청장", t="검토 및 협의내용 통보", d="보완기간·공휴일 제외", day="30일 (연장 40일)\n※일부 20일(30일)"),
            dict(a="승인기관", t="협의내용 반영 · 사업계획 승인"),
            dict(a="사업자", t="협의내용 이행 · 관리")],
         "환경영향평가법 제43~46조, 동법 시행령 제62조"),
        ("사후환경영향조사 절차", [
            dict(a="사업자", t="사업 착공 · 사후환경영향조사 실시", d="평가서의 사후환경영향조사 계획에 따른 항목·주기"),
            dict(a="사업자", t="조사결과 통보", d="승인기관 및 기후에너지환경부장관(환경청)"),
            dict(a="승인기관", t="조사결과 검토", d="주변 환경 피해 여부 확인"),
            [dict(a="이상 없음", t="조사 지속 · 종료"), dict(a="피해 우려", t="저감방안 등 조치 요청 · 명령", opt=True)],
            dict(a="사업자", t="조치 이행 및 결과 통보")],
         "환경영향평가법 제36조, 동법 시행규칙 [별표 1]")],
    4: [("기후변화영향평가 절차 (환경영향평가 병행)", [
            dict(a="계획수립기관·사업자", t="대상 여부 확인", d="전략환경영향평가 · 환경영향평가 대상 중 온실가스 다배출 등 대통령령 대상"),
            dict(a="계획수립기관·사업자", t="기후변화영향평가서 작성 (별책)", d="평가대상지역 결정 → 기후변화 현황조사 → 영향 예측·분석 → 온실가스 감축목표·감축·적응방안"),
            dict(a="승인기관", t="환경영향평가 등 협의 요청 시 함께 협의 요청"),
            dict(a="기후에너지환경부장관", t="기후변화영향평가 검토 · 협의", d="정보 수집·자료 요구 가능", day="환경영향평가 등\n협의기간 내"),
            dict(a="계획수립기관·사업자", t="협의내용 반영 · 이행")],
         "기후위기 대응을 위한 탄소중립·녹색성장 기본법 제23조, 동법 시행령, 「기후변화영향평가 방법 등에 관한 규정」(고시)")],
    5: [("일반 해양이용협의 절차 (해양이용영향평가법, 2026.09.18 시행)", [
            dict(a="사업자", t="해양이용협의서 작성", d="공유수면 점용·사용, 매립, 골재채취 예정지 지정, 어업면허 등"),
            dict(a="처분기관", t="면허등 전 협의 요청"),
            dict(a="해양수산부장관 (지방해양수산청)", t="협의서 검토", d="해양이용영향검토기관 의견 청취 (영향 경미 사업은 생략 가능), 보완·조정 요청 최대 2회"),
            dict(a="해양수산부장관 (지방해양수산청)", t="협의의견 통보", d="보완·조정 기간, 공휴일·토요일 제외", day="30일\n(재난복구 15일)"),
            dict(a="처분기관", t="협의의견 반영 · 면허등"),
            dict(a="사업자", t="해양환경영향조사", d="해양이용영향평가법 제29조")],
         "해양이용영향평가법 제9~12·21·29조, 동법 시행령 제15조 (종전 해양환경관리법 제84조 해역이용협의 대체)"),
        ("해양이용영향평가 절차", [
            dict(a="사업자", t="평가준비서 작성 · 제출"),
            dict(a="해양수산부장관", t="평가항목·범위 결정 (심의)", d="결정내용 공개 · 주민 의견 청취"),
            dict(a="사업자", t="평가서 초안 작성 · 제출", d="처분기관·해양수산부장관 등"),
            dict(a="주민 등", t="초안 공고·공람 · 설명회 (필요 시 공청회)", d="공람 20~60일, 설명회 7일 전 공고, 공람 종료 후 7일 이내 의견", day="공람 20~60일"),
            dict(a="사업자", t="평가서 작성 · 협의 요청 (처분기관 경유)"),
            dict(a="해양수산부장관 (지방해양수산청)", t="검토 · 협의의견 통보", d="해양이용영향검토기관 의견, 보완·조정 기간 제외", day="45일"),
            dict(a="처분기관", t="협의의견 반영 · 면허등"),
            dict(a="사업자", t="해양환경영향조사 (사후)")],
         "해양이용영향평가법 제13~21·29조, 동법 시행령 제8·9·15조")],
    6: [("해양환경영향조사 절차", [
            dict(a="처분기관", t="면허등 (해양이용협의·영향평가 완료 사업)"),
            dict(a="사업자", t="해양환경영향조사 실시", d="조사 대상사업·항목·기간 : 해양수산부령"),
            dict(a="사업자", t="해양환경영향조사서 통보", d="처분기관의 장 및 해양수산부장관"),
            dict(a="해양수산부장관", t="조사결과 검토"),
            [dict(a="피해 없음", t="조사 지속 · 종료"), dict(a="피해 인정", t="처분기관 통해 조치 명령", d="공법 변경·사업규모 축소 등", opt=True)],
            dict(a="사업자", t="피해 방지조치 · 결과 통보")],
         "해양이용영향평가법 제29조 (종전 해양환경관리법 제95조)")],
    7: [("해양공간적합성협의 절차", [
            dict(a="계획수립·지정 기관", t="해양공간적합성협의 요청", d="해양이용·개발계획 수립·변경, 지구·구역 지정·변경 시 / 관계기관 협의·해역이용협의 등 다른 절차보다 먼저 요청"),
            dict(a="해양수산부장관", t="적합성 검토", d="해양공간계획 부합성·입지 적절성 등, 해양공간계획평가 전문기관 지원, 필요 시 보완 요청·현지조사"),
            dict(a="해양수산부장관", t="검토의견(협의결과) 통보", d="보완기간·공휴일·토요일 제외", day="45일 (시행령 제16조)"),
            dict(a="계획수립·지정 기관", t="협의결과 반영 · 계획 수립 / 지구 지정"),
            dict(a="계획수립·지정 기관", t="(반영 곤란 시) 재협의 요청", d="위치·범위, 사유, 사유 종료 예정일 등", opt=True),
            dict(a="해양수산부장관", t="재협의 결과 회신", day="20일 (시행령 제17조)", opt=True)],
         "해양공간계획 및 관리에 관한 법률 제15조, 동법 시행령 제13·15~17조")],
    8: [("공유수면 매립기본계획 수립 절차", [
            dict(a="해양수산부장관", t="매립기본계획 수립 (10년마다)", d="관계 중앙행정기관·시·도지사 협의·의견 청취"),
            dict(a="중앙연안관리심의회", t="심의"),
            dict(a="해양수산부장관", t="매립기본계획 고시"),
            dict(a="해양수산부장관", t="타당성 검토 (5년마다) · 필요 시 변경")],
         "공유수면 관리 및 매립에 관한 법률 제22·27조"),
        ("공유수면 매립면허 ~ 준공 절차", [
            dict(a="사업자", t="매립면허 신청", d="매립기본계획 반영 구역, 해양공간적합성·해양이용협의·환경영향평가 등 선행"),
            dict(a="관계기관", t="관계 행정기관 협의", day="20일 이내 의견"),
            dict(a="면허관청", t="매립면허 · 고시", d="10만m² 이상 해양수산부장관, 그 외 시·도지사"),
            dict(a="사업자", t="매립실시계획 승인 신청", d="권리자 착공동의 또는 보상·피해방지시설 선행", day="면허일부터\n1년 이내"),
            dict(a="면허관청", t="실시계획 승인 → 매립공사"),
            dict(a="사업자", t="준공검사 신청"),
            dict(a="면허관청", t="준공검사확인증 발급 · 고시", d="관련 법률 준공인가 의제 (제45조)"),
            dict(a="사업자", t="매립지 소유권 취득", d="공공용지 국가·지자체 귀속, 총사업비 상당 면허취득자 (제46조)")],
         "공유수면 관리 및 매립에 관한 법률 제28·38·45·46조, 동법 시행령 제34조"),
        ("공유수면 점용·사용허가 절차", [
            dict(a="사업자", t="점용·사용허가 신청", d="구조물 설치, 준설, 공유수면 점용 등"),
            dict(a="관리청", t="관계기관 협의 · 해양이용협의(해당 시)", d="필요 시 공고 14일 이상", day="20일 이내 의견"),
            dict(a="관리청", t="점용·사용허가", d="해양공간계획 부합성·어업 영향 등 고려, 구조물 최대 30년"),
            dict(a="사업자", t="실시계획 승인 신청 (소규모는 신고)", day="허가일부터\n1년 이내"),
            dict(a="관리청", t="실시계획 승인 → 공사 → 준공검사 · 확인증 발급")],
         "공유수면 관리 및 매립에 관한 법률 제8·11·12·17·18조, 동법 시행령 제7조")],
    9: [("재해영향성검토 절차 (행정계획)", [
            dict(a="관계행정기관", t="재해영향성검토 협의 요청", d="행정계획 확정 전"),
            dict(a="국립재난안전연구원 등", t="사전검토", day="14일 이내", opt=True),
            dict(a="행정안전부장관·시·도지사", t="검토 · 협의결과 통보", d="보완요청 30일 범위(기간 제외), 공휴일·토요일 제외", day="30일\n(연장 10일)"),
            dict(a="관계행정기관", t="협의결과 반영 · 조치결과 통보", day="통보일부터\n30일 이내")],
         "자연재해대책법 제4·5조, 동법 시행령 제3·4·7조"),
        ("재해영향평가 절차 (개발사업)", [
            dict(a="사업자", t="재해영향평가서 작성", d="재해 영향 예측·저감대책, 배수처리계획 등"),
            dict(a="관계행정기관", t="협의 요청", d="개발사업 허가 등 전"),
            dict(a="국립재난안전연구원 등", t="사전검토", day="14일 이내", opt=True),
            dict(a="재해영향평가심의위원회", t="심의", d="재해 위험요인·인근 영향·저감계획 검토"),
            dict(a="행정안전부장관·시·도지사", t="협의결과 통보", d="5만m² 이상 또는 10km 이상 45일 / 그 외 30일 / 공장설립승인 20일", day="45일·30일\n(연장 10일)"),
            dict(a="관계행정기관", t="협의결과 반영 후 허가 · 조치결과 통보", day="30일 이내"),
            dict(a="사업자", t="협의내용 이행 (이행 확인)")],
         "자연재해대책법 제4~7조, 동법 시행령 제3·4·6의2·7조")],
    10: [("교통영향평가 절차", [
            dict(a="사업자", t="교통영향평가서 작성", d="교통영향평가 대행자 (설계계약과 분리)"),
            dict(a="승인관청", t="평가서 제출", d="제출 시기 : 시행령 별표 1"),
            dict(a="교통영향평가심의위원회", t="심의", d="회의 7일 전 일정 통보, 9명 이내 무작위 선정"),
            dict(a="승인관청", t="개선필요사항 통보"),
            dict(a="사업자", t="(이견 시) 이의신청", day="통보일부터\n30일 이내", opt=True),
            dict(a="승인관청", t="이의신청 결과 통보", day="60일 이내", opt=True),
            dict(a="승인관청", t="개선필요사항 반영 · 사업 승인"),
            dict(a="사업자", t="이행 · 변경 심의", d="규모 30% 이상 증가, 7년 이상 공사중지 후 재개 등")],
         "도시교통정비 촉진법 제15~22조, 동법 시행령 제13조의3~제13조의8")],
    11: [("도시·군계획시설 결정 절차", [
            dict(a="입안권자 (시장·군수)", t="도시·군관리계획(시설) 입안", d="기초조사, 환경성 검토 등"),
            dict(a="주민", t="주민 의견청취", d="공고 후 14일 이상 열람, 검토결과 열람 종료 후 60일 이내 통보", day="열람 14일 이상"),
            dict(a="지방의회", t="의견청취"),
            dict(a="관계기관", t="관계 행정기관 협의", day="30일 이내 의견\n(법 제30조)"),
            dict(a="도시계획위원회", t="심의"),
            dict(a="결정권자 (시·도지사 등)", t="결정 · 고시 · 열람"),
            dict(a="사업시행자", t="실시계획 인가 → 시설사업 시행")],
         "국토의 계획 및 이용에 관한 법률 제25~32·43·88조, 동법 시행령 제22·25조")],
    12: [("에너지사용계획 협의 절차", [
            dict(a="사업주관자", t="에너지사용계획 수립", d="공공 : 연료·열 2,500 TOE / 전력 1천만 kWh 이상, 민간 : 5,000 TOE / 2천만 kWh 이상"),
            dict(a="사업주관자", t="기후에너지환경부장관에게 제출", d="제출 시기 : 시행령 별표 1"),
            dict(a="한국에너지공단", t="검토 (위탁)"),
            dict(a="기후에너지환경부장관", t="협의(공공) · 의견청취(민간) 결과 통보", day="30일\n(연장 20일)"),
            dict(a="사업주관자", t="(이견 시) 이의신청", day="30일 이내", opt=True),
            dict(a="사업주관자", t="이행계획 제출 · 실시설계 반영", d="실시설계 확정 후 14일 이내 반영내용 제출, 협의 완료 전 공사 시행 금지")],
         "에너지이용 합리화법 제10·11조, 동법 시행령 제20·23~26·51조 (2026.05.28 시행본)")],
    13: [("지하안전평가 절차", [
            dict(a="사업자", t="지하안전평가서 작성", d="굴착깊이 20m 이상 (10~20m 소규모 지하안전평가)"),
            dict(a="승인기관", t="협의 요청", d="협의 요청 시기 : 시행령 별표 1"),
            dict(a="국토교통부장관 (지방국토관리청)", t="검토 · 협의결과 통보", d="보완기간·공휴일 제외, 국토안전관리원 등 지원", day="30일 (연장 50일)"),
            dict(a="승인기관", t="협의내용 반영 · 사업 승인"),
            dict(a="사업자", t="(이견 시) 협의내용 조정 요청", d="결과 30일(연장 50일) 이내 통보", day="90일 이내\n(승인대상 75일)", opt=True),
            dict(a="사업자", t="착공후지하안전조사", d="매월 말 기준 다음 달 10일까지 제출, 종료 후 15일 이내 조사서 제출")],
         "지하안전관리에 관한 특별법 제14~23조, 동법 시행령 제17·19·21·23·25·43조 (2026.02.01 시행본)")],
    14: [("설계안전성 검토(DFS) 절차", [
            dict(a="설계자", t="설계안전검토보고서 작성", d="실시설계 시 시공과정 위험요소 저감"),
            dict(a="발주청", t="국토안전관리원에 검토 의뢰"),
            dict(a="국토안전관리원", t="검토 · 결과 통보", day="의뢰일부터\n20일 이내"),
            dict(a="발주청", t="설계 반영 · 착공 전 국토교통부장관 제출")],
         "건설기술 진흥법 제62조, 동법 시행령 제75조의2 (2026.06.09 시행본)"),
        ("안전관리계획 수립 절차", [
            dict(a="건설사업자", t="안전관리계획 수립", d="1·2종 시설물, 지하 10m 이상 굴착 등 (시행령 제98조)"),
            dict(a="발주청·인허가기관", t="착공 전 제출 (변경 시 동일)"),
            dict(a="국토안전관리원", t="1·2종 시설물 검토 의뢰 시 검토", opt=True),
            dict(a="발주청·인허가기관", t="검토결과 통보", day="제출일부터\n20일 이내"),
            dict(a="발주청·인허가기관", t="국토교통부장관 제출", day="통보일부터\n7일 이내"),
            dict(a="건설사업자", t="안전관리계획 이행 · 점검")],
         "건설기술 진흥법 제62조, 동법 시행령 제98조")],
    15: [("유해·위험방지계획서 절차 (건설업)", [
            dict(a="사업주", t="유해·위험방지계획서 작성", d="별지 제17호서식 + 별표 10 서류"),
            dict(a="사업주", t="한국산업안전보건공단 제출 (2부)", d="공사 준비기간은 착공으로 보지 않음", day="착공 전날까지"),
            dict(a="한국산업안전보건공단", t="심사 · 결과 통보", day="접수일부터\n15일 이내"),
            [dict(a="판정", t="적정"), dict(a="판정", t="조건부 적정", d="일부 개선"), dict(a="판정", t="부적정", d="계획 변경 · 착공 중지 등", opt=True)],
            dict(a="한국산업안전보건공단", t="공사 중 확인", d="자체심사 업체는 자체확인 (사망재해 시 공단 확인)", day="6개월 이내마다")],
         "산업안전보건법 제42·43조, 동법 시행규칙 제42~47조 (2026.08.01 시행본)")],
    16: [("해상교통안전진단 절차", [
            dict(a="사업자", t="해상교통안전진단 실시", d="안전진단대행업자, 진단 불필요 판단 시 의견서 제출 → 30일 이내 회신"),
            dict(a="처분기관", t="허가 신청 시 안전진단서 제출받음"),
            dict(a="처분기관", t="해양수산부장관에게 진단서 제출", d="허가 등 전", day="10일 이내"),
            dict(a="해양수산부장관", t="검토 · 검토의견 통보", d="전문기관 의견 청취 가능, 보완·협의기간 제외", day="45일"),
            dict(a="처분기관", t="사업자에게 검토의견 통보", day="10일 이내"),
            dict(a="사업자", t="(이견 시) 이의신청 → 결과 20일(연장 10일)", day="30일 이내", opt=True),
            dict(a="처분기관", t="검토의견 반영 · 허가 등 → 이행 확인", d="미이행 시 이행명령 · 사업중지명령")],
         "해상교통안전법 제13~17조 (2024.07.26 시행, 종전 해사안전법) — 국가기관·지자체는 장관 직접 협의 45일")],
    17: [("해상풍력 계획입지 인허가 절차 (해상풍력법, 2026.03.26 시행)", [
            dict(a="기후에너지환경부·해양수산부", t="해상풍력 입지정보망 구축 · 운영"),
            dict(a="해상풍력발전위원회", t="예비지구 지정 (의결 · 고시)", d="풍황·어업·해상교통·환경·군사 등 요건, 시·도지사 신청 가능"),
            dict(a="해상풍력발전위원회", t="기본설계안 확정 · 고시"),
            dict(a="민관협의회 (주민·어업인)", t="협의 · 열람 · 공청회(설명회)", day="통보 후 3개월\n이내 구성"),
            dict(a="해상풍력발전위원회", t="발전지구 지정", d="전력계통 연계 확인, 이익공유"),
            dict(a="해상풍력발전위원회", t="사업자 선정 (입찰)", d="발전단가·재무능력·상생·산업기여"),
            dict(a="사업자", t="실시계획 수립 · 승인 신청", d="환경성평가 포함", day="선정일부터\n2년 이내"),
            dict(a="관계기관", t="관계 행정기관 협의", d="기간 내 의견 없으면 협의 간주", day="30일 이내"),
            dict(a="해상풍력발전위원회", t="실시계획 승인 (28개 법률 인허가 의제) · 고시", day="14일 이상 열람"),
            dict(a="사업자", t="착공 → 준공인가", day="승인일부터\n3년 이내 착공")],
         "해상풍력 보급 촉진 및 산업 육성에 관한 특별법 제6~31조")],
    18: [("어업피해 영향조사 · 보상 절차 (일반 실무)", [
            dict(a="사업시행자", t="어업피해조사 용역 발주", d="수산 분야 전문 조사기관"),
            dict(a="조사기관", t="조사계획 수립 · 어업인 설명", d="조사범위·방법·기준일 협의"),
            dict(a="조사기관", t="현장조사 · 피해범위·정도 예측"),
            dict(a="조사기관", t="조사 결과보고서 제출"),
            dict(a="사업시행자", t="보상계획 공고 · 열람 → 감정평가"),
            dict(a="사업시행자", t="보상 협의"),
            [dict(a="협의 성립", t="보상금 지급 · 공사"), dict(a="협의 불성립", t="토지수용위원회 재결 → 이의재결·행정소송", opt=True)]],
         "공익사업을 위한 토지 등의 취득 및 보상에 관한 법률 및 동법 시행규칙 제44조(어업권의 평가 등), 수산업법 — 법정 처리기간 없음, 사업별 협약 확인")],
    19: [("매장유산 지표조사 절차", [
            dict(a="사업시행자", t="지표조사 실시 (매장유산 조사기관)", d="국가·지자체 사업은 미리 국가유산청장에게 통보"),
            dict(a="사업시행자", t="지표조사 보고서 제출", d="문헌·현장조사, 조사기관 의견", day="조사 완료일부터\n20일 이내"),
            dict(a="지자체", t="의견 제출 (요청 시)", day="7일 이내", opt=True),
            dict(a="국가유산청장", t="검토결과 통보", day="제출일부터\n30일 이내"),
            [dict(a="결과", t="조치 없음 → 공사"), dict(a="결과", t="표본·시굴·정밀발굴조사"), dict(a="결과", t="입회조사 등", opt=True)],
            dict(a="사업시행자", t="발굴조사 (착수 2주 전 통보, 완료 20일 이내 보고)", d="현지·이전·기록보존 조치")],
         "매장유산 보호 및 조사에 관한 법률 제6~12조, 동법 시행령 제5조의2~4·8·12·13·14조 (2026.05.17 시행본) / 지정 문화유산 주변은 「문화유산의 보존 및 활용에 관한 법률」 현상변경 허가")],
    20: [("수저준설토사 처리 · 유효활용 절차 (일반 실무)", [
            dict(a="사업자", t="준설계획 수립"),
            dict(a="전문검사기관", t="준설토사 성분·오염도 검사"),
            dict(a="사업자", t="유효활용기준(용도·오염도) 충족 여부 판단"),
            [dict(a="기준 충족", t="유효활용 (매립재·성토재 등)", d="해양이용협의 시 일괄 협의 가능"),
             dict(a="기준 미충족", t="해양배출 또는 육상처리", d="해양폐기물 및 해양오염퇴적물 관리법", opt=True)],
            dict(a="지방해양수산청", t="협의 · 승인 · 사후관리")],
         "「수저준설토사 유효활용기준」(해양수산부 고시), 해양폐기물 및 해양오염퇴적물 관리법 — 세부 조문·기간은 현행 고시 확인 필요")],
    21: [("설계의 경제성 등 검토(설계VE) 절차", [
            dict(a="발주청", t="대상 확인", d="총공사비 100억 이상 기본·실시설계 / 실시설계 후 3년 이상 지나 발주 / 공사비 10% 이상 조정 설계변경"),
            dict(a="발주청", t="설계VE 검토조직 구성"),
            dict(a="VE팀", t="정보수집 · 기능분석"),
            dict(a="VE팀", t="대안 창출 · 평가 · 제안서 작성"),
            dict(a="발주청", t="채택 여부 결정 · 설계 반영"),
            dict(a="발주청", t="검토결과·반영결과 국토교통부장관 제출")],
         "건설기술 진흥법 시행령 제75조, 「설계공모, 기본설계 등의 시행 및 설계의 경제성 등 검토에 관한 지침」(국토교통부 고시)")],
    22: [("경관심의 절차", [
            [dict(a="사회기반시설 (시행령 제18조)", t="도로·철도 500억 이상\n하천시설 300억 이상", d="기본설계 완료 전 (곤란 시 실시설계 완료 전)"),
             dict(a="개발사업 (시행령 제19조)", t="도시지역 3만m² 이상\n도시지역 외 30만m² 이상", d="심의 시기 : 시행령 별표"),
             dict(a="건축물 (시행령 제21조)", t="경관법 제28조 대상", d="건축허가 전")],
            dict(a="사업자", t="경관심의 신청", d="사전경관계획 : 30만m² 이상 또는 연면적 20만m² 이상"),
            dict(a="경관위원회", t="심의 (소속 관리청·국토교통부·허가권자)", d="회의 결과 10일 이내 홈페이지 공개"),
            dict(a="사업자", t="심의결과 설계 반영", d="면적 30% 이상 증감 등 변경 시 재심의")],
         "경관법 제26~28조, 동법 시행령 제18~21·26조 (2025.10.01 시행본)")],
    23: [("공공디자인 사업 추진 절차", [
            dict(a="문화체육관광부·시·도", t="공공디자인 진흥 종합계획(5년)·지역계획", d="공공디자인위원회·지역위원회 심의"),
            dict(a="공공기관", t="공공디자인 사업 기획", d="기본원칙(공공성·안전성·접근성·주민참여) 준수"),
            dict(a="공공기관", t="공공디자인 용역 · 필요 시 공청회"),
            dict(a="추진협의체", t="위원회 자문 요청", opt=True),
            dict(a="지자체 위원회", t="공공디자인 심의 (지자체 조례 대상)", d="개별 사업 심의는 법률이 아닌 지자체 조례로 운영", opt=True),
            dict(a="공공기관", t="설계 반영 · 시행")],
         "공공디자인의 진흥에 관한 법률 제5·6·10~17조 (2025.10.01 시행본), 관할 지자체 공공디자인 조례")],
    24: [("항만공간 공공디자인 협의 절차 (일반 실무)", [
            dict(a="설계자", t="가이드라인 적용 대상 확인", d="항만시설 5대 분야 40개 유형"),
            dict(a="설계자", t="기본설계 반영 · 체크리스트 작성"),
            dict(a="지방해양수산청·항만공사", t="협의 · 자문"),
            dict(a="설계자", t="실시설계 반영"),
            dict(a="발주청", t="시공 · 유지관리 반영")],
         "항만공간의 공공디자인 가이드라인 (해양수산부 예규) — 법정 처리기간 없음, 예규 현행본 확인")],
}


@st.cache_data(show_spinner=False)
def flow_pngs(n):
    return [(cap, flow_png(cap, steps, basis)) for cap, steps, basis in FLOWS.get(n, [])]


def show_flows(n, has_old=False):
    """6. 절차 — 현행 법령 기준 흐름도 표시 (+ 기존 참고 그림 보기 토글)"""
    st.markdown("<div style='background:#eff6ff;border-left:4px solid #1d4ed8;padding:6px 12px;margin:4px 0 10px;border-radius:0 6px 6px 0;"
                "color:#1e293b;font-size:0.88rem'>📌 아래 흐름도는 <b>현행 법령(2026.10 확인) 기준</b>으로 새로 작성한 도식입니다. "
                "주황 상자 = 법정 기간 (보완기간·공휴일 등 제외 규정 별도), 점선 = 해당 시·선택 단계.</div>", unsafe_allow_html=True)
    for cap, png in flow_pngs(n):
        st.image(png, caption=cap, use_container_width=True)
    global _OLD_ON
    _OLD_ON = st.toggle("기존 참고 그림 보기 (구 자료 — 현행 법령과 다를 수 있음)", key=f"old_img_{n}") if has_old else False


_OLD_ON = False


def _old_img(path, caption=None, width=None):
    if _OLD_ON and Path(path).exists():
        st.image(path, caption=caption, width=width)


# =====================================================================
# ★ [v2.1] 항목별 대상범위 · 근거 위치 (법 → 시행령 → 별표) — 2026.10 확인
#    ✔ = 현행 조문 확인, ※ = 별표 원문(HWP/PDF)·고시 확인 필요
# =====================================================================
SCOPE_INFO = {
    1: dict(scope=["법 제9조① 18개 분야 계획 : 도시 개발 · 산업입지/산업단지 · 에너지 · **항만의 건설** · 도로 · 수자원 · 철도 · 공항 · 하천 · **개간 및 공유수면의 매립** · 관광단지 · 산지 · 특정지역 · 체육시설 · 폐기물처리시설 · 국방·군사 · 토석·모래·자갈 채취 · 가축분뇨관리기본계획",
                   "법 제9조② 구분 : **정책계획**(기본방향·지침 제시) / **개발기본계획**(개발구역 지정, 실시계획의 기준이 되는 계획)",
                   "구체적 대상계획 : 정책계획 15개 · 개발기본계획 86개 계획 (2021 검토 기준, 현행 개수는 별표 2 확인)",
                   "[별표 2] 항만·해양 분야 대상계획 예 : **항만법 제5조 항만기본계획**(해양수산부장관이 관계 중앙행정기관과 협의하는 때), **항만 재개발 및 주변지역 발전에 관한 법률 제9조 항만재개발사업계획**, 마리나항만 기본계획·사업계획, 어촌·어항법 제17조 어항의 지정(지정 전), 공유수면매립 기본계획",
                   "평가항목 등 결정 시 환경영향평가협의회 심의 생략 : 개발기본계획 사업계획 면적 **6만㎡ 미만** (시행령 제8조)"],
            where=["「환경영향평가법」 제9조(전략환경영향평가의 대상) ✔", "같은 법 시행령 제7조(대상계획의 종류)② ✔",
                   "시행령 [별표 2] 전략환경영향평가 대상계획 및 협의 요청시기 ※"],
            timing="계획 수립·확정 전, 관계기관의 장과 협의하는 때 ([별표 2] '협의 요청시기' 열)"),
    2: dict(scope=["법 제22조① 18개 분야 사업 : 도시 개발 · 산업단지 · 에너지 · **항만의 건설** · 도로 · 수자원 · 철도 · 공항 · 하천 · **개간 및 공유수면의 매립** · 관광단지 · 산지 · 특정지역 · 체육시설 · 폐기물처리시설 · 국방·군사 · 토석 채취 · 가축분뇨처리시설",
                   "구체적 종류·규모 : 17개 분야 78개 세부사업 — **[별표 3] 제4호 '항만의 건설'** :",
                   "　가. 어항개발사업 / 나. **항만법 항만시설** / 라. 신항만건설사업 / 바. 마리나항만 — ① **외곽시설 길이 300m 이상** 또는 공유수면 **3만㎡ 이상 매립** 수반 ② **계류시설** : 공유수면 **3만㎡ 이상 매립** 수반 ③ 그 밖의 항만시설 : 매립 수반 시 **매립 3만㎡ 이상**, 매립 없으면 **사업면적 15만㎡ 이상**",
                   "　다. 항만·신항만 **준설사업** : 준설면적 **10만㎡ 이상** 또는 준설량 **20만㎥ 이상** (항로·정박지 유지준설, 오염물질 제거 준설 제외)",
                   "　마. **항만재개발사업** : 사업면적 **30만㎡ 이상** 또는 위 ①~③ 시설",
                   "**[별표 3] 제10호 '공유수면의 매립'** : 무역항·연안항·신항만·자연환경보전지역 매립 **3만㎡ 이상**, 그 밖의 지역 **30만㎡ 이상**",
                   "협의 요청시기 : 관리청 시행 = 항만법 제9조⑨ 항만개발사업 고시 전 / 항만공사 = 항만공사법 제22조 실시계획 승인 전 / 비관리청 = 항만법 제9조② 허가 전 / 매립 = 공유수면법 제28조 면허(국가·지자체는 제35조 협의·승인) 전",
                   "재협의(시행령 제54조) : 승인 후 5년 이내 미착공, 규모 30% 이상 증가, 최소 평가대상 규모 이상 증가, 7년 이상 공사중지 후 재개",
                   "변경협의(시행령 제55조) : 규모 10% 이상 증가, 부지면적 15% 이상 토지이용계획 변경 등"],
            where=["「환경영향평가법」 제22조(환경영향평가의 대상) ✔", "같은 법 시행령 제31조(대상사업 및 범위)② ✔",
                   "시행령 [별표 3] 환경영향평가 대상사업의 구체적인 종류, 범위 및 협의 요청시기 ※ (항만 : 제4호)",
                   "재협의·변경협의 : 법 제32·33조, 시행령 제54·55조"],
            timing="사업계획 등의 승인 전 ([별표 3] '협의 요청시기' 열) — 평가준비서 심의 30일, 협의 45일(연장 60일)"),
    3: dict(scope=["소규모 : 법 제43조① — ① 보전이 필요한 지역·난개발 우려 지역(보전용도지역)에서 시행 + ② 환경영향평가 대상이 아닌 개발사업 (두 요건 모두)",
                   "[별표 4] 용도지역별 사업계획 면적 : 관리지역 — **보전관리 5,000㎡ · 생산관리 7,500㎡ · 계획관리 10,000㎡** 이상 / **농림지역 7,500㎡** / **자연환경보전지역 5,000㎡** / **개발제한구역 5,000㎡** 이상 (그 밖에 자연환경보전법·습지보전법 등 보호지역 기준)",
                   "제외 : 응급조치 사업, 군사기밀·국가안보 사업 (법 제43조②)",
                   "사후환경영향조사 : 환경영향평가 대상사업 — 대상사업·조사기간은 시행규칙 [별표 1]"],
            where=["「환경영향평가법」 제43조(소규모 환경영향평가의 대상) ✔", "같은 법 시행령 제59조 ✔ · [별표 4] 소규모 환경영향평가 대상사업의 종류, 범위 및 협의 요청시기 ※",
                   "사후조사 : 법 제36조 ✔ · 시행규칙 제19조 · [별표 1] 대상사업 및 조사기간 ※"],
            timing="소규모 : 사업계획 승인 전, 협의 30일(연장 40일) / 사후조사 : 착공 후, 조사기간 종료 후 60일 이내 통보 (1년 이상은 연도별)"),
    4: dict(scope=["전략환경영향평가 · 환경영향평가 대상 계획·개발사업 중 **온실가스를 다량 배출하는 사업 등 대통령령으로 정하는 계획·사업** (법 제23조①)",
                   "적용 예 : 에너지 개발, 산업단지 조성, 폐기물 처리시설 설치 등 — 세부 대상은 탄소중립기본법 시행령에서 확인",
                   "평가 내용 : 사업이 기후변화에 미치는 영향 + 기후변화로 사업이 받는 영향 (감축·적응방안)"],
            where=["「기후위기 대응을 위한 탄소중립·녹색성장 기본법」 제23조(기후변화영향평가) ✔", "같은 법 시행령 (기후변화영향평가 대상 계획·사업) ※",
                   "「기후변화영향평가 방법 등에 관한 규정」(기후에너지환경부 고시) ※"],
            timing="평가준비서 작성 단계부터 병행 → 전략·환경영향평가 협의 요청 시 함께 요청 (평가서는 별책)"),
    5: dict(scope=["일반 해양이용협의(법 제9조) : **공유수면 점용·사용허가**, **매립면허**, 바다골재채취 예정지 지정, 일부 양식업 면허 등 면허등 대상",
                   "해양이용영향평가(법 제13조) : 공유수면 준설·굴착, 토석 채취, 흙·돌 투기 등 수심에 영향을 미치는 행위, 해저광물·광물 채취, 해양심층수, 바다골재, 재생에너지(해상풍력) 등이 **일정 규모 이상**",
                   "해양 영향 경미 사업 : 검토기관 의견 청취 생략 가능 (법 제12조② 단서, 종전 '간이 해역이용협의')",
                   "재협의(시행령 제17조) : 면적·길이 30% 이상 증가, 7년 이상 중지 후 재개",
                   "[종전 별표 15 일반 협의 기준 — 신법 별표 1 대조] 항만시설 : **계류·외곽·임항교통시설 길이 150m 이상 또는 점용 3천㎡ 이상**, 기능시설 점용 3천㎡ 이상, **준설 5만㎡ 이상 또는 10만㎥ 이상**(유지준설 제외), 그 밖의 항만시설 점용 5만㎡ 이상 / 인공구조물 150m·3천㎡ / 굴착 2만㎡·5만㎥ / 취·배수관 지름 400mm 이상 / **매립은 바다·바닷가 매립 전부**",
                   "[종전 기준] 준설 10만㎡ 또는 20만㎥ 이상, 토석 채취·투기량 영해 20만㎥ · EEZ 40만㎥ 이상 등은 **해양이용영향평가** 대상 범위"],
            where=["「해양이용영향평가법」 제9조(협의 대상)·제13조(평가 대상) ✔ — 2026.9.18 시행", "같은 법 시행령 [별표 1] 해양이용협의 대상 범위 ※ · [별표 2] 해양이용영향평가 대상 규모 ※",
                   "종전 : 해양환경관리법 제84·85조, 시행령 [별표 15·16] (2024.12.31 삭제)"],
            timing="면허등(점용·사용허가·매립면허 등) 전 — 해양공간적합성협의 이후 요청 / 협의의견 일반 30일, 영향평가 45일"),
    6: dict(scope=["해양이용협의·해양이용영향평가를 거쳐 면허등을 받은 사업", "조사 항목 : 해양환경기준이 정해진 항목(수질·퇴적물) + 협의의견 통보 시 지정 항목",
                   "조사 기간·주기(종전 별표 17) : 일반 협의 사업 = 사업 시작 ~ 완료, 반기 1회 (매립 1.5만㎡ 미만 제외) / 영향평가 사업 = 사업 시작 ~ 완료 후 3년, 시행 중 분기 1회·완료 후 반기 1회",
                   "결과 제출 : 단년도 조사 종료 후 30일 이내, 다년도 다음 해 1월 31일까지 / 사후환경영향조사 실시 사업은 생략 가능"],
            where=["「해양이용영향평가법」 제29조(해양환경영향조사) ✔", "대상사업·조사항목·조사기간 : 해양수산부령(시행규칙) ※",
                   "종전 : 해양환경관리법 제95조, 시행령 제71조 · [별표 17]"],
            timing="면허등 후 사업 시행 기간 (조사서 : 처분기관 · 해양수산부장관 통보)"),
    7: dict(scope=["법 제15조① 8종 계획 : 해양관광단지 개발 · 석유 채취 · 광물·골재 채취 · **항만·어항 개발** · 수자원 개발 · 해양에너지 개발 · 어장 개발 · 그 밖의 해양자원 이용·개발 계획",
                   "구체적 대상 : 25개 법률 48개 계획 및 지구·구역 (항만기본계획, 어항개발계획, 해양관광단지 등)",
                   "요청 주체 : 계획을 승인·수립·변경하거나 지구·구역을 지정하는 중앙행정기관·지방자치단체의 장"],
            where=["「해양공간계획 및 관리에 관한 법률」 제15조(해양공간적합성협의) ✔", "같은 법 시행령 제13조② ✔ · [별표] 해양공간적합성협의 대상 및 협의 요청시기 ※ (2025.5.1 개정)",
                   "검토기간 : 시행령 제16조(45일) · 재협의 제17조(20일) ✔"],
            timing="관계 행정기관 협의 전, 해양이용협의·해양이용영향평가 요청 전 (시행령 제13조② 단서)"),
    8: dict(scope=["점용·사용허가(법 제8조①) 11개 행위 : 인공구조물(부두·방파제·교량 등) 신·개·증축·제거, 접한 토지 굴착, **준설·굴착**, 토지 조성, 취·배수, 토석 채취, 식물 재배, **흙·돌 투기**, 국가시설 점용, 광물 채취, 기타 점용",
                   "허가기간(법 제11조) : 부두·방파제·교량 등 견고한 구조물 30년, 그 밖의 구조물 15년, 기타 5년",
                   "매립(법 제28조) : 매립기본계획(10년마다, 5년마다 타당성 검토)에 반영된 구역 — 매립목적 17개 시설용지([별표 2])",
                   "면허관청 : 10만㎡ 이상 해양수산부장관, 무역항 해양수산부(지방청 위임), 그 외 시·도지사"],
            where=["「공유수면 관리 및 매립에 관한 법률」 제8조·제11조·제17조(점용·사용) ✔", "같은 법 제22·23·27조(매립기본계획), 제28조(매립면허)·제38조(실시계획)·제45조(준공검사) ✔",
                   "같은 법 시행령 제7조(관계기관 협의 20일)·제34조 ✔ · [별표 2] 매립목적 ※"],
            timing="항만개발사업 실시계획 승인 전 — 점용·사용 실시계획 : 허가 후 1년 이내 / 매립 실시계획 : 면허 후 1년 이내"),
    9: dict(scope=["재해영향성검토(행정계획) : 37개 법령 47개 행정계획 — **규모 무관** / 해양 분야 : 공유수면매립 기본계획, 어항개발계획, 항만배후단지개발 종합계획, 신항만건설 기본계획, 마리나항만 사업계획",
                   "재해영향평가(개발사업) 해양 분야 : **항만법 제10조 항만개발사업 실시계획**(수립 전, 비관리청은 승인 전), 신항만건설사업 실시계획, **공유수면매립 실시계획**(제38조), 마리나항만 실시계획, 어항개발사업계획",
                   "재해영향평가(개발사업) : 48개 법령 59개 개발사업 — **면적 5만㎡ 이상 또는 길이 10km 이상** (협의 45일)",
                   "소규모 재해영향평가 : **면적 5천㎡ 이상 5만㎡ 미만 또는 길이 2km 이상 10km 미만** (협의 30일)",
                   "제외(시행령 제6조①) : 재해복구사업, 부지 조성이 끝났거나 시행 중인 지구 안의 개발사업"],
            where=["「자연재해대책법」 제4조(재해영향평가등의 협의) ✔", "같은 법 시행령 제4조(협의기간) ✔ · 제6조(협의 대상 및 방법) ✔",
                   "시행령 [별표 1] 재해영향평가등의 협의 대상 행정계획 및 개발사업의 범위 및 협의시기 ※"],
            timing="행정계획 확정 전 / 개발사업 실시계획 승인·개발행위 허가 전 — 사전검토 14일, 협의 45일·30일(연장 10일)"),
    10: dict(scope=["도시교통정비지역 또는 그 교통권역에서 하는 법 제15조① 사업 : 도시 개발 · 산업단지 · 에너지 · **항만의 건설** · 도로 · 철도 · 공항 · 관광단지 · 특정지역 · 체육시설 · 건축물(공동주택·창고·운수시설 등 20종) · 민간투자사업",
                    "구체적 범위 : 11개 분야 29개 대상사업 — **[별표 1] 라목 '항만의 건설' : 연간 하역능력 150만 톤 이상** (파이프라인 등 자동화 설비로 차량 수송수요가 없는 기능시설은 협의 후 제외)",
                    "제출 시기(항만) : 항만법 제10조 실시계획 수립·승인 전 (항만공사 시행 시 항만공사법 제22조 실시계획 승인 전)",
                    "시·도 조례 : 별표 1 규모의 50% 이상 범위에서 대상 확대 가능 (시행령 제13조의2⑦)"],
             where=["「도시교통정비 촉진법」 제15조(교통영향평가의 실시대상) ✔", "같은 법 시행령 제13조의2(대상사업 등) ✔",
                    "시행령 [별표 1] 교통영향평가 대상사업의 범위 및 교통영향평가서의 제출·심의 시기 ※"],
             timing="[별표 1]의 제출·심의 시기 (사업계획 승인 전) — 이의신청 30일, 결과 통보 60일"),
    11: dict(scope=["기반시설(국토계획법 제2조6호, 시행령 제2조) 7종 : 교통시설(도로·철도·**항만**·공항 등) · 공간시설 · 유통·공급시설 · 공공·문화체육시설 · 방재시설 · 보건위생시설 · 환경기초시설",
                    "지상·수상·공중·수중 또는 지하에 기반시설을 설치하려면 미리 도시·군관리계획으로 결정 (법 제43조①)",
                    "도시지역 외 등 결정 없이 설치 가능한 경우 : 시행령 제35조 확인"],
             where=["「국토의 계획 및 이용에 관한 법률」 제2조·제43조(도시·군계획시설의 설치·관리) ✔", "결정 절차 : 법 제25~32조, 시행령 제22조(주민 의견청취 14일 이상)·제25조 ✔",
                    "관계 행정기관 협의 30일 : 법 제30조 ✔"],
             timing="도시·군계획시설사업 실시계획 인가 전 (입안 → 주민·의회 의견 → 협의 → 심의 → 결정·고시)"),
    12: dict(scope=["대상 사업(시행령 제20조①) : 도시개발 · 산업단지 개발 · 에너지 개발 · **항만 건설** · 철도 · 공항 · 관광단지 등",
                    "공공사업주관자 : 연료·열 연간 **2,500 TOE 이상** 또는 전력 연간 **1천만 kWh 이상** 시설",
                    "민간사업주관자 : 연료·열 연간 **5,000 TOE 이상** 또는 전력 연간 **2천만 kWh 이상** 시설"],
             where=["「에너지이용 합리화법」 제10조(에너지사용계획의 협의) ✔", "같은 법 시행령 제20조(대상사업 및 규모)①~④ ✔ — 대상 사업 8종 중 제4호 **항만건설사업** · [별표 1] 제출 시기 ※",
                    "검토 위탁 : 시행령 제51조(한국에너지공단) ✔"],
             timing="[별표 1] 제출 시기 (사업계획 승인 전) — 결과 통보 30일(연장 20일), 협의 완료 전 공사 시행 금지"),
    13: dict(scope=["지하안전평가 : 굴착깊이 **20m 이상** 굴착공사를 수반하는 사업",
                    "소규모 지하안전평가 : 굴착깊이 **10m 이상 20m 미만** (시행령 제23조)",
                    "착공후지하안전조사 : 평가서에 기재된 실시기간 동안 조사 (시행령 제21조)"],
             where=["「지하안전관리에 관한 특별법」 제14조(지하안전평가 대상)·제23조(소규모) ✔", "같은 법 시행령 제16조③ · [별표 1] 협의 요청 시기 ※, 제17조(협의기간 30일·연장 50일) ✔",
                    "시행령 제21조(착공후조사)·제23조(소규모 대상)·제43조(권한 위임) ✔"],
             timing="사업계획 승인 전 ([별표 1]) — 협의 30일(연장 50일)"),
    14: dict(scope=["안전관리계획 대상(시행령 제98조①) : **1·2종 시설물** 건설공사, **지하 10m 이상 굴착**, 폭발물 사용, 10층 이상 건축물, 일정 건설기계 사용 공사 등",
                    "설계안전성 검토(시행령 제75조의2) : 안전관리계획 수립 대상 공사의 **실시설계** 시 국토안전관리원에 검토 의뢰"],
             where=["「건설기술 진흥법」 제62조(건설공사의 안전관리) ✔", "같은 법 시행령 제75조의2(설계의 안전성 검토) ✔ · 제98조(안전관리계획의 수립 대상) ✔"],
             timing="설계안전성 검토 : 실시설계 시 (검토 20일) / 안전관리계획 : 착공 전 제출 (검토 20일, 통보 후 7일 이내 국토교통부 제출)"),
    15: dict(scope=["건설공사 대상(산업안전보건법 시행령 제42조③) : 지상 높이 **31m 이상** 건축물·인공구조물, 연면적 3만㎡ 이상 건축물, **최대 지간 50m 이상** 교량, 터널, 다목적·발전용 댐, **깊이 10m 이상 굴착** 등",
                    "제조업 등 (시행령 제42조①②) : 해당 업종·설비 — 본 가이드는 건설공사 기준"],
             where=["「산업안전보건법」 제42조(유해위험방지계획서의 작성·제출) ✔", "같은 법 시행령 제42조(대상 사업장·건설공사) ※ 조문 확인",
                    "같은 법 시행규칙 제42~47조(제출·심사·확인) ✔ — 2026.8.1 시행본"],
             timing="착공 전날까지 한국산업안전보건공단 제출 — 심사 15일, 공사 중 6개월 이내마다 확인"),
    16: dict(scope=["대상사업(법 제2조14호) : 항로·정박지 지정·변경, 통항 금지·제한 수역 설정, **수역 내 교량·터널·케이블** 건설, **항만·부두 개발·재개발**, 그 밖에 대통령령으로 정하는 사업",
                    "[대상 범위 — 종전 해사안전법 시행령 별표, 해상교통안전법 시행령 대조] **길이 100m 이상 선박이 통항하는 수역의 교량·터널**(수심 4m 미만 제외), 지정 항로·정박지를 횡단하는 해월케이블",
                    "**계류시설·방파제·파제제·방조제 등 시설물** : 공유수면 점용·사용 또는 매립 수역 **길이 200m 이상 또는 면적 2만㎡ 이상** (수심 4m 미만 제외, 국가어항·마리나 시설 제외)",
                    "**길이 100m 이상 선박이 이용하는 계류시설 건설**, 계류시설 길이·접안능력 확장 (거대선 10%, 그 밖 20% 이상), 무역항·연안항 신규 지정, 항로·정박지 인근(최대선박 길이 3배 이내) 방파제 건설, 최고속력 60노트 이상 선박 투입 해운업",
                    "제출 불필요 판단 시 의견서 제출 → 30일 이내 회신 (법 제14조)"],
             where=["「해상교통안전법」 제2조14호·제13~17조 ✔ — 2024.7.26 시행 (종전 해사안전법)", "같은 법 시행령 (안전진단 대상사업의 범위) ※ · 시행규칙 (해상교통안전진단기준)"],
             timing="허가등을 받으려는 경우 처분기관에 진단서 제출 → 10일 이내 해양수산부 제출 → 45일 검토"),
    17: dict(scope=["해상풍력 발전사업 : 예비지구 → 발전지구 지정 → 입찰로 사업자 선정 → 실시계획 승인 (28개 법률 인허가 의제)",
                    "기존 사업자 : 시행 전 전기사업허가를 받은 자는 사업자 선정 신청 가능 (부칙 제2조)",
                    "계획입지 외 전기사업허가 제한 : 2028.3.26부터 (법 제33조①)"],
             where=["「해상풍력 보급 촉진 및 산업 육성에 관한 특별법」 제6~31조 ✔ — 2026.3.26 시행", "같은 법 시행령 (세부 기간·절차) ※"],
             timing="예비지구 지정 이후 단계별 — 실시계획 신청 : 선정일부터 2년 이내, 착공 : 승인일부터 3년 이내"),
    18: dict(scope=["공익사업 시행으로 **면허·허가·신고어업**의 어업권 등이 제한·정지·취소되거나 피해가 예상되는 사업 (매립, 항만건설, 준설, 해상풍력 등)",
                    "보상 대상 : 사업 고시일 및 사업 시행 당시 적법한 면허·허가·신고어업자 (대법원 2011두5728)",
                    "공유수면 매립면허 신청 시 피해영향조사서 첨부 (공유수면법 시행령 제12조 지정기관 조사)"],
             where=["「공익사업을 위한 토지 등의 취득 및 보상에 관한 법률」 시행규칙 제44조(어업권의 평가 등) ✔", "「수산업법」·「양식산업발전법」 (어업 손실보상) ※",
                    "참고 : 어업피해영향조사 안내 (해양수산 전문 조사기관)"],
             timing="기본설계·실시계획 승인 전 조사 → 보상계획 공고 → 협의 → (불성립 시) 재결 — 법정 처리기간 없음"),
    19: dict(scope=["지표조사 대상(종전 시행령 제4조①) : ① **토지에서 시행하는 건설공사 사업면적 3만㎡ 이상** ② 내수면 건설공사 3만㎡ 이상 (골재채취 15만㎡) ③ **연안(연안관리법)에서 시행하는 건설공사 3만㎡ 이상** (골재채취 15만㎡) ④ 그 미만이라도 지자체장이 필요하다고 인정하는 공사",
                    "국가·지자체 사업은 미리 국가유산청장에게 통보 (시행령 제5조의2)",
                    "보고서 : 조사 완료일부터 20일 이내 제출 → 국가유산청 30일 이내 검토결과 통보 → 표본·시굴·정밀발굴조사 등",
                    "현상변경 허가 : 지정 문화유산 및 역사문화환경 보존지역(외곽 경계로부터 일정 범위) 안의 건설공사"],
             where=["「매장유산 보호 및 조사에 관한 법률」 제6조(지표조사) ✔ · 시행령 제5조의2~4 ✔ (대상 규모 조문 ※ 확인)",
                    "「문화유산의 보존 및 활용에 관한 법률」 현상변경 허가 조항 (구 문화재보호법 제35조) ※"],
             timing="사업계획 수립·기본설계 단계 (공사 착수 전)"),
    20: dict(scope=["항만 건설·항로 유지 준설 등에서 발생한 수저준설토사", "유효활용기준(용도·오염도) 충족 시 매립재·성토재 등으로 활용, 미충족 시 해양배출·육상처리"],
             where=["「수저준설토사 유효활용기준 등에 관한 규정」(해양수산부 고시) ※", "「해양폐기물 및 해양오염퇴적물 관리법」 (종전 해양환경관리법 제110조 연계) ※"],
             timing="준설계획·실시설계 단계 (해양이용협의 시 일괄 협의 가능)"),
    21: dict(scope=["총공사비 **100억원 이상** 건설공사의 기본설계 및 실시설계 (시행령 제75조①1호)", "실시설계 완료 후 **3년 이상** 지나 발주하는 경우 (3호)",
                    "시공 중 총공사비·공종별 공사비 **10% 이상** 조정 설계변경 (2호)", "그 밖에 발주청이 필요하다고 인정하는 경우 (4호)"],
             where=["「건설기술 진흥법」 제39조의3 (설계의 경제성 등 검토) ※ 조문 확인", "같은 법 시행령 제75조(설계의 경제성등 검토) ✔",
                    "「설계공모, 기본설계 등의 시행 및 설계의 경제성 등 검토에 관한 지침」(국토교통부 고시) ※"],
             timing="기본설계·실시설계 단계 — 검토·반영 결과 국토교통부장관 제출 (시행령 제75조④)"),
    22: dict(scope=["사회기반시설(시행령 제18조) : 도로·철도·도시철도 **총사업비 500억원 이상**, 하천시설 **300억원 이상**",
                    "개발사업(시행령 제19조) : 도시지역 **3만㎡ 이상**, 도시지역 외 **30만㎡ 이상** (별표 제3호다목 사업 20만㎡)",
                    "사전경관계획(시행령 제20조) : 30만㎡ 이상 또는 건축 연면적 합계 20만㎡ 이상", "건축물(법 제28조) : 건축허가 전 (시행령 제21조)"],
             where=["「경관법」 제26조(사회기반시설)·제27조(개발사업)·제28조(건축물) ✔", "같은 법 시행령 제18~21조 ✔ · [별표] 개발사업의 종류·심의 시기 ※ — 2025.10.1 시행본"],
             timing="사회기반시설 : 기본설계 완료 전 (곤란 시 실시설계 완료 전) / 개발사업 : [별표] 시기 / 건축물 : 건축허가 전"),
    23: dict(scope=["공공기관이 조성·제작·설치하는 공공시설물 (대중교통·보행안전·편의·공급·녹지·안내시설물 등, 법 제2조3호)",
                    "개별 사업 심의는 법률이 아닌 **관할 지자체 공공디자인 조례**로 운영 (법은 종합계획·지역계획 심의)"],
             where=["「공공디자인의 진흥에 관한 법률」 제2·5·6·10~17조 ✔ — 2025.10.1 시행본", "관할 시·도, 시·군·구 공공디자인 조례 및 [별표] 심의 대상 ※"],
             timing="기본·실시설계 단계 (조례에서 정한 시기)"),
    24: dict(scope=["항만법에 따른 항만시설 5대 분야 40개 유형 146개 시설물 (기본시설·기능시설·지원시설·항만친수시설·공통 공공시설물)"],
             where=["「항만공간의 공공디자인 가이드라인」(해양수산부 예규) 제1장 제3조(적용범위) ※"],
             timing="기본·실시설계 단계 — 법정 협의기간 없음"),
}


def scope_html(n):
    d = SCOPE_INFO.get(n)
    if not d:
        return ""
    li = lambda xs: "".join(f"<li style='margin:2px 0'>{x}</li>" for x in xs)
    md = lambda s_: _kit_re.sub(r"\*\*(.+?)\*\*", r"<b style='color:#b91c1c'>\1</b>", s_)
    return (f"<div style='border:1px solid #bfdbfe;border-radius:8px;overflow:hidden;margin:8px 0 12px'>"
            f"<div style='background:#1e3a8a;color:#fff;font-weight:800;padding:6px 12px'>📍 대상범위 · 근거 위치 (2026.10 확인 · ✔ 현행 조문 확인 / ※ 별표·고시 원문 확인 필요 — 별표 수치는 '해양&항만 설계ENG 행정규칙집' 수록 기준)</div>"
            f"<table style='width:100%;border-collapse:collapse;font-size:13px;color:#0f172a'>"
            f"<tr><td style='width:120px;background:#eff6ff;font-weight:700;padding:6px 10px;border-top:1px solid #dbeafe;vertical-align:top'>대상범위 요약</td>"
            f"<td style='padding:6px 10px;border-top:1px solid #dbeafe'><ul style='margin:0;padding-left:18px'>{li([md(x) for x in d['scope']])}</ul></td></tr>"
            f"<tr><td style='background:#eff6ff;font-weight:700;padding:6px 10px;border-top:1px solid #dbeafe;vertical-align:top'>근거 위치<br>(법→시행령→별표)</td>"
            f"<td style='padding:6px 10px;border-top:1px solid #dbeafe'><ul style='margin:0;padding-left:18px'>{li(d['where'])}</ul></td></tr>"
            f"<tr><td style='background:#eff6ff;font-weight:700;padding:6px 10px;border-top:1px solid #dbeafe'>협의·실시 시기</td>"
            f"<td style='padding:6px 10px;border-top:1px solid #dbeafe'>{d['timing']}</td></tr></table></div>")


def show_scope(n):
    st.markdown(scope_html(n), unsafe_allow_html=True)


# =====================================================================
# ★ 종합 보고서 생성 엔진 (캐싱 적용으로 화면 새로고침 방지)
# =====================================================================
REPORT_DATA = [
    {
        "title": "1. 전략환경영향평가",
        "content": [
            "• 개요: 환경에 영향을 미치는 계획을 수립할 때 환경보전계획과의 부합 여부를 확인하고, 대안의 설정 및 분석을 통해 환경적 측면에서 계획의 적정성과 입지의 타당성을 사전에 검토하는 제도입니다.",
            "• 실시근거: 환경영향평가법 제9조, 동법 시행령 제7조제2항 및 제22조제2항.",
            "• 대상계획 및 협의시기: 도시 개발, 항만 건설, 도로 건설 등 정책/개발기본계획. 계획수립자가 관계기관의 장과 협의할 때 실시합니다.",
            "👉 근거법령: (환경영향평가법) 시행령 [별표 2]",
            "• 협의기관: 기후에너지환경부장관 또는 지방(유역)환경청장 (평가주체: 행정기관의 장)",
            "• 평가항목: 환경보전계획 부합성, 계획 연계성, 입지 타당성 등. 한국환경정책평가연구원 검토.",
            "• 절차 및 양식: 환경평가협의회 심의(30일) ➔ 스코핑 ➔ 주민의견 청취 ➔ 평가서 작성 및 협의.",
            "👉 법정양식: (환경영향평가법 시행규칙) [별지 서식]"
        ],
        "images": [
            ("전략환경영향평가 절차-개발기본계획.png", "전략환경영향평가 절차 (개발기본계획)"),
            ("전략환경영향평가 절차-정책계획.png", "전략환경영향평가 절차 (정책계획)")
        ]
    },
    {
        "title": "2. 환경영향평가",
        "content": [
            "• 개요: 특정 계획이나 사업이 환경에 미치는 영향을 미리 예측·평가하여 환경보전방안을 마련함으로써 친환경적이고 지속가능한 발전을 도모합니다.",
            "• 실시근거: 환경영향평가법 제22조 및 동법 시행령 제31조.",
            "• 대상사업 및 협의시기: 항만 건설, 수자원 개발 등 17개 분야 78개 세부사업.",
            "👉 근거법령: (환경영향평가법) 시행령 [별표 3]",
            "• 협의기관: 기후에너지환경부장관 또는 지방환경청장 (대상사업을 하려는 자가 주체)",
            "• 평가항목: 동·식물상, 수질, 해양, 지형·지질, 소음·진동 등 총 21개 항목.",
            "• 절차 및 양식: 평가서 초안 작성 ➔ 주민의견 수렴 ➔ 협의 요청 ➔ KEI 검토 ➔ 협의내용 통보.",
            "👉 법정양식: (환경영향평가법 시행규칙) [별지 서식]"
        ],
        "images": [("환경영향평가 절차.png", "환경영향평가 절차 흐름도")]
    },
    {
        "title": "3. 소규모 환경영향평가 및 사후환경영향조사",
        "content": [
            "• 개요: 보전이 필요한 지역 및 난개발 우려 지역 개발 시 소규모 평가 실시, 사업 착공 후에는 사후환경영향조사를 통해 환경 영향을 관리합니다.",
            "• 실시근거: 환경영향평가법 제36조(사후), 제43조(소규모).",
            "• 대상사업 및 협의시기: 보전관리지역 등 9개 분야 20개 소규모 개발사업, 또는 협의가 완료된 환경영향평가 대상사업(사후조사).",
            "👉 소규모 대상: (환경영향평가법) 시행령 [별표 4] / 사후조사 대상: (환경영향평가법) 시행규칙 [별표 1]",
            "• 협의기관: 관할 지방(유역)환경청장.",
            "• 평가항목: 자연생태환경, 수질 등 17개 항목(소규모) 및 사후 관리 계획 항목.",
            "• 절차 및 양식: 착공 후 정기 조사 ➔ 조사결과 및 조치결과 통보서 제출.",
            "👉 법정양식: (환경영향평가법 시행규칙) [별지 서식]"
        ],
        "images": [
            ("소규모 환경영향평가 절차.png", "소규모 환경영향평가 절차 흐름도"),
            ("사후환경영향평가 절차.png", "사후환경영향조사 절차 흐름도")
        ]
    },
    {
        "title": "4. 기후영향평가",
        "content": [
            "• 개요: 국가 온실가스 감축 목표 달성에 기여하기 위해 주요 계획과 개발사업이 기후변화에 미치는 영향을 사전에 평가하고 저감 방안을 수립합니다.",
            "• 실시근거: 기후위기 대응을 위한 탄소중립·녹색성장 기본법 제23조 및 동법 시행령 (전략환경영향평가·환경영향평가에 포함하여 실시, 협의 요청 시 함께 요청).",
            "• 대상사업 및 협의시기: 전략환경영향평가 또는 환경영향평가 협의 요청 시 포함하여 실시.",
            "  - [대상 사업] 에너지 개발, 도시 개발, 산업입지 및 산업단지 조성, 항만 건설, 수자원 개발 등 온실가스 다배출 및 기후변화 취약성이 높은 10개 분야 주요 계획 및 사업",
            "👉 대상범위 상세: (탄소중립기본법 시행령) 기후변화영향평가 대상 계획·개발사업 / 방법: 「기후변화영향평가 방법 등에 관한 규정」(고시)",
            "• 협의기관: 기후에너지환경부장관.",
            "• 평가항목: 온실가스 배출량 산정, 기후변화 적응 및 취약성 평가.",
            "• 절차 및 양식: 영향평가 대상 확인 ➔ 기후변화 영향 예측 및 저감계획 수립 ➔ 협의 완료.",
            "👉 법정양식: (환경영향평가법 시행규칙)"
        ],
        "images": []
    },
    {
        "title": "5. 일반 및 간이 해양 이용협의 및 해양 이용영향평가",
        "content": [
            "• 개요: 해양 개발 행위의 적정성과 예상되는 해양환경 영향을 사전에 검토 및 평가하는 예방적 정책 수단입니다.",
            "• 실시근거: 해양이용영향평가법 제9조(일반 해양이용협의)·제13조(해양이용영향평가) — 2026.9.18 시행 (종전 해양환경관리법 제84·85조 대체).",
            "• 대상사업 및 협의시기: 공유수면 점용·사용 및 매립, 항만 건설 등. 행정계획 확정 이후 실시계획 승인 전.",
            "👉 대상: (해양이용영향평가법) 시행령 [별표 1] (종전 해양환경관리법 시행령 별표 15·16은 2024.12.31 삭제)",
            "• 협의기관: 해양수산부장관 (지방해양수산청 위임), 해양이용영향검토기관 검토 — 협의의견 통보: 일반 해양이용협의 30일, 해양이용영향평가 45일",
            "• 평가항목: 해양물리, 해양화학, 생태계, 수산자원 등 9~14개 항목.",
            "• 절차 및 양식: 협의서 작성 ➔ 제출 ➔ 검토기관 심사 ➔ 통보.",
            "👉 법정양식: (해양이용영향평가법 시행규칙) [별지 서식]"
        ],
        "table": {
            "headers": ["구분", "간이 해양 이용협의", "일반 해양 이용협의"],
            "rows": [
                ["대상 규모", "소규모 사업, 점·사용 면적이 상대적으로 작은 경우", "일정 규모 이상의 대규모 사업, 면적이 넓은 경우"],
                ["환경 영향", "해양 환경에 미치는 영향이 경미할 것으로 예상되는 사업", "해양 환경 및 생태계에 상당한 영향을 미칠 우려가 있는 사업"],
                ["조사 항목", "필수 항목 위주의 비교적 간소화된 해양 조사", "수질, 저질, 동식물 플랑크톤, 저서생물 등 광범위하고 정밀한 조사"],
                ["소요 기간", "상대적으로 짧음 (수주 ~ 수개월)", "4계절 조사가 필요할 수도 있어 매우 김 (수개월 ~ 1년 이상)"],
                ["비용 (수수료)", "합리적인 수준", "조사 항목에 비례하여 비용 단가 가중"]
            ]
        },
        "images": [
            ("일반 및 간이해양이용협의 절차.png", "일반 및 간이 해양 이용협의 절차"),
            ("해양이용영향평가 절차.png", "해양 이용영향평가 절차"),
            ("해양이용협의 절차도.png", "해양 이용협의 절차도") 
        ]
    },
    {
        "title": "6. 해양환경영향조사",
        "content": [
            "• 개요: 해양 이용협의 또는 해양 이용영향평가 처분 이후 실제 사업 시행 중 발생하는 해양환경 영향을 지속해서 조사합니다.",
            "• 실시근거: 해양이용영향평가법 제29조 (종전 해양환경관리법 제95조).",
            "• 대상사업 및 협의시기: 해양 이용협의 및 해양 이용영향평가 대상사업 일체.",
            "👉 대상·항목·기간: (해양이용영향평가법) 시행규칙 (해양수산부령)",
            "• 협의기관: 해양수산부장관 또는 지방해양수산청장.",
            "• 평가항목: 해양환경기준이 정하여진 수질, 퇴적물 항목 등.",
            "• 절차 및 양식: 정기 조사 실시 ➔ 해양환경영향조사 결과 통보.",
            "👉 법정양식: (해양이용영향평가법 시행규칙) [별지 서식]"
        ],
        "images": []
    },
    {
        "title": "7. 해양공간적합성협의",
        "content": [
            "• 개요: 해양이용·개발계획 수립 및 구역 지정 시 해양공간계획과의 부합 여부, 입지 적정성 등을 사전에 협의합니다.",
            "• 실시근거: 해양공간계획 및 관리에 관한 법률 제15조.",
            "• 대상사업 및 협의시기: 해양관광단지, 항만·어항, 수자원 등 25개 법률의 48개 계획.",
            "👉 대상범위: (해양공간계획 및 관리에 관한 법률) 시행령 [별표 2]",
            "• 협의기관: 해양수산부장관.",
            "• 평가항목: 해양공간계획 정책방향 부합성, 입지 적절성, 지속가능성.",
            "• 절차 및 양식: 협의 요청 ➔ 적합성 검토(45일) ➔ 동의/부동의 결정 및 통보.",
            "👉 법정양식: (해양공간계획 및 관리에 관한 법률 시행규칙) [별지 서식]"
        ],
        "images": [
            ("해양공간접합성협의 절차.png", "해양공간적합성협의 절차 흐름도"),
            ("해양공간접합성협의 절차- 요청.png", "해양공간적합성협의 요청 절차 흐름도")
        ]
    },
    {
        "title": "8. 공유수면 점용·사용허가 및 매립",
        "content": [
            "• 개요: 공유수면을 독점적으로 사용(점용)하거나 토석을 채워 토지(매립)를 조성하기 위한 권리를 설정받는 제도입니다.",
            "• 실시근거: 공유수면 관리 및 매립에 관한 법률 제8조(점용·사용), 제28조(매립면허).",
            "• 대상사업 및 협의시기: 인공구조물 설치 등 11개 점용행위 및 매립목적 달성.",
            "👉 매립목적: (공유수면 관리 및 매립에 관한 법률) 시행령 [별표 2]",
            "• 협의기관: 해양수산부장관, 지방해양수산청장 또는 관할 지자체.",
            "• 평가항목: 사업계획서, 구적도, 설계도서, 환경영향평가서 등 적정성 검토.",
            "• 절차 및 양식: 신청서 제출 ➔ 타당성 검토 ➔ 허가 ➔ 고시.",
            "👉 법정양식: (공유수면 관리 및 매립에 관한 법률 시행규칙) [별지 서식]"
        ],
        "images": [
            ("공유수면매립 기본계획수립.png", "공유수면매립 기본계획수립 절차"),
            ("공유수면매립 절차.png", "공유수면매립 절차 상세"),
            ("공유수면매립 흐름도.png", "공유수면매립 흐름도"),
            ("공유수면매립 점용･사용허가 절차.png", "공유수면 점용·사용허가 절차 1"),
            ("공유수면매립 점용･사용허가 절차-2.png", "공유수면 점용·사용허가 절차 2"),
            ("공유수면매립 점용･사용허가 절차-3.png", "공유수면 점용·사용허가 절차 3")
        ]
    },
    {
        "title": "9. 재해영향평가 및 재해영향성검토 (소규모 포함)",
        "content": [
            "• 개요: 개발 사업의 허가나 행정계획 수립 초기에 자연재해에 미치는 영향을 미리 평가하여 재해를 예방하는 제도입니다.",
            "• 실시근거: 자연재해대책법 제4조 및 시행령 제6조.",
            "• 대상사업 및 협의시기: 48개 법령에 따른 59개 개발사업.",
            "👉 대상범위: (자연재해대책법) 시행령 [별표 1]",
            "• 협의기관: 행정안전부장관, 시·도지사, 시장·군수·구청장 (사전검토: 국립재난안전연구원).",
            "• 평가항목: 배수처리계획도, 침수흔적도 검토 및 재해영향 예측·저감대책.",
            "• 절차 및 양식: 사전검토 요청(14일) ➔ 심의 ➔ 결과 통보(30~45일) ➔ 설계 반영.",
            "👉 법정양식: (자연재해대책법 시행규칙) [별지 서식]"
        ],
        "images": [
            ("재해영향성 검토 절차.jpg", "재해영향성 검토 절차 흐름도"),
            ("재해영향평가 절차.jpg", "재해영향평가 절차 흐름도")
        ]
    },
    {
        "title": "10. 교통영향평가",
        "content": [
            "• 개요: 사업 시행 시 발생하는 교통량과 교통흐름의 변화를 예측하여 교통안전 문제점을 최소화할 대책을 마련합니다.",
            "• 실시근거: 도시교통정비 촉진법 제15조 및 시행령 제13조의2.",
            "• 대상사업 및 협의시기: 항만, 공항, 도로 건설 등 11개 분야 29개 개발사업.",
            "👉 대상범위: (도시교통정비 촉진법) 시행령 [별표 1]",
            "• 협의기관: 국토교통부장관 또는 관할 시·도지사.",
            "• 평가항목: 장래 교통수요 예측, 문제점 분석, 교통개선대책안 및 공사 중 교통처리대책.",
            "• 절차 및 양식: 평가서 제출 ➔ 심의위원회 심의 ➔ 개선사항 통보 ➔ 사업계획 반영.",
            "👉 법정양식: (도시교통정비 촉진법 시행규칙) [별지 서식]"
        ],
        "images": [("교통영향평가 절차.png", "교통영향평가 절차 흐름도")]
    },
    {
        "title": "11. 도시계획시설결정",
        "content": [
            "• 개요: 도로, 항만, 철도 등 기반시설을 도시관리계획으로 결정하여 설치하기 위한 행정 절차입니다.",
            "• 실시근거: 국토의 계획 및 이용에 관한 법률 제43조.",
            "• 대상사업 및 협의시기: 도시관리계획 입안 및 결정 고시 전.",
            "  - [대상 시설] 7대 기반시설(교통·공간·유통공급·공공문화체육·방재·보건위생·환경기초시설)의 신설, 변경, 정비 (예: 항만, 도로, 공원, 하수도 등)",
            "👉 대상범위 상세: (국토의 계획 및 이용에 관한 법률 시행령) 제2조",
            "• 협의기관: 국토교통부, 관할 시·도지사, 시장·군수.",
            "• 평가항목: 시설의 종류, 명칭, 위치, 규모 등 도시계획 측면의 적합성.",
            "• 절차 및 양식: 입안 ➔ 주민/의회 의견청취 ➔ 관계기관 협의 ➔ 고시.",
            "👉 법정양식: (국토의 계획 및 이용에 관한 법률 시행규칙)"
        ],
        "images": []
    },
    {
        "title": "12. 에너지사용계획 협의",
        "content": [
            "• 개요: 대규모 도시개발 및 산업단지 조성 시 에너지 수요 예측 및 고효율 사용 방안을 사전에 수립합니다.",
            "• 실시근거: 에너지이용 합리화법 제8조.",
            "• 대상사업 및 협의시기: 대규모 민간/공공 개발사업 및 시설.",
            "👉 대상범위: (에너지이용 합리화법) 시행령 [별표 1]",
            "• 협의기관: 기후에너지환경부 (한국에너지공단 검토) — 결과 통보 30일 (20일 범위 연장).",
            "• 평가항목: 에너지 수요 예측, 공급계획, 신재생에너지 보급 계획, 이용 효율 향상 방안.",
            "• 절차 및 양식: 계획서 작성 ➔ 공단 평가 ➔ 협의 결과 통보.",
            "👉 법정양식: (에너지이용 합리화법 시행규칙) [별지 서식]"
        ],
        "images": []
    },
    {
        "title": "13. 지하안전평가",
        "content": [
            "• 개요: 대규모 굴착 공사(10m 이상) 진행 시 지반침하 등을 예방하기 위해 인허가 전 지하안전 영향을 평가합니다.",
            "• 실시근거: 지하안전관리에 관한 특별법 제14조, 제23조.",
            "• 대상사업 및 협의시기: 굴착 깊이 10m~20m(소규모), 20m 이상(일반).",
            "👉 대상범위: (지하안전관리에 관한 특별법) 시행령 [별표 1]",
            "• 협의기관: 국토교통부 (지방국토관리청 위임, 국토안전관리원 등 위탁) — 협의 30일 (연장 시 50일).",
            "• 평가항목: 지반/지질 현황, 지하수 변화, 지반 침하 위험도 예측 및 안전 대책.",
            "• 절차 및 양식: 평가서 제출 ➔ 전문기관 검토 ➔ 협의 내용 이행.",
            "👉 법정양식: (지하안전관리에 관한 특별법 시행규칙) [별지 서식]"
        ],
        "images": []
    },
    {
        "title": "14. 설계안전성검토(DFS) 및 안전관리계획 수립",
        "content": [
            "• 개요: 설계 단계부터 시공 위험요소를 저감(DFS)하고, 착공 전 건설재해 예방을 위한 안전관리계획을 수립합니다.",
            "• 실시근거: 건설기술 진흥법 제62조.",
            "• 대상사업 및 협의시기: 1종 및 2종 시설물, 지하 10m 이상 굴착 등 안전관리계획 수립 대상 공사.",
            "👉 대상범위: (건설기술 진흥법) 시행령 [별표 8]",
            "• 협의기관: 발주청, 국토안전관리원.",
            "• 평가항목: 시공 절차 및 주의사항, 위험요소 저감 대책, 추락·붕괴 방지 대책.",
            "• 절차 및 양식: 계획서 작성 ➔ 발주청 및 관리원 검토 ➔ 적정 통보.",
            "👉 법정양식: (건설기술 진흥법 시행규칙) [별지 서식]"
        ],
        "images": []
    },
    {
        "title": "15. 유해·위험방지계획서",
        "content": [
            "• 개요: 건설공사 착공 전 재해 유발 위험이 높은 특수 공종의 안전 대책을 수립하여 제출하고 심사받습니다.",
            "• 실시근거: 산업안전보건법 제42조.",
            "• 대상사업 및 협의시기: 지상 31m 이상, 최대지간 50m 이상 교량, 10m 이상 굴착 등.",
            "👉 대상범위: (산업안전보건법) 시행규칙 제42조",
            "• 협의기관: 고용노동부 (한국산업안전보건공단 심사).",
            "• 평가항목: 공사개요, 안전보건관리계획, 작업공종별 유해·위험방지계획 등.",
            "• 절차 및 양식: 계획서 제출 ➔ 공단 심사 ➔ 적정 여부 통보 ➔ 확인.",
            "👉 법정양식: (산업안전보건법 시행규칙) [별지 서식]"
        ],
        "images": []
    },
    {
        "title": "16. 해상교통안전진단",
        "content": [
            "• 개요: 해상교통안전에 영향을 미칠 수 있는 항만 개발, 해상 교량 건설 등의 사업을 추진할 때 선박 통항의 안전성을 사전에 진단합니다.",
            "• 실시근거: 해상교통안전법 제13~17조 (2024.7.26 시행, 종전 해사안전법).",
            "• 대상사업 및 협의시기: 수역의 설정/변경, 해상수역 시설물 건설 등.",
            "👉 대상범위: (해상교통안전법) 제2조·제13조 및 시행령",
            "• 협의기관: 해양수산부 (지방해양수산청).",
            "• 평가항목: 해상교통현황 조사, 통항 안전성 시뮬레이션, 안전대책 수립.",
            "👉 평가기준: (해상교통안전법 시행규칙) 해상교통안전진단기준",
            "• 절차 및 양식: 진단서 제출(처분기관 → 해양수산부 10일 이내) ➔ 해양수산부 검토·의견 통보(45일) ➔ 허가 반영 ➔ 이행 확인.",
            "👉 법정양식: (해상교통안전법 시행규칙) [별지 서식]"
        ],
        "images": []
    },
    {
        "title": "17. 해상풍력발전 인허가",
        "content": [
            "• 개요: 해상풍력 발전사업 추진을 위한 발전사업 허가, 공유수면 점·사용, 환경영향평가 등 종합 인허가 절차입니다.",
            "• 실시근거: 해상풍력 보급 촉진 및 산업 육성에 관한 특별법 (약칭: 해상풍력법).",
            "• 대상사업 및 협의시기: 예비지구 지정, 발전지구 지정 및 해상풍력 발전사업 실시계획 승인 전.",
            "👉 근거법령: (해상풍력 보급 촉진 및 산업 육성에 관한 특별법)",
            "• 협의기관: 기후에너지환경부, 산업통상자원부, 해양수산부 및 관할 지자체.",
            "• 평가항목: 해상교통안전진단, 해양 이용영향평가, 환경영향평가, 어업피해영향조사 등 종합 검토.",
            "• 절차 및 양식: 예비지구 지정 ➔ 발전지구 지정 ➔ 실시계획 승인.",
            "👉 관련 법정 양식 확인"
        ],
        "images": []
    },
    {
        "title": "18. 어업피해영향 조사",
        "content": [
            "• 개요: 해양 개발 및 항만 공사 등으로 인해 어업권에 미치는 피해를 조사하고 보상 대책을 수립하기 위한 필수 조사입니다.",
            "• 실시근거: 수산업법 및 어업피해 보상 관련 규정.",
            "• 대상사업 및 협의시기: 공유수면 매립, 항만 건설, 해상풍력 및 준설 등 어업권에 손실을 주는 개발사업.",
            "👉 참고 기관 가이드: 어업피해영향조사 안내 (https://www.marinelab.co.kr/index.php?cate=003006001)",
            "• 협의기관: 관할 지자체 (시·도지사, 시장·군수·구청장) 및 수협 등 어업인 대표.",
            "• 평가항목: 공사 시행으로 인한 수산자원 감소, 양식장 피해 범위 산정 및 보상액 산출.",
            "• 절차 및 양식: 어업피해조사 실시계획 승인 ➔ 피해 영향 조사 용역 시행 ➔ 보상 협의 및 재결.",
            "👉 법정양식: (수산업법 시행규칙) [별지 서식]"
        ],
        "images": []
    },
    {
        "title": "19. 문화재 지표조사 및 현상변경 허가",
        "content": [
            "• 개요: 사업 부지 내 매장유산 유무를 확인(지표조사)하고, 지정 문화재 주변 건설공사 시 문화재 보존에 미치는 영향을 검토합니다.",
            "• 실시근거: 매장유산 보호 및 조사에 관한 법률 제6조, 문화유산의 보존 및 활용에 관한 법률.",
            "• 대상사업 및 협의시기: 사업 면적 3만㎡ 이상 건설공사(지표조사), 역사문화환경 보존지역 내 공사.",
            "👉 대상범위: (매장유산 보호 및 조사에 관한 법률) 시행령 [별표 1]",
            "• 협의기관: 국가유산청, 관할 지자체.",
            "• 평가항목: 매장유산의 분포 여부 및 문화재 경관 훼손 여부 등.",
            "• 절차 및 양식: 조사기관 의뢰 ➔ 결과 보고서 제출 ➔ 보존 조치 또는 발굴조사 전환.",
            "👉 법정양식: (매장유산 보호 및 조사에 관한 법률 시행규칙) [별지 서식]"
        ],
        "images": []
    },
    {
        "title": "20. 수저준설토사 유효활용",
        "content": [
            "• 개요: 항만 및 수역 개발 시 발생하는 오염되지 않은 토사를 매립재, 인공 섬 조성 등 자원으로 유효활용하기 위한 절차입니다.",
            "• 실시근거: 해양환경관리법 제110조 및 「수저준설토사 유효활용기준」(해양수산부 고시) — ※ 현행 「해양폐기물 및 해양오염퇴적물 관리법」 조문 확인 필요.",
            "• 대상사업 및 협의시기: 항만 건설 및 항로 유지 준설 공사 등에서 발생한 토사 처리 시.",
            "👉 관련 규정: (해양환경관리법) 시행령 [별표 17]",
            "• 협의기관: 해양수산부 (지방해양수산청).",
            "• 평가항목: 준설토의 오염도 검사, 성분 분석, 활용 대상지의 적정성.",
            "• 절차 및 양식: 유효활용 계획서(신고서) 제출 ➔ 타당성 검토 ➔ 승인.",
            "👉 법정양식: (해양환경관리법 시행규칙) [별지 제46호 서식]"
        ],
        "images": []
    },
    {
        "title": "21. 설계의 경제성(VE) 검토 및 설계자문",
        "content": [
            "• 개요: 100억 원 이상 공공 건설사업의 예산 절감, 기능 향상을 위해 설계 대안을 창출(VE)하고 기술적 타당성을 검증(자문)합니다.",
            "• 실시근거: 건설기술 진흥법 시행령 제73조.",
            "• 대상사업 및 협의시기: 총공사비 100억 원 이상인 건설공사의 기본/실시설계.",
            "👉 관련 규정: (건설기술 진흥법) 시행령 제73조",
            "• 협의기관: 발주청 (자체 설계자문위원회 또는 기술심의위원회 구성).",
            "• 평가항목: 비용 절감 방안, 기능 및 품질 향상 방안 대안 도출.",
            "• 절차 및 양식: VE팀 구성 ➔ 기능 분석 ➔ 제안서 작성 ➔ 발주청 승인.",
            "👉 국토교통부 고시 (설계의 경제성등 검토에 관한 지침)"
        ],
        "images": []
    },
    {
        "title": "22. 경관심의 (경관법)",
        "content": [
            "• 개요: 지역의 자연경관 및 역사·문화경관을 보전하고 훼손된 경관을 개선·복원하며, 새로운 경관을 창출하기 위해 건축물, 시설물 등의 경관을 사전에 심의하는 제도입니다.",
            "• 실시근거: 경관법 제26조(개발사업의 경관심의) 및 제27조(건축물의 경관심의).",
            "• 대상사업 및 협의시기: 실시설계 완료 전.",
            "  - [개발사업] 도시지역 3만㎡ 이상, 비도시지역 30만㎡ 이상 (경관법 시행령 제19조 및 별표)",
            "  - [사회기반시설] 총사업비 500억 원 이상의 도로·철도, 300억 원 이상의 하천시설사업 (경관법 시행령 제18조)",
            "👉 대상범위 상세: (경관법 시행령) 제18조[별표] 및 제19조",
            "• 협의기관: 국토교통부, 관할 지자체 경관위원회.",
            "• 평가항목: 경관계획과의 부합 여부, 주변 경관과의 조화, 랜드마크 조성 등.",
            "• 절차 및 양식: 경관심의 신청 ➔ 경관위원회 심의 ➔ 결과 통보 및 반영.",
            "👉 법정양식: (경관법 시행규칙) [별지 서식]"
        ],
        "images": []
    },
    {
        "title": "23. 공공디자인 심의 (공공디자인의 진흥에 관한 법률)",
        "content": [
            "• 개요: 국가 및 지자체 등 공공기관이 조성·제작·설치하는 공공시설물 등의 안전성, 사용성, 편의성 및 심미성을 높이기 위해 공공디자인 진흥 가이드라인 및 관련 사항을 심의합니다.",
            "• 실시근거: 공공디자인의 진흥에 관한 법률 제9조, 제10조 및 각 지자체 공공디자인 조례.",
            "• 대상사업 및 협의시기: 기본 및 실시설계 단계.",
            "  - [대상 시설물] 공공기관이 조성·제작·설치하는 대중교통시설물, 보행안전시설물, 편의시설물, 공급시설물, 녹지시설물, 안내시설물 등 (법 제2조제3호)",
            "👉 대상범위 상세: (공공디자인의 진흥에 관한 법률) 제2조제3호 및 관할 지자체 조례 [별표]",
            "• 협의기관: 문화체육관광부, 관할 지자체 공공디자인위원회.",
            "• 평가항목: 공공디자인 종합계획 및 가이드라인 준수 여부, 유니버설 디자인 적용 여부 등.",
            "• 절차 및 양식: 심의 신청 ➔ 공공디자인위원회 심의 ➔ 결과 반영.",
            "👉 법정양식: 관할 지자체 (공공디자인 조례) 관련 서식"
        ],
        "images": []
    },
    {
        "title": "24. 항만공간 공공디자인 협의",
        "content": [
            "• 개요: 항만시설 및 주변 공간의 디자인 품질을 향상시키고 항만의 정체성을 확보하여, 국민이 안전하고 쾌적하게 이용할 수 있도록 가이드라인 적용 여부를 검토합니다.",
            "• 실시근거: 해양수산부 예규 (항만공간의 공공디자인 가이드라인).",
            "• 대상사업 및 협의시기: 실시설계 단계.",
            "  - [대상 시설물] 항만법에 따른 5대 분야 40개 유형 146개 시설물 전체",
            "  - (기본시설, 기능시설, 지원시설, 항만친수시설, 공통 공공시설물 등)",
            "👉 대상범위 상세: (항만공간의 공공디자인 가이드라인) 제1장 제3조(적용범위)",
            "• 협의기관: 해양수산부 및 관할 지방해양수산청, 항만공사.",
            "• 평가항목: 항만 정체성 반영, 안전성, 편의성, 심미성, 친환경성 등 가이드라인 적용 여부.",
            "• 절차 및 양식: 설계 반영 ➔ 관계기관 협의 및 자문 ➔ 실시계획 반영.",
            "👉 관련지침: 해양수산부 예규 (항만공간의 공공디자인 가이드라인)"
        ],
        "images": []
    }
]

def get_image_base64(path):
    if Path(path).exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

@st.cache_data
def get_html_bytes(res_df):
    html = f"""
    <html>
    <head><meta charset="utf-8"><title>인허가 법령 종합 보고서</title>
    <style>
        body {{ font-family: 'Malgun Gothic', sans-serif; margin: 30px; color: #333; line-height: 1.6; }}
        h1, h2, h3 {{ color: #1E3A8A; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 30px; }}
        th, td {{ border: 1px solid #ccc; padding: 8px 12px; text-align: left; font-size: 13px; }}
        th {{ background-color: #f4f4f4; text-align: center; }}
        .guide-box {{ background: #f9f9f9; border-left: 4px solid #1E3A8A; padding: 15px; margin-bottom: 25px; }}
        img {{ max-width: 100%; height: auto; margin-top: 15px; border: 1px solid #cbd5e1; }}
        .img-caption {{ font-size: 13px; color: #334155; text-align: center; font-weight: bold; margin-bottom: 20px; }}
    </style>
    </head>
    <body>
        <h1>🏛️ 인허가 관련 법령 및 상세 가이드 종합 보고서</h1>
        <p>생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>1. 법령 업데이트 결과 대시보드</h2>
        {res_df.to_html(escape=False, index=False)}
        
        <h2>2. 설계 시행 주요 인허가 상세 가이드 (1~24 항목)</h2>
    """
    for item in REPORT_DATA:
        html += f"<div class='guide-box'><h3>{item['title']}</h3>"
        for text_line in item['content']:
            html += f"<p>{text_line}</p>"
            
        if "table" in item:
            html += "<table><tr>"
            for th in item['table']['headers']:
                html += f"<th>{th}</th>"
            html += "</tr>"
            for tr in item['table']['rows']:
                html += "<tr>"
                for td in tr:
                    html += f"<td>{td}</td>"
                html += "</tr>"
            html += "</table>"
            
        html += scope_html(REPORT_DATA.index(item) + 1)
        for cap_, png_ in flow_pngs(REPORT_DATA.index(item) + 1):
            html += f"<div style='text-align:center;'><img src='data:image/png;base64,{base64.b64encode(png_).decode()}' style='max-width:100%;'><p class='img-caption'>{cap_} (현행 법령 기준 흐름도)</p></div>"
        html += "</div>"
    html += "</body></html>"
    return html.encode("utf-8")

@st.cache_data
def get_docx_bytes(res_df):
    doc = Document()
    doc.add_heading('인허가 관련 법령 및 상세 가이드 종합 보고서', level=0)
    doc.add_paragraph(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    doc.add_heading('1. 법령 업데이트 결과 대시보드', level=1)
    table = doc.add_table(rows=len(res_df) + 1, cols=len(res_df.columns))
    table.style = 'Table Grid'
    for j, col_name in enumerate(res_df.columns):
        table.cell(0, j).text = str(col_name)
    for i, row in res_df.iterrows():
        for j, val in enumerate(row):
            clean_val = str(val).replace('<b>', '').replace('</b>', '').replace('</a>', '').replace('</a', '')
            if 'href="' in clean_val:
                clean_val = "원문 링크 참조"
            table.cell(i + 1, j).text = clean_val
            
    doc.add_heading('2. 설계 시행 주요 인허가 상세 가이드 (1~24 항목)', level=1)
    for item in REPORT_DATA:
        doc.add_heading(item['title'], level=2)
        for text_line in item['content']:
            doc.add_paragraph(text_line)
            
        if "table" in item:
            tb = doc.add_table(rows=1, cols=len(item['table']['headers']))
            tb.style = 'Table Grid'
            for i, th in enumerate(item['table']['headers']):
                tb.cell(0, i).text = th
            for tr in item['table']['rows']:
                row_cells = tb.add_row().cells
                for i, td in enumerate(tr):
                    row_cells[i].text = td
                    
        _si = SCOPE_INFO.get(REPORT_DATA.index(item) + 1)
        if _si:
            _cl = lambda t: _kit_re.sub(r"<[^>]+>|\*\*", "", t)
            doc.add_paragraph("[대상범위 · 근거 위치]")
            for _t in _si["scope"]:
                doc.add_paragraph("· " + _cl(_t))
            for _t in _si["where"]:
                doc.add_paragraph("근거 : " + _cl(_t))
            doc.add_paragraph("협의·실시 시기 : " + _cl(_si["timing"]))
        for cap_, png_ in flow_pngs(REPORT_DATA.index(item) + 1):
            doc.add_picture(BytesIO(png_), width=Inches(6.3))
            para = doc.add_paragraph(f"{cap_} (현행 법령 기준 흐름도)")
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
    docx_buffer = BytesIO()
    doc.save(docx_buffer)
    docx_buffer.seek(0)
    return docx_buffer.getvalue()

# =====================================================================
# ★ 사이드바 UI 설정
# =====================================================================

# =====================================================================
# ★ 메인 화면 UI (상단: 대시보드)
# =====================================================================
st.title("🏛️ 인허가 관련 법령 자동 업데이트 대시보드")
_pj_credit()                    # [공통블록] 제작자 표시
kit_css()
st.markdown("항만 및 개발 사업에 수반되는 핵심 **영향평가 및 인허가 업무** 관련 법령들의 최신 제·개정 상태를 추적합니다.")

# =====================================================================
# ★ 23번 앱 사용설명서 (16번 블록식처럼 제목 바로 밑 — 2026-11-02 독립 앱 요청, 11-09 맨 앞으로)
#    내용 = Home 23번 사용설명서 + 현재 화면 기준 정정 (키 입력 위치 · Secrets 키 · [cite] 표기 삭제)
# =====================================================================
# 개인 · 조직 통합 앱(pages/ 안)에서는 Home 에 같은 설명서가 있어 숨김 — 독립 앱 · 원본에서만 (11.02 사용자 '독립 앱만')
if Path(__file__).resolve().parent.name != "pages":
    st.markdown("""
23. **인허가 (License & Permit)**: 항만 · 개발 사업의 영향평가 · 인허가 관련 법령 자동 업데이트 및 상세 가이드 프로그램 (2026.09.08 작성)
""")

    with st.expander("👉 인허가 관련 법령 자동 업데이트 대시보드 앱 사용설명서 보기"):
        st.markdown(r"""
    **■ 🏛️ 인허가 관련 법령 자동 업데이트 대시보드 사용자 매뉴얼**

    항만 및 개발 사업에 수반되는 핵심 **영향평가 및 인허가 업무** 관련 법령들의 최신 제·개정 상태를 추적하고, 종합 보고서를 자동 생성하는 시스템입니다.

    ---

    ### **Ⅰ. 주요 기능 및 사용 방법**

    **📍 1단계: 인허가-법령 리스트 확인 및 편집**
    * 왼쪽 **[1. 인허가-법령 리스트]** 표에서 기본으로 짝지어진 주요 인허가 항목(전략환경영향평가, 해양이용영향평가, 재해영향평가 등)과 검색할 법령명을 확인합니다.
    * 필요하면 새로운 인허가 항목과 정확한 법령명을 직접 추가하거나 수정할 수 있습니다.

    **📍 2단계: 최신 법령 데이터 업데이트 실행**
    * 오른쪽 **[2. 법령 업데이트 결과 대시보드]** 위의 **🔑 법제처 API 키 (OC)** 칸을 확인합니다.
      * 칸 옆에 **'🔑 등록된 법제처 키 사용 중'** 이 보이면 칸을 비워 둔 채로 쓰면 됩니다 (관리자가 등록한 키 사용).
      * 다른 키를 쓰려면 칸에 넣습니다 (법제처 OPEN API 승인 · 이 앱 서버 주소 등록이 된 OC).
    * **[🚀 최신 법령 데이터 업데이트 실행]** 버튼을 누르면 법제처 서버와 통신하여 각 법령의 실제 법령명, 시행일자, 공포일자, 제개정구분, 상세링크(원문)를 자동으로 모읍니다. 법령에 없으면 행정규칙(훈령 · 예규 · 고시)에서 다시 찾습니다.
    * 법제처가 조회를 거부하면 표에 **'⛔ 법제처 거부 : 사유'** 와 빨간 안내 상자가 나옵니다 — 키 · 등록한 서버 주소를 확인하세요.

    **📍 3단계: 업데이트 결과 대시보드 확인 및 다운로드**
    * 업데이트가 끝나면 오른쪽 화면에 각 인허가 법령의 최신 상태가 표로 정리되어 나타납니다.
    * 결과표 아래 다운로드 버튼으로 **Excel, HTML, MS Word(.docx)** 형식의 종합 보고서를 저장할 수 있습니다.

    **📍 4단계: 설계범위 기반 인허가 분석**
    * 시설 선택 → 규모 입력 (또는 설계보고서 PDF 자동 추출) → 24개 인허가의 필수 / 해당 가능 판정, 단계별 로드맵, Excel 을 제공합니다.
    * 판정은 입력값에 따른 1차 검토 결과입니다. '해당 가능' 항목은 각 시행령 별표의 규모 기준과 관계기관 사전협의로 최종 확인하십시오.

    **📍 5단계: 설계 시행 주요 인허가 상세 가이드 열람**
    * 화면 아래 상세 가이드에서 각 인허가의 개요, 실시근거, 대상사업 및 협의시기, 협의기관, 평가항목과 대상범위 · 근거 위치(법 → 시행령 → 별표)를 확인합니다.
    * **6. 절차 및 양식 보기** 를 펼치면 현행 법령(2026.10 확인) 기준 절차 흐름도와 법제처 원문 링크가 포함된 법정 양식 정보를 볼 수 있습니다.
    """)
        st.markdown("---")
        st.markdown("##### 🗂 상세 변경 이력")
        st.markdown("""
* **10.08** 화면 양식 통일 (10번 EP 기준)
* **10.12** 현행 법령(2026.10) 기준 인허가 절차 흐름도 24개 분야 31종 신규 도식화 · 근거 법령 정정, '설계범위 기반 인허가 분석'(시설·규모 입력 또는 설계보고서 PDF 자동 추출 → 24개 인허가 판정 · 단계별 로드맵 · Excel), 항목별 대상범위 · 근거 위치 표, 발주방식(일반 / 턴키·기술제안)별 시기 · 수행 주체 구분
* **10.20** 인허가 로드맵 그림 범례 색 구분 (■ 파랑 = 필수 · ■ 주황 = 해당 가능) · '2. 분석 결과' 판정 기준 설명 상자 · 법령 검색에 없으면 행정규칙(훈령·예규·고시)에서 다시 찾음
* **10.23** 검증보고서 22-25번 반영 — 법령명 완전일치 항목 채택(없으면 '확인 필요'), 공사 위치 '육역'인데 해역 시설이 있으면 경고, 민간 사업 VE '해당 가능', 총공사비 소수 표시, 기후영향평가 근거 법령 = 탄소중립기본법
* **10.30** 법제처 공용 'test' 키 거부(사용자 정보 검증 실패)에 맞춰 — 등록된 법제처 키(Secrets) 자동 사용, 조회 거부 사유를 표 · 안내 상자에 표시
* **11.02** 앱 화면에 사용설명서 추가
    """)


col1, col2 = st.columns([1, 2], vertical_alignment="top")
_H = ("<div style='height:52px;display:flex;align-items:center;border-left:6px solid #1d4ed8;padding-left:10px;"
      "margin:0 0 10px;font-size:clamp(1.0rem,1.6vw,1.4rem);font-weight:800;color:#1e3a8a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{}</div>")

with col1:
    st.markdown(_H.format("📝 1. 인허가-법령 리스트&nbsp;<span style='font-size:0.68em;color:#475569'>(편집 가능)</span>"), unsafe_allow_html=True)
    edited_df = _pj_tset("tb_edited_df", st.data_editor(
        _pj_tbl("tb_edited_df", st.session_state['mapping_df']),
        num_rows="dynamic",
        use_container_width=True,
        height=650,
        column_config={
            "인허가명": st.column_config.TextColumn("인허가명", required=True),
            "검색 법령명": st.column_config.TextColumn("검색 법령명 (정확한 명칭)", required=True)
        }
    ))
    st.session_state['mapping_df'] = edited_df
    update_btn = st.button("🚀 최신 법령 데이터 업데이트 실행", use_container_width=True, type="primary")

with col2:
    st.markdown(_H.format("📊 2. 법령 업데이트 결과 대시보드"), unsafe_allow_html=True)
    _k1, _k2 = st.columns([1.15, 1], vertical_alignment="bottom")
    with _k1:
        _sec_oc = _law_oc_secret()
        user_api_key = st.text_input("⚙️ 시스템 설정 — 🔑 법제처 API 키 (OC)", value="", type="password",
                                     placeholder="비워 두면 등록된 키 사용" if _sec_oc else "본인 OC 키 입력",
                                     help="비워 두면 관리자가 등록한 키(Streamlit Cloud Secrets 'LAW_OC')를 씁니다. 다른 키를 쓰려면 입력하세요 — "
                                          "open.law.go.kr 에서 OPEN API 활용 신청 (이 앱의 서버 주소 등록) 후 승인된 OC. "
                                          "공용 'test' 키는 2026.10 현재 법제처가 '사용자 정보 검증 실패'로 거부합니다.", key="in_시스템_설정_법제처_API_키_OC_필수")
    _typed = user_api_key.strip()
    if _typed == "test" and _sec_oc:          # 예전 저장 파일 · 입력의 'test' 는 등록 키로 바꿔 씀
        _typed = ""
    _eff_key = _typed or _sec_oc or "test"
    with _k2:
        if _typed:
            st.info("🔑 입력한 OC 키 사용 (법제처 승인 · 서버 주소 등록 필요)")
        elif _sec_oc:
            st.success("🔑 등록된 법제처 키 사용 중")
        else:
            st.warning("💡 등록된 키가 없어 공용 'test' 키로 조회합니다 — 법제처가 거부할 수 있으니 본인 OC 키를 넣으세요")
    if update_btn:
        if edited_df.empty:
            st.warning("리스트가 비어있습니다.")
        else:
            with st.spinner("데이터 수집 중..."):
                laws_to_fetch = edited_df["검색 법령명"].dropna().unique()
                results = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    futures = [executor.submit(fetch_law_info, _eff_key, law) for law in laws_to_fetch]
                    for f in concurrent.futures.as_completed(futures):
                        results.append(f.result())
                api_df = pd.DataFrame(results)
                final_df = pd.merge(edited_df, api_df, on="검색 법령명", how="left")
                final_df['상세링크'] = final_df['상세링크'].apply(lambda l: f'<a target="_blank" href="{l}">법령 원문</a>' if l != "-" else "-")
                st.session_state['result_df'] = final_df

    if not st.session_state['result_df'].empty:
        res_df = st.session_state['result_df']
        _deny = res_df['실제 법령명'].astype(str).str.startswith(_LAW_DENY)
        if _deny.any():
            st.error(f"⛔ 법제처가 조회를 거부했습니다 ({int(_deny.sum())}/{len(res_df)}건) — "
                     f"{res_df.loc[_deny, '실제 법령명'].iloc[0].split(' : ', 1)[-1]}\n\n"
                     "👉 open.law.go.kr 에서 OPEN API 활용 신청 (이 앱의 서버 IP · 도메인 주소 등록) → 승인된 본인 OC 키를 위 칸에 넣고 다시 실행하세요.")
        st.write(
            res_df.to_html(escape=False, index=False, justify='center').replace(
                '<table', '<table style="width:100%; border-collapse: collapse; text-align:center; font-size:13px;" border="1"'
            ),
            unsafe_allow_html=True
        )
        st.write("---")
        
        st.subheader("🖨️ 종합 보고서 다운로드 (Excel / HTML / MS Word)")
        
        # 엑셀 처리
        excel_df = res_df.copy()
        excel_df['상세링크'] = excel_df['상세링크'].str.replace(r'<.*?>', '', regex=True)

        def _law_xl_bytes(_d=excel_df):   # [2026-11-16] 누를 때 만듦
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                _d.to_excel(writer, index=False, sheet_name='법령업데이트_결과')
            return excel_buffer.getvalue()
        
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        with col_dl1:
            st.download_button(
                label="💾 Excel 다운로드",
                data=_law_xl_bytes,
                file_name=f"인허가법령_보고서_{datetime.now():%Y%m%d}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
        with col_dl2:
            st.download_button(
                label="🌐 HTML 보고서 다운로드",
                data=lambda _d=res_df: get_html_bytes(_d),   # [2026-11-16] 누를 때 만듦
                file_name=f"인허가법령_종합보고서_{datetime.now():%Y%m%d}.html",
                mime="text/html",
                use_container_width=True
            )
            
        with col_dl3:
            if DOCX_AVAILABLE:
                st.download_button(
                    label="📝 MS Word (.docx) 다운로드",
                    data=lambda _d=res_df: get_docx_bytes(_d),   # [2026-11-16] 누를 때 만듦
                    file_name=f"인허가법령_종합보고서_{datetime.now():%Y%m%d}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            else:
                st.button("📝 MS Word 다운로드 (python-docx 미설치)", disabled=True, use_container_width=True)
    else:
        st.info("👈 좌측 상단의 '업데이트 실행' 버튼을 먼저 눌러주세요.")

# =====================================================================
# ★ [v2.0] 설계범위 기반 인허가 분석 (시설·규모·입지 → 관련 인허가 판정)
# =====================================================================
st.markdown("---")
st.header("🧭 설계범위 기반 인허가 분석")
st.markdown("사업 입지와 설계 대상 시설·규모를 입력하면 관련 인허가를 판정합니다. "
            "**● 필수** = 법령 기준 확인 / **◐ 해당 가능** = 대상 유형 해당, 규모 기준은 시행령 별표 확인 필요 / **○ 해당 없음**")

SCOPE_FAC = pd.DataFrame([
    {"선택": True, "시설": "방파제", "규모": 500.0, "단위": "m"},
    {"선택": False, "시설": "호안 (외곽·투기장 호안)", "규모": 0.0, "단위": "m"},
    {"선택": True, "시설": "안벽", "규모": 300.0, "단위": "m"},
    {"선택": False, "시설": "잔교", "규모": 0.0, "단위": "m"},
    {"선택": False, "시설": "물양장", "규모": 0.0, "단위": "m"},
    {"선택": False, "시설": "계류시설 (부잔교·돌핀 등)", "규모": 0.0, "단위": "개소"},
    {"선택": True, "시설": "준설", "규모": 200000.0, "단위": "m³"},
    {"선택": False, "시설": "준설토 투기장", "규모": 0.0, "단위": "m²"},
    {"선택": False, "시설": "공유수면 매립 (부지 조성)", "규모": 0.0, "단위": "m²"},
    {"선택": False, "시설": "항로·박지 신설·변경", "규모": 0.0, "단위": "m²"},
    {"선택": False, "시설": "배후부지·육상 부지조성", "규모": 0.0, "단위": "m²"},
    {"선택": False, "시설": "건축물 (터미널·창고 등)", "규모": 0.0, "단위": "m² (연면적)"},
    {"선택": False, "시설": "해상교량·해저케이블·터널", "규모": 0.0, "단위": "m"},
    {"선택": False, "시설": "진입도로", "규모": 0.0, "단위": "km"},
    {"선택": False, "시설": "해상풍력발전", "규모": 0.0, "단위": "MW"},
])

# [2026-11-06] 판정 기준표 — 판정 코드는 이 표의 값만 씀 (법이 바뀌면 여기만 고침)
#   확인 : '조문 ✔' = 현행 조문 확인 / '별표 ※' = 별표 수치 (행정규칙집 수록값, 별표 원문 확인 필요) / '종전 ※' = 종전 기준 (신법 별표 원문 확인 필요)
SCOPE_TH = {
    "eia_outer":   (300, "m", 2, "환경영향평가", "외곽시설(방파제 · 호안) 길이", "환경영향평가법 시행령 [별표 3] 제4호", "별표 ※"),
    "eia_recl":    (30000, "m²", 2, "환경영향평가", "항만시설 공유수면 매립 면적", "[별표 3] 제4호", "별표 ※"),
    "eia_area":    (150000, "m²", 2, "환경영향평가", "그 밖의 항만시설 사업면적 (매립 없음)", "[별표 3] 제4호", "별표 ※"),
    "eia_dred_a":  (100000, "m²", 2, "환경영향평가", "준설 면적 (유지준설 제외)", "[별표 3] 제4호 다목", "별표 ※"),
    "eia_dred_v":  (200000, "m³", 2, "환경영향평가", "준설량 (유지준설 제외)", "[별표 3] 제4호 다목", "별표 ※"),
    "eia_redev":   (300000, "m²", 2, "환경영향평가", "항만재개발 사업면적", "[별표 3] 제4호 마목", "별표 ※"),
    "eia_r10_p":   (30000, "m²", 2, "환경영향평가", "공유수면 매립 (무역항 · 연안항 · 자연환경보전지역)", "[별표 3] 제10호", "별표 ※"),
    "eia_r10_o":   (300000, "m²", 2, "환경영향평가", "공유수면 매립 (그 밖의 지역)", "[별표 3] 제10호", "별표 ※"),
    "eia_re":      (30, "%", 2, "환경영향평가", "재협의 : 규모 증가율", "시행령 제54조", "별표 ※"),
    "eia_mod":     (10, "%", 2, "환경영향평가", "변경협의 : 규모 증가율", "시행령 제55조", "별표 ※"),
    "mar_ia_da":   (100000, "m²", 5, "해양이용영향평가", "준설 면적 (유지준설 제외)", "종전 해양환경관리법 시행령 [별표 16] — 신법 [별표 2] 대조", "종전 ※"),
    "mar_ia_dv":   (200000, "m³", 5, "해양이용영향평가", "준설량 (유지준설 제외)", "종전 [별표 16] — 신법 [별표 2] 대조", "종전 ※"),
    "mar_g_len":   (150, "m", 5, "일반 해양이용협의", "계류 · 외곽시설 길이", "종전 [별표 15] — 신법 [별표 1] 대조", "종전 ※"),
    "mar_g_occ":   (3000, "m²", 5, "일반 해양이용협의", "공유수면 점용 · 사용 면적", "종전 [별표 15] — 신법 [별표 1] 대조", "종전 ※"),
    "mar_g_da":    (50000, "m²", 5, "일반 해양이용협의", "준설 면적 (유지준설 제외)", "종전 [별표 15] — 신법 [별표 1] 대조", "종전 ※"),
    "mar_g_dv":    (100000, "m³", 5, "일반 해양이용협의", "준설량 (유지준설 제외)", "종전 [별표 15] — 신법 [별표 1] 대조", "종전 ※"),
    "mar_re":      (30, "%", 5, "해양이용협의", "재협의 : 면적 · 길이 증가율", "해양이용영향평가법 시행령 제17조", "별표 ※"),
    "dis_a":       (50000, "m²", 9, "재해영향평가", "개발사업 면적", "자연재해대책법 시행령 [별표 1]", "별표 ※"),
    "dis_l":       (10, "km", 9, "재해영향평가", "개발사업 길이", "시행령 [별표 1]", "별표 ※"),
    "dis_sa":      (5000, "m²", 9, "소규모 재해영향평가", "개발사업 면적", "시행령 [별표 1]", "별표 ※"),
    "dis_sl":      (2, "km", 9, "소규모 재해영향평가", "개발사업 길이", "시행령 [별표 1]", "별표 ※"),
    "trf_cargo":   (150, "만 톤", 10, "교통영향평가", "항만 연간 하역능력", "도시교통정비 촉진법 시행령 [별표 1] 라목", "별표 ※"),
    "en_pub_toe":  (2500, "TOE", 12, "에너지사용계획", "공공 : 연료 · 열 연간", "에너지이용 합리화법 시행령 제20조", "조문 ✔"),
    "en_pub_kwh":  (1000, "만 kWh", 12, "에너지사용계획", "공공 : 전력 연간", "시행령 제20조", "조문 ✔"),
    "en_prv_toe":  (5000, "TOE", 12, "에너지사용계획", "민간 : 연료 · 열 연간", "시행령 제20조", "조문 ✔"),
    "en_prv_kwh":  (2000, "만 kWh", 12, "에너지사용계획", "민간 : 전력 연간", "시행령 제20조", "조문 ✔"),
    "ug_big":      (20, "m", 13, "지하안전평가", "굴착깊이", "지하안전관리에 관한 특별법 제14조", "조문 ✔"),
    "ug_small":    (10, "m", 13, "소규모 지하안전평가", "굴착깊이", "같은 법 제23조 · 시행령 제23조", "조문 ✔"),
    "saf_exc":     (10, "m", 14, "안전관리계획", "지하 굴착깊이", "건설기술 진흥법 시행령 제98조", "조문 ✔"),
    "haz_exc":     (10, "m", 15, "유해 · 위험방지계획서", "굴착깊이", "산업안전보건법 시행령 제42조", "별표 ※"),
    "haz_hgt":     (31, "m", 15, "유해 · 위험방지계획서", "지상 높이", "시행령 제42조", "별표 ※"),
    "haz_span":    (50, "m", 15, "유해 · 위험방지계획서", "교량 최대 지간", "시행령 제42조", "별표 ※"),
    "mts_ship":    (100, "m", 16, "해상교통안전진단", "이용 선박 길이 (계류시설)", "해상교통안전법 시행령 (대상사업 범위)", "종전 ※"),
    "mts_len":     (200, "m", 16, "해상교통안전진단", "시설물 점용 · 매립 수역 길이", "같은 시행령", "종전 ※"),
    "mts_area":    (20000, "m²", 16, "해상교통안전진단", "시설물 점용 · 매립 수역 면적", "같은 시행령", "종전 ※"),
    "mts_depth":   (4, "m", 16, "해상교통안전진단", "제외 : 수심 미만 수역", "같은 시행령", "종전 ※"),
    "heri_area":   (30000, "m²", 19, "매장유산 지표조사", "건설공사 사업면적", "매장유산법 시행령 (대상 규모)", "별표 ※"),
    "ve_cost":     (100, "억원", 21, "설계의 경제성 검토", "총공사비", "건설기술 진흥법 시행령 제75조", "조문 ✔"),
    "ls_urban":    (30000, "m²", 22, "경관심의", "개발사업 : 도시지역", "경관법 시행령 제19조", "조문 ✔"),
    "ls_rural":    (300000, "m²", 22, "경관심의", "개발사업 : 도시지역 외", "경관법 시행령 제19조", "조문 ✔"),
    "ls_road":     (500, "억원", 22, "경관심의", "도로 총사업비", "경관법 시행령 제18조", "조문 ✔"),
}
# [별표 4] 소규모 환경영향평가 — 용도지역별 사업계획 면적 (m²)
SMALL_ZONE = {"해당 없음 (보전용도지역 아님)": None, "보전관리지역": 5000, "생산관리지역": 7500, "계획관리지역": 10000,
              "농림지역": 7500, "자연환경보전지역": 5000, "개발제한구역": 5000}
for _zk, _zv in SMALL_ZONE.items():
    if _zv:
        SCOPE_TH[f"small_{_zk}"] = (_zv, "m²", 3, "소규모 환경영향평가", f"{_zk} 사업계획 면적", "환경영향평가법 시행령 [별표 4]", "별표 ※")
SCOPE_TODO = [  # 판정에 아직 넣지 않은 것 — 원문 확인 필요
    ("2 · 5", "외곽시설 길이를 방파제 · 호안 '가장 긴 것' 으로 볼지 '합산' 으로 볼지", "지금 : 가장 긴 것으로 판정, 합산이면 넘는 경우 '◐ 해당 가능' 으로 표시"),
    ("5", "해양이용영향평가법(2026.9.18 시행) 시행령 [별표 1 · 2] 신법 수치", "지금 : 종전 해양환경관리법 시행령 [별표 15 · 16] 수치로 판정"),
    ("2 · 3", "같은 사업자 연접 개발 · 단계 사업의 규모 합산 규정", "지금 : 판정에 넣지 않음 (입력한 규모만)"),
    ("2", "재협의 '최소 평가대상 규모 이상 증가' 의 규모 정의 (면적 · 길이)", "지금 : 사업면적 증가 ≥ 15만 m² 또는 외곽 길이 증가 ≥ 300 m"),
]


def _th(k):
    return SCOPE_TH[k][0]


def scope_th_df():
    return pd.DataFrame([{"번호": v[2], "인허가": v[3], "항목": v[4], "기준값": f"{v[0]:,} {v[1]}", "근거": v[5], "확인": v[6]}
                         for v in SCOPE_TH.values()]).sort_values("번호", kind="stable")


SCOPE_UNITS = {"방파제": "m", "호안 (외곽·투기장 호안)": "m", "안벽": "m", "잔교": "m", "물양장": "m", "계류시설 (부잔교·돌핀 등)": "개소",
               "준설": "m³", "준설토 투기장": "m²", "공유수면 매립 (부지 조성)": "m²", "항로·박지 신설·변경": "m²",
               "배후부지·육상 부지조성": "m²", "건축물 (터미널·창고 등)": "m² (연면적)", "해상교량·해저케이블·터널": "m", "진입도로": "km",
               "해상풍력발전": "MW"}
_PDF_KEYS = {"방파제": ["방파제"], "호안 (외곽·투기장 호안)": ["호안"], "안벽": ["안벽"], "잔교": ["잔교"], "물양장": ["물양장"],
             "계류시설 (부잔교·돌핀 등)": ["부잔교", "돌핀"], "준설": ["준설"], "준설토 투기장": ["투기장"], "공유수면 매립 (부지 조성)": ["매립"],
             "항로·박지 신설·변경": ["항로", "박지", "선회장"], "배후부지·육상 부지조성": ["배후부지", "부지조성"],
             "건축물 (터미널·창고 등)": ["터미널", "건축물", "창고"], "해상교량·해저케이블·터널": ["해상교량", "해저케이블", "해저터널", "연륙교"],
             "진입도로": ["진입도로", "연결도로"], "해상풍력발전": ["해상풍력"]}
_UNIT_RE = {"m": r"(?:L\s*=\s*)?([\d,]+(?:\.\d+)?)\s*(?:m|M|미터)(?![²³23a-zA-Z])",
            "m³": r"([\d,]+(?:\.\d+)?)\s*(만|천)?\s*(?:㎥|m3|m³|M3|입방미터)",
            "m²": r"([\d,]+(?:\.\d+)?)\s*(만|천)?\s*(?:㎡|m2|m²|M2|제곱미터)",
            "m² (연면적)": r"([\d,]+(?:\.\d+)?)\s*(만|천)?\s*(?:㎡|m2|m²|M2|제곱미터)",
            "km": r"([\d,]+(?:\.\d+)?)\s*(?:km|㎞|킬로미터)", "MW": r"([\d,]+(?:\.\d+)?)\s*(?:MW|㎿)", "개소": r"([\d,]+)\s*(?:개소|기|개)"}


def _pdf_text(data):
    """PDF 텍스트 추출 (pypdf → pdfplumber → PyMuPDF 순서)"""
    try:
        from pypdf import PdfReader
        return "\n".join((pg.extract_text() or "") for pg in PdfReader(BytesIO(data)).pages)
    except Exception:
        pass
    try:
        import pdfplumber
        with pdfplumber.open(BytesIO(data)) as pdf:
            return "\n".join((pg.extract_text() or "") for pg in pdf.pages)
    except Exception:
        pass
    try:
        import fitz
        with fitz.open(stream=data, filetype="pdf") as doc:
            return "\n".join(pg.get_text() for pg in doc)
    except Exception:
        return ""


def _num(txt, mult=None):
    v = float(txt.replace(",", ""))
    return v * (10000 if mult == "만" else (1000 if mult == "천" else 1))


@st.cache_data(show_spinner=False)
def parse_design_pdf(data):
    """설계보고서 PDF → 시설·규모·공사비·굴착깊이·면적·입지 키워드 추출 (근거 문장 포함)"""
    import re as _re
    text = _pdf_text(data)
    flat = _re.sub(r"[ \t]+", " ", text)
    out = {"facs": {}, "ev": [], "pages_chars": len(flat)}
    _bad = ("피해", "사례", "파손", "유실", "붕괴", "재해", "참고", "타 항만", "외국")
    out["cands"] = {}
    for fac, keys in _PDF_KEYS.items():
        best, ev = 0.0, ""
        cands = []
        for k in keys:
            for m in _re.finditer(k, flat):
                win = flat[m.end(): m.end() + 70]
                cut = [win.find(kk) for f2, ks in _PDF_KEYS.items() if f2 != fac for kk in ks if kk not in k and win.find(kk) >= 0]
                if cut:
                    win = win[:min(cut)]
                um = _re.search(_UNIT_RE[SCOPE_UNITS[fac]], win)
                if um:
                    try:
                        v = _num(um.group(1), um.group(2) if um.lastindex and um.lastindex >= 2 else None)
                    except Exception:
                        continue
                    if 0 < v < 1e9:
                        e_ = flat[max(0, m.start() - 15): m.end() + um.end() + 5].replace("\n", " ").strip()
                        ctx = flat[max(0, m.start() - 40): m.end() + um.end() + 20]
                        cands.append((v, e_, any(b in ctx for b in _bad)))
        if cands:
            uniq = {}
            for v, e_, bad in cands:
                if v not in uniq or (uniq[v][1] and not bad):
                    uniq[v] = (e_, bad)
            order = sorted(uniq.items(), key=lambda t: (t[1][1], -t[0]))   # 정상 문장 우선 · 큰 값 우선
            best, (ev, _b) = order[0][0], order[0][1]
            out["cands"][fac] = [(v, e_, bad) for v, (e_, bad) in order[:8]]
            out["facs"][fac] = best
            out["ev"].append((fac, f"{best:,.1f} {SCOPE_UNITS[fac]}", ev))
    m = _re.search(r"(총\s*공사비|총\s*사업비|추정\s*공사비|공사비)[^\d]{0,20}([\d,]+(?:\.\d+)?)\s*(억|백만|천원|원)", flat)
    if m:
        v = float(m.group(2).replace(",", ""))
        out["cost"] = v if m.group(3) == "억" else (v / 100 if m.group(3) == "백만" else (v / 1e5 if m.group(3) == "천원" else v / 1e8))
        out["ev"].append(("총공사비", f"{out['cost']:,.1f} 억원", flat[m.start(): m.end() + 5]))
    m = _re.search(r"굴착\s*(?:깊이|심도|고)?[^\d]{0,12}([\d.]+)\s*m", flat)
    if m:
        out["exc"] = float(m.group(1))
        out["ev"].append(("굴착깊이", f"{out['exc']:g} m", flat[m.start(): m.end() + 3]))
    m = _re.search(r"(사업\s*면적|부지\s*면적|총\s*면적|사업\s*부지)[^\d]{0,15}([\d,]+(?:\.\d+)?)\s*(만|천)?\s*(?:㎡|m2|m²)", flat)
    if m:
        out["area"] = _num(m.group(2), m.group(3))
        out["ev"].append(("사업면적", f"{out['area']:,.0f} m²", flat[m.start(): m.end() + 3]))
    for k in ("무역항", "연안항", "국가어항", "지방어항"):
        if k in flat:
            out["port"] = k
            break
    out["urban"] = "도시지역" in flat
    out["heri"] = any(k in flat for k in ("문화유산", "문화재", "매장유산"))
    out["fish"] = any(k in flat for k in ("어업권", "양식장", "어장"))
    return out


st.markdown("##### 📥 입력 방식")
sc_mode = st.radio("입력 방식 선택", ["✍️ 직접 입력 (시설 선택 → 규모 입력)", "📄 설계보고서 PDF 분석 (자동 추출 후 수정)"], horizontal=True,
                   label_visibility="collapsed", key="scope_mode")
_pdf = {}
_pk = "m"
if sc_mode.startswith("📄"):
    up = st.file_uploader("설계보고서 PDF 첨부 (텍스트가 있는 PDF — 스캔 이미지 PDF 는 추출 불가)", type=["pdf"], key="scope_pdf")
    if up is not None:
        _bytes = up.getvalue()
        with st.spinner("설계보고서에서 시설·규모를 추출하는 중..."):
            _pdf = parse_design_pdf(_bytes)
        _pk = f"p{abs(hash(_bytes[:2000])) % 10 ** 8}"
        if _pdf.get("pages_chars", 0) < 50:
            st.error("PDF 에서 텍스트를 추출하지 못했습니다 (스캔 이미지 PDF 일 수 있음). 직접 입력을 이용하십시오.")
        else:
            st.success(f"추출 완료 — 시설 {len(_pdf['facs'])}종, 근거 {len(_pdf['ev'])}건. 아래 입력란에 자동 반영되었으니 확인·수정 후 결과를 보십시오.")
            _xunit = {**SCOPE_UNITS, "총공사비": "억원", "굴착깊이": "m", "사업면적": "m²"}
            _xval = {**_pdf.get("facs", {}), **{k: _pdf[kk] for k, kk in (("총공사비", "cost"), ("굴착깊이", "exc"),
                                                                        ("사업면적", "area")) if kk in _pdf}}
            _rows = []
            for a, b, c in _pdf["ev"]:
                cl = _pdf.get("cands", {}).get(a, [])
                _rows.append({"적용": True, "항목": a, "값": float(_xval.get(a, 0.0)), "단위": _xunit.get(a, ""),
                              "다른 후보값": " / ".join(f"{v:,.0f}" + (" (사례?)" if bad else "") for v, _e, bad in cl[1:6]),
                              "근거 문장 (PDF)": c})
            st.markdown("**✏️ 추출 결과 확인·수정** — 값을 고치거나, 적용을 해제하거나, 항목을 바꾸거나, 맨 아래 행에 새 항목을 "
                        "추가할 수 있습니다. 수정한 값이 아래 입력란과 판정에 바로 반영됩니다.")
            _ed = st.data_editor(
                pd.DataFrame(_rows, columns=["적용", "항목", "값", "단위", "다른 후보값", "근거 문장 (PDF)"]),
                key=f"scope_pdf_ed_{abs(hash(_bytes[:2000])) % 10 ** 8}", num_rows="dynamic", hide_index=True,
                use_container_width=True,
                column_config={
                    "적용": st.column_config.CheckboxColumn("적용", width="small", default=True),
                    "항목": st.column_config.SelectboxColumn("항목", options=list(_xunit), required=True, width="medium"),
                    "값": st.column_config.NumberColumn("값 (수정)", min_value=0.0, format="%.1f", width="small"),
                    "단위": st.column_config.TextColumn("단위", disabled=True, width="small"),
                    "다른 후보값": st.column_config.TextColumn("다른 후보값 (PDF)", disabled=True, width="medium"),
                    "근거 문장 (PDF)": st.column_config.TextColumn("근거 문장 (PDF)", disabled=True, width="large")})
            _facs2, _sig = {}, []
            for _, rw in _ed.iterrows():
                it, vv = rw.get("항목"), rw.get("값")
                if not rw.get("적용", True) or not isinstance(it, str) or vv is None or vv != vv:
                    continue
                vv = float(vv)
                _sig.append((it, vv))
                if it in SCOPE_UNITS:
                    _facs2[it] = vv
                elif it == "총공사비":
                    _pdf["cost"] = vv
                elif it == "굴착깊이":
                    _pdf["exc"] = vv
                elif it == "사업면적":
                    _pdf["area"] = vv
            for it, kk in (("총공사비", "cost"), ("굴착깊이", "exc"), ("사업면적", "area")):
                if it not in [a for a, _ in _sig]:
                    _pdf.pop(kk, None)
            _pdf = {**_pdf, "facs": _facs2}
            _pk = f"{_pk}_{abs(hash(tuple(_sig))) % 10 ** 6}"
            if any(bad for cl in _pdf.get("cands", {}).values() for _v, _e, bad in cl[:1]):
                st.warning("일부 항목의 근거 문장에 '피해·사례' 등 단어가 있어 설계 규모가 아닐 수 있습니다. 다른 후보값을 확인하십시오.")

with st.expander("📝 1. 사업 개요 · 입지 · 설계 대상 시설 입력", expanded=True):
    c1, c2, c3 = st.columns(3)
    sc_name = c1.text_input("사업명", value="○○항 ○○부두 축조공사", key=f"sc_name_{_pk}")
    sc_region = c2.selectbox("지역 (시·도)", ["부산", "인천", "울산", "경기", "강원", "충남", "전북", "전남", "경북", "경남", "제주", "기타"], index=9, key=f"sc_reg_{_pk}")
    _ports = ["무역항", "연안항", "국가어항", "지방어항", "기타 (항만구역 외)"]
    sc_port = c3.selectbox("항만 구분", _ports, index=_ports.index(_pdf["port"]) if _pdf.get("port") in _ports else 0, key=f"sc_port_{_pk}")
    c4, c5, c6 = st.columns(3)
    sc_stage = c4.selectbox("사업 단계", ["상위계획 수립·변경 (항만기본계획 등)", "기본설계", "실시설계"], index=1, key=f"sc_stage_{_pk}")
    sc_order = st.radio("발주 방식", ["🏛️ 일반 발주 (기본설계·실시설계 용역 분리)", "🏗️ 턴키 · 기술제안 (설계·시공 일괄)"],
                        horizontal=True, key=f"sc_order_{_pk}",
                        help="턴키 : 발주처의 기초조사·기본계획 용역에서 환경·해역·재해 등 계획 단계 인허가를 대부분 이행 → "
                             "입찰 기본설계는 인허가 없음 → 낙찰자가 실시설계 단계에서 시행 인허가 수행")
    sc_tk = sc_order.startswith("🏗️")
    sc_owner = c5.radio("사업 주체", ["공공", "민간"], horizontal=True, key=f"sc_owner_{_pk}")
    sc_loc = c6.radio("공사 위치", ["해역", "해역 + 육역", "육역"], horizontal=True, key=f"sc_loc_{_pk}")
    c7, c8, c9, c10 = st.columns(4)
    sc_urban = c7.checkbox("도시지역 (국토계획법)", value=bool(_pdf.get("urban", False)), key=f"sc_urb_{_pk}")
    sc_cons = c8.checkbox("보호구역 포함 (해양보호구역 · 습지보호지역 등)", value=False, key=f"sc_cons_{_pk}",
                          help="자연환경보전법 · 습지보전법 등 보호지역 — 소규모 환경영향평가 [별표 4] 보호지역 기준 확인 (용도지역은 아래 칸)")
    sc_heri = c9.checkbox("지정 문화유산 주변", value=bool(_pdf.get("heri", False)), key=f"sc_heri_{_pk}")
    sc_fish = c10.checkbox("어업권·양식장 인접", value=bool(_pdf.get("fish", True)), key=f"sc_fish_{_pk}")
    d1, d2, d3, d4 = st.columns(4)
    sc_cost = d1.number_input("총공사비 (억원)", value=float(_pdf.get("cost", 800.0)), step=10.0, min_value=0.0, key=f"sc_cost_{_pk}")
    sc_area = d2.number_input("사업면적 (m², 육·해역 합계)", value=float(_pdf.get("area", 120000.0)), step=1000.0, min_value=0.0, key=f"sc_area_{_pk}")
    sc_exc = d3.number_input("최대 굴착깊이 (m, 육상)", value=float(_pdf.get("exc", 0.0)), step=1.0, min_value=0.0, key=f"sc_exc_{_pk}")
    sc_hgt = d4.number_input("최고 구조물 높이 (m)", value=0.0, step=1.0, min_value=0.0, key=f"sc_hgt_{_pk}")
    e1, e2, e3, e4 = st.columns(4)
    sc_span = e1.number_input("최대 교량 지간 (m)", value=0.0, step=5.0, min_value=0.0, key=f"sc_span_{_pk}")
    sc_toe = e2.number_input("연간 연료·열 사용량 (TOE)", value=0.0, step=100.0, min_value=0.0, help="미확정이면 0 → '해당 가능'으로 판정", key=f"sc_toe_{_pk}")
    sc_kwh = e3.number_input("연간 전력 사용량 (만 kWh)", value=0.0, step=100.0, min_value=0.0, key=f"sc_kwh_{_pk}")
    sc_cls = e4.checkbox("1·2종 시설물 포함 (시설물안전법)", value=True, help="외곽시설·계류시설 등 규모 기준 해당 여부", key=f"sc_cls_{_pk}")
    f1, f2, f3, f4 = st.columns(4)
    sc_cargo = f1.number_input("연간 하역능력 (만 톤)", value=0.0, step=10.0, min_value=0.0, key=f"sc_cargo_{_pk}", help="교통영향평가 항만 기준 150만 톤")
    sc_ship = f2.number_input("최대 이용 선박 길이 (m)", value=0.0, step=10.0, min_value=0.0, key=f"sc_ship_{_pk}", help="해상교통안전진단 : 100m 이상 선박 계류시설")
    sc_redev = f3.checkbox("항만재개발사업", value=False, key=f"sc_redev_{_pk}")
    sc_maint = f4.checkbox("유지준설 (항로·정박지 유지)", value=False, key=f"sc_maint_{_pk}", help="환경영향평가·해양이용 준설 기준에서 제외")
    # [2026-11-06] 규모 판정 보강 입력
    g1, g2, g3, g4 = st.columns(4)
    sc_zone = g1.selectbox("용도지역 (육상 사업 부지)", list(SMALL_ZONE), index=0, key=f"sc_zone_{_pk}",
                           help="소규모 환경영향평가 [별표 4] 용도지역별 면적 : 보전관리 5천 · 생산관리 7,500 · 계획관리 1만 · 농림 7,500 · "
                                "자연환경보전 5천 · 개발제한구역 5천 m² 이상 (사업면적과 비교). 자연환경보전지역 매립은 [별표 3] 제10호 3만 m² 기준")
    sc_dred_a = g2.number_input("준설 면적 (m²)", value=0.0, step=1000.0, min_value=0.0, key=f"sc_dreda_{_pk}",
                                help="환경영향평가 준설면적 10만 m² · 해양이용협의 준설면적 기준 (유지준설은 제외). 0 = 미입력")
    sc_occ = g3.number_input("공유수면 점용·사용 면적 (m², 매립 제외)", value=0.0, step=1000.0, min_value=0.0, key=f"sc_occ_{_pk}",
                             help="일반 해양이용협의 점용 3천 m² · 해상교통안전진단 수역 면적 2만 m² 기준. 0 = 미입력")
    sc_shallow = g4.checkbox(f"시설 수역 수심 {SCOPE_TH['mts_depth'][0]} m 미만", value=False, key=f"sc_shal_{_pk}",
                             help="해상교통안전진단 : 수심 4m 미만 수역의 시설물 · 교량은 대상에서 제외")
    sc_chg = st.checkbox("🔁 변경 · 증설 사업 (기존 사업의 환경영향평가 · 해양이용협의 협의 완료)", value=False, key=f"sc_chg_{_pk}",
                         help="재협의 (환경영향평가법 시행령 제54조 · 해양이용영향평가법 시행령 제17조) · 변경협의 (시행령 제55조) 판정")
    sc_area0, sc_outer0, sc_5y, sc_7y = 0.0, 0.0, False, False
    if sc_chg:
        h1, h2, h3, h4 = st.columns(4)
        sc_area0 = h1.number_input("기 협의 사업면적 (m²)", value=0.0, step=1000.0, min_value=0.0, key=f"sc_area0_{_pk}",
                                   help="위 '사업면적' 은 변경 후 전체 면적으로 넣으십시오")
        sc_outer0 = h2.number_input("기 협의 외곽시설 길이 (m)", value=0.0, step=10.0, min_value=0.0, key=f"sc_outer0_{_pk}",
                                    help="아래 방파제 · 호안 규모는 변경 후 전체 길이로 넣으십시오")
        sc_5y = h3.checkbox("협의 후 5년 이내 미착공", value=False, key=f"sc_5y_{_pk}")
        sc_7y = h4.checkbox("7년 이상 공사중지 후 재개", value=False, key=f"sc_7y_{_pk}")
    st.markdown("**설계 대상 시설 선택** — 선택한 시설의 규모 입력란이 아래에 나타납니다")
    _def = list(_pdf["facs"].keys()) if _pdf.get("facs") else ["방파제", "안벽", "준설"]
    sc_sel = st.multiselect("설계 대상 시설", list(SCOPE_UNITS), default=_def, key=f"sc_sel_{_pk}", label_visibility="collapsed")
    _dflt = {"방파제": 500.0, "안벽": 300.0, "준설": 200000.0}
    _vals = {}
    if sc_sel:
        gc = st.columns(4)
        for k_, fac in enumerate(sc_sel):
            dv = float(_pdf.get("facs", {}).get(fac, _dflt.get(fac, 0.0)))
            _vals[fac] = gc[k_ % 4].number_input(f"{fac} ({SCOPE_UNITS[fac]})", value=dv, min_value=0.0,
                                                 step=1000.0 if SCOPE_UNITS[fac].startswith("m²") or SCOPE_UNITS[fac] == "m³" else 10.0,
                                                 key=f"sc_v_{fac}_{_pk}")
    sc_fac = pd.DataFrame([{"선택": f in sc_sel, "시설": f, "규모": _vals.get(f, 0.0), "단위": u} for f, u in SCOPE_UNITS.items()])
    _SEA_FACS = ("방파제", "호안 (외곽·투기장 호안)", "안벽", "잔교", "물양장", "계류시설 (부잔교·돌핀 등)", "준설",
                 "준설토 투기장", "공유수면 매립 (부지 조성)", "항로·박지 신설·변경", "해상교량·해저케이블·터널", "해상풍력발전")
    if sc_loc == "육역" and any(f in sc_sel for f in _SEA_FACS):
        st.warning("⚠️ 공사 위치를 '육역'으로 골랐는데 해역 시설(" + ", ".join(f for f in sc_sel if f in _SEA_FACS) +
                   ")이 선택되어 있습니다. 해역 시설이 있으면 해역 인허가(공유수면 · 해양이용협의 · 해상교통안전진단 · 어업피해 등)를 "
                   "빼지 않고 판정합니다 — 공사 위치를 '해역' 또는 '해역 + 육역'으로 바꾸십시오. (검증보고서 23-2)")


def _fsel(name):
    r = sc_fac[sc_fac["시설"] == name]
    return (bool(r["선택"].iloc[0]), float(r["규모"].iloc[0] or 0)) if len(r) else (False, 0.0)


def analyze_scope():
    S = {k: _fsel(k) for k in SCOPE_FAC["시설"]}
    sel = lambda k: S[k][0]
    val = lambda k: S[k][1] if S[k][0] else 0.0
    sea_fac = any(sel(k) for k in ("방파제", "호안 (외곽·투기장 호안)", "안벽", "잔교", "물양장", "계류시설 (부잔교·돌핀 등)", "준설",
                                   "준설토 투기장", "공유수면 매립 (부지 조성)", "항로·박지 신설·변경", "해상교량·해저케이블·터널", "해상풍력발전"))
    sea_works = sea_fac                       # [2026-10-23 검증보고서 23-2] '육역'이라도 해역 시설이 있으면 해역 공사로 봄 (경고는 입력란 아래)
    loc_sea = sc_loc != "육역" or sea_fac
    recl = val("공유수면 매립 (부지 조성)") + val("준설토 투기장")
    land = sc_loc != "해역" or sel("배후부지·육상 부지조성") or sel("건축물 (터미널·창고 등)") or sel("진입도로")
    port_dev = any(sel(k) for k in ("방파제", "안벽", "잔교", "물양장", "계류시설 (부잔교·돌핀 등)", "항로·박지 신설·변경", "호안 (외곽·투기장 호안)"))
    plan = sc_stage.startswith("상위계획")
    R = []
    CMP = []                                  # [2026-11-06] (번호, 항목, 값, 기준, 단위) — 기준 근접 표시용
    T = _th

    def add(no, name, mark, why, agency, period, phase):
        R.append({"번호": no, "인허가": name, "판정": mark, "판정 사유": why, "협의·허가기관": agency, "법정 기간": period, "시기": phase})

    def c_(no, label, v, k):
        """기준 비교 한 줄 'label v ≥ t' + 근접 목록 등록"""
        t, u = SCOPE_TH[k][0], SCOPE_TH[k][1]
        CMP.append((no, label, v, t, u))
        return f"{label} {v:,.0f} {u} {'≥' if v >= t else '<'} {t:,} {u}"

    F, P, N = "● 필수", "◐ 해당 가능", "○ 해당 없음"
    add(1, "전략환경영향평가", P if plan else N,
        "항만기본계획 등 상위계획 수립·변경 단계 — 시행령 별표 2 대상계획 확인" if plan else "설계 단계 (상위계획에서 기 이행 여부만 확인)",
        "기후에너지환경부(환경청)", "30일 (연장 40일)", "계획")
    # [별표 3] 제4호 항만의 건설 · 제10호 공유수면 매립 (행정규칙집 수록 기준)
    bw, rv = val("방파제"), val("호안 (외곽·투기장 호안)")
    outer, outer_sum = max(bw, rv), bw + rv
    dred_m3 = 0.0 if sc_maint else val("준설")
    dred_a = 0.0 if (sc_maint or not sel("준설")) else float(sc_dred_a)
    recl_only = val("공유수면 매립 (부지 조성)")
    hits, miss, maybe = [], [], []

    def chk(cond_on, label, v, k, sink=None):
        if not cond_on:
            return
        t_ = c_(2, label, v, k)
        (hits if v >= T(k) else (sink if sink is not None else miss)).append(t_)
    chk(outer > 0, "외곽시설 길이 (가장 긴 것)", outer, "eia_outer")
    if outer < T("eia_outer") <= outer_sum:
        maybe.append(f"방파제 + 호안 합산 {outer_sum:,.0f} m ≥ {T('eia_outer'):,} m — 합산 기준이면 대상 (※ 원문 확인 필요)")
    chk(recl > 0 and (port_dev or sc_port != "기타 (항만구역 외)"), "항만시설 매립", recl, "eia_recl")
    chk(not recl and port_dev and sc_area > 0, "그 밖의 항만시설 사업면적", sc_area, "eia_area")
    chk(sel("준설") and not sc_maint and dred_a > 0, "준설 면적", dred_a, "eia_dred_a")
    chk(sel("준설") and not sc_maint, "준설량", dred_m3, "eia_dred_v")
    chk(sc_redev, "항만재개발 사업면적", sc_area, "eia_redev")
    _r10 = "eia_r10_p" if (sc_port in ("무역항", "연안항") or sc_zone == "자연환경보전지역") else "eia_r10_o"
    chk(recl_only > 0, "공유수면 매립 ([별표 3] 제10호, " + ("무역항·연안항·자연환경보전지역" if _r10 == "eia_r10_p" else "그 밖의 지역") + ")",
        recl_only, _r10)
    if recl_only > 0 and _r10 == "eia_r10_o" and sc_cons and recl_only >= T("eia_r10_p"):
        maybe.append(f"매립 {recl_only:,.0f} m² — 보호구역이 자연환경보전지역이면 3만 m² 기준 (용도지역 확인)")
    _dnote = " · 준설 면적 미입력 (면적 10만 m² 기준 확인)" if (sel("준설") and not sc_maint and dred_a <= 0) else ""
    eia_t = (sea_works and (port_dev or recl > 0 or sel("준설"))) or (land and sc_area > 0)
    if sc_chg:                                 # [2026-11-06] 변경 · 증설 사업 : 재협의 · 변경협의
        _ra = (sc_area - sc_area0) / sc_area0 * 100 if sc_area0 > 0 else 0.0
        _ro = (outer - sc_outer0) / sc_outer0 * 100 if sc_outer0 > 0 else 0.0
        _rr = max(_ra, _ro)
        _rt = f"증가율 면적 {_ra:,.1f} % · 외곽 길이 {_ro:,.1f} %"
        _big = (sc_area0 > 0 and (sc_area - sc_area0) >= T("eia_area")) or (sc_outer0 > 0 and (outer - sc_outer0) >= T("eia_outer"))
        CMP[:] = [c for c in CMP if c[0] != 2]       # 변경 사업 : 신규 기준 근접은 표시하지 않음
        if sc_5y or sc_7y or _rr >= T("eia_re") or _big:
            m2 = F
            w2 = ("재협의 (시행령 제54조) : " + ", ".join(x for x, ok in (("협의 후 5년 이내 미착공", sc_5y), ("7년 이상 공사중지 후 재개", sc_7y),
                                                                          (f"{_rt} — 최대 {_rr:,.1f} % ≥ {T('eia_re')} %", _rr >= T("eia_re")),
                                                                          ("증가 규모가 최소 평가대상 규모 이상 (※ 규모 정의 원문 확인)", _big)) if ok))
        elif _rr >= T("eia_mod"):
            m2, w2 = F, f"변경협의 (시행령 제55조) : {_rt} — 최대 {_rr:,.1f} % ≥ {T('eia_mod')} %"
        else:
            m2, w2 = P, f"변경 규모 작음 ({_rt} < {T('eia_mod')} %) — 부지면적 15 % 이상 토지이용계획 변경 등 변경협의 사유 확인 (시행령 제55조)"
        CMP.append((2, "변경 규모 증가율 (재협의)", _rr, T("eia_re"), "%"))
    elif hits:
        m2, w2 = F, "[별표 3] 기준 충족 : " + ", ".join(hits)
    elif maybe:
        m2, w2 = P, "; ".join(maybe) + (" / 그 밖 : " + "; ".join(miss) if miss else "") + _dnote
    elif eia_t and not (sea_works and (port_dev or recl > 0 or sel("준설"))):
        m2, w2 = P, "육상 개발 — [별표 3] 해당 분야 (산업단지 · 도시 개발 · 물류시설 등) 사업면적 기준 확인" + (f" (사업면적 {sc_area:,.0f} m²)" if sc_area else "")
    elif eia_t:
        m2, w2 = P, ("항만건설 유형이나 [별표 3] 규모 미만 : " + ("; ".join(miss) if miss else ("유지준설 → 준설 기준 제외 ([별표 3] 제4호 다목)"
                                                                                        if (sc_maint and sel("준설")) else "규모 미입력")) + _dnote
                     + " — 연접 · 단계 사업 합산 여부 확인")
    else:
        m2, w2 = N, "대상 유형 아님"
    add(2, "환경영향평가", m2, w2, "기후에너지환경부(환경청)", "45일 (연장 60일)", "기본설계")
    _T3 = SMALL_ZONE.get(sc_zone)
    if m2 == F:
        m3, w3 = N, "환경영향평가 대상 → 소규모 환경영향평가 대상 아님 (법 제43조①)"
    elif _T3:
        _t3 = c_(3, f"{sc_zone} 사업면적", sc_area, f"small_{sc_zone}")
        if sc_area >= _T3:
            m3 = F if m2 == N else P
            w3 = f"[별표 4] {_t3}" + (" — 환경영향평가 대상이 아니면 소규모 대상" if m3 == P else "")
        else:
            m3, w3 = N, f"[별표 4] {_t3}"
    elif sc_cons:
        m3, w3 = P, "보호구역 포함 — 자연환경보전법 · 습지보전법 등 보호지역 [별표 4] 기준 확인 (용도지역을 고르면 면적으로 판정)"
    else:
        m3, w3 = N, "보전용도지역 · 보호구역 아님"
    add(3, "소규모 환경영향평가", m3, w3, "지방·유역환경청", "30일 (연장 40일)", "기본설계")
    add(4, "기후변화영향평가", P if m2 != N or plan else N, "전략·환경영향평가 대상 중 탄소중립기본법 시행령 대상이면 병행 실시",
        "기후에너지환경부", "환경영향평가 협의기간 내", "기본설계")
    # [2026-11-06] 해양이용협의 구분 (종전 해양환경관리법 시행령 별표 15 · 16 수치 — 신법 별표 1 · 2 원문 확인 필요)
    _old = " (※ 종전 별표 15 · 16 수치 — 신법 시행령 별표 1 · 2 원문 확인 필요)"
    if not sea_works:
        m5, w5, p5 = N, "해역 공사 없음", "일반 30일 / 영향평가 45일"
    elif sc_chg:
        _mr = max((max(sc_area, 0) - sc_area0) / sc_area0 * 100 if sc_area0 > 0 else 0.0,
                  (outer - sc_outer0) / sc_outer0 * 100 if sc_outer0 > 0 else 0.0)
        if sc_7y or _mr >= T("mar_re"):
            m5, w5 = F, ("재협의 (시행령 제17조) : " + ("7년 이상 중지 후 재개" if sc_7y else f"면적 · 길이 증가 {_mr:,.1f} % ≥ {T('mar_re')} %"))
        else:
            m5, w5 = P, f"면적 · 길이 증가 {_mr:,.1f} % < {T('mar_re')} % — 재협의 아님, 새 점용 · 사용 면허등이 있으면 그 협의 확인"
        p5 = "일반 30일 / 영향평가 45일"
    else:
        ia, gen, low = [], [], []
        for lab, v, k, sink in (("준설 면적", dred_a, "mar_ia_da", ia), ("준설량", dred_m3, "mar_ia_dv", ia)):
            if sel("준설") and not sc_maint and v > 0:
                (sink if v >= T(k) else low).append(c_(5, lab, v, k))
        _len5 = max(val("방파제"), val("호안 (외곽·투기장 호안)"), val("안벽"), val("잔교"), val("물양장"))
        if recl > 0:
            gen.append(f"매립 {recl:,.0f} m² (바다 · 바닷가 매립은 규모 무관)")
        for lab, v, k, on in (("계류 · 외곽시설 길이", _len5, "mar_g_len", _len5 > 0), ("점용 · 사용 면적", sc_occ, "mar_g_occ", sc_occ > 0),
                              ("준설 면적", dred_a, "mar_g_da", sel("준설") and not sc_maint and dred_a > 0),
                              ("준설량", dred_m3, "mar_g_dv", sel("준설") and not sc_maint and dred_m3 > 0)):
            if on and not (ia and k in ("mar_g_da", "mar_g_dv")):
                (gen if v >= T(k) else low).append(c_(5, lab, v, k))
        if ia:
            m5, w5, p5 = F, "해양이용영향평가 : " + ", ".join(ia) + _old, "영향평가 45일"
        elif gen:
            m5, w5, p5 = F, "일반 해양이용협의 : " + ", ".join(gen) + (" (영향평가 미만 : " + "; ".join(low) + ")" if low else "") + _old, "일반 30일"
        else:
            m5 = F
            w5 = ("해양이용협의 (공유수면 점용 · 사용) — 일반 협의 규모 미만 : " + ("; ".join(low) if low else "규모 미입력")
                  + " → 해양 영향 경미 사업이면 검토기관 의견 청취 생략 가능 (법 제12조② 단서)"
                  + ("" if sc_occ > 0 else " · 점용 · 사용 면적을 넣으면 더 정확") + _old)
            p5 = "일반 30일"
    add(5, "해양이용협의 / 해양이용영향평가", m5, w5, "해양수산부(지방해양수산청)", p5, "기본·실시설계")
    add(6, "해양환경영향조사", P if sea_works else N, "해양이용협의·영향평가 처분 후 조사 (해양수산부령 대상·기간)", "해양수산부", "-", "시공 중")
    add(7, "해양공간적합성협의", F if (plan and loc_sea) else (P if sea_works else N),
        "해양 이용·개발계획 수립·변경 / 지구 지정 시 다른 절차보다 먼저 요청" if plan else "상위계획(항만기본계획 등)에서 기 협의 여부 확인 — 변경 시 협의",
        "해양수산부", "45일 (재협의 20일)", "계획")
    if sea_works:
        why8 = "해역 구조물 설치·준설 → 공유수면 점용·사용허가" + (f" ({sc_occ:,.0f} m²)" if sc_occ > 0 else "")
        if recl > 0:
            why8 += f" / 매립 {recl:,.0f} m² → 매립기본계획 반영 + 매립면허 ({'해양수산부장관' if recl >= 100000 else '시·도지사'})"
        add(8, "공유수면 점용·사용허가 / 매립면허", F, why8, "공유수면관리청 · 면허관청", "관계기관 의견 20일", "실시설계")
    else:
        add(8, "공유수면 점용·사용허가 / 매립면허", N, "해역 공사 없음", "-", "-", "-")
    _km = val("진입도로")
    if plan:
        m9, w9 = F, "행정계획(항만기본계획·매립기본계획 등) → 재해영향성검토 (규모 무관)"
    elif sc_area >= T("dis_a") or _km >= T("dis_l"):
        m9, w9 = F, f"항만개발사업 실시계획 — {c_(9, '면적', sc_area, 'dis_a')}" + (f" / {c_(9, '길이', _km, 'dis_l')}" if _km else "") + " → 재해영향평가 (45일)"
    elif sc_area >= T("dis_sa") or _km >= T("dis_sl"):
        m9, w9 = F, f"{c_(9, '면적', sc_area, 'dis_a')} · {c_(9, '면적', sc_area, 'dis_sa')}" + (f" / 길이 {_km:,.1f} km" if _km else "") + " → 소규모 재해영향평가 (30일)"
    else:
        m9, w9 = N, c_(9, "면적", sc_area, "dis_sa") + (f" · {c_(9, '길이', _km, 'dis_sl')}" if _km else "")
    add(9, "재해영향평가 (재해영향성검토)", m9, w9,
        "행정안전부 · 시·도", "45일 / 30일 (연장 10일)", "기본설계")
    _m10 = F if sc_cargo >= T("trf_cargo") else (P if (land and (sel("배후부지·육상 부지조성") or sel("건축물 (터미널·창고 등)") or sel("진입도로"))) else N)
    _t10 = c_(10, "연간 하역능력", sc_cargo, "trf_cargo") if sc_cargo > 0 else ""
    add(10, "교통영향평가", _m10,
        f"항만의 건설 : {_t10} (도시교통정비지역·교통권역 내)" if _m10 == F else
        "배후단지·건축물·도로 — [별표 1] 규모 확인 (항만 : 하역능력 150만 톤)" + (f" · {_t10}" if _t10 else ""), "승인관청 (심의위원회)", "심의 (이의신청 30/60일)", "기본설계")
    add(11, "도시·군계획시설 결정", P if (land and sc_urban) else N, "도시지역 내 기반시설(항만·도로 등) 설치 시 도시관리계획 결정 확인",
        "시·도지사 등", "관계기관 협의 30일", "계획·기본설계")
    _kt, _kk = ("en_pub_toe", "en_pub_kwh") if sc_owner == "공공" else ("en_prv_toe", "en_prv_kwh")
    t_pub, t_prv = T(_kt), T(_kk)
    if sc_toe >= t_pub or sc_kwh >= t_prv:
        m12, w12 = F, f"{c_(12, '연료·열', sc_toe, _kt)} / {c_(12, '전력', sc_kwh, _kk)} ({sc_owner} 기준)"
    elif sc_toe == 0 and sc_kwh == 0:
        m12, w12 = P, f"항만건설 대상 사업 — 에너지 사용량 확정 후 판정 ({sc_owner} 기준 {t_pub:,} TOE / {t_prv:,}만 kWh)"
    else:
        m12, w12 = N, f"{c_(12, '연료·열', sc_toe, _kt)} / {c_(12, '전력', sc_kwh, _kk)} ({sc_owner} 기준 미만)"
    add(12, "에너지사용계획 협의", m12, w12, "기후에너지환경부 (에너지공단)", "30일 (연장 20일)", "기본설계")
    m13 = F if sc_exc >= T("ug_small") else N
    _t13 = c_(13, "굴착", sc_exc, "ug_big" if sc_exc >= T("ug_small") else "ug_small") if sc_exc > 0 else "굴착 없음"
    add(13, "지하안전평가", m13, (f"{_t13} → 지하안전평가" if sc_exc >= T("ug_big") else (f"{_t13} → 소규모 지하안전평가" if sc_exc >= T("ug_small") else _t13)),
        "국토교통부 (지방국토관리청)", "30일 (연장 50일)", "실시설계")
    m14 = F if (sc_cls or sc_exc >= T("saf_exc")) else P
    add(14, "설계안전성 검토 · 안전관리계획", m14, "1·2종 시설물 또는 굴착 10m 이상 → 안전관리계획(착공 전), 실시설계 시 설계안전성 검토" if m14 == F else "안전관리계획 대상 여부 확인 (시행령 제98조)",
        "발주청 · 국토안전관리원", "검토 20일", "실시설계·착공 전")
    m15 = F if (sc_exc >= T("haz_exc") or sc_hgt >= T("haz_hgt") or sc_span >= T("haz_span")) else N
    _t15 = [c_(15, lb, v, k) for lb, v, k in (("굴착", sc_exc, "haz_exc"), ("높이", sc_hgt, "haz_hgt"), ("교량 지간", sc_span, "haz_span")) if v > 0]
    add(15, "유해·위험방지계획서", m15, (" / ".join(_t15) if _t15 else "굴착 · 높이 · 지간 입력 없음") + (" → 해당" if m15 == F else " — 기준 미해당"),
        "한국산업안전보건공단", "심사 15일", "착공 전날까지")
    _w16, _x16 = [], []
    if sc_ship >= T("mts_ship") and port_dev: _w16.append(c_(16, "계류시설 이용 선박 길이", sc_ship, "mts_ship"))
    elif sc_ship > 0 and port_dev: _x16.append(c_(16, "선박 길이", sc_ship, "mts_ship"))
    _l16 = max(val("방파제"), val("안벽"), val("잔교"), val("물양장"), val("호안 (외곽·투기장 호안)"))
    _a16 = max(recl, float(sc_occ))
    if not sc_shallow:
        if _l16 >= T("mts_len") or _a16 >= T("mts_area"):
            _w16.append(c_(16, "시설물 수역 길이", _l16, "mts_len") + " 또는 " + c_(16, "점용·매립 면적", _a16, "mts_area"))
        elif _l16 > 0 or _a16 > 0:
            _x16.append(c_(16, "수역 길이", _l16, "mts_len") + " · " + c_(16, "면적", _a16, "mts_area"))
        if sel("해상교량·해저케이블·터널"): _w16.append("수역 내 교량·터널·케이블")
    else:
        _x16.append(f"수심 {T('mts_depth')} m 미만 수역 → 시설물 · 교량 규모 기준 제외")
    if sel("항로·박지 신설·변경"): _w16.append("항로·정박지 지정·변경")
    m16 = F if (_w16 and loc_sea) else (P if (port_dev and loc_sea) else N)
    add(16, "해상교통안전진단", m16, ("; ".join(_w16) + ("" if sc_shallow else " (수심 4m 미만 수역 제외)")) if m16 == F else
        ("항만시설 — " + ("; ".join(_x16) if _x16 else "규모 기준(선박 100m, 수역 200m·2만m²) 미입력") + " — 제출 불필요 의견서 여부 확인" if m16 == P else "대상 사업 없음"),
        "해양수산부", "검토 45일", "기본설계")
    add(17, "해상풍력 인허가 (해상풍력법)", F if sel("해상풍력발전") else N, "해상풍력 발전사업 — 발전지구·실시계획 승인" if sel("해상풍력발전") else "해당 없음",
        "해상풍력발전위원회", "관계기관 협의 30일", "계획")
    add(18, "어업피해영향조사", F if (sea_works and sc_fish) else (P if sea_works else N), "해역 공사 + 어업권·양식장 인접 → 피해조사·보상", "사업시행자 · 지자체", "-", "기본설계·시공 전")
    add(19, "매장유산 지표조사 / 현상변경", F if (sc_area >= T("heri_area") or sc_heri) else N,
        c_(19, "사업면적", sc_area, "heri_area") + (" / 지정 문화유산 주변 → 현상변경 허가 검토" if sc_heri else ""),
        "국가유산청", "검토 30일", "기본설계")
    add(20, "수저준설토사 유효활용", P if sel("준설") else N, "준설토 성분·오염도 검사 후 유효활용·처리 방안 협의", "지방해양수산청", "-", "실시설계")
    _cost_t = f"{sc_cost:,.2f}".rstrip("0").rstrip(".")          # [2026-10-23 검증보고서 23-4] 99.99 → '100' 반올림 표시 방지
    CMP.append((21, "총공사비", sc_cost, T("ve_cost"), "억원"))
    if sc_cost < T("ve_cost"):
        m21, w21 = N, f"총공사비 {_cost_t}억원 < {T('ve_cost')}억원 (시행령 제75조)"
    elif sc_owner == "공공":
        m21, w21 = F, f"총공사비 {_cost_t}억원 ≥ {T('ve_cost')}억원 (시행령 제75조)"
    else:                                                        # [2026-10-23 검증보고서 23-3] 제75조는 발주청 건설공사 대상
        m21, w21 = P, f"총공사비 {_cost_t}억원 ≥ {T('ve_cost')}억원 — 민간 사업 : 시행령 제75조는 발주청 건설공사 대상이므로 발주청 해당 여부 확인"
    add(21, "설계의 경제성 검토 (VE)", m21, w21, "발주청", "-", "기본·실시설계")
    _lk = "ls_urban" if sc_urban else "ls_rural"
    lsc = sc_area >= T(_lk) or (sel("진입도로") and sc_cost >= T("ls_road"))
    _t22 = c_(22, "개발사업 면적 (" + ("도시" if sc_urban else "도시 외") + ")", sc_area, _lk)
    add(22, "경관심의", P if lsc else N, (_t22 + " 또는 도로 500억 이상 — 사업 유형 별표 확인") if lsc else _t22 + " — 면적·사업비 기준 미해당",
        "경관위원회", "-", "기본설계")
    add(23, "공공디자인 심의", P if sc_owner == "공공" else N, "공공시설물 설치 — 지자체 공공디자인 조례 확인", "지자체 위원회", "-", "기본·실시설계")
    add(24, "항만공간 공공디자인 협의", P if (port_dev and sc_port != "기타 (항만구역 외)") else N, "항만시설 — 항만공간 공공디자인 가이드라인(예규) 적용", "지방해양수산청·항만공사", "-", "기본·실시설계")
    # [2026-11-06] 기준 근접 (기준의 90 % 이상 · 미만) — 설계 변경 때 대상이 될 수 있음
    near = {}
    for no, lab, v, t, u in CMP:
        if t and v > 0 and 0.9 * t <= v < t:
            near.setdefault(no, []).append(f"{lab} {v:,.0f} {u} (기준 {t:,} {u} 의 {v / t * 100:.0f} %)")
    for r in R:
        if r["번호"] in near:
            r["판정 사유"] = "⚠ 기준 근접 : " + ", ".join(near[r["번호"]]) + " — " + r["판정 사유"]
    df = pd.DataFrame(R)
    df.attrs["near"] = near
    return df


# 턴키 : 번호 → (단계번호, 시기, 수행 주체)  0 = 기초조사·기본계획(발주처) / 2 = 실시설계(낙찰자) / 3 = 착공 전·시공 중
_TK_PHASE = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 7: 0, 9: 0, 11: 0, 17: 0, 19: 0, 22: 0,
             8: 2, 10: 2, 12: 2, 13: 2, 14: 2, 16: 2, 18: 2, 20: 2, 21: 2, 23: 2, 24: 2, 6: 3, 15: 3}
_TK_NOTE = {5: "실시설계 단계 공유수면 점용·사용 시 변경협의", 10: "기본계획에서 기 이행 시 변경 여부만 확인",
            16: "기본계획 단계 진단 결과가 있으면 실시설계 시 변경 진단", 18: "보상 계획은 발주처 기본계획에서 수립"}


def apply_delivery(df, turnkey):
    """발주방식에 따라 '시기'·'수행 주체'·'_단계' 재배정"""
    d = df.copy()
    key = lambda ph: 0 if ("계획" in ph and "기본" not in ph) else (1 if ph.startswith("기본") else (2 if ph.startswith("실시") else 3))
    if not turnkey:
        d["_단계"] = [key(x) if x != "-" else 3 for x in d["시기"]]
        d["수행 주체"] = ["발주처 (상위계획)" if k == 0 else ("시공사" if k == 3 else "설계용역사 (발주처 명의)") for k in d["_단계"]]
        return d
    ph_name = {0: "기초조사·기본계획 (발주처 용역)", 2: "실시설계 (낙찰자)", 3: "착공 전·시공 중"}
    who = {0: "발주처", 2: "낙찰자 (설계·시공 일괄)", 3: "시공사 (낙찰자)"}
    d["_단계"] = [_TK_PHASE.get(int(n), 2) for n in d["번호"]]
    d["시기"] = [ph_name[k] for k in d["_단계"]]
    d["수행 주체"] = [who[k] for k in d["_단계"]]
    d["판정 사유"] = [r + (f" ※ 턴키 : {_TK_NOTE[int(n)]}" if int(n) in _TK_NOTE and m != "○ 해당 없음" else "")
                  for n, r, m in zip(d["번호"], d["판정 사유"], d["판정"])]
    return d


def scope_roadmap_png(df):
    _fplt.rcParams["font.family"] = _flow_font()
    _fplt.rcParams["axes.unicode_minus"] = False
    tk = bool(df.attrs.get("turnkey"))
    phases = (["기초조사·기본계획\n(발주처)", "기본설계 (입찰)\n인허가 없음", "실시설계\n(낙찰자)", "착공 전·시공 중"] if tk
              else ["계획", "기본설계", "실시설계", "착공 전·시공 중"])
    d = df[df["판정"] != "○ 해당 없음"].copy()
    d["단계"] = d["_단계"]
    cols = {"● 필수": "#1d4ed8", "◐ 해당 가능": "#f59e0b"}
    fig, ax = _fplt.subplots(figsize=(11, 0.42 * max(len(d), 4) + 1.6))
    for i, (_, r) in enumerate(d.sort_values(["단계", "번호"]).iterrows()):
        y = -i
        ax.barh(y, 0.92, left=r["단계"] + 0.04, color=cols[r["판정"]], alpha=0.9 if r["판정"].startswith("●") else 0.55, height=0.62)
        _nm = r["인허가"].split(" (")[0].split(" / ")[0]
        ax.text(r["단계"] + 0.08, y, f"{r['번호']}. {_nm if len(_nm) <= 15 else _nm[:14] + '…'}", va="center", fontsize=8.6, color="white" if r["판정"].startswith("●") else "#1f2937",
                fontweight="bold")
        if r["법정 기간"] not in ("-", ""):
            ax.text(4.05, y, r["법정 기간"], va="center", fontsize=8.6, color="#c2410c", fontweight="bold")
    for k, ph in enumerate(phases):
        ax.axvspan(k, k + 1, color="#f1f5f9" if k % 2 == 0 else "white", zorder=0)
        ax.text(k + 0.5, 1.0, ph, ha="center", va="center", fontsize=9.5 if tk else 10, fontweight="bold",
                color="#94a3b8" if (tk and k == 1) else "#1e3a8a")
    if tk:
        ax.text(1.5, -len(d) / 2 + 0.5, "인허가 미수행\n(기 협의 결과 반영 ·\n실시설계 인허가 계획 수립)", ha="center",
                va="center", fontsize=9, color="#64748b", style="italic")
    ax.text(4.6, 1.0, "법정 기간", ha="center", fontsize=9.5, fontweight="bold", color="#c2410c")
    ax.set_xlim(0, 5.3)
    ax.set_ylim(-len(d) + 0.4, 1.5)
    ax.axis("off")
    ax.set_title(f"인허가 로드맵 — {sc_name}  [{'턴키 · 설계시공 일괄' if tk else '일반 발주'}]",
                 fontsize=12, fontweight="bold", loc="left")
    # [2026-10-20] 범례를 막대와 같은 색으로 (제목 글자 '■' 는 둘 다 검은색이라 구분이 안 됨)
    from matplotlib.patches import Patch as _Patch
    fig.tight_layout()
    fig.legend(handles=[_Patch(facecolor=cols["● 필수"], alpha=0.9, label="필수"),
                        _Patch(facecolor=cols["◐ 해당 가능"], alpha=0.55, label="해당 가능")],
               loc="upper right", bbox_to_anchor=(0.99, 0.995), ncol=2, fontsize=10, frameon=True, edgecolor="#cbd5e1",
               handlelength=1.6, handleheight=1.1, borderpad=0.4, columnspacing=1.2)
    buf = _fio.BytesIO()
    fig.savefig(buf, format="png", dpi=130)
    _fplt.close(fig)
    return buf.getvalue()



# [2026-11-06] 아이디어 10 — 판정된 인허가의 근거 조문 · 법제처 바로가기 (SCOPE_INFO 의 근거 위치 · 시기 그대로, 원문 없는 제출서류 목록은 만들지 않음)
def _law_names(where_list):
    import re as _r
    out = []
    for w in where_list:
        for nm in _r.findall(r"「([^」]+)」", w):
            if nm not in out:
                out.append(nm)
    return out


def _law_url(q):
    from urllib.parse import quote as _q
    return f"https://www.law.go.kr/lsSc.do?menuId=1&query={_q(q)}"


def scope_links_rows(df):
    rows = []
    for _, r in df[df["판정"] != "○ 해당 없음"].iterrows():
        d = SCOPE_INFO.get(int(r["번호"]), {})
        laws = _law_names(d.get("where", []))
        rows.append({"번호": int(r["번호"]), "인허가": r["인허가"], "판정": r["판정"],
                     "근거 위치 (법 → 시행령 → 별표)": " / ".join(d.get("where", [])) or "-",
                     "협의 · 실시 시기": d.get("timing", "-"),
                     "법령": laws,
                     "바로가기": [(nm, _law_url(nm)) for nm in laws] + [(nm + " 시행령", _law_url(nm + " 시행령")) for nm in laws
                                                                       if not nm.endswith(("규정", "가이드라인", "조례")) and "시행령" not in nm][:2]})
    return rows


def scope_links_html(rows):
    import html as _h
    md = lambda s_: _kit_re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", _h.escape(str(s_)))
    tr = []
    for r in rows:
        lk = " · ".join(f"<a href='{u}' target='_blank'>{_h.escape(n)}</a>" for n, u in r["바로가기"]) or "-"
        tr.append(f"<tr><td style='text-align:center'>{r['번호']}</td><td><b>{_h.escape(r['인허가'])}</b><br><span style='font-size:12px'>{r['판정']}</span></td>"
                  f"<td style='font-size:12.5px'>{md(r['근거 위치 (법 → 시행령 → 별표)'])}</td><td style='font-size:12.5px'>{md(r['협의 · 실시 시기'])}</td>"
                  f"<td style='font-size:12.5px'>{lk}</td></tr>")
    th = "".join(f"<th style='background:#1e3a8a;color:#fff;padding:5px'>{x}</th>" for x in ("번호", "인허가", "근거 위치 (법 → 시행령 → 별표)", "협의 · 실시 시기", "법제처 바로가기"))
    return ("<table style='width:100%;border-collapse:collapse;color:#0f172a' border='1' cellpadding='5'>"
            f"<tr>{th}</tr>{''.join(tr)}</table>")


# [2026-11-06] 아이디어 9 — 인허가 일정표 : 단계 기간(사용자 가정) + 법정 검토 기간 (각 인허가 '법정 기간' 칸의 첫 일수)
def _legal_days(period, why=""):
    import re as _r
    p = str(period or "")
    if not p or p.strip() == "-" or p.startswith("심의") or "협의기간 내" in p:
        return None
    parts = [x for x in p.split("/")]
    pick = parts[1] if (len(parts) > 1 and "소규모" in str(why)) else parts[0]
    m = _r.search(r"(\d+)\s*일", pick) or _r.search(r"(\d+)\s*일", p)
    return int(m.group(1)) if m else None


def scope_schedule(df, start, plan_m, base_m, det_m, done=()):
    import pandas as _pd
    st0 = _pd.Timestamp(start)
    b = [st0]
    for mth in (plan_m, base_m, det_m):
        b.append(b[-1] + _pd.DateOffset(months=int(mth)))
    ends = {0: b[1], 1: b[2], 2: b[3]}
    rows = []
    for _, r in df[df["판정"] != "○ 해당 없음"].iterrows():
        k = int(r["_단계"])
        dd = _legal_days(r["법정 기간"], r["판정 사유"])
        note = ""
        if k >= 3:
            s_ = b[3]
            e_ = s_ + _pd.Timedelta(days=dd or 0)
        else:
            e_ = ends[k]
            s_ = e_ - _pd.Timedelta(days=dd or 0)
            if k == 0 and int(plan_m) == 0:
                note = "착수 전 완료 필요 (상위계획에서 이행 · 기 이행 확인)"
            elif s_ < b[k]:
                note = "법정 검토 기간이 단계 기간보다 김 — 앞 단계에서 미리 요청"
        rows.append({"번호": int(r["번호"]), "인허가": r["인허가"], "판정": r["판정"], "단계": r["시기"], "비고": note,
                     "법정 검토 (일)": dd if dd is not None else "-", "협의 요청 늦어도": s_.date(), "협의 완료 목표": e_.date(),
                     "상태": "완료 (이미 받음)" if int(r["번호"]) in done else "예정", "_k": k, "_s": s_, "_e": e_})
    return _pd.DataFrame(rows), b


def scope_gantt_png(sd, b, title):
    import matplotlib.dates as _md
    _fplt.rcParams["font.family"] = _flow_font()
    _fplt.rcParams["axes.unicode_minus"] = False
    n = max(len(sd), 3)
    fig, ax = _fplt.subplots(figsize=(11.5, 0.42 * n + 1.9))
    names = ["기초조사·기본계획", "기본설계 (입찰)", "실시설계 (낙찰자)"] if sd.attrs.get("tk") else ["계획", "기본설계", "실시설계"]
    for k in range(3):
        if b[k + 1] > b[k]:
            ax.axvspan(b[k], b[k + 1], color="#f1f5f9" if k % 2 == 0 else "#ffffff", zorder=0)
            ax.text(b[k] + (b[k + 1] - b[k]) / 2, 0.9, f"{names[k]}\n{b[k]:%y.%m} – {b[k + 1]:%y.%m}", ha="center", va="bottom",
                    fontsize=9.5, fontweight="bold", color="#1e3a8a")
    ax.axvline(b[3], color="#c2410c", lw=1.2, ls="--")
    ax.axvline(b[0], color="#1e3a8a", lw=1.0, ls=":")
    ax.text(b[0], 1.55, f"착수 {b[0]:%y.%m.%d}", ha="left", va="bottom", fontsize=9, color="#1e3a8a")
    ax.text(b[3], 0.9, f"착공 전\n{b[3]:%y.%m.%d}", ha="left", va="bottom", fontsize=9.5, fontweight="bold", color="#c2410c")
    for i, (_, r) in enumerate(sd.sort_values(["_k", "_s", "번호"]).iterrows()):
        y = -i
        done = r["상태"].startswith("완료")
        col = "#94a3b8" if done else ("#1d4ed8" if r["판정"].startswith("●") else "#f59e0b")
        w = (r["_e"] - r["_s"]).days
        if w > 0:
            ax.barh(y, w, left=r["_s"], height=0.6, color=col, alpha=0.9 if not done else 0.6)
        else:
            ax.plot([r["_e"]], [y], marker="D", color=col, ms=7)
        nm = r["인허가"].split(" (")[0].split(" / ")[0]
        lab = f"{r['번호']}. {nm[:16]}" + (" (완료)" if done else "") + (f"  {r['법정 검토 (일)']}일" if r["법정 검토 (일)"] != "-" else "  (법정 기간 없음)")
        ax.annotate(lab, (r["_s"], y), xytext=(-6, 0), textcoords="offset points", ha="right", va="center", fontsize=8.6,
                    color="#475569" if done else "#0f172a")
    import pandas as _pd
    span = max(b[3] - b[0], _pd.Timedelta(days=60))
    lo = min(b[0], sd["_s"].min()) - span * 0.32
    hi = max(b[3] + span * 0.12, sd["_e"].max() + _pd.Timedelta(days=10))
    ax.set_xlim(lo, hi)
    ax.set_ylim(-n + 0.4, 1.9)
    ax.set_yticks([])
    ax.xaxis.set_major_formatter(_md.DateFormatter("%y.%m"))
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    fig.tight_layout()
    buf = _fio.BytesIO()
    fig.savefig(buf, format="png", dpi=130)
    _fplt.close(fig)
    return buf.getvalue()


_sc_raw = analyze_scope()
sc_df = apply_delivery(_sc_raw, sc_tk)
sc_df.attrs["turnkey"] = sc_tk
sc_df.attrs["near"] = _sc_raw.attrs.get("near", {})
n_f = (sc_df["판정"] == "● 필수").sum()
n_p = (sc_df["판정"] == "◐ 해당 가능").sum()
st.markdown(f"#### 2. 분석 결과 — 필수 **{n_f}건** · 해당 가능 **{n_p}건** · 해당 없음 {len(sc_df) - n_f - n_p}건")
# [2026-10-20] 판정 기준 간단 설명 (색 = 로드맵 막대 색)
st.markdown(
    "<div style='background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:9px 14px;margin:2px 0 10px;"
    "font-size:0.9rem;color:#0f172a;line-height:1.75'>"
    "<b>판정 기준</b><br>"
    "<span style='color:#1d4ed8;font-weight:800'>● 필수</span> — 입력값이 법령 기준(규모·대상)을 넘음 → 반드시 이행<br>"
    "<span style='color:#d97706;font-weight:800'>◐ 해당 가능</span> — 대상 유형에는 들어가나 입력값만으로 규모 기준을 확정할 수 없음 "
    "→ 시행령 별표 기준 · 관계기관 사전협의로 확인 (사용량 · 준설량 · 하역능력 등을 넣으면 필수 / 해당 없음으로 바뀜)<br>"
    "<span style='color:#64748b;font-weight:800'>○ 해당 없음</span> — 대상 유형이 아니거나 규모 기준 미만"
    "</div>", unsafe_allow_html=True)
show_cols = ["번호", "인허가", "판정", "판정 사유", "협의·허가기관", "법정 기간", "시기", "수행 주체"]
if sc_tk:
    st.info("🏗️ **턴키 · 기술제안 발주** — ① 발주처의 기초조사·기본계획 용역에서 환경영향평가·해양이용영향평가·재해영향평가 등 "
            "계획 단계 인허가를 이행하고, ② 입찰 기본설계 단계는 인허가를 수행하지 않으며 (기 협의 결과 반영·실시설계 인허가 계획 수립), "
            "③ 낙찰자가 실시설계 단계에서 공유수면 점용·사용, 해상교통안전진단, 에너지사용계획, 지하안전평가, 설계안전성 검토 등 시행 인허가를 "
            "수행합니다. (건설기술 진흥법 시행령 제69~71조 · 일괄입찰 등 집행기준 — 발주처 입찰안내서로 최종 확인)")
only = st.checkbox("해당 없음 항목 숨기기", value=True, key="scope_hide")
view = sc_df[sc_df["판정"] != "○ 해당 없음"] if only else sc_df
st.markdown(kit_table(view[show_cols], wrap=True), unsafe_allow_html=True)
if sc_df.attrs.get("near"):
    _nn = sc_df.attrs["near"]
    _nm_ = dict(zip(sc_df["번호"], sc_df["인허가"]))
    st.warning("⚠ **기준 근접** (기준값의 90 % 이상 · 미만) — 설계 변경으로 규모가 조금만 늘어도 대상이 될 수 있습니다.\n\n" +
               "\n".join(f"- {n}. {_nm_.get(n, '')} : " + ", ".join(v) for n, v in sorted(_nn.items())))
with st.expander("📏 판정 기준표 (판정에 쓰는 기준값 · 근거 · 확인 상태)"):
    st.caption("판정은 이 표의 값만 씁니다. 확인 : **조문 ✔** = 현행 조문 확인 / **별표 ※** = 별표 수치 (해양&항만 설계ENG 행정규칙집 수록값, "
               "별표 원문 확인 필요) / **종전 ※** = 종전 해양환경관리법 · 해사안전법 기준 (신법 별표 원문 확인 필요)")
    st.markdown(kit_table(scope_th_df(), wrap=True), unsafe_allow_html=True)
    st.markdown("**판정에 아직 넣지 않은 것 (원문 확인 필요)**")
    st.markdown(kit_table(pd.DataFrame(SCOPE_TODO, columns=["번호", "확인할 것", "지금 처리"]), wrap=True), unsafe_allow_html=True)
_rm = scope_roadmap_png(sc_df)
st.image(_rm, caption="인허가 로드맵 (사업 단계별 배치, 상세 절차는 아래 가이드의 '6. 절차' 흐름도 참조)", use_container_width=True)
st.caption("※ 판정은 입력값에 따른 1차 검토 결과입니다. '해당 가능' 항목은 각 시행령 별표의 규모 기준과 관계기관 사전협의로 최종 확인하십시오. "
           "기준일 : 2026.10 (해양이용영향평가법 2026.9.18 시행, 해상교통안전법, 기후에너지환경부 개편 반영).")
_lk_rows = scope_links_rows(sc_df)
with st.expander(f"🔗 판정된 인허가 {len(_lk_rows)}건 — 근거 조문 · 협의 시기 · 법제처 바로가기"):
    st.caption("근거 위치 · 시기는 아래 '상세 가이드' 의 대상범위 표와 같은 내용입니다 (✔ 현행 조문 확인 / ※ 별표 · 고시 원문 확인 필요). "
               "바로가기는 법제처 국가법령정보센터 검색 화면으로 열립니다. 제출서류는 각 법령 시행규칙 [별지 서식] 에서 확인하십시오.")
    st.markdown(scope_links_html(_lk_rows), unsafe_allow_html=True)
with st.expander("📅 인허가 일정표 (법정 검토 기간 기준)"):
    st.caption("단계 기간은 입력하신 가정값이고, 막대 길이는 각 인허가의 '법정 기간' (협의 · 검토 일수) 입니다. "
               "평가서 작성 · 현지조사 · 주민의견 수렴 같은 준비 기간은 사업마다 달라 넣지 않았습니다 — 그만큼 더 앞당겨 시작해야 합니다. "
               "계획 · 기본 · 실시설계 단계 인허가는 그 단계가 끝나기 전에 협의를 마치도록, 착공 전 인허가는 실시설계가 끝난 뒤에 배치했습니다.")
    _q1, _q2, _q3, _q4 = st.columns(4)
    _sch_start = _q1.date_input("착수일", value=datetime.now().date(), key="sc_sch_start")
    _sch_p = _q2.number_input("계획 단계 (개월)", value=6 if (sc_stage.startswith("상위계획") or sc_tk) else 0, min_value=0, max_value=60, step=1, key=f"sc_sch_p_{int(sc_stage.startswith('상위계획') or sc_tk)}",
                              help="상위계획 · 턴키 기초조사 단계가 없으면 0")
    _sch_b = _q3.number_input("기본설계 (개월)", value=8, min_value=0, max_value=60, step=1, key="sc_sch_b")
    _sch_d = _q4.number_input("실시설계 (개월)", value=10, min_value=0, max_value=60, step=1, key="sc_sch_d")
    _cands = [f"{int(n)}. {nm}" for n, nm, m in zip(sc_df["번호"], sc_df["인허가"], sc_df["판정"]) if m != "○ 해당 없음"]
    _done_sel = st.multiselect("이미 받은(완료) 인허가", _cands, default=[], key="sc_sch_done", help="고르면 회색 '완료' 로 표시")
    _done = {int(x.split(".")[0]) for x in _done_sel}
    sc_sch, _sch_b_ = scope_schedule(sc_df, _sch_start, _sch_p, _sch_b, _sch_d, _done)
    sc_sch.attrs["tk"] = sc_tk
    if len(sc_sch):
        st.image(scope_gantt_png(sc_sch, _sch_b_, f"인허가 일정표 — {sc_name}"), use_container_width=True)
        _left = sc_sch[~sc_sch["상태"].str.startswith("완료")]
        if len(_left):
            _first = _left.sort_values("_s").iloc[0]
            st.info(f"가장 먼저 협의를 요청해야 하는 것 : **{_first['번호']}. {_first['인허가']}** — 늦어도 {_first['협의 요청 늦어도']} 요청 "
                    f"(법정 검토 {_first['법정 검토 (일)']}일, 준비 기간 별도)" + (f" · {_first['비고']}" if _first["비고"] else ""))
        st.markdown(kit_table(sc_sch[["번호", "인허가", "판정", "단계", "법정 검토 (일)", "협의 요청 늦어도", "협의 완료 목표", "상태", "비고"]], wrap=True),
                    unsafe_allow_html=True)
    else:
        st.caption("해당 인허가가 없습니다.")
def _sc_xl_bytes():   # [2026-11-16] 누를 때 만듦
    _xb = BytesIO()
    with pd.ExcelWriter(_xb, engine="openpyxl") as _w:
        pd.DataFrame([{"항목": k, "값": v} for k, v in [("사업명", sc_name), ("지역", sc_region), ("항만 구분", sc_port), ("사업 단계", sc_stage), ("발주 방식", sc_order[2:].strip()),
                                                         ("사업 주체", sc_owner), ("공사 위치", sc_loc), ("총공사비(억원)", sc_cost), ("사업면적(m²)", sc_area),
                                                         ("최대 굴착깊이(m)", sc_exc), ("용도지역", sc_zone), ("준설 면적(m²)", sc_dred_a),
                                                         ("공유수면 점용·사용 면적(m²)", sc_occ), ("수심 4m 미만", "예" if sc_shallow else "아니오"),
                                                         ("변경·증설 사업", "예" if sc_chg else "아니오")] + ([("기 협의 사업면적(m²)", sc_area0), ("기 협의 외곽 길이(m)", sc_outer0),
                                                         ("5년 이내 미착공", "예" if sc_5y else "아니오"), ("7년 이상 공사중지 후 재개", "예" if sc_7y else "아니오")] if sc_chg else [])
                                                        + [("기준일", "2026.11")]]).to_excel(_w, sheet_name="사업개요", index=False)
        sc_fac[sc_fac["선택"]].to_excel(_w, sheet_name="설계대상시설", index=False)
        sc_df[show_cols].to_excel(_w, sheet_name="인허가판정", index=False)
        scope_th_df().to_excel(_w, sheet_name="판정기준표", index=False)
        pd.DataFrame([{k: v for k, v in r.items() if k not in ("법령", "바로가기")} | {"법제처 바로가기": " / ".join(u for _n, u in r["바로가기"])}
                      for r in _lk_rows]).to_excel(_w, sheet_name="근거·바로가기", index=False)
        if len(sc_sch):
            sc_sch[["번호", "인허가", "판정", "단계", "법정 검토 (일)", "협의 요청 늦어도", "협의 완료 목표", "상태", "비고"]].to_excel(_w, sheet_name="인허가일정", index=False)
    return _xb.getvalue()

st.download_button("💾 인허가 분석 결과 Excel 다운로드", data=_sc_xl_bytes, file_name=f"인허가분석_{sc_name}.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# =====================================================================
# ★ 하단: 설계 시행 주요 인허가 상세 가이드 (화면 UI)
# =====================================================================
st.markdown("---")
st.header("📖 설계 시행 주요 인허가 상세 가이드")
st.markdown("각 항목을 클릭하여 세부 검토 내용을 확인하세요. 괄호 안의 법령명을 클릭하시면 법제처에서 해당 법령을 즉시 조회하실 수 있습니다.")

with st.expander("1. 전략환경영향평가"):
    st.info("""
    * **1. 개요**: 환경에 영향을 미치는 계획을 수립할 때 환경보전계획과의 부합 여부를 확인하고, 대안의 설정 및 분석을 통해 환경적 측면에서 계획의 적정성과 입지의 타당성을 사전에 검토하는 제도입니다.
    * **2. 실시근거**: 환경영향평가법 제9조, 동법 시행령 제7조제2항 및 제22조제2항에 근거합니다.
    * **3. 대상계획 및 협의시기**: 
      * 내용: 도시 개발, 항만 건설, 도로 건설 등 정책/개발기본계획. 계획수립자가 관계기관의 장과 협의할 때 실시합니다.
      * 👉 근거법령: ([환경영향평가법](https://www.law.go.kr/lsSc.do?menuId=1&query=환경영향평가법)) 시행령 [별표 2] 대상계획
    * **4. 협의기관**: 기후에너지환경부장관 또는 지방(유역)환경청장 (평가주체: 행정기관의 장)
    * **5. 평가항목**: 환경보전계획 부합성, 계획 연계성, 입지 타당성 등. 한국환경정책평가연구원 검토.
    """)
    show_scope(1)
    with st.expander("6. 절차 및 양식 보기 (상세 흐름도 포함)"):
        show_flows(1, has_old=True)
        st.markdown("환경평가협의회 심의(30일) ➔ 스코핑 ➔ 주민의견 청취 ➔ 평가서 작성 및 협의.")
        st.markdown("👉 법정양식: ([환경영향평가법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=환경영향평가법+시행규칙)) [별지 서식]")
        if Path("전략환경영향평가 절차-개발기본계획.png").exists():
            _old_img("전략환경영향평가 절차-개발기본계획.png", caption="전략환경영향평가 절차 (개발기본계획)", width=750)
        if Path("전략환경영향평가 절차-정책계획.png").exists():
            _old_img("전략환경영향평가 절차-정책계획.png", caption="전략환경영향평가 절차 (정책계획)", width=750)

with st.expander("2. 환경영향평가"):
    st.info("""
    * **1. 개요**: 특정 계획이나 사업이 환경에 미치는 영향을 미리 예측·평가하여 환경보전방안을 마련함으로써 친환경적이고 지속가능한 발전을 도모합니다.
    * **2. 실시근거**: 환경영향평가법 제22조 및 동법 시행령 제31조에 따릅니다.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 항만 건설, 수자원 개발 등 17개 분야 78개 세부사업. 
      * 👉 근거법령: ([환경영향평가법](https://www.law.go.kr/lsSc.do?menuId=1&query=환경영향평가법)) 시행령 [별표 3] 대상사업
    * **4. 협의기관**: 기후에너지환경부장관 또는 지방환경청장 (대상사업을 하려는 자가 주체)
    * **5. 평가항목**: 동·식물상, 수질, 해양, 지형·지질, 소음·진동 등 총 21개 항목.
    """)
    show_scope(2)
    with st.expander("6. 절차 및 양식 보기 (환경영향평가 흐름도 포함)"):
        show_flows(2, has_old=True)
        st.markdown("평가서 초안 작성 ➔ 주민의견 수렴 ➔ 협의 요청 ➔ KEI 검토 ➔ 협의내용 통보.")
        st.markdown("👉 법정양식: ([환경영향평가법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=환경영향평가법+시행규칙)) [별지 서식]")
        if Path("환경영향평가 절차.png").exists():
            _old_img("환경영향평가 절차.png", caption="환경영향평가 절차 흐름도", width=750)

with st.expander("3. 소규모 환경영향평가 및 사후환경영향조사"):
    st.info("""
    * **1. 개요**: 보전이 필요한 지역 및 난개발 우려 지역 개발 시 소규모 평가 실시, 사업 착공 후에는 사후환경영향조사를 통해 환경 영향을 관리합니다.
    * **2. 실시근거**: 환경영향평가법 제36조(사후), 제43조(소규모).
    * **3. 대상사업 및 협의시기**: 
      * 내용: 보전관리지역 등 9개 분야 20개 소규모 개발사업, 또는 협의가 완료된 환경영향평가 대상사업(사후조사).
      * 👉 소규모 대상: ([환경영향평가법](https://www.law.go.kr/lsSc.do?menuId=1&query=환경영향평가법)) 시행령 [별표 4]  
      * 👉 사후조사 대상: ([환경영향평가법](https://www.law.go.kr/lsSc.do?menuId=1&query=환경영향평가법)) 시행규칙 [별표 1]
    * **4. 협의기관**: 관할 지방(유역)환경청장.
    * **5. 평가항목**: 자연생태환경, 수질 등 17개 항목(소규모) 및 사후 관리 계획 항목.
    """)
    show_scope(3)
    with st.expander("6. 절차 및 양식 보기 (소규모 환경영향평가 및 사후조사 흐름도 포함)"):
        show_flows(3, has_old=True)
        st.markdown("착공 후 정기 조사 ➔ 조사결과 및 조치결과 통보서 제출.")
        st.markdown("👉 법정양식: ([환경영향평가법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=환경영향평가법+시행규칙)) [별지 서식]")
        if Path("소규모 환경영향평가 절차.png").exists():
            _old_img("소규모 환경영향평가 절차.png", caption="소규모 환경영향평가 절차 흐름도", width=750)
        if Path("사후환경영향평가 절차.png").exists():
            _old_img("사후환경영향평가 절차.png", caption="사후환경영향조사 절차 흐름도", width=750)

with st.expander("4. 기후영향평가"):
    st.info("""
    * **1. 개요**: 국가 온실가스 감축 목표 달성에 기여하기 위해 주요 계획과 개발사업이 기후변화에 미치는 영향을 사전에 평가하고 저감 방안을 수립합니다.
    * **2. 실시근거**: 기후위기 대응을 위한 탄소중립·녹색성장 기본법 제23조 및 동법 시행령 (전략환경영향평가·환경영향평가에 포함하여 실시, 협의 요청 시 함께 요청).
    * **3. 대상사업 및 협의시기**: 전략환경영향평가 또는 환경영향평가 협의 요청 시 포함하여 실시.
      * 내용: **에너지 개발, 도시 개발, 산업입지 및 산업단지 조성, 항만 건설, 수자원 개발 등** 온실가스 다배출 및 기후변화 취약성이 높은 10개 분야 주요 행정계획 및 대규모 개발사업
      * 👉 대상범위 상세: ([탄소중립기본법 시행령](https://www.law.go.kr/lsSc.do?menuId=1&query=기후위기+대응을+위한+탄소중립·녹색성장+기본법+시행령)) 기후변화영향평가 대상 / 「기후변화영향평가 방법 등에 관한 규정」(고시)
    * **4. 협의기관**: 기후에너지환경부장관.
    * **5. 평가항목**: 온실가스 배출량 산정, 기후변화 적응 및 취약성 평가.
    """)
    show_scope(4)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(4, has_old=False)
        st.markdown("영향평가 대상 확인 ➔ 기후변화 영향 예측 및 저감계획 수립 ➔ 협의 완료.")
        st.markdown("👉 법정양식: ([환경영향평가법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=환경영향평가법+시행규칙))")

with st.expander("5. 일반 및 간이 해양 이용협의 및 해양 이용영향평가"):
    st.markdown("""
    * **1. 개요**: 해양 개발 행위의 적정성과 예상되는 해양환경 영향을 사전에 검토 및 평가하는 예방적 정책 수단입니다.
    * **2. 실시근거**: 해양이용영향평가법 제9조(일반 해양이용협의)·제13조(해양이용영향평가) — **2026.9.18 시행** (종전 해양환경관리법 제84·85조 대체).
    * **3. 대상사업 및 협의시기**: 
      * 내용: 공유수면 점용·사용 및 매립, 항만 건설 등. 행정계획 확정 이후 실시계획 승인 전.
      * 👉 대상: ([해양이용영향평가법](https://www.law.go.kr/lsSc.do?menuId=1&query=해양이용영향평가법)) 시행령 [별표 1] (종전 해양환경관리법 시행령 별표 15·16은 삭제)  
    * **4. 협의기관**: 해양수산부장관 (지방해양수산청 위임), 해양이용영향검토기관 검토 — 협의의견 통보: 일반 해양이용협의 30일, 해양이용영향평가 45일
    * **5. 평가항목**: 해양물리, 해양화학, 생태계, 수산자원 등 9~14개 항목.
    
    ---
    ### 📊 일반 해양 이용협의 vs 간이 해양 이용협의 비교
    """)
    
    comparison_df = pd.DataFrame({
        "구분": ["대상 규모", "환경 영향", "조사 항목", "소요 기간", "비용 (수수료)"],
        "간이 해양 이용협의": [
            "소규모 사업, 점·사용 면적이 상대적으로 작은 경우",
            "해양 환경에 미치는 영향이 경미할 것으로 예상되는 사업",
            "필수 항목 위주의 비교적 간소화된 해양 조사",
            "상대적으로 짧음 (수주 ~ 수개월)",
            "합리적인 수준"
        ],
        "일반 해양 이용협의": [
            "일정 규모 이상의 대규모 사업, 면적이 넓은 경우",
            "해양 환경 및 생태계에 상당한 영향을 미칠 우려가 있는 사업",
            "수질, 저질, 동식물 플랑크톤, 저서생물 등 광범위하고 정밀한 조사",
            "4계절 조사가 필요할 수도 있어 매우 김 (수개월 ~ 1년 이상)",
            "조사 항목에 비례하여 비용 단가 가중"
        ]
    })
    st.table(comparison_df)
    
    show_scope(5)
    with st.expander("6. 절차 및 양식 보기 (해양 이용협의 및 영향평가 절차 흐름도 포함)"):
        show_flows(5, has_old=True)
        st.markdown("협의서 작성 ➔ 제출 ➔ 검토기관 심사 ➔ 통보.")
        st.markdown("👉 법정양식: ([해양이용영향평가법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=해양이용영향평가법+시행규칙)) [별지 서식]")
        if Path("일반 및 간이해양이용협의 절차.png").exists():
            _old_img("일반 및 간이해양이용협의 절차.png", caption="일반 및 간이 해양 이용협의 절차", width=750)
        if Path("해양이용영향평가 절차.png").exists():
            _old_img("해양이용영향평가 절차.png", caption="해양 이용영향평가 절차", width=750)
        if Path("해양이용협의 절차도.png").exists():
            _old_img("해양이용협의 절차도.png", caption="해양 이용협의 절차도", width=750)

with st.expander("6. 해양환경영향조사"):
    st.info("""
    * **1. 개요**: 해양 이용협의 또는 해양 이용영향평가 처분 이후 실제 사업 시행 중 발생하는 해양환경 영향을 지속해서 조사합니다.
    * **2. 실시근거**: 해양이용영향평가법 제29조 (종전 해양환경관리법 제95조).
    * **3. 대상사업 및 협의시기**: 
      * 내용: 해양 이용협의 및 해양 이용영향평가 대상사업 일체.
      * 👉 대상·항목·기간: ([해양이용영향평가법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=해양이용영향평가법+시행규칙)) (해양수산부령)
    * **4. 협의기관**: 해양수산부장관 또는 지방해양수산청장.
    * **5. 평가항목**: 해양환경기준이 정하여진 수질, 퇴적물 항목 등.
    """)
    show_scope(6)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(6, has_old=False)
        st.markdown("정기 조사 실시 ➔ 해양환경영향조사 결과 통보.")
        st.markdown("👉 법정양식: ([해양이용영향평가법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=해양이용영향평가법+시행규칙)) [별지 서식]")

with st.expander("7. 해양공간적합성협의"):
    st.info("""
    * **1. 개요**: 해양이용·개발계획 수립 및 구역 지정 시 해양공간계획과의 부합 여부, 입지 적정성 등을 사전에 협의합니다.
    * **2. 실시근거**: 해양공간계획 및 관리에 관한 법률 제15조.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 해양관광단지, 항만·어항, 수자원 등 25개 법률의 48개 계획.
      * 👉 대상범위: ([해양공간계획 및 관리에 관한 법률](https://www.law.go.kr/lsSc.do?menuId=1&query=해양공간계획)) 시행령 [별표 2]
    * **4. 협의기관**: 해양수산부장관.
    * **5. 평가항목**: 해양공간계획 정책방향 부합성, 입지 적절성, 지속가능성.
    """)
    show_scope(7)
    with st.expander("6. 절차 및 양식 보기 (해양공간적합성협의 흐름도 포함)"):
        show_flows(7, has_old=True)
        st.markdown("협의 요청 ➔ 적합성 검토(45일) ➔ 동의/부동의 결정 및 통보.")
        st.markdown("👉 법정양식: ([해양공간계획 및 관리에 관한 법률 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=해양공간계획+시행규칙)) [별지 서식]")
        if Path("해양공간접합성협의 절차.png").exists():
            _old_img("해양공간접합성협의 절차.png", caption="해양공간적합성협의 절차 흐름도", width=750)
        if Path("해양공간접합성협의 절차- 요청.png").exists():
            _old_img("해양공간접합성협의 절차- 요청.png", caption="해양공간적합성협의 요청 절차 흐름도", width=750)

with st.expander("8. 공유수면 점용·사용허가 및 매립"):
    st.info("""
    * **1. 개요**: 공유수면을 독점적으로 사용(점용)하거나 토석을 채워 토지(매립)를 조성하기 위한 권리를 설정받는 제도입니다.
    * **2. 실시근거**: 공유수면 관리 및 매립에 관한 법률 제8조(점용·사용), 제28조(매립면허).
    * **3. 대상사업 및 협의시기**: 
      * 내용: 인공구조물 설치 등 11개 점용행위 및 매립목적 달성.
      * 👉 매립목적: ([공유수면 관리 및 매립에 관한 법률](https://www.law.go.kr/lsSc.do?menuId=1&query=공유수면관리및매립에관한법률)) 시행령 [별표 2]
    * **4. 협의기관**: 해양수산부장관, 지방해양수산청장 또는 관할 지자체.
    * **5. 평가항목**: 사업계획서, 구적도, 설계도서, 환경영향평가서 등 적정성 검토.
    """)
    show_scope(8)
    with st.expander("6. 절차 및 양식 보기 (공유수면매립 및 점용허가 흐름도 포함)"):
        show_flows(8, has_old=True)
        st.markdown("신청서 제출 ➔ 타당성 검토 ➔ 허가 ➔ 고시.")
        st.markdown("👉 법정양식: ([공유수면 관리 및 매립에 관한 법률 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=공유수면관리및매립에관한법률+시행규칙)) [별지 서식]")
        
        for img_name, cap in [
            ("공유수면매립 기본계획수립.png", "공유수면매립 기본계획수립 절차"),
            ("공유수면매립 절차.png", "공유수면매립 절차 상세"),
            ("공유수면매립 흐름도.png", "공유수면매립 흐름도"),
            ("공유수면매립 점용･사용허가 절차.png", "공유수면 점용·사용허가 절차 1"),
            ("공유수면매립 점용･사용허가 절차-2.png", "공유수면 점용·사용허가 절차 2"),
            ("공유수면매립 점용･사용허가 절차-3.png", "공유수면 점용·사용허가 절차 3")
        ]:
            if Path(img_name).exists():
                _old_img(img_name, caption=cap, width=750)

with st.expander("9. 재해영향평가 및 재해영향성검토 (소규모 포함)"):
    st.info("""
    * **1. 개요**: 개발 사업의 허가나 행정계획 수립 초기에 자연재해에 미치는 영향을 미리 평가하여 재해를 예방하는 제도입니다.
    * **2. 실시근거**: 자연재해대책법 제4조 및 시행령 제6조.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 48개 법령에 따른 59개 개발사업.
      * 👉 대상범위: ([자연재해대책법](https://www.law.go.kr/lsSc.do?menuId=1&query=자연재해대책법)) 시행령 [별표 1]
    * **4. 협의기관**: 행정안전부장관, 시·도지사, 시장·군수·구청장 (사전검토: 국립재난안전연구원).
    * **5. 평가항목**: 배수처리계획도, 침수흔적도 검토 및 재해영향 예측·저감대책.
    """)
    show_scope(9)
    with st.expander("6. 절차 및 양식 보기 (재해영향평가/검토 흐름도 포함)"):
        show_flows(9, has_old=True)
        st.markdown("사전검토 요청(14일) ➔ 심의 ➔ 결과 통보(30~45일) ➔ 설계 반영.")
        st.markdown("👉 법정양식: ([자연재해대책법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=자연재해대책법+시행규칙)) [별지 서식]")
        if Path("재해영향성 검토 절차.jpg").exists():
            _old_img("재해영향성 검토 절차.jpg", caption="재해영향성 검토 절차 흐름도", width=750)
        if Path("재해영향평가 절차.jpg").exists():
            _old_img("재해영향평가 절차.jpg", caption="재해영향평가 절차 흐름도", width=750)

with st.expander("10. 교통영향평가"):
    st.info("""
    * **1. 개요**: 사업 시행 시 발생하는 교통량과 교통흐름의 변화를 예측하여 교통안전 문제점을 최소화할 대책을 마련합니다.
    * **2. 실시근거**: 도시교통정비 촉진법 제15조 및 시행령 제13조의2.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 항만, 공항, 도로 건설 등 11개 분야 29개 개발사업.
      * 👉 대상범위: ([도시교통정비 촉진법](https://www.law.go.kr/lsSc.do?menuId=1&query=도시교통정비촉진법)) 시행령 [별표 1]
    * **4. 협의기관**: 국토교통부장관 또는 관할 시·도지사.
    * **5. 평가항목**: 장래 교통수요 예측, 문제점 분석, 교통개선대책안 및 공사 중 교통처리대책.
    """)
    show_scope(10)
    with st.expander("6. 절차 및 양식 보기 (교통영향평가 흐름도 포함)"):
        show_flows(10, has_old=True)
        st.markdown("평가서 제출 ➔ 심의위원회 심의 ➔ 개선사항 통보 ➔ 사업계획 반영.")
        st.markdown("👉 법정양식: ([도시교통정비 촉진법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=도시교통정비촉진법+시행규칙)) [별지 서식]")
        if Path("교통영향평가 절차.png").exists():
            _old_img("교통영향평가 절차.png", caption="교통영향평가 절차 흐름도", width=750)

with st.expander("11. 도시계획시설결정"):
    st.info("""
    * **1. 개요**: 도로, 항만, 철도 등 기반시설을 도시관리계획으로 결정하여 설치하기 위한 행정 절차입니다.
    * **2. 실시근거**: 국토의 계획 및 이용에 관한 법률 제43조.
    * **3. 대상사업 및 협의시기**: 도시관리계획 입안 및 결정 고시 전.
      * 내용: **7대 기반시설**(교통·공간·유통공급·공공문화체육·방재·보건위생·환경기초시설)의 신설, 변경, 정비 (예: 항만, 도로, 철도, 공원, 하수도 등)
      * 👉 대상범위 상세: ([국토의 계획 및 이용에 관한 법률 시행령](https://www.law.go.kr/lsSc.do?menuId=1&query=국토의계획및이용에관한법률+시행령)) 제2조
    * **4. 협의기관**: 국토교통부, 관할 시·도지사, 시장·군수.
    * **5. 평가항목**: 시설의 종류, 명칭, 위치, 규모 등 도시계획 측면의 적합성.
    """)
    show_scope(11)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(11, has_old=False)
        st.markdown("입안 ➔ 주민/의회 의견청취 ➔ 관계기관 협의 ➔ 고시.")
        st.markdown("👉 법정양식: ([국토의 계획 및 이용에 관한 법률 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=국토의계획및이용에관한법률+시행규칙))")

with st.expander("12. 에너지사용계획 협의"):
    st.info("""
    * **1. 개요**: 대규모 도시개발 및 산업단지 조성 시 에너지 수요 예측 및 고효율 사용 방안을 사전에 수립합니다.
    * **2. 실시근거**: 에너지이용 합리화법 제8조.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 대규모 민간/공공 개발사업 및 시설.
      * 👉 대상범위: ([에너지이용 합리화법](https://www.law.go.kr/lsSc.do?menuId=1&query=에너지이용합리화법)) 시행령 [별표 1]
    * **4. 협의기관**: 기후에너지환경부 (한국에너지공단 검토) — 결과 통보 30일 (20일 범위 연장).
    * **5. 평가항목**: 에너지 수요 예측, 공급계획, 신재생에너지 보급 계획, 이용 효율 향상 방안.
    """)
    show_scope(12)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(12, has_old=False)
        st.markdown("계획서 작성 ➔ 공단 평가 ➔ 협의 결과 통보.")
        st.markdown("👉 법정양식: ([에너지이용 합리화법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=에너지이용합리화법+시행규칙)) [별지 서식]")

with st.expander("13. 지하안전평가"):
    st.info("""
    * **1. 개요**: 대규모 굴착 공사(10m 이상) 진행 시 지반침하 등을 예방하기 위해 인허가 전 지하안전 영향을 평가합니다.
    * **2. 실시근거**: 지하안전관리에 관한 특별법 제14조, 제23조.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 굴착 깊이 10m~20m(소규모), 20m 이상(일반).
      * 👉 대상범위: ([지하안전관리에 관한 특별법](https://www.law.go.kr/lsSc.do?menuId=1&query=지하안전관리에관한특별법)) 시행령 [별표 1]
    * **4. 협의기관**: 국토교통부 (지방국토관리청 위임, 국토안전관리원 등 위탁) — 협의 30일 (연장 시 50일).
    * **5. 평가항목**: 지반/지질 현황, 지하수 변화, 지반 침하 위험도 예측 및 안전 대책.
    """)
    show_scope(13)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(13, has_old=False)
        st.markdown("평가서 제출 ➔ 전문기관 검토 ➔ 협의 내용 이행.")
        st.markdown("👉 법정양식: ([지하안전관리에 관한 특별법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=지하안전관리에관한특별법+시행규칙)) [별지 서식]")

with st.expander("14. 설계안전성검토(DFS) 및 안전관리계획 수립"):
    st.info("""
    * **1. 개요**: 설계 단계부터 시공 위험요소를 저감(DFS)하고, 착공 전 건설재해 예방을 위한 안전관리계획을 수립합니다.
    * **2. 실시근거**: 건설기술 진흥법 제62조.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 1종 및 2종 시설물, 지하 10m 이상 굴착 등 안전관리계획 수립 대상 공사.
      * 👉 대상범위: ([건설기술 진흥법](https://www.law.go.kr/lsSc.do?menuId=1&query=건설기술진흥법)) 시행령 [별표 8]
    * **4. 협의기관**: 발주청, 국토안전관리원.
    * **5. 평가항목**: 시공 절차 및 주의사항, 위험요소 저감 대책, 추락·붕괴 방지 대책.
    """)
    show_scope(14)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(14, has_old=False)
        st.markdown("계획서 작성 ➔ 발주청 및 관리원 검토 ➔ 적정 통보.")
        st.markdown("👉 법정양식: ([건설기술 진흥법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=건설기술진흥법+시행규칙)) [별지 서식]")

with st.expander("15. 유해·위험방지계획서"):
    st.info("""
    * **1. 개요**: 건설공사 착공 전 재해 유발 위험이 높은 특수 공종의 안전 대책을 수립하여 제출하고 심사받습니다.
    * **2. 실시근거**: 산업안전보건법 제42조.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 지상 31m 이상, 최대지간 50m 이상 교량, 10m 이상 굴착 등.
      * 👉 대상범위: ([산업안전보건법](https://www.law.go.kr/lsSc.do?menuId=1&query=산업안전보건법)) 시행규칙 제42조
    * **4. 협의기관**: 고용노동부 (한국산업안전보건공단 심사).
    * **5. 평가항목**: 공사개요, 안전보건관리계획, 작업공종별 유해·위험방지계획 등.
    """)
    show_scope(15)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(15, has_old=False)
        st.markdown("계획서 제출 ➔ 공단 심사 ➔ 적정 여부 통보 ➔ 확인.")
        st.markdown("👉 법정양식: ([산업안전보건법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=산업안전보건법+시행규칙)) [별지 서식]")

with st.expander("16. 해상교통안전진단"):
    st.info("""
    * **1. 개요**: 해상교통안전에 영향을 미칠 수 있는 항만 개발, 해상 교량 건설 등의 사업을 추진할 때 선박 통항의 안전성을 사전에 진단합니다.
    * **2. 실시근거**: 해상교통안전법 제13~17조 (2024.7.26 시행, 종전 해사안전법).
    * **3. 대상사업 및 협의시기**: 
      * 내용: 수역의 설정/변경, 해상수역 시설물 건설 등.
      * 👉 대상범위: ([해상교통안전법](https://www.law.go.kr/lsSc.do?menuId=1&query=해상교통안전법)) 제2조·제13조 및 시행령
    * **4. 협의기관**: 해양수산부 (지방해양수산청).
    * **5. 평가항목**: 해상교통현황 조사, 통항 안전성 시뮬레이션, 안전대책 수립.  
      👉 평가기준: ([해상교통안전법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=해상교통안전법+시행규칙)) 해상교통안전진단기준
    """)
    show_scope(16)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(16, has_old=False)
        st.markdown("진단서 제출 ➔ 해상교통안전진단 심사위원회 심의 ➔ 결과 통보.")
        st.markdown("👉 법정양식: ([해상교통안전법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=해상교통안전법+시행규칙)) [별지 서식]")

with st.expander("17. 해상풍력발전 인허가"):
    st.info("""
    * **1. 개요**: 해상풍력 발전사업 추진을 위한 발전사업 허가, 공유수면 점·사용, 환경영향평가 등 종합 인허가 절차입니다.
    * **2. 실시근거**: 해상풍력 보급 촉진 및 산업 육성에 관한 특별법 (약칭: 해상풍력법).
    * **3. 대상사업 및 협의시기**: 
      * 내용: 예비지구 지정, 발전지구 지정 및 해상풍력 발전사업 실시계획 승인 전.
      * 👉 근거법령: ([해상풍력 보급 촉진 및 산업 육성에 관한 특별법](https://www.law.go.kr/lsSc.do?menuId=1&query=해상풍력보급촉진및산업육성에관한특별법))
    * **4. 협의기관**: 기후에너지환경부, 산업통상자원부, 해양수산부 및 관할 지자체.
    * **5. 평가항목**: 해상교통안전진단, 해양 이용영향평가, 환경영향평가, 어업피해영향조사 등 종합 검토.
    """)
    show_scope(17)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(17, has_old=False)
        st.markdown("예비지구 지정 ➔ 발전지구 지정 ➔ 실시계획 승인.")
        st.markdown("👉 관련 법정 양식 확인")

with st.expander("18. 어업피해영향 조사"):
    st.info("""
    * **1. 개요**: 해양 개발 및 항만 공사 등으로 인해 어업권에 미치는 피해를 조사하고 보상 대책을 수립하기 위한 필수 조사입니다.
    * **2. 실시근거**: 수산업법 및 어업피해 보상 관련 규정.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 공유수면 매립, 항만 건설, 해상풍력 및 준설 등 어업권에 손실을 주는 개발사업.
      * 👉 참고 기관 가이드: [어업피해영향조사 안내 바로가기](https://www.marinelab.co.kr/index.php?cate=003006001)
    * **4. 협의기관**: 관할 지자체 (시·도지사, 시장·군수·구청장) 및 수협 등 어업인 대표.
    * **5. 평가항목**: 공사 시행으로 인한 수산자원 감소, 양식장 피해 범위 산정 및 보상액 산출.
    """)
    show_scope(18)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(18, has_old=False)
        st.markdown("어업피해조사 실시계획 승인 ➔ 피해 영향 조사 용역 시행 ➔ 보상 협의 및 재결.")
        st.markdown("👉 법정양식: ([수산업법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=수산업법+시행규칙)) [별지 서식]")

with st.expander("19. 문화재 지표조사 및 현상변경 허가"):
    st.info("""
    * **1. 개요**: 사업 부지 내 매장유산 유무를 확인(지표조사)하고, 지정 문화재 주변 건설공사 시 문화재 보존에 미치는 영향을 검토합니다.
    * **2. 실시근거**: 매장유산 보호 및 조사에 관한 법률 제6조, 문화유산의 보존 및 활용에 관한 법률.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 사업 면적 3만㎡ 이상 건설공사(지표조사), 역사문화환경 보존지역 내 공사.
      * 👉 대상범위: ([매장유산 보호 및 조사에 관한 법률](https://www.law.go.kr/lsSc.do?menuId=1&query=매장유산보호및조사에관한법률)) 시행령 [별표 1]
    * **4. 협의기관**: 국가유산청, 관할 지자체.
    * **5. 평가항목**: 매장유산의 분포 여부 및 문화재 경관 훼손 여부 등.
    """)
    show_scope(19)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(19, has_old=False)
        st.markdown("조사기관 의뢰 ➔ 결과 보고서 제출 ➔ 보존 조치 또는 발굴조사 전환.")
        st.markdown("👉 법정양식: ([매장유산 보호 및 조사에 관한 법률 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=매장유산보호및조사에관한법률+시행규칙)) [별지 서식]")

with st.expander("20. 수저준설토사 유효활용"):
    st.info("""
    * **1. 개요**: 항만 및 수역 개발 시 발생하는 오염되지 않은 토사를 매립재, 인공 섬 조성 등 자원으로 유효활용하기 위한 절차입니다.
    * **2. 실시근거**: 해양환경관리법 제110조 및 「수저준설토사 유효활용기준」(해양수산부 고시) — ※ 현행 「해양폐기물 및 해양오염퇴적물 관리법」 조문 확인 필요.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 항만 건설 및 항로 유지 준설 공사 등에서 발생한 토사 처리 시.
      * 👉 관련 규정: ([해양환경관리법](https://www.law.go.kr/lsSc.do?menuId=1&query=해양환경관리법)) 시행령 [별표 17]
    * **4. 협의기관**: 해양수산부 (지방해양수산청).
    * **5. 평가항목**: 준설토의 오염도 검사, 성분 분석, 활용 대상지의 적정성.
    """)
    show_scope(20)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(20, has_old=False)
        st.markdown("유효활용 계획서(신고서) 제출 ➔ 타당성 검토 ➔ 승인.")
        st.markdown("👉 법정양식: ([해양환경관리법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=해양환경관리법+시행규칙)) [별지 제46호 서식]")

with st.expander("21. 설계의 경제성(VE) 검토 및 설계자문"):
    st.info("""
    * **1. 개요**: 100억 원 이상 공공 건설사업의 예산 절감, 기능 향상을 위해 설계 대안을 창출(VE)하고 기술적 타당성을 검증(자문)합니다.
    * **2. 실시근거**: 건설기술 진흥법 시행령 제73조.
    * **3. 대상사업 및 협의시기**: 
      * 내용: 총공사비 100억 원 이상인 건설공사의 기본/실시설계.
      * 👉 관련 규정: ([건설기술 진흥법](https://www.law.go.kr/lsSc.do?menuId=1&query=건설기술진흥법)) 시행령 제73조
    * **4. 협의기관**: 발주청 (자체 설계자문위원회 또는 기술심의위원회 구성).
    * **5. 평가항목**: 비용 절감 방안, 기능 및 품질 향상 방안 대안 도출.
    """)
    show_scope(21)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(21, has_old=False)
        st.markdown("VE팀 구성 ➔ 기능 분석 ➔ 제안서 작성 ➔ 발주청 승인.")
        st.markdown("👉 [🔗 국토교통부 고시 (설계의 경제성등 검토에 관한 지침)](https://www.law.go.kr/LSW/admRulInfoPush.do?admRulSeq=2100000228795)")

with st.expander("22. 경관심의 (경관법)"):
    st.info("""
    * **1. 개요**: 지역의 자연경관 및 역사·문화경관을 보전하고 훼손된 경관을 개선·복원하며, 새로운 경관을 창출하기 위해 건축물, 시설물 등의 경관을 사전에 심의하는 제도입니다.
    * **2. 실시근거**: 경관법 제26조(개발사업의 경관심의) 및 제27조(건축물의 경관심의).
    * **3. 대상사업 및 협의시기**: 실시설계 완료 전.
      * 내용: 
        * **[개발사업]** 도시지역 3만㎡ 이상, 비도시지역 30만㎡ 이상
        * **[사회기반시설]** 총사업비 500억 원 이상의 도로·철도, 300억 원 이상의 하천시설사업 (경관법 시행령 제18조)
      * 👉 대상범위 상세: ([경관법 시행령](https://www.law.go.kr/lsSc.do?menuId=1&query=경관법+시행령)) 제18조[별표] 및 제19조
    * **4. 협의기관**: 국토교통부, 관할 지자체 경관위원회.
    * **5. 평가항목**: 경관계획과의 부합 여부, 주변 경관과의 조화, 랜드마크 조성 등.
    """)
    show_scope(22)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(22, has_old=False)
        st.markdown("경관심의 신청 ➔ 경관위원회 심의 ➔ 결과 통보 및 반영.")
        st.markdown("👉 법정양식: ([경관법 시행규칙](https://www.law.go.kr/lsSc.do?menuId=1&query=경관법+시행규칙)) [별지 서식]")

with st.expander("23. 공공디자인 심의 (공공디자인의 진흥에 관한 법률)"):
    st.info("""
    * **1. 개요**: 국가 및 지자체 등 공공기관이 조성·제작·설치하는 공공시설물 등의 안전성, 사용성, 편의성 및 심미성을 높이기 위해 공공디자인 진흥 가이드라인 및 관련 사항을 심의합니다.
    * **2. 실시근거**: 공공디자인의 진흥에 관한 법률 제9조, 제10조 및 각 지자체 공공디자인 조례.
    * **3. 대상사업 및 협의시기**: 기본 및 실시설계 단계.
      * 내용: 공공기관이 조성·제작·설치하는 **대중교통시설물, 보행안전시설물, 편의시설물, 공급시설물, 녹지시설물, 안내시설물 등** (법 제2조제3호)
      * 👉 대상범위 상세: ([공공디자인의 진흥에 관한 법률](https://www.law.go.kr/lsSc.do?menuId=1&query=공공디자인의진흥에관한법률)) 제2조제3호 및 해당 지자체 조례 [별표]
    * **4. 협의기관**: 문화체육관광부, 관할 지자체 공공디자인위원회.
    * **5. 평가항목**: 공공디자인 종합계획 및 가이드라인 준수 여부, 유니버설 디자인 적용 여부 등.
    """)
    show_scope(23)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(23, has_old=False)
        st.markdown("심의 신청 ➔ 공공디자인위원회 심의 ➔ 결과 반영.")
        st.markdown("👉 법정양식: 관할 지자체 ([공공디자인 조례](https://www.law.go.kr/lsSc.do?menuId=1&query=공공디자인)) 관련 서식")

with st.expander("24. 항만공간 공공디자인 협의"):
    st.info("""
    * **1. 개요**: 항만시설 및 주변 공간의 디자인 품질을 향상시키고 항만의 정체성을 확보하여, 국민이 안전하고 쾌적하게 이용할 수 있도록 가이드라인 적용 여부를 검토합니다.
    * **2. 실시근거**: 해양수산부 예규 (항만공간의 공공디자인 가이드라인).
    * **3. 대상사업 및 협의시기**: 실시설계 단계.
      * 내용: 항만법에 따른 **5대 분야 40개 유형 146개 시설물 전체** (기본시설, 기능시설, 지원시설, 항만친수시설, 공통 공공시설물 등)
      * 👉 대상범위 상세: ([항만공간의 공공디자인 가이드라인](https://www.law.go.kr/lsSc.do?menuId=1&query=항만공간의공공디자인가이드라인)) 제1장 제3조(적용범위)
    * **4. 협의기관**: 해양수산부 및 관할 지방해양수산청, 항만공사.
    * **5. 평가항목**: 항만 정체성 반영, 안전성, 편의성, 심미성, 친환경성 등 가이드라인 적용 여부.
    """)
    show_scope(24)
    with st.expander("6. 절차 및 양식 보기"):
        show_flows(24, has_old=False)
        st.markdown("설계 반영 ➔ 관계기관 협의 및 자문 ➔ 실시계획 반영.")
        st.markdown("👉 관련지침: 해양수산부 예규 ([항만공간의 공공디자인 가이드라인](https://www.law.go.kr/lsSc.do?menuId=1&query=항만공간의공공디자인가이드라인))")


_pj_end()                   # [공통블록] 입력란 아래(또는 화면 맨 아래) 💾 · 🧾 · 📚
