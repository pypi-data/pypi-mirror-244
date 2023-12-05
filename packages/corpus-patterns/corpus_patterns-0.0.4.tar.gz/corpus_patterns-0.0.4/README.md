# corpus-patterns

![Github CI](https://github.com/justmars/corpus-patterns/actions/workflows/main.yml/badge.svg)

A preparatory utils library.

## Create a custom tokenizer

```py
from corpus_patterns import set_tokenizer

nlp = spacy.blank("en")
nlp.tokenizer = set_tokenizer(nlp)
```

The tokenizer:

1. Removes dashes from infixes
2. Adds prefix/suffix rules for parenthesis/brackets
3. Adds special exceptions to treat dotted text as a single token

## Add .jsonl files to directory

Each file will contain lines of spacy matcher patterns.

```py
from corpus_patterns import create_rules
from pathlib import Path

create_rules(folder=Path(Path("location-here")))  # check directory
```

## Utils

1. `annotate_fragments()` - given an nlp object and some `*.txt` files, create a single annotation `*.jsonl` file
2. `extract_lines_from_txt_files()` - accepts an iterator of `*.txt` files and yields each line (after sorting the same and ensuring uniqueness of content).
3. `split_data()` - given a list of text strings, split the same into two groups and return a dictionary containing these groups based on the ratio provided (defaults to 0.80)
