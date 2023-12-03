# Markdown line block extension

[![PyPI - Version](https://img.shields.io/pypi/v/markdown-lineblocks.svg)](https://pypi.org/project/markdown-lineblocks)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/markdown-lineblocks.svg)](https://pypi.org/project/markdown-lineblocks)

A [Python-Markdown](https://python-markdown.github.io/) extension to render line blocks.

Example:
```
| Normally these lines would
| Run together. But here
| They are separate
```


-----

## Installation

```console
pip install markdown-lineblocks
```

## Usage

```py
import markdown
text = ...  # your Markdown source
html = markdown.markdown(text, extensions='lineblocks')
```

To use with [MkDocs](https://www.mkdocs.org/), add the following to `mkdocs.yml`:
```yaml
markdown_extensions:
  - lineblocks
```


## Licence

`markdown-lineblocks` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) licence.
