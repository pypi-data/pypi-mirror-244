import itertools
from typing import Any

from .patterns_juridical import org_options, ph_options
from .utils import spacy_in, spacy_re

extras = " ".join(org_options)
extras += " " + " ".join(ph_options)
extras += " . , et al. et al the Jr Jr. Sr Sr. III IV Partnership Dev't"
misc = spacy_in([e.lower() for e in extras.split()], default="LOWER", op="*")
cov = spacy_re("\\([A-Z]+\\)", op="?")
vs = [spacy_in(["v.", "vs."])]
party_styles: list[dict[str, Any]] = [
    {"IS_UPPER": True, "OP": "{1,6}", "ORTH": {"NOT_IN": ["In"]}},
    {"IS_TITLE": True, "OP": "{1,6}", "ORTH": {"NOT_IN": ["In"]}},
]


def create_vs_patterns(parties: list[dict[str, Any]] = party_styles) -> list[list[dict[str, Any]]]:
    return [([a, cov, misc] + vs + [b, cov, misc]) for a, b in itertools.product(parties, repeat=2)]
