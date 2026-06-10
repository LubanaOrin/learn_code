"""Build the capstone presentation as an editable PPTX package.

The environment does not include python-pptx, so this script writes a minimal
OpenXML PowerPoint package directly. Slides use editable text boxes and shapes.
Speaker notes are saved both inside notes-slide XML parts and as a Markdown file.
"""

from __future__ import annotations

import html
import zipfile
from pathlib import Path

import pandas as pd


TASK_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = TASK_DIR / "outputs" / "presentation"
PPTX_PATH = OUTPUT_DIR / "osmi_mental_health_capstone_presentation.pptx"
NOTES_PATH = OUTPUT_DIR / "osmi_mental_health_speaker_notes.md"

SLIDE_W = 13_333_333
SLIDE_H = 7_500_000

INK = "1F2933"
MUTED = "5F6B7A"
PAPER = "F7F7F3"
WHITE = "FFFFFF"
TEAL = "2F6F73"
RED = "C25746"
GOLD = "D39B5F"
VIOLET = "6D4C7D"
LINE = "D8DEE6"


def emu(px: int) -> int:
    return int(px * 9525)


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def solid_fill(color: str) -> str:
    return f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'


def no_line() -> str:
    return '<a:ln><a:noFill/></a:ln>'


def line(color: str = LINE, width: int = 10_000) -> str:
    return f'<a:ln w="{width}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln>'


