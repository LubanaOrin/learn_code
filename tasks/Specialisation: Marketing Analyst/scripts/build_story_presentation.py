"""Build a story-led Marketing Campaign Comparison PowerPoint.

This reuses the OpenXML helper functions from the Product Analyst project so
the Marketing deck has the same controlled, presentation-like feel instead of
the plain Pandoc default.
"""

from __future__ import annotations

import importlib.util
import re
import zipfile
from math import log10
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parents[1]
REPO_TASKS = TASK_DIR.parent
PRODUCT_BUILDER = (
    REPO_TASKS
    / "Specialisation: Product Analyst"
    / "scripts"
    / "build_presentation.py"
)
OUTPUT_DIR = TASK_DIR / "outputs" / "FINAL_SUBMISSION_FILES"
PPTX_PATH = OUTPUT_DIR / "marketing_campaign_comparison_presentation.pptx"
NOTES_PATH = OUTPUT_DIR / "marketing_campaign_comparison_speaker_notes.md"
CHART_DIR = TASK_DIR / "outputs" / "charts"

TITLE_SHAPE_IDS = {
    1: {12},
    2: {51},
    3: {101},
    4: {181},
    5: {221},
    6: {261},
    7: {301},
    8: {391},
    9: {441},
    10: {521},
}


def load_helpers():
    spec = importlib.util.spec_from_file_location("product_ppt_builder", PRODUCT_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load Product Analyst presentation helpers.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.OUTPUT_DIR = OUTPUT_DIR
    module.PPTX_PATH = PPTX_PATH
    module.NOTES_PATH = NOTES_PATH
    module.CHART_DIR = CHART_DIR
    return module


def set_text_run_size(shape_xml: str, size: int) -> str:
    return re.sub(r'(<a:rPr\b[^>]*\bsz=")\d+(")', rf"\g<1>{size * 100}\2", shape_xml)


def standardize_slide_type(slide_xml: str, slide_number: int) -> str:
    """Apply the requested Arial type and presentation-wide size rules."""
    slide_xml = slide_xml.replace('typeface="Aptos"', 'typeface="Arial"')
    slide_xml = slide_xml.replace('typeface="Aptos Display"', 'typeface="Arial"')
    title_ids = TITLE_SHAPE_IDS[slide_number]
    title_size = 60 if slide_number == 1 else 40
    body_size = 24 if slide_number == 1 else 20

    def replace_shape(match: re.Match[str]) -> str:
        shape_xml = match.group(0)
        shape_id = int(match.group(1))
        return set_text_run_size(shape_xml, title_size if shape_id in title_ids else body_size)

    return re.sub(r"<p:sp>.*?<p:cNvPr id=\"(\d+)\".*?</p:sp>", replace_shape, slide_xml, flags=re.S)


def standardize_pptx_theme() -> None:
    rebuilt_path = PPTX_PATH.with_suffix(".arial.tmp.pptx")
    with zipfile.ZipFile(PPTX_PATH, "r") as source, zipfile.ZipFile(rebuilt_path, "w", zipfile.ZIP_DEFLATED) as target:
        for item in source.infolist():
            content = source.read(item.filename)
            if item.filename == "ppt/theme/theme1.xml":
                text = content.decode("utf-8")
                text = text.replace('name="Aptos"', 'name="Arial"')
                text = text.replace('typeface="Aptos Display"', 'typeface="Arial"')
                text = text.replace('typeface="Aptos"', 'typeface="Arial"')
                content = text.encode("utf-8")
            target.writestr(item, content)
    rebuilt_path.replace(PPTX_PATH)


def right_arrow(m, shape_id: int, x: int, y: int, w: int, h: int, color: str) -> str:
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{shape_id}" name="Arrow"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
        <a:prstGeom prst="rightArrow"><a:avLst/></a:prstGeom>
        {m.solid_fill(color)}{m.no_line()}
      </p:spPr>
      <p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>
    </p:sp>
    """


def editable_bar_chart(
    m,
    shape_id: int,
    rows: list[tuple[str, float, str]],
    x: int,
    y: int,
    w: int,
    row_gap: int,
    bar_h: int,
    color: str,
    title: str,
    log_scale: bool = False,
) -> list[str]:
    emu = m.emu
    chart: list[str] = [
        m.text_box(shape_id, title, x, y, w, emu(28), 15, m.INK, True),
        m.straight_line(shape_id + 1, x, y + emu(42), x + w, y + emu(42), m.LINE),
    ]
    label_w = emu(210)
    value_w = emu(145)
    bar_x = x + label_w + emu(18)
    bar_max_w = w - label_w - value_w - emu(40)
    values = [max(value, 1) for _, value, _ in rows]
    max_value = max(log10(v) if log_scale else v for v in values)
    for idx, (label, value, value_label) in enumerate(rows):
        row_y = y + emu(64 + idx * row_gap)
        scaled = log10(max(value, 1)) if log_scale else value
        bar_w = max(emu(18), int(bar_max_w * scaled / max_value))
        bar_color = color if idx < 3 else m.ORANGE
        chart += [
            m.text_box(shape_id + 10 + idx * 5, label, x, row_y - emu(6), label_w, emu(34), 13, m.INK, False, "r"),
            m.rect(shape_id + 11 + idx * 5, bar_x, row_y, bar_w, emu(bar_h), bar_color, None),
            m.text_box(
                shape_id + 12 + idx * 5,
                value_label,
                bar_x + bar_w + emu(10),
                row_y - emu(6),
                value_w,
                emu(34),
                13,
                m.INK,
            ),
        ]
    return chart


def build_slides(m):
    slides: list[str] = []
    notes: list[str] = []
    images: dict[int, list[str]] = {}

    emu = m.emu

    # Slide 1
    e = [
        m.rect(10, 0, 0, m.SLIDE_W, m.SLIDE_H, m.INK, None),
        m.text_box(11, "MARKETING ANALYST", emu(78), emu(70), emu(650), emu(34), 13, m.ORANGE, True),
        m.text_box(
            12,
            "Referral Engagement Benchmark",
            emu(78),
            emu(145),
            emu(930),
            emu(230),
            38,
            m.WHITE,
            True,
        ),
        m.text_box(
            13,
            "Marketing Campaign Comparison\nModeled session duration by campaign and weekday",
            emu(78),
            emu(430),
            emu(830),
            emu(95),
            19,
            "D8DEE6",
        ),
        m.text_box(
            14,
            "Source: BigQuery raw events export",
            emu(78),
            emu(640),
            emu(750),
            emu(34),
            13,
            "C7CED6",
        ),
    ]
    slides.append(m.slide_xml(e, bg=m.INK))
    notes.append("Open with the business message: the goal is to decide which campaign signal is reliable enough for a marketing manager to use.")

    # Slide 2
    e = m.header(
        50,
        "DECISION FRAME",
        "Reliable Engagement Decision",
        "The marketing manager needs weekday campaign trends with enough evidence to support action.",
    )
    e += m.bullet_list(
        60,
        [
            "Referral traffic is consistently longer than organic traffic across the week.",
            "Data Share Promo has the longest reliable weighted average, but a smaller sample.",
            "Black Friday and holiday spikes are interesting, but too small for strong claims.",
        ],
        emu(110),
        emu(310),
        emu(650),
        70,
    )
    e += [
        m.rect(90, emu(820), emu(310), emu(320), emu(210), "EEF5FF", m.BLUE),
        m.text_box(91, "Decision rule", emu(850), emu(338), emu(260), emu(34), 22, m.BLUE, True, "c"),
        m.text_box(
            92,
            "Trust high-session patterns.\nUse tiny samples as follow-up leads.",
            emu(850),
            emu(392),
            emu(260),
            emu(92),
            17,
            m.INK,
            False,
            "c",
        ),
    ]
    slides.append(m.slide_xml(e))
    notes.append("Explain the decision rule: a marketing analyst should not simply pick the tallest bar. We need enough sessions to trust a trend.")

    # Slide 3
    e = m.header(
        100,
        "METRIC DESIGN",
        "Session Modeling Logic",
        "The raw events table does not include a ready-made session ID.",
    )
    steps = [
        ("Raw events", "date, time,\nuser, campaign"),
        ("Session flag", "new day or\n30+ min gap"),
        ("Modeled session", "first event to\nlast event"),
        ("Summary", "campaign by\nweekday"),
    ]
    for i, (title, body) in enumerate(steps):
        x = emu(70 + i * 295)
        y = emu(325)
        e += [
            m.rect(120 + i * 6, x, y, emu(240), emu(165), m.WHITE, m.LINE),
            m.text_box(121 + i * 6, title, x + emu(16), y + emu(18), emu(208), emu(32), 20, m.INK, True, "c"),
            m.text_box(122 + i * 6, body, x + emu(16), y + emu(88), emu(208), emu(56), 13, m.MUTED, False, "c"),
        ]
        if i < 3:
            e.append(right_arrow(m, 145 + i, x + emu(252), y + emu(55), emu(55), emu(34), m.BLUE))
    e += m.bullet_list(
        160,
        [
            "New session: different day or 30+ minute gap.",
            "Duration: last event minus first event.",
            "Modeled metric: explain limitations clearly.",
        ],
        emu(125),
        emu(575),
        emu(1000),
        43,
    )
    slides.append(m.slide_xml(e))
    notes.append("This slide teaches the session modeling logic. It also prepares for questions about how time on site was interpreted.")

    # Slide 4
    e = m.header(
        180,
        "CORE PATTERN",
        "Referral Duration Lead",
        "In the reliable comparison set, referral stays above organic on every weekday.",
    )
    e += [m.picture(190, "rId3", emu(540), emu(275), emu(650), emu(370), "Weekday duration chart")]
    e += m.bullet_list(
        200,
        [
            "Referral weighted average: 5.54 minutes.",
            "Organic weighted average: 4.06 minutes.",
            "Data Share Promo is higher overall, but less stable because the sample is smaller.",
        ],
        emu(95),
        emu(310),
        emu(410),
        66,
    )
    slides.append(m.slide_xml(e))
    notes.append("Lead with the strongest visual evidence: referral is consistently above organic across weekdays.")
    images[4] = ["reliable_campaign_weekday_duration.png"]

    # Slide 5
    e = m.header(
        220,
        "EVIDENCE WEIGHT",
        "Sample Size Risk",
        "Large session counts make organic and referral patterns much safer to interpret.",
    )
    e += editable_bar_chart(
        m,
        230,
        [
            ("Organic", 102309, "102,309"),
            ("Referral", 82353, "82,353"),
            ("Other", 33023, "33,023"),
            ("Data Share", 1294, "1,294"),
            ("NewYear V1", 66, "66"),
            ("NewYear V2", 39, "39"),
        ],
        emu(515),
        emu(285),
        emu(650),
        50,
        22,
        m.BLUE,
        "Modeled sessions by campaign",
        log_scale=True,
    )
    e += m.bullet_list(
        330,
        [
            "Organic: 102,309 modeled sessions.",
            "Referral: 82,353 modeled sessions.",
            "Data Share Promo: 1,294 modeled sessions.",
            "Several named campaigns have fewer than 100 sessions.",
        ],
        emu(95),
        emu(300),
        emu(380),
        56,
    )
    slides.append(m.slide_xml(e))
    notes.append("This slide is the evidence-quality slide. It prevents overclaiming small named campaigns.")

    # Slide 6
    e = m.header(
        260,
        "EXPLORATORY SIGNAL",
        "Small-Sample Spikes",
        "Most of the highest raw averages are based on 2-9 modeled sessions.",
    )
    e += editable_bar_chart(
        m,
        270,
        [
            ("BF V2 Sun", 26.73, "26.73\nn=4"),
            ("BF V2 Fri", 19.88, "19.88\nn=2"),
            ("BF V2 Mon", 17.59, "17.59\nn=9"),
            ("BF V1 Sat", 17.56, "17.56\nn=5"),
            ("Holiday V1 Sat", 12.59, "12.59\nn=5"),
            ("Holiday V1 Wed", 12.53, "12.53\nn=2"),
        ],
        emu(515),
        emu(285),
        emu(650),
        65,
        18,
        m.PURPLE,
        "Highest weekday averages",
    )
    e += [
        m.rect(360, emu(95), emu(315), emu(360), emu(165), "FFF5EB", m.ORANGE),
        m.text_box(361, "BlackFriday_V1\nFriday", emu(125), emu(340), emu(300), emu(52), 18, m.INK, True, "c"),
        m.text_box(362, "12.44 min\nn=2", emu(125), emu(405), emu(300), emu(58), 16, m.ORANGE, True, "c"),
        m.text_box(
            363,
            "Answer to stakeholder question: it did not take longer than 1 hour.",
            emu(95),
            emu(510),
            emu(365),
            emu(65),
            17,
            m.INK,
        ),
    ]
    slides.append(m.slide_xml(e))
    notes.append("Use this slide to answer the likely stakeholder question and explain why high averages from tiny samples are not enough for a budget decision.")

    # Slide 7
    e = m.header(
        300,
        "INTERPRETATION",
        "Duration Interpretation",
        "Duration is a useful engagement signal, but it is not automatically a performance win.",
    )
    e += [
        m.rect(310, emu(105), emu(310), emu(470), emu(220), "EEF5FF", m.BLUE),
        m.text_box(311, "Good interpretation", emu(135), emu(338), emu(410), emu(34), 22, m.BLUE, True),
    ]
    e += m.bullet_list(
        320,
        ["Stronger interest", "More product browsing", "Better-fit traffic"],
        emu(145),
        emu(395),
        emu(370),
        42,
    )
    e += [
        m.rect(340, emu(700), emu(310), emu(470), emu(220), "FFF1F0", m.RED),
        m.text_box(341, "Risk interpretation", emu(730), emu(338), emu(410), emu(34), 22, m.RED, True),
    ]
    e += m.bullet_list(
        350,
        ["Confusion", "Friction", "Inactive browser tabs"],
        emu(740),
        emu(395),
        emu(370),
        42,
    )
    e += [
        m.text_box(
            370,
            "Next decision should combine duration with purchases, revenue, and conversion rate.",
            emu(170),
            emu(595),
            emu(920),
            emu(42),
            20,
            m.INK,
            True,
            "c",
        )
    ]
    slides.append(m.slide_xml(e))
    notes.append("Explain that a longer session can mean engagement or friction. This is why the next analysis should connect duration to conversion and revenue.")

    # Slide 8
    e = m.header(
        390,
        "LIMITATIONS",
        "Modeling Limits",
        "The analysis is useful for direction, but not causal proof of campaign quality.",
    )
    e += m.bullet_list(
        400,
        [
            "Session IDs were not available, so sessions were estimated.",
            "Single-event sessions have a duration of 0 minutes.",
            "Campaign attribution may be incomplete when campaign values are missing.",
            "Small campaign samples can move sharply with one unusual visit.",
            "The analysis does not prove that longer sessions create more revenue.",
        ],
        emu(110),
        emu(300),
        emu(1040),
        58,
    )
    slides.append(m.slide_xml(e))
    notes.append("This slide shows analytical maturity. Name the assumptions and boundaries clearly so the metric is easy to defend.")

    # Slide 9
    e = m.header(
        440,
        "ACTION PLAN",
        "Outcome Follow-Up",
        "Longer sessions matter most if they also lead to conversion or revenue.",
    )
    e += [
        m.rect(450, emu(95), emu(300), emu(300), emu(170), m.WHITE, m.LINE),
        m.text_box(451, "1", emu(118), emu(325), emu(48), emu(45), 28, m.BLUE, True, "c"),
        m.text_box(452, "Link to\nrevenue", emu(175), emu(332), emu(185), emu(78), 16, m.INK, True, "c"),
        m.rect(460, emu(480), emu(300), emu(300), emu(170), m.WHITE, m.LINE),
        m.text_box(461, "2", emu(503), emu(325), emu(48), emu(45), 28, m.GREEN, True, "c"),
        m.text_box(462, "Segment\ntraffic", emu(560), emu(332), emu(185), emu(78), 16, m.INK, True, "c"),
        m.rect(470, emu(865), emu(300), emu(300), emu(170), m.WHITE, m.LINE),
        m.text_box(471, "3", emu(888), emu(325), emu(48), emu(45), 28, m.ORANGE, True, "c"),
        m.text_box(472, "Compare\nmedian", emu(945), emu(332), emu(185), emu(78), 16, m.INK, True, "c"),
    ]
    e += m.bullet_list(
        490,
        [
            "Review zero-duration sessions separately.",
            "Use real session IDs when available.",
            "Treat small spikes as investigation leads.",
        ],
        emu(170),
        emu(525),
        emu(900),
        43,
    )
    slides.append(m.slide_xml(e))
    notes.append("Turn the analysis into a practical next step. The marketing manager can use this to decide what to ask for next.")

    # Slide 10
    e = m.header(
        520,
        "FINAL DECISION",
        "Decision Summary",
        "Use referral as the reliable benchmark and investigate Data Share Promo next.",
    )
    e += [
        m.rect(530, emu(120), emu(310), emu(1020), emu(105), "EEF5FF", m.BLUE),
        m.text_box(
            531,
            "Decision: compare future campaigns against referral's stable weekday engagement pattern.",
            emu(155),
            emu(338),
            emu(950),
            emu(42),
            23,
            m.INK,
            True,
            "c",
        ),
    ]
    e += m.bullet_list(
        550,
        [
            "Referral is the most dependable benchmark.",
            "Data Share Promo needs conversion and revenue follow-up.",
            "Tiny holiday samples are only investigation leads.",
        ],
        emu(150),
        emu(500),
        emu(980),
        58,
    )
    slides.append(m.slide_xml(e))
    notes.append("Close with a clear decision summary. The project tells the manager what to trust and what to investigate next.")

    return slides, notes, images


def main() -> None:
    m = load_helpers()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    slides, notes, images = build_slides(m)
    slides = [standardize_slide_type(slide, idx) for idx, slide in enumerate(slides, start=1)]
    m.write_pptx(slides, notes, images)
    standardize_pptx_theme()
    m.write_notes_md(notes)
    print(f"Saved PPTX: {PPTX_PATH}")
    print(f"Saved speaker notes: {NOTES_PATH}")


if __name__ == "__main__":
    main()
