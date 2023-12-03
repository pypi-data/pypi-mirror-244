# SPDX-FileCopyrightText: 2023 Matthew Francis <mjay.francis@gmail.com>
#
# SPDX-License-Identifier: MIT
"""
Line blocks extension for Python-Markdown
"""

from __future__ import annotations

import logging
import re
from xml.etree import ElementTree

from markdown import Extension, Markdown
from markdown.blockprocessors import BlockProcessor

logger = logging.getLogger("markdown_lineblocks")


class LineBlockProcessor(BlockProcessor):
    """Markdown BlockProcessor for line blocks."""

    _first_line_pattern = re.compile(
        r"""
        \|               # A pipe character
        (                # followed by, optionally,
            \            # a space
            (            # then either nothing or
                .*[^|]   # any number of characters not ending in a pipe
            )?
        )?
        $                # with nothing else following
    """,
        re.VERBOSE,
    )

    _line_block_pattern = re.compile(
        r"""
        ^                # Start of line, then
        \|               # a pipe character
        (?:              # followed by, optionally,
            \ .*         # a space and any number of characters
            (?:          # then, zero or more times,
                \n       # a new line followed by
                \ {2}.*  # two spaces and any number of characters
            )*
        )?
        $                # End of line
    """,
        re.VERBOSE | re.MULTILINE,
    )

    def test(self, parent: ElementTree.Element, block: str):  # noqa:ARG002
        first_line = block.split('\n')[0]
        return self._first_line_pattern.match(first_line)

    def run(self, parent: ElementTree.Element, blocks: list[str]):
        block = blocks.pop(0)

        last_match_end = -1
        lines = []
        for match in self._line_block_pattern.finditer(block):
            if match.start(0) == last_match_end + 1:
                lines.append(match[0])
                last_match_end = match.end(0)
            else:
                remainder = block[last_match_end + 1 :]
                blocks.insert(0, remainder)
                break

        split_lines = [[part[2:] for part in line.split('\n')] for line in lines]
        formatted_block = '<br />\n'.join('\n'.join(split_line) for split_line in split_lines)
        self.parser.parseBlocks(parent, [formatted_block])


class LineBlockExtension(Extension):
    def extendMarkdown(self, md: Markdown):  # noqa:N802
        blockprocessors = md.parser.blockprocessors
        blockprocessors.register(LineBlockProcessor(md.parser), 'lineblocks', 101)


def makeExtension(**kwargs):  # noqa:N802
    return LineBlockExtension(**kwargs)
