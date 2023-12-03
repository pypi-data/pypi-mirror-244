# Markdown grid table extension

[![PyPI - Version](https://img.shields.io/pypi/v/markdown-grids.svg)](https://pypi.org/project/markdown-grids)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/markdown-grids.svg)](https://pypi.org/project/markdown-grids)

A [Python-Markdown](https://python-markdown.github.io/) extension to render grid tables.

Example:
```
+-------------------+------------------+----------------+
| Header 1          | Header 2         | Header 3       |
+===================+==================+================+
| Cells can span multiple columns      | Cells can span |
+--------------------------------------+ multiple rows  |
| Text in cells *can be* **formatted** |                |
|                                      |                |
| > and can contain arbitrary          |                |
| > multi-line blocks                  |                |
+--------------------------------------+----------------+
```


-----

## Installation

```console
pip install markdown-grids
```

## Usage

```py
import markdown
text = ...  # your Markdown source
html = markdown.markdown(text, extensions='grids')
```

To use with [MkDocs](https://www.mkdocs.org/), add the following to `mkdocs.yml`:
```yaml
markdown_extensions:
  - grids
```

Because whitespace in a grid table is structural, it is not possible to indicate a newline in a
cell with two spaces at the end of the line.
Two possible solutions to this are:
- The [New-Line-to-Break extension](https://python-markdown.github.io/extensions/nl2br/)
- The [Markdown line block extension](https://github.com/mjayfrancis/markdown-grids)


## Licence

`markdown-grids` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) licence.
