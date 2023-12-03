# SPDX-FileCopyrightText: 2023 Matthew Francis <mjay.francis@gmail.com>
#
# SPDX-License-Identifier: MIT
"""
Grid tables extension for Python-Markdown
"""

from __future__ import annotations

import logging
import re
from itertools import count, groupby
from textwrap import dedent
from typing import MutableMapping, NamedTuple, Sequence
from xml.etree import ElementTree

from markdown import Extension, Markdown
from markdown.blockprocessors import BlockProcessor

logger = logging.getLogger("markdown_grids")


class Address(NamedTuple):
    """A character address within a text table."""

    y: int
    x: int


class Node(NamedTuple):
    """A node in the graph of a parsed text table."""

    address: Address
    cell_end_address: Address | None
    down: Node | None
    right: Node | None
    content: str


class Cell(NamedTuple):
    """A cell parsed from a text table."""

    rowspan: int
    colspan: int
    content: str


class GridTableOps:
    """Operations that examine a grid table."""

    _header_edge_pattern = re.compile('\\+=+\\+')

    _text: Sequence[str]

    def find_right(self, from_address: Address) -> Address | None:
        """Find the next node (+) in the table to the right of an address."""
        line = self._text[from_address.y]
        for i in range(from_address.x + 1, len(self._text[from_address.y])):
            char = line[i]
            if char == '+':
                return Address(from_address.y, i)
            if char not in ('-', '='):
                break
        return None

    def find_down(self, from_address: Address) -> Address | None:
        """Find the next node (+) in the table downwards from an address."""
        for i in range(from_address.y + 1, len(self._text)):
            if from_address.x >= len(self._text[i]):
                break
            char = self._text[i][from_address.x]
            if char == '+':
                return Address(i, from_address.x)
            if char != '|':
                break
        return None

    def is_header_edge(self, from_address: Address) -> bool:
        """Test if the edge to the right of an address is a header edge"""
        return bool(self._header_edge_pattern.match(self._text[from_address.y][from_address.x :]))

    def get_text_rect(self, from_address: Address, to_address: Address) -> Sequence[str]:
        """Get text from the rectangle between two addresses."""
        lines = [
            self._text[y][from_address.x + 1 : to_address.x].rstrip() for y in range(from_address.y + 1, to_address.y)
        ]

        # Dedent content by one space if possible
        if all(line[:1] in ('', ' ') for line in lines):
            lines = [line[1:] for line in lines]

        return lines

    def __init__(self, text: Sequence[str]):
        self._text = text


class GridTableGraph:
    """Builds a directed acyclic graph representing a grid table."""

    all_nodes: Sequence[Node]
    header_nodes: Sequence[Node]
    body_nodes: Sequence[Node]

    def __init__(self, grid_table_ops: GridTableOps):
        node_cache: MutableMapping[Address, Node] = {}

        def find_cell_end(down: Node, right: Node) -> Address:
            down_search_node = down
            while down_search_node.down and not down_search_node.right:
                down_search_node = down_search_node.down

            right_search_node = right
            while right_search_node.right and not right_search_node.down:
                right_search_node = right_search_node.right

            return Address(down_search_node.address.y, right_search_node.address.x)

        def recurse(address: Address | None) -> Node | None:
            if address is None:
                return None
            if address in node_cache:
                return node_cache[address]

            down = recurse(grid_table_ops.find_down(address))
            right = recurse(grid_table_ops.find_right(address))

            if down and right:
                cell_end_address = find_cell_end(down, right)
                content = '\n'.join(grid_table_ops.get_text_rect(address, cell_end_address))
            else:
                cell_end_address = None
                content = ''

            node = Node(address=address, cell_end_address=cell_end_address, down=down, right=right, content=content)
            node_cache[address] = node
            return node

        root = recurse(Address(0, 0))
        assert root is not None

        self.all_nodes = sorted(node_cache.values())
        start_of_body = search_node = self.all_nodes[0]
        while search_node.down:
            search_node = search_node.down
            if grid_table_ops.is_header_edge(search_node.address):
                start_of_body = search_node
                break

        self.header_nodes = [n for n in self.all_nodes if n.cell_end_address and n < start_of_body]
        self.body_nodes = [n for n in self.all_nodes if n.cell_end_address and n >= start_of_body]

        # There should be only one target node (bottom right)
        if len({n for n in self.all_nodes if not n.down and not n.right}) > 1:
            logger.warning(
                'Error in grid table format: Non-rectangular table cell or broken internal line. '
                'Some cells may not be rendered correctly'
            )


