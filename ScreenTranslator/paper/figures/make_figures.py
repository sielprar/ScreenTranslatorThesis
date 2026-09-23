import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
CAPTURES = ROOT / "study/evaluation/captures"
ABLATION = ROOT / "study/evaluation/ablation/captures"
LATENCY = ROOT / "study/evaluation/latency/20260922T235014Z/samples.csv"
ABLATION_LATENCY = ROOT / "study/evaluation/ablation/latency/samples.csv"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

INK = "#0b0b0b"
INK_2 = "#52514e"
RULE = "#c9c8c2"
SURFACE = "#ffffff"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
NEUTRAL = "#b9b8b1"


def box(ax, x, y, w, h, title, body="", fill="#f4f4f1", edge=RULE):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.0,rounding_size=0.12",
                                fc=fill, ec=edge, lw=1.0))
    if body:
        ax.text(x, y + h / 2 - 0.2, title, ha="center", va="top",
                fontsize=8.5, fontweight="bold", color=INK)
        ax.text(x, y + h / 2 - 0.55, body, ha="center", va="top",
                fontsize=7, color=INK_2, linespacing=1.35)
    else:
        ax.text(x, y, title, ha="center", va="center", fontsize=9,
                fontweight="bold", color=INK)


def arrow(ax, x1, y1, x2, y2, label="", dashed=False, lx=0.1, ha="left"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=10, lw=1.0, color=INK_2,
                                 linestyle=(0, (4, 3)) if dashed else "-",
                                 shrinkA=0, shrinkB=0))
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2, label, fontsize=7,
                color=INK_2, ha=ha, va="center")


