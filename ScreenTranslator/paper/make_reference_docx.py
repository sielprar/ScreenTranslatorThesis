import re
import subprocess
import zipfile
from pathlib import Path

OUT = Path(__file__).resolve().parent / "reference.docx"
FONT = "Times New Roman"
BLACK = "000000"

ONE = '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto" />'
ONE_HALF = '<w:spacing w:before="0" w:after="120" w:line="360" w:lineRule="auto" />'


def rpr(size_pt, bold=False, italic=False):
    half = int(size_pt * 2)
    return ("<w:rPr>"
            f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:eastAsia="{FONT}" w:cs="{FONT}" />'
            + ("<w:b /><w:bCs />" if bold else '<w:b w:val="0" /><w:bCs w:val="0" />')
            + ("<w:i /><w:iCs />" if italic else '<w:i w:val="0" /><w:iCs w:val="0" />')
            + f'<w:color w:val="{BLACK}" />'
            f'<w:sz w:val="{half}" /><w:szCs w:val="{half}" />'
            "</w:rPr>")


def ppr(spacing, jc=None, page_break=False, keep_next=False, extra=""):
    return ("<w:pPr>"
            + ("<w:keepNext /><w:keepLines />" if keep_next else "")
            + ("<w:pageBreakBefore />" if page_break else "")
            + spacing
            + (f'<w:jc w:val="{jc}" />' if jc else "")
            + extra
            + "</w:pPr>")


def heading_spacing(before_pt, after_pt):
    return (f'<w:spacing w:before="{before_pt * 20}" w:after="{after_pt * 20}" '
            'w:line="240" w:lineRule="auto" />')


PARAGRAPH = {
    "Normal": (ppr(ONE_HALF, "both"), rpr(12)),
    "BodyText": (ppr(ONE_HALF, "both"), rpr(12)),
    "FirstParagraph": (ppr(ONE_HALF, "both"), rpr(12)),
    "Compact": (ppr(ONE, "left"), rpr(12)),
    "Title": (ppr(heading_spacing(0, 12), "center"), rpr(20, bold=True)),
    "Subtitle": (ppr(heading_spacing(0, 12), "center"), rpr(14)),
    "Author": (ppr(ONE, "center"), rpr(12)),
    "Date": (ppr(ONE, "center"), rpr(12)),
    "AbstractTitle": (ppr(heading_spacing(0, 12), "left", page_break=True, keep_next=True),
                      rpr(18, bold=True)),
    "Abstract": (ppr(ONE_HALF, "both"), rpr(12)),
    "Heading1": (ppr(heading_spacing(0, 18), "left", page_break=True, keep_next=True,
                     extra='<w:outlineLvl w:val="0" />'), rpr(18, bold=True)),
    "Heading2": (ppr(heading_spacing(18, 6), "left", keep_next=True,
                     extra='<w:outlineLvl w:val="1" />'), rpr(14, bold=True)),
    "Heading3": (ppr(heading_spacing(12, 6), "left", keep_next=True,
                     extra='<w:outlineLvl w:val="2" />'), rpr(12, bold=True)),
    "TOCHeading": (ppr(heading_spacing(0, 18), "left", page_break=True, keep_next=True),
                   rpr(18, bold=True)),
    "Bibliography": (ppr('<w:spacing w:before="0" w:after="120" w:line="240" w:lineRule="auto" />',
                         "left", extra='<w:ind w:left="360" w:hanging="360" />'), rpr(10)),
    "FootnoteText": (ppr(ONE, "both"), rpr(10)),
    "FootnoteBlockText": (ppr(ONE, "both"), rpr(10)),
    "BlockText": (ppr('<w:spacing w:before="120" w:after="120" w:line="240" w:lineRule="auto" />',
                      "both", extra='<w:ind w:left="567" w:right="567" />'), rpr(12)),
    "Caption": (ppr('<w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto" />',
                    "left"), rpr(12, italic=True)),
    "TableCaption": (ppr('<w:spacing w:before="240" w:after="60" w:line="240" w:lineRule="auto" />',
                         "left", keep_next=True), rpr(12, italic=True)),
    "ImageCaption": (ppr('<w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto" />',
                         "left"), rpr(12, italic=True)),
    "Figure": (ppr(ONE, "center"), None),
    "CaptionedFigure": (ppr('<w:spacing w:before="240" w:after="0" w:line="240" w:lineRule="auto" />',
                            "center", keep_next=True), None),
}
def char_rpr():
    return ("<w:rPr>"
            f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:eastAsia="{FONT}" w:cs="{FONT}" />'
            f'<w:color w:val="{BLACK}" /></w:rPr>')


CHARACTER = {
    "Hyperlink": char_rpr(),
    "VerbatimChar": char_rpr(),
    "FootnoteReference": ('<w:rPr><w:vertAlign w:val="superscript" />'
                          f'<w:color w:val="{BLACK}" /></w:rPr>'),
}
SOURCE_CODE = (
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="SourceCode">'
    '<w:name w:val="Source Code" /><w:basedOn w:val="Normal" /><w:link w:val="VerbatimChar" />'
    + ppr(ONE, "left", extra='<w:wordWrap w:val="off" />') + rpr(10) + "</w:style>")


def set_parts(xml, style_id, new_ppr, new_rpr):
    m = re.search(r'<w:style [^>]*w:styleId="' + style_id + r'"[^>]*>.*?</w:style>', xml, re.S)
    assert m, style_id
    block = m.group(0)
    for tag, new in (("w:pPr", new_ppr), ("w:rPr", new_rpr)):
        if new is None:
            continue
        block, n = re.subn(r"<" + tag + r">.*?</" + tag + r">|<" + tag + r" />", new, block,
                           count=1, flags=re.S)
        if n == 0:
            block = block.replace("</w:style>", new + "</w:style>")
    return xml[:m.start()] + block + xml[m.end():]


def build():
    default = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                             check=True, capture_output=True).stdout
    tmp = OUT.with_suffix(".src.docx")
    tmp.write_bytes(default)
    zin = zipfile.ZipFile(tmp)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                xml = data.decode()
                xml = re.sub(r"<w:rPrDefault>.*?</w:rPrDefault>",
                             "<w:rPrDefault>" + rpr(12) + "</w:rPrDefault>", xml, flags=re.S)
                xml = re.sub(r"<w:pPrDefault>.*?</w:pPrDefault>",
                             "<w:pPrDefault>" + ppr(ONE_HALF) + "</w:pPrDefault>", xml,
                             flags=re.S)
                for sid, (p, r) in PARAGRAPH.items():
                    xml = set_parts(xml, sid, p, r)
                for sid, r in CHARACTER.items():
                    xml = set_parts(xml, sid, None, r)
                if 'w:styleId="SourceCode"' not in xml:
                    xml = xml.replace("</w:styles>", SOURCE_CODE + "</w:styles>")
                xml = re.sub(r"<w:rFonts [^>]*/>",
                             f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:eastAsia="{FONT}" '
                             f'w:cs="{FONT}" />', xml)
                xml = re.sub(r'<w:color [^>]*/>', f'<w:color w:val="{BLACK}" />', xml)
                xml = re.sub(r"<w:u [^>]*/>", "", xml)
                data = xml.encode()
            elif item.filename == "word/theme/theme1.xml":
                xml = data.decode()
                xml = re.sub(r'(<a:(?:major|minor)Font>\s*<a:latin typeface=")[^"]*"',
                             r'\g<1>' + FONT + '"', xml)
                data = xml.encode()
            zout.writestr(item, data)
    zin.close()
    tmp.unlink()


if __name__ == "__main__":
    build()
    print(f"wrote {OUT}")