class GridTableParser:
    """Parses a grid table."""

    header_rows: Sequence[Sequence[Cell]]
    body_rows: Sequence[Sequence[Cell]]

    def __init__(self, text: Sequence[str]):
        graph = GridTableGraph(GridTableOps(text))

        y_to_row = dict(zip(sorted({node.address.y for node in graph.all_nodes}), count()))
        x_to_col = dict(zip(sorted({node.address.x for node in graph.all_nodes}), count()))

        def rows(nodes: Sequence[Node]):
            return [
                [
                    Cell(
                        rowspan=y_to_row[node.cell_end_address.y] - y_to_row[node.address.y],  # type: ignore
                        colspan=x_to_col[node.cell_end_address.x] - x_to_col[node.address.x],  # type: ignore
                        content=node.content,
                    )
                    for node in row
                ]
                for _, row in groupby(nodes, lambda n: n.address.y)
            ]

        self.header_rows = rows(graph.header_nodes)
        self.body_rows = rows(graph.body_nodes)


class GridTableProcessor(BlockProcessor):
    """Markdown BlockProcessor for grid tables."""

    _table_start_end_pattern = re.compile('^\\+(-+(\\+-+)*)\\+$')
    _table_second_line_pattern = re.compile('^\\|(.*)\\|$')

    def test(self, parent: ElementTree.Element, block: str):  # noqa:ARG002
        lines = [line.rstrip() for line in dedent(block).split('\n')]

        if len(lines) >= 3:  # noqa:PLR2004
            start_match = self._table_start_end_pattern.match(lines[0])
            second_line_match = self._table_second_line_pattern.match(lines[1])
            end_match = self._table_start_end_pattern.match(lines[-1])
            return start_match and second_line_match and end_match

        return False

    def run(self, parent: ElementTree.Element, blocks: list[str]):
        block = blocks.pop(0)
        lines = [line.rstrip() for line in dedent(block).split('\n')]

        if len({*map(len, lines)}) > 1:
            logger.warning(
                'Error in grid table format: One or more table lines differ in length. Falling back to plain text'
            )
            pre_element = ElementTree.SubElement(parent, 'pre')
            pre_element.text = '\n'.join(lines)
        else:
            grid_table_parser = GridTableParser(lines)
            table_element = ElementTree.SubElement(parent, 'table')

            def render_table_section(section_tag: str, cell_tag: str, rows: Sequence[Sequence[Cell]]):
                section_element = ElementTree.SubElement(table_element, section_tag)
                for row in rows:
                    row_element = ElementTree.SubElement(section_element, 'tr')
                    for cell in row:
                        cell_element = ElementTree.SubElement(row_element, cell_tag)
                        if cell.colspan > 1:
                            cell_element.set('colspan', f'{cell.colspan}')
                        if cell.rowspan > 1:
                            cell_element.set('rowspan', f'{cell.rowspan}')
                        content_blocks = cell.content.split('\n\n')
                        self.parser.parseBlocks(cell_element, content_blocks)

            if grid_table_parser.header_rows:
                render_table_section('thead', 'th', grid_table_parser.header_rows)

            render_table_section('tbody', 'td', grid_table_parser.body_rows)


class GridTableExtension(Extension):
    def extendMarkdown(self, md: Markdown):  # noqa:N802
        blockprocessors = md.parser.blockprocessors
        blockprocessors.register(GridTableProcessor(md.parser), 'grids', 101)


def makeExtension(**kwargs):  # noqa:N802
    return GridTableExtension(**kwargs)
