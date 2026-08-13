from __future__ import annotations

from pathlib import Path

from .morphology import CableEdge, CableTree, load_neurom_cable_tree


def collapse_unifurcations(tree: CableTree) -> CableTree:
    """Contract non-root nodes that have exactly one child.

    Length and membrane area are additive along the contracted cable, so ordinary
    morphology totals and root-to-tip cable distances are preserved. The resulting
    nodes are only the abstract soma/root, true forks, and terminal tips.
    """
    children = tree.children()
    lookup = tree.edge_lookup()
    one_child = [
        node for node, kids in enumerate(children)
        if node != tree.root and len(kids) == 1
    ]
    if not one_child:
        return tree

    new_id = {tree.root: 0}
    next_id = 1
    edges: list[CableEdge] = []

    def node_id(old: int) -> int:
        nonlocal next_id
        if old not in new_id:
            new_id[old] = next_id
            next_id += 1
        return new_id[old]

    def follow(parent_old: int, parent_new: int, child_old: int) -> None:
        first = lookup[(parent_old, child_old)]
        length = first.length
        area = first.area
        sources = [first.source] if first.source else []
        cursor = child_old

        while len(children[cursor]) == 1:
            nxt = children[cursor][0]
            edge = lookup[(cursor, nxt)]
            length += edge.length
            area += edge.area
            if edge.source:
                sources.append(edge.source)
            cursor = nxt

        child_new = node_id(cursor)
        edges.append(CableEdge(
            parent=parent_new,
            child=child_new,
            length=length,
            area=area,
            source="|".join(sources),
        ))
        for nxt in children[cursor]:
            follow(cursor, child_new, nxt)

    for child in children[tree.root]:
        follow(tree.root, 0, child)

    out = CableTree(n_nodes=next_id, root=0, edges=tuple(edges))
    out_children = out.children()
    if any(
        node != out.root and len(kids) == 1
        for node, kids in enumerate(out_children)
    ):
        raise AssertionError("unifurcation contraction failed")
    return out


def load_structural_cable_tree(path: str | Path) -> CableTree:
    """Load morphology and remove tracing-only one-child section boundaries."""
    return collapse_unifurcations(load_neurom_cable_tree(path))