def pipeline_diagram():
    fig, ax = plt.subplots(figsize=(6.7, 8.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 13)
    ax.axis("off")
    L, R, C = 2.6, 9.4, 6.0

    box(ax, C, 12.3, 10.4, 1.0, "UI events",
        "window change · content change · scroll · video timer")
    box(ax, C, 10.85, 10.4, 1.1, "Pass scheduler",
        "one pass at a time; a new event → exactly one re-run;\n"
        "120 ms pause after scrolling; stale passes are discarded")
    box(ax, C, 9.45, 6.4, 0.8, "Path choice: ≥15 text nodes,\nnot an image viewer or video app?")

    box(ax, L, 7.7, 4.8, 1.55, "Path 1: accessibility tree",
        "depth-first walk: ≤500 nodes,\ndepth ≤30, no containers >30%;\n"
        "same fingerprint → previous cards",
        fill="#eaf1fb", edge=BLUE)
    box(ax, R, 7.7, 4.8, 1.55, "Path 2: screenshot",
        "hide cards, 96 ms pause;\ntakeScreenshot; 17×16 dHash:\n"
        "≤3 bits → previous cards", fill="#fdeee7", edge=ORANGE)
    box(ax, R, 5.85, 4.8, 1.45, "OCR: ML Kit (Latin)",
        "scales 1× and 1.75×,\nmerged by IoU; filters;\n"
        "at most 120 lines", fill="#fdeee7", edge=ORANGE)
    box(ax, R, 4.15, 4.8, 1.4, "Language routing",
        "(TextRouting) Cyrillic →\nTesseract rus; doubtful line →\n"
        "Tesseract eng+rus; language focus", fill="#fdeee7", edge=ORANGE)

    box(ax, C, 2.5, 10.4, 1.0, "Language identification and translation to English",
        "ML Kit Language ID + Translate · lines in parallel · LRU caches of 512",
        fill="#e8f6f0", edge=AQUA)
    box(ax, C, 1.0, 10.4, 1.1, "Translation cards",
        "style: median border colour, contrast-checked text colour, 0.6 × line height;\n"
        "TYPE_ACCESSIBILITY_OVERLAY window, touches pass through; FrameTrace row")

    arrow(ax, C, 11.8, C, 11.4)
    arrow(ax, C, 10.3, C, 9.85)
    arrow(ax, 4.2, 9.05, L, 8.48, "yes", lx=-0.15, ha="right")
    arrow(ax, 7.8, 9.05, R, 8.48, "no", lx=0.15)
    arrow(ax, 5.05, 7.35, 6.95, 7.35, dashed=True)
    ax.text(6.0, 7.62, "0 cards", fontsize=7, color=INK_2, ha="center")
    arrow(ax, R, 6.92, R, 6.58)
    arrow(ax, R, 5.12, R, 4.85)
    arrow(ax, R, 3.45, 8.3, 3.0)
    arrow(ax, L, 6.92, L, 3.0)
    arrow(ax, C, 2.0, C, 1.55)

    fig.savefig(OUT / "fig4_1_pipeline.png", dpi=220, bbox_inches="tight",
                facecolor=SURFACE)
    plt.close(fig)


def load(path, crop=None, mask_avatar=False):
    im = Image.open(path).convert("RGB")
    if mask_avatar:
        d = ImageDraw.Draw(im)
        d.ellipse((884, 276, 1024, 416), fill="#d9d9d4")
    return im.crop(crop) if crop else im


def panels(images, labels, name, width_in=6.7):
    h = max(im.height for im in images)
    w = sum(im.width for im in images)
    fig_w = width_in
    fig_h = fig_w * h / w + 0.35
    fig, axes = plt.subplots(1, len(images), figsize=(fig_w, fig_h),
                             gridspec_kw={"width_ratios": [im.width for im in images],
                                          "wspace": 0.04})
    for ax, im, label in zip(axes, images, labels):
        ax.imshow(im)
        ax.set_title(label, fontsize=9, color=INK, pad=4)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(RULE)
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


def screenshots():
    s = CAPTURES / "settings_ru/20260922T231056Z"
    top = (0, 240, 1080, 2400)
    panels([load(s / "source.png", top, True), load(s / "output.png", top, True)],
           ["(a) original screen", "(b) with translation cards"], "fig6_1_settings_ru.png",
           width_in=5.2)

    e = CAPTURES / "browser_es/20260922T232431Z"
    art = (0, 220, 1080, 2000)
    panels([load(e / "source.png", art), load(e / "output.png", art)],
           ["(a) original page", "(b) OCR path"], "fig6_2_browser_es.png",
           width_in=5.2)

    r_src = CAPTURES / "browser_ru/20260922T232504Z/source.png"
    r_a11y = CAPTURES / "browser_ru/20260922T232504Z/output.png"
    r_ocr = ABLATION / "browser_ru/20260923T001711Z/output.png"
    art = (0, 220, 1080, 1900)
    panels([load(r_src, art), load(r_a11y, art), load(r_ocr, art)],
           ["(a) original page", "(b) accessibility tree", "(c) OCR path"],
           "fig6_5_browser_ru_paths.png")

    m = CAPTURES / "menu_ru/20260922T231443Z"
    crop = (0, 830, 720, 1330)
    panels([load(m / "source.png", crop), load(m / "output.png", crop)],
           ["(a) part of the original menu", "(b) with translation cards"],
           "fig6_3_menu_ru.png")


def latency_stages():
    rows = [r for r in csv.DictReader(LATENCY.open()) if r["scenario"] == "first_view"]
    rows += [r for r in csv.DictReader(ABLATION_LATENCY.open())
             if r["case_id"] == "browser_es" and r["flags"] == "a11y=0"]
    cases = [("settings_ru", "Settings (ru), tree"),
             ("browser_ru", "Wikipedia (ru), tree"),
             ("browser_es", "Wikipedia (es), OCR*"),
             ("menu_fr", "French menu, OCR"),
             ("menu_ru", "Russian menu, OCR")]
    stages = [("harvest_ms", "Tree walk", BLUE),
              ("ocr_ms", "OCR", ORANGE),
              ("nmt_ms", "Language and translation (incl. Tesseract)", AQUA),
              ("overlay_ms", "Rendering", YELLOW)]

    means = []
    for case, _ in cases:
        rs = [r for r in rows if r["case_id"] == case]
        m = {k: sum(float(r[k]) for r in rs) / len(rs) for k, _, _ in stages}
        m["total"] = sum(float(r["total_ms"]) for r in rs) / len(rs)
        m["other"] = m["total"] - sum(m[k] for k, _, _ in stages)
        m["n"] = len(rs)
        means.append(m)

    fig, ax = plt.subplots(figsize=(6.7, 2.9))
    y = list(range(len(cases)))[::-1]
    for yi, m in zip(y, means):
        left = 0.0
        for key, label, color in stages + [("other", "Other", NEUTRAL)]:
            v = m[key]
            ax.barh(yi, v, left=left, height=0.56, color=color,
                    edgecolor=SURFACE, linewidth=1.5)
            if v >= 380:
                ax.text(left + v / 2, yi, f"{v / 1000:.1f}",
                        ha="center", va="center", fontsize=7, color=INK)
            left += v
        ax.text(left + 60, yi, f"{m['total'] / 1000:.2f} s (n={m['n']})",
                va="center", fontsize=7.5, color=INK)

    ax.set_yticks(y)
    ax.set_yticklabels([label for _, label in cases], fontsize=8, color=INK)
    ax.set_xlabel("Mean pass time, ms (first view)", fontsize=8, color=INK_2)
    ax.set_xlim(0, 6400)
    ax.xaxis.grid(True, color="#e6e5e0", lw=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(RULE)
    ax.tick_params(colors=INK_2, labelsize=7.5, length=0)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in stages] + \
              [plt.Rectangle((0, 0), 1, 1, color=NEUTRAL)]
    ax.legend(handles, [l for _, l, _ in stages] + ["Other (not measured separately)"],
              ncol=3, fontsize=7.5, frameon=False, loc="lower left",
              bbox_to_anchor=(0, 1.0), handlelength=1.2, columnspacing=1.2)
    fig.savefig(OUT / "fig6_4_latency_stages.png", dpi=220, bbox_inches="tight",
                facecolor=SURFACE)
    plt.close(fig)
    return means


if __name__ == "__main__":
    pipeline_diagram()
    screenshots()
    for m in latency_stages():
        print({k: round(v) for k, v in m.items()})
