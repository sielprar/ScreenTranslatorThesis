from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Vocab:

    chars: list[str]
    _char_to_id: dict[str, int] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self._char_to_id = {c: i for i, c in enumerate(self.chars)}

    @classmethod
    def from_file(cls, path: Path) -> "Vocab":
        chars = Path(path).read_text(encoding="utf-8").splitlines()
        return cls(chars=chars)

    @property
    def blank_id(self) -> int:
        return self.chars.index("<blank>")

    def __len__(self) -> int:
        return len(self.chars)

    def encode(self, s: str) -> list[int]:
        return [self._char_to_id[c] for c in s]

    def decode(self, ids: list[int], remove_blanks: bool = True) -> str:
        out: list[str] = []
        for i in ids:
            c = self.chars[i]
            if c == "<blank>":
                if remove_blanks:
                    continue
                out.append("<blank>")
                continue
            out.append(c)
        return "".join(out)
