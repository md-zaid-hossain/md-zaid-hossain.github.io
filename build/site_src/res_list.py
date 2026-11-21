#!/usr/bin/env python3
"""Home 03 RESEARCH: calm citation list (approved by Zaid 2026-11-18, option A).
Year · type line · title · venue · full author list (only Zaid in bold) · journal metrics · quiet links.
Journal metrics: Impact Factor (JCR) and CiteScore (Scopus), June 2026 releases. Update once a year."""

ME = "Md. Zaid Hossain"
PUBS = [  # year, kind, tier, first author?, title, venue, publisher, authors, doi, impact factor, citescore
    ("2026", "JOURNAL", "Q1", True,
     "Leakage-controlled machine learning for work-related musculoskeletal disorder risk classification among garment sewing-machine operators",
     "Results in Engineering 32 (2026) 113789", "Elsevier", "Md. Zaid Hossain, M. G. Kibria, B. U. Arif, S. H. Ratul",
     "10.1016/j.rineng.2026.113789", "9.4", "8.8"),
    ("2026", "JOURNAL", "Q1", False,
     "A simulation-based context-aware multimodal ML framework for proactive worker safety monitoring in resource-constrained factories",
     "Array 31 (2026) 101198", "Elsevier", "N. Morshed, M. S. I. Seam, Md. Zaid Hossain, M. A. Amin",
     "10.1016/j.array.2026.101198", "5.3", "10.1"),
    ("2025", "CONFERENCE", "IEEE", True,
     "AI-Driven Early Warning System for Industrial Shutdowns on High-Risk Pollution Days: A Case Study on Dhaka Air Quality",
     "IEEE QPAIN 2025 · BAUST, Saidpur", "IEEE", "Md. Zaid Hossain, N. Morshed, S. I. Seam",
     "10.1109/QPAIN66474.2025.11171883", None, None),
]
# Zaid 21 Nov 2026 (option B): one NOW row with both studies; the FDM PLA study links to its study page
ONGOING = [("FDM print settings and the bending, surface roughness and hardness of PLA, with Tonoy Chowdhury.", "#"),
           ("Explainable ML for cardiovascular disease prediction: a systematic multi-paradigm benchmark.", None)]
METRIC_NOTE = "IF · Journal Impact Factor (JCR) &nbsp;·&nbsp; CITESCORE · Scopus &nbsp;·&nbsp; 2026 RELEASES"

CSS = """
/* ===== 03 Research: calm citation list ===== */
.rcl{border:1px solid var(--line2);border-radius:12px;background:var(--surface);padding:6px 12px}
.rcl .rit{display:grid;grid-template-columns:70px 1fr auto;gap:0 24px;padding:18px 12px;border-bottom:1px solid var(--line);border-radius:8px;transition:background .25s ease}
.rcl .rit:last-of-type{border-bottom-color:transparent}
.rcl .ryr{font:600 13px 'IBM Plex Mono',monospace;color:var(--muted);padding-top:1px;transition:color .25s ease}
.rcl .rtg{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.rcl .rtg em{font-style:normal;color:var(--acc-t)}
.rcl h3{font-size:16px;line-height:1.4;margin:6px 0 0;max-width:780px;transition:transform .25s ease}
.rcl .rvn{font-size:13.5px;color:var(--body);margin-top:6px}
.rcl .rau{font-size:13.5px;color:var(--muted);line-height:1.45;margin-top:2px}
.rcl .rau b{color:var(--strong);font-weight:600}
.rcl .rrs{display:flex;flex-direction:column;align-items:flex-end;gap:12px;align-self:start}
.rcl .rmt{display:flex;gap:14px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.rcl .rmt span{display:inline-flex;align-items:baseline;gap:6px}
.rcl .rmt b{font:500 12.5px 'IBM Plex Mono',monospace;letter-spacing:.02em;color:var(--body);transition:color .25s ease}
.rcl .rit:hover .rmt b{color:var(--strong)}
.rcl .rlk{display:flex;gap:14px;align-items:flex-start}
.rcl .rlk a{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);border-bottom:1px dotted var(--line2);padding-bottom:1px;transition:color .25s ease,border-color .25s ease}
.rcl .rlk a:hover{color:var(--acc-t);border-bottom-color:var(--acc-t)}
.rcl .rit:hover{background:var(--surface2)}
.rcl .rit:hover h3{transform:translateX(3px)}
.rcl .rit:hover .ryr{color:var(--strong)}
.rcl .rit.rgo{border-top:1px dashed var(--line2);margin-top:2px}
.rcl .rit.rgo h3{font-size:15px;color:var(--body);font-weight:500}
.rcl .rit.rgo h3+h3{margin-top:8px}
.rcl .rsp{white-space:nowrap;margin-left:6px;font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t);border-bottom:1px dotted var(--acc-t);padding-bottom:1px}
.rcl .rsp:hover{color:var(--strong);border-bottom-color:var(--strong)}
.rcl .rgn{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.rcl .rgn b{color:var(--strong);font-weight:600}
.rcl .rnt{padding:10px 12px 8px;border-top:1px solid var(--line);font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
@media (max-width:760px){
  .rcl{padding:4px 6px}
  .rcl .rit{grid-template-columns:1fr;gap:2px;padding:14px 8px}
  .rcl h3{font-size:15px}
  .rcl .rrs{align-items:flex-start;margin-top:10px;gap:10px}
  .rcl .rnt{padding:10px 8px 6px;line-height:1.6}
}
"""


def html():
    rows = ""
    for (year, kind, tier, first, title, venue, pub, auth, doi, jif, cs) in PUBS:
        tag = " · ".join([kind, f"<em>{tier}</em>"] + (["1ST AUTHOR"] if first else []))
        metrics = (f'<div class="rmt"><span>IF <b>{jif}</b></span><span>CITESCORE <b>{cs}</b></span></div>'
                   if jif else "")
        rows += (f'<div class="rit"><div class="ryr">{year}</div><div><div class="rtg">{tag}</div><h3>{title}</h3>'
                 f'<div class="rvn">{venue} · {pub}</div><div class="rau">{auth.replace(ME, f"<b>{ME}</b>")}</div></div>'
                 f'<div class="rrs">{metrics}<div class="rlk"><a href="https://doi.org/{doi}" target="_blank" rel="noopener">DOI ↗</a>'
                 f'<a href="https://doi.org/{doi}" target="_blank" rel="noopener">PDF</a>'
                 f'<a href="#" data-cite="{auth} ({year}). {title}. {venue}. https://doi.org/{doi}">CITE</a></div></div></div>')
    now = "".join(f'<h3>{t}' + (f' <a class="rsp" href="{u}">STUDY PAGE →</a>' if u else "") + "</h3>" for t, u in ONGOING)
    rows += (f'<div class="rit rgo"><div class="ryr">NOW</div><div><div class="rtg">IN PROGRESS · {len(ONGOING)}</div>{now}</div>'
             f'<div class="rrs"><div class="rgn">+ ICMERE 2025 · <b>full list</b></div></div></div>')
    return f'<div class="rcl">{rows}<div class="rnt">{METRIC_NOTE}</div></div>'
