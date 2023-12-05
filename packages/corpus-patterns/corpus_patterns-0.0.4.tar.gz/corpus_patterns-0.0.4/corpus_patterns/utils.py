import re
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

import srsly  # type: ignore
from pydantic.functional_validators import AfterValidator
from rich.jupyter import print
from spacy.language import Language
from spacy.tokens import Doc
from typing_extensions import Annotated

camel_case_pattern = re.compile(r".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)")


def uncamel(text: str) -> list[str]:
    """For text in camelCaseFormatting, convert into a list of strings."""
    return [m.group(0) for m in camel_case_pattern.finditer(text)]


def check_titlecased_word(v: str) -> str:
    assert all(bit.istitle for bit in v.split("-")), f"{v} is not titlecased."
    return v


TitledString = Annotated[str, AfterValidator(check_titlecased_word)]


def create_regex_options(texts: Iterable[str]):
    return "(" + "|".join(texts) + ")"


def spacy_re(v: str, anchored: bool = True, op: str | None = None) -> dict[str, Any]:
    """Helper function to add an anchored, i.e. `^`<insert value `v` here>`$`
    regex pattern, following `{"TEXT": {"REGEX": f"^{v}$"}}` spacy convention,
    unless modified by arguments.
    """
    if anchored:
        v = f"^{v}$"
    result = {"TEXT": {"REGEX": v}}
    return result | {"OP": op} if op else result


def spacy_in(v_list: list[str], default: str = "ORTH", op: str | None = None):
    """Helper function to add a specific list of options following
    `{"ORTH": {"IN": v_list}}` spacy convention, unless modified by arguments.
    """
    result = {default: {"IN": v_list}}
    return result | {"OP": op} if op else result


def set_optional_node():
    """Deal with nodes like (R.A.), [PD]"""
    _open = create_regex_options(texts=("\\(", "\\["))
    _close = create_regex_options(texts=("\\)", "\\]"))
    _in = "[\\w\\.]+"
    regex = "".join([_open, _in, _close])
    return spacy_re(v=regex, op="?")


def see(doc: Doc):
    """Rich jupyter-based print spacy-entities and span groups from `doc`."""

    def extract_ents(doc):
        for key in list(set(ent.label_ for ent in doc.ents)):
            data = {"label": key, "ents": []}
            for ent in doc.ents:
                if ent.label_ == key:
                    data["ents"].append(ent.text)
            yield data

    print(list(extract_ents(doc)))
    for spans_key, group in doc.spans.items():
        if spans := [f"{idx}: {v}" for idx, v in enumerate(group)]:
            print(f"{spans_key=}: {spans=}")


def make_uniform_lines(file: Path, min_char: int = 5) -> list[str]:
    """Updates file with sorted lines, filtering those not reaching `min_char` length."""
    raw_lines = file.read_text().splitlines()
    lines = sorted(set(bit for bit in raw_lines if bit.strip() and len(bit) > min_char))
    file.write_text("\n".join(lines))
    return lines


def extract_lines_from_txt_files(files: Iterable[Path]) -> Iterator[str]:
    """For each file listed in the path, extract each line of the file."""
    for file in files:
        if file.suffix != ".txt":
            raise Exception(f"{file=} must be a .txt file separated by lines.")
        yield from make_uniform_lines(file)  # sort before split


def split_data(texts: list[str], ratio: float = 0.80) -> dict[str, set[str]]:
    """The result of splitting `texts` on a ratio = text strings for each category, e.g.:
    {"dev": list of strings (the first 20%), "train": list of strings (the balance of 80%)}
    """
    max_count = len(texts)
    train_count = int(max_count * ratio)
    dev_count = max_count - train_count
    res: dict[str, set[str]] = {"train": set(), "dev": set()}
    for idx, text in enumerate(texts):
        category = res["dev"] if idx < dev_count else res["train"]
        category.add(text)
    return res


def annotate_lines(
    nlp: Language,
    texts: set[str],
    is_readable: bool = True,
) -> Iterator[tuple[str, dict[str, Any]]]:
    """Collects annotated data, consisting of tuples where first item is a string,
    second item is a dict with an `entities` key. If `is_readable is `True`, the annotated texts
    are gathered into a separate `readables` key per entry. Readables not necessary for training
    and are used here to help determine whether the annotations are correct."""
    for doc in nlp.pipe(texts):
        data: dict[str, Any] = {}
        if not doc.ents:
            continue
        data["entities"] = [[e.start, e.end, e.label_] for e in doc.ents]
        if is_readable:
            data["readables"] = [doc[e.start : e.end].text for e in doc.ents]
        yield (doc.text, data)


def annotate_fragments(nlp: Language, target_file: Path, txt_files: Iterable[Path]):
    """Helper function to consolidate all the `txt_files` and extract each line from
    the same for the purpose of annotating it based on the `nlp` object. Each annotation
    will then be written into a `target_file`."""
    texts = set(extract_lines_from_txt_files(txt_files))
    data: list[tuple[str, dict[str, Any]]] = list(annotate_lines(nlp=nlp, texts=texts))
    srsly.write_json(path=target_file, data=data)
    return target_file