def text_box(
    shape_id: int,
    text: str,
    x: int,
    y: int,
    w: int,
    h: int,
    size: int = 24,
    color: str = INK,
    bold: bool = False,
    align: str = "l",
    name: str = "Text",
) -> str:
    bold_attr = ' b="1"' if bold else ""
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{shape_id}" name="{esc(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        <a:noFill/>{no_line()}
      </p:spPr>
      <p:txBody>
        <a:bodyPr wrap="square" anchor="t"><a:spAutoFit/></a:bodyPr><a:lstStyle/>
        <a:p><a:pPr algn="{align}"/>
          <a:r><a:rPr lang="en-US" sz="{size * 100}"{bold_attr}><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="Aptos"/></a:rPr><a:t>{esc(text)}</a:t></a:r>
        </a:p>
      </p:txBody>
    </p:sp>
    """


def rect(
    shape_id: int,
    x: int,
    y: int,
    w: int,
    h: int,
    fill: str = WHITE,
    stroke: str | None = LINE,
    name: str = "Rectangle",
) -> str:
    stroke_xml = no_line() if stroke is None else line(stroke)
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{shape_id}" name="{esc(name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
        <a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom>
        {solid_fill(fill)}{stroke_xml}
      </p:spPr>
      <p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>
    </p:sp>
    """


def straight_line(shape_id: int, x1: int, y1: int, x2: int, y2: int, color: str = LINE) -> str:
    x = min(x1, x2)
    y = min(y1, y2)
    w = abs(x2 - x1) or 1
    h = abs(y2 - y1) or 1
    flip_h = ' flipH="1"' if x2 < x1 else ""
    flip_v = ' flipV="1"' if y2 < y1 else ""
    return f"""
    <p:cxnSp>
      <p:nvCxnSpPr><p:cNvPr id="{shape_id}" name="Line"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>
      <p:spPr>
        <a:xfrm{flip_h}{flip_v}><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
        <a:prstGeom prst="line"><a:avLst/></a:prstGeom>
        {line(color, 18000)}
      </p:spPr>
    </p:cxnSp>
    """


def slide_xml(elements: list[str], bg: str = PAPER) -> str:
    body = "\n".join(elements)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr>{solid_fill(bg)}</p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {body}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def notes_xml(note: str, slide_rel_id: str = "rId1") -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
         xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
         xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Speaker Notes"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="685800" y="914400"/><a:ext cx="7772400" cy="5486400"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/>{no_line()}</p:spPr>
        <p:txBody><a:bodyPr wrap="square"/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="1200"/><a:t>{esc(note)}</a:t></a:r></a:p></p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:notes>"""


def rels(rels_items: list[tuple[str, str, str]]) -> str:
    items = "\n".join(
        f'<Relationship Id="{rid}" Type="{rtype}" Target="{target}"/>'
        for rid, rtype, target in rels_items
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{items}
</Relationships>"""


def bar_chart(shape_start: int, labels: list[str], values: list[float], x: int, y: int, w: int, h: int, color: str) -> list[str]:
    elements = []
    max_v = max(values)
    bar_h = h // len(values) - emu(8)
    for idx, (label, value) in enumerate(zip(labels, values)):
        yy = y + idx * (bar_h + emu(18))
        bw = int(w * value / max_v)
        elements.append(text_box(shape_start, label, x, yy, emu(190), bar_h, 15, MUTED))
        elements.append(rect(shape_start + 1, x + emu(205), yy, bw, bar_h, color, None))
        elements.append(text_box(shape_start + 2, f"{value:.1f}%", x + emu(215) + bw, yy, emu(100), bar_h, 16, INK, True))
        shape_start += 3
    return elements


def kpi(shape_id: int, label: str, value: str, x: int, y: int, w: int, h: int, accent: str) -> list[str]:
    return [
        rect(shape_id, x, y, w, h, WHITE, LINE),
        rect(shape_id + 1, x, y, emu(8), h, accent, None),
        text_box(shape_id + 2, label, x + emu(24), y + emu(18), w - emu(40), emu(28), 13, MUTED),
        text_box(shape_id + 3, value, x + emu(24), y + emu(52), w - emu(40), h - emu(58), 24, INK, True),
    ]


def title_slide(title: str, subtitle: str, kicker: str, footer: str) -> list[str]:
    elements = [
        rect(10, 0, 0, SLIDE_W, SLIDE_H, INK, None),
        text_box(11, kicker, emu(80), emu(70), emu(520), emu(36), 13, GOLD, True),
        text_box(12, title, emu(80), emu(150), emu(890), emu(310), 38, WHITE, True),
        text_box(13, subtitle, emu(80), emu(505), emu(850), emu(78), 21, "D8DEE6"),
        text_box(14, footer, emu(80), emu(640), emu(1000), emu(34), 13, "C7CED6"),
    ]
    elements += kpi(20, "Survey responses", "1,259", emu(955), emu(140), emu(250), emu(100), GOLD)
    elements += kpi(30, "Sought treatment", "50.6%", emu(955), emu(270), emu(250), emu(100), TEAL)
    elements += kpi(40, "Coworker comfort", "17.9%", emu(955), emu(400), emu(250), emu(100), RED)
    return elements


def standard_header(shape_id: int, kicker: str, claim: str, support: str) -> list[str]:
    return [
        text_box(shape_id, kicker, emu(70), emu(44), emu(460), emu(28), 12, TEAL, True),
        text_box(shape_id + 1, claim, emu(70), emu(78), emu(1000), emu(104), 28, INK, True),
        text_box(shape_id + 2, support, emu(70), emu(190), emu(1020), emu(48), 14, MUTED),
        straight_line(shape_id + 3, emu(70), emu(250), emu(1210), emu(250), LINE),
    ]


def build_slides() -> tuple[list[str], list[str]]:
    slides: list[str] = []
    notes: list[str] = []

    slides.append(slide_xml(title_slide(
        "Workplace mental health is treated privately, but disclosure at work remains constrained.",
        "A quantitative survey analysis of the OSMI Mental Health in Tech dataset",
        "CAPSTONE PRESENTATION",
        "Data Analytics Capstone Project | OSMI Mental Health in Tech Survey via Kaggle",
    ), bg=INK))
    notes.append("Introduce the project as a quantitative survey analysis. Explain that the focus is not diagnosing mental health, but understanding patterns in treatment-seeking, workplace support, perceived consequences, and disclosure comfort. Mention that the deck follows the same story as the notebook, dashboard, and written report.")

    e = standard_header(10, "RESEARCH DESIGN", "The project tests how workplace support and stigma relate to treatment-seeking.", "Research question: What workplace and personal factors are associated with mental health treatment-seeking and disclosure comfort among technology workers?")
    for i, (h, txt) in enumerate([
        ("H1", "Benefits awareness is associated with treatment-seeking."),
        ("H2", "Expected negative consequences reduce disclosure comfort."),
        ("H3", "Work interference is associated with treatment-seeking."),
        ("H4", "Support indicators differ by company context."),
    ]):
        x = emu(90 + (i % 2) * 555)
        y = emu(270 + (i // 2) * 155)
        e += [rect(20 + i*5, x, y, emu(500), emu(115), WHITE, LINE),
              text_box(21 + i*5, h, x + emu(22), y + emu(18), emu(58), emu(42), 22, TEAL, True),
              text_box(22 + i*5, txt, x + emu(92), y + emu(20), emu(365), emu(70), 18, INK)]
    slides.append(slide_xml(e))
    notes.append("State the research question and hypotheses. Emphasize that this is a survey-based quantitative study using segmentation, hypothesis testing, and logistic regression. Say that the aim is to demonstrate research thinking: variables, hypotheses, tests, interpretation, limitations.")

    e = standard_header(50, "DATASET", "The Kaggle survey gives enough structure for a reproducible quantitative study.", "The raw file has 1,259 responses and 27 columns; the cleaned analysis file has 56 columns after variable creation.")
    e += kpi(60, "Raw rows", "1,259", emu(90), emu(265), emu(250), emu(105), TEAL)
    e += kpi(70, "Raw columns", "27", emu(370), emu(265), emu(250), emu(105), GOLD)
    e += kpi(80, "Cleaned columns", "56", emu(650), emu(265), emu(250), emu(105), VIOLET)
    e += kpi(90, "Invalid ages fixed", "8", emu(930), emu(265), emu(250), emu(105), RED)
    e += [
        text_box(100, "Cleaning choices", emu(90), emu(450), emu(280), emu(34), 20, INK, True),
        text_box(101, "Ages outside 18-75 were treated as missing. Gender values were grouped from 49 raw responses into four broader analysis categories. Binary and ordered variables were created for treatment, benefits, work interference, leave difficulty, and disclosure comfort.", emu(90), emu(492), emu(1040), emu(105), 17, MUTED),
    ]
    slides.append(slide_xml(e))
    notes.append("Explain one row as one survey response. Mention that survey data is often messy because respondents can type values differently. Highlight two important cleaning decisions: impossible ages and many gender values. This shows data preparation and reproducibility.")

    e = standard_header(110, "KEY PATTERN", "Treatment-seeking is common, but workplace disclosure comfort is much lower.", "50.6% sought treatment, while 41.0% would discuss mental health with a supervisor and only 17.9% with coworkers.")
    e += bar_chart(120, ["Sought treatment", "Supervisor comfort", "Coworker comfort"], [50.6, 41.0, 17.9], emu(105), emu(300), emu(520), emu(250), TEAL)
    e += [rect(140, emu(900), emu(292), emu(265), emu(275), WHITE, LINE),
          text_box(141, "Main insight", emu(925), emu(320), emu(210), emu(34), 20, INK, True),
          text_box(142, "Many respondents act privately by seeking treatment, while fewer feel safe discussing mental health needs at work.", emu(925), emu(372), emu(205), emu(160), 14, MUTED)]
    slides.append(slide_xml(e))
    notes.append("This is the main story slide. Walk through the three percentages slowly. The point is not simply that treatment is high, but that openness at work is lower, especially with coworkers. This creates the logic for the later recommendations.")

    e = standard_header(150, "WORKPLACE SUPPORT", "Benefit and care-option awareness are linked with higher treatment-seeking.", "Treatment rate is 63.9% when benefits are known, compared with 37.0% when respondents do not know whether benefits exist.")
    e += [rect(160, emu(95), emu(300), emu(500), emu(280), WHITE, LINE),
          text_box(161, "Employer benefits", emu(125), emu(328), emu(380), emu(34), 21, INK, True),
          text_box(162, "Known benefits", emu(130), emu(390), emu(230), emu(32), 18, MUTED),
          text_box(163, "63.9%", emu(400), emu(384), emu(180), emu(38), 24, TEAL, True),
          text_box(164, "No benefits", emu(130), emu(455), emu(230), emu(32), 18, MUTED),
          text_box(165, "48.4%", emu(400), emu(449), emu(180), emu(38), 24, TEAL, True),
          text_box(166, "Don't know", emu(130), emu(520), emu(230), emu(32), 18, MUTED),
          text_box(167, "37.0%", emu(400), emu(514), emu(180), emu(38), 24, TEAL, True)]
    e += [rect(180, emu(690), emu(300), emu(500), emu(280), WHITE, LINE),
          text_box(181, "Care options", emu(720), emu(328), emu(380), emu(34), 21, INK, True),
          text_box(182, "Known options", emu(725), emu(390), emu(230), emu(32), 18, MUTED),
          text_box(183, "69.1%", emu(990), emu(384), emu(180), emu(38), 24, GOLD, True),
          text_box(184, "No options", emu(725), emu(455), emu(230), emu(32), 18, MUTED),
          text_box(185, "41.3%", emu(990), emu(449), emu(180), emu(38), 24, GOLD, True),
          text_box(186, "Not sure", emu(725), emu(520), emu(230), emu(32), 18, MUTED),
          text_box(187, "39.2%", emu(990), emu(514), emu(180), emu(38), 24, GOLD, True)]
    slides.append(slide_xml(e))
    notes.append("Use this slide for H1. Explain that awareness matters: people who know that benefits or care options exist show higher treatment-seeking rates. The chi-square tests for both benefits and care options are statistically significant with p-values below 0.001.")

    e = standard_header(200, "WORK INTERFERENCE", "Treatment-seeking rises sharply when mental health interferes with work.", "85.4% of respondents reporting frequent work interference had sought treatment; only 14.1% of those reporting no interference had done so.")
    e += bar_chart(210, ["Often", "Sometimes", "Rarely", "Never", "Missing"], [85.4, 77.0, 70.5, 14.1, 1.5], emu(120), emu(280), emu(820), emu(330), VIOLET)
    slides.append(slide_xml(e))
    notes.append("Use this for H3. Explain that work interference is a strong severity/context signal. Be careful with language: this is association, not causation. The missing group likely includes people who did not answer because the question may not apply.")

    e = standard_header(250, "DISCLOSURE RISK", "Expected consequences are strongly connected to lower discussion comfort.", "Perceived negative consequences are statistically associated with both supervisor and coworker discussion comfort.")
    e += kpi(260, "Supervisor consequence test", "χ² 461.66", emu(100), emu(290), emu(305), emu(110), RED)
    e += kpi(270, "Coworker consequence test", "χ² 285.53", emu(445), emu(290), emu(305), emu(110), RED)
    e += kpi(280, "Both p-values", "< 0.001", emu(790), emu(290), emu(305), emu(110), TEAL)
    e += [text_box(290, "Interpretation", emu(120), emu(470), emu(990), emu(82), 22, INK, True),
          text_box(291, "When respondents expect negative consequences, workplace mental health conversations become less comfortable. This supports the stigma/disclosure-risk part of the capstone story.", emu(120), emu(520), emu(990), emu(75), 17, MUTED)]
    slides.append(slide_xml(e))
    notes.append("Use this for H2. Explain that stigma is measured indirectly through expected consequences and comfort discussing mental health. The tests show strong associations, so the recommendations should include confidentiality, manager training, and culture change.")

    e = standard_header(300, "MODEL", "The treatment-seeking model separates groups well, but it remains associative.", "Logistic regression predicted treatment-seeking with ROC AUC 0.891 on the test set.")
    e += kpi(310, "ROC AUC", "0.891", emu(95), emu(285), emu(260), emu(105), TEAL)
    e += kpi(320, "Accuracy", "0.819", emu(385), emu(285), emu(260), emu(105), GOLD)
    e += kpi(330, "Recall", "0.862", emu(675), emu(285), emu(260), emu(105), VIOLET)
    e += [text_box(340, "Positive model signals", emu(100), emu(455), emu(400), emu(36), 20, INK, True),
          text_box(341, "Work interference, family history, coworker discussion comfort, care options, and benefits.", emu(100), emu(515), emu(1000), emu(55), 19, MUTED)]
    slides.append(slide_xml(e))
    notes.append("Explain logistic regression in simple terms: it models a yes/no outcome. Here the outcome is whether someone sought treatment. ROC AUC of 0.891 means the model separates the two groups well, but it still does not prove causation.")

    e = standard_header(350, "RECOMMENDATIONS", "The practical response is to make support visible, confidential, and culturally safe.", "Recommendations connect directly to the evidence: benefits, care options, disclosure comfort, and work interference.")
    recommendations = [
        ("Clarify benefits", "Make mental health benefits easy to find and understand."),
        ("Protect confidentiality", "Communicate anonymity and privacy protections clearly."),
        ("Train managers", "Only 41.0% were comfortable discussing mental health with supervisors."),
        ("Reduce stigma", "Only 17.9% were comfortable discussing mental health with coworkers."),
        ("Monitor interference", "Use work interference as an early signal for support needs."),
    ]
    for i, (head, body) in enumerate(recommendations):
        y = emu(260 + i * 72)
        e += [text_box(360 + i*3, f"{i+1}", emu(105), y, emu(44), emu(42), 20, TEAL, True, "c"),
              text_box(361 + i*3, head, emu(175), y, emu(260), emu(36), 19, INK, True),
              text_box(362 + i*3, body, emu(455), y, emu(650), emu(36), 16, MUTED)]
    slides.append(slide_xml(e))
    notes.append("Connect each recommendation to a result. For example, benefit clarity follows from the benefit and care-option findings. Manager training follows from the low supervisor discussion comfort. Stigma reduction follows from the very low coworker comfort.")

    e = standard_header(390, "LIMITATIONS", "The study is useful for evidence, but it should not be overclaimed.", "The correct interpretation is association in a self-reported, non-random public survey sample.")
    limitations = [
        "Observational data cannot prove cause and effect.",
        "Survey respondents are not a random sample of all technology workers.",
        "Self-reported answers may include recall or social desirability bias.",
        "Some variables have missing values, especially work_interfere.",
        "Gender grouping simplifies diverse self-described identities.",
    ]
    for i, item in enumerate(limitations):
        e += [rect(400 + i*2, emu(100), emu(265 + i*70), emu(28), emu(28), GOLD, None),
              text_box(401 + i*2, item, emu(150), emu(255 + i*70), emu(930), emu(44), 19, INK)]
    slides.append(slide_xml(e))
    notes.append("Use this slide to show research maturity. A good quantitative analyst does not overclaim. Say clearly that the analysis shows associations, not causal effects, and that the sample may not represent all technology workers.")

    e = standard_header(430, "CLOSE", "Private treatment is common, but workplace openness remains constrained.", "50.6% sought treatment, but only 41.0% were comfortable with supervisors and 17.9% with coworkers.")
    e += [text_box(440, "Final takeaway", emu(120), emu(285), emu(980), emu(54), 30, TEAL, True),
          text_box(441, "Offering mental health resources is not enough. Technology employers need visible benefits, trusted care options, confidentiality, and team cultures where mental health can be discussed safely.", emu(120), emu(355), emu(980), emu(120), 24, INK),
          text_box(442, "Source: OSMI Mental Health in Tech Survey via Kaggle. Analysis files, notebook, dashboard, and report are saved in the project repository.", emu(120), emu(620), emu(1000), emu(34), 13, MUTED)]
    slides.append(slide_xml(e))
    notes.append("Close by restating the main gap. This is the sentence to remember: treatment-seeking is common, but workplace openness is constrained. Mention that the project demonstrates quantitative research skills: cleaning, segmentation, tests, model, dashboard, and written report.")

    return slides, notes


def write_pptx(slides: list[str], notes: list[str]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    slide_count = len(slides)
    if slide_count != len(notes):
        raise ValueError(f"Slide count ({slide_count}) does not match notes count ({len(notes)}).")

    content_overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>',
    ]
    for i in range(1, slide_count + 1):
        content_overrides.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
        content_overrides.append(f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>')

    content_types = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  {''.join(content_overrides)}
</Types>"""

    slide_id_list = "\n".join(
        f'<p:sldId id="{255 + i}" r:id="rId{i}"/>' for i in range(1, slide_count + 1)
    )
    presentation = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
 <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId{slide_count + 1}"/></p:sldMasterIdLst>
 <p:notesMasterIdLst><p:notesMasterId r:id="rId{slide_count + 3}"/></p:notesMasterIdLst>
 <p:sldIdLst>{slide_id_list}</p:sldIdLst>
 <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="wide"/>
 <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>"""

    pres_rels_items = [
        (f"rId{i}", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide", f"slides/slide{i}.xml")
        for i in range(1, slide_count + 1)
    ]
    pres_rels_items += [
        (f"rId{slide_count + 1}", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "slideMasters/slideMaster1.xml"),
        (f"rId{slide_count + 2}", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "theme/theme1.xml"),
        (f"rId{slide_count + 3}", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster", "notesMasters/notesMaster1.xml"),
    ]

    master = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>"""

    layout = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank">
<p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>"""

    notes_master = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notesMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:notesMaster>"""

    theme = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Capstone Theme"><a:themeElements><a:clrScheme name="Capstone"><a:dk1><a:srgbClr val="1F2933"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="5F6B7A"/></a:dk2><a:lt2><a:srgbClr val="F7F7F3"/></a:lt2><a:accent1><a:srgbClr val="2F6F73"/></a:accent1><a:accent2><a:srgbClr val="C25746"/></a:accent2><a:accent3><a:srgbClr val="D39B5F"/></a:accent3><a:accent4><a:srgbClr val="6D4C7D"/></a:accent4><a:accent5><a:srgbClr val="52796F"/></a:accent5><a:accent6><a:srgbClr val="9CA3AF"/></a:accent6><a:hlink><a:srgbClr val="2F6F73"/></a:hlink><a:folHlink><a:srgbClr val="6D4C7D"/></a:folHlink></a:clrScheme><a:fontScheme name="Aptos"><a:majorFont><a:latin typeface="Aptos Display"/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/></a:minorFont></a:fontScheme><a:fmtScheme name="Default"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>"""

    with zipfile.ZipFile(PPTX_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels([("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml")]))
        z.writestr("ppt/presentation.xml", presentation)
        z.writestr("ppt/_rels/presentation.xml.rels", rels(pres_rels_items))
        z.writestr("ppt/slideMasters/slideMaster1.xml", master)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
            ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "../theme/theme1.xml"),
        ]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", layout)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", rels([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "../slideMasters/slideMaster1.xml"),
        ]))
        z.writestr("ppt/notesMasters/notesMaster1.xml", notes_master)
        z.writestr("ppt/notesMasters/_rels/notesMaster1.xml.rels", rels([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "../theme/theme1.xml"),
        ]))
        z.writestr("ppt/theme/theme1.xml", theme)
        for i, slide in enumerate(slides, start=1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide)
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels([
                ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
                ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide", f"../notesSlides/notesSlide{i}.xml"),
            ]))
            z.writestr(f"ppt/notesSlides/notesSlide{i}.xml", notes_xml(notes[i - 1]))
            z.writestr(f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels", rels([
                ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide", f"../slides/slide{i}.xml"),
                ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster", "../notesMasters/notesMaster1.xml"),
            ]))


def write_notes_md(notes: list[str]) -> None:
    lines = ["# Speaker Notes\n"]
    for i, note in enumerate(notes, start=1):
        lines.append(f"## Slide {i}\n")
        lines.append(note)
        lines.append("")
    NOTES_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    slides, notes = build_slides()
    write_pptx(slides, notes)
    write_notes_md(notes)
    print(f"Saved PPTX: {PPTX_PATH}")
    print(f"Saved speaker notes: {NOTES_PATH}")


if __name__ == "__main__":
    main()
