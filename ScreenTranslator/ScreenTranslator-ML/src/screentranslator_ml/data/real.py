from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Polygon:
    text: str
    points: list[tuple[float, float]]


@dataclass
class RealRecord:
    image_name: str
    polygons: list[Polygon]


def parse_labelstudio_export(export_path: Path) -> list[RealRecord]:
    data = json.loads(Path(export_path).read_text(encoding="utf-8"))
    out: list[RealRecord] = []
    for row in data:
        img = row["data"]["image"].rstrip("/")
        img_name = img.rsplit("/", 1)[-1]
        polys_by_id: dict[str, dict] = {}
        for ann in row["annotations"]:
            for r in ann["result"]:
                rid = r["id"]
                slot = polys_by_id.setdefault(rid, {})
                if r["type"] == "polygonlabels":
                    slot["points"] = [(x, y) for x, y in r["value"]["points"]]
                elif r["type"] == "textarea":
                    slot["text"] = r["value"]["text"][0]
        polys = [
            Polygon(text=v["text"], points=v["points"])
            for v in polys_by_id.values()
            if "text" in v and "points" in v
        ]
        out.append(RealRecord(image_name=img_name, polygons=polys))
    return out
