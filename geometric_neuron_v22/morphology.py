from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class CableEdge:
    parent: int
    child: int
    length: float
    area: float
    source: str = ""

    def __post_init__(self) -> None:
        if self.parent == self.child:
            raise ValueError("self-edge")
        if not np.isfinite(self.length) or self.length <= 0:
            raise ValueError(f"invalid cable length: {self.length}")
        if not np.isfinite(self.area) or self.area <= 0:
            raise ValueError(f"invalid cable area: {self.area}")


@dataclass(frozen=True)
class CableTree:
    n_nodes: int
    root: int
    edges: tuple[CableEdge, ...]

    def __post_init__(self) -> None:
        if self.n_nodes < 2:
            raise ValueError("a cable tree needs at least two nodes")
        if not 0 <= self.root < self.n_nodes:
            raise ValueError("root outside node range")
        if len(self.edges) != self.n_nodes - 1:
            raise ValueError("expected a connected tree: edges != nodes - 1")

        parents = set()
        touched = {self.root}
        for edge in self.edges:
            if not 0 <= edge.parent < self.n_nodes or not 0 <= edge.child < self.n_nodes:
                raise ValueError("edge endpoint outside node range")
            if edge.child == self.root:
                raise ValueError("root cannot have a parent")
            if edge.child in parents:
                raise ValueError("node has more than one parent")
            parents.add(edge.child)
            touched.add(edge.parent)
            touched.add(edge.child)
        if len(touched) != self.n_nodes:
            raise ValueError("tree contains untouched nodes")

        # Directed reachability catches cycles/disconnected components that pass counts.
        children = self.children()
        seen: set[int] = set()
        stack = [self.root]
        while stack:
            node = stack.pop()
            if node in seen:
                raise ValueError("cycle detected")
            seen.add(node)
            stack.extend(children[node])
        if len(seen) != self.n_nodes:
            raise ValueError("tree is not fully reachable from root")

    def children(self) -> list[list[int]]:
        out = [[] for _ in range(self.n_nodes)]
        for edge in self.edges:
            out[edge.parent].append(edge.child)
        return out

    def edge_lookup(self) -> dict[tuple[int, int], CableEdge]:
        return {(edge.parent, edge.child): edge for edge in self.edges}

    @property
    def total_length(self) -> float:
        return float(sum(edge.length for edge in self.edges))

    @property
    def total_area(self) -> float:
        return float(sum(edge.area for edge in self.edges))

    @property
    def number_of_forking_points(self) -> int:
        children = self.children()
        return sum(1 for node, kids in enumerate(children) if node != self.root and len(kids) >= 2)

    @property
    def number_of_bifurcations(self) -> int:
        children = self.children()
        return sum(1 for node, kids in enumerate(children) if node != self.root and len(kids) == 2)

    @property
    def number_of_leaves(self) -> int:
        children = self.children()
        return sum(1 for node, kids in enumerate(children) if node != self.root and not kids)

    @property
    def longest_root_to_tip_path(self) -> float:
        children = self.children()
        lookup = self.edge_lookup()
        distance = np.full(self.n_nodes, -np.inf, dtype=float)
        distance[self.root] = 0.0
        stack = [self.root]
        while stack:
            parent = stack.pop()
            for child in children[parent]:
                distance[child] = distance[parent] + lookup[(parent, child)].length
                stack.append(child)
        leaves = [node for node, kids in enumerate(children) if node != self.root and not kids]
        if not leaves:
            raise ValueError("tree has no terminal tips")
        return float(max(distance[node] for node in leaves))

    def basic_features(self) -> dict[str, float | int]:
        return {
            "n_nodes": self.n_nodes,
            "n_edges": len(self.edges),
            "total_dendritic_length": self.total_length,
            "total_dendritic_area": self.total_area,
            "number_of_forking_points": self.number_of_forking_points,
            "number_of_bifurcations": self.number_of_bifurcations,
            "number_of_leaves": self.number_of_leaves,
            "longest_root_to_tip_path": self.longest_root_to_tip_path,
        }


def _section_length(points: np.ndarray) -> float:
    xyz = np.asarray(points, dtype=float)[:, :3]
    if len(xyz) < 2:
        raise ValueError("section contains fewer than two points")
    return float(np.linalg.norm(np.diff(xyz, axis=0), axis=1).sum())


def load_neurom_cable_tree(path: str | Path) -> CableTree:
    """Load one ASC/SWC/H5 morphology and collapse it to NeuroM sections.

    NeuroM sections already run between structural events (root/fork/tip), which is
    the collapse wanted by the V22 preregistration. All non-axon neurites share one
    abstract soma/root node. Soma membrane area itself is not included in the
    dendritic-area total.

    NeuroM is imported lazily so core operator tests do not require it.
    """

    try:
        import neurom as nm
    except ImportError as exc:  # pragma: no cover - exercised in real-data workflow
        raise RuntimeError(
            "NeuroM is required for morphology files. Install with "
            "`pip install -e '.[morphology]'`."
        ) from exc

    morphology = nm.load_morphology(str(Path(path)))
    root = 0
    next_node = 1
    edges: list[CableEdge] = []

    for neurite_index, neurite in enumerate(morphology.neurites):
        if neurite.type == nm.AXON:
            continue

        endpoint_by_section: dict[int, int] = {}
        for section in nm.iter_sections(neurite):
            if section.parent is None:
                parent_node = root
            else:
                try:
                    parent_node = endpoint_by_section[section.parent.id]
                except KeyError as exc:
                    raise ValueError(
                        "NeuroM section iteration was not parent-before-child"
                    ) from exc

            child_node = next_node
            next_node += 1
            endpoint_by_section[section.id] = child_node

            length = _section_length(section.points)
            area = float(section.area)
            edges.append(
                CableEdge(
                    parent=parent_node,
                    child=child_node,
                    length=length,
                    area=area,
                    source=f"neurite={neurite_index};section={section.id}",
                )
            )

    if not edges:
        raise ValueError(f"no non-axon cable sections found in {path}")

    return CableTree(n_nodes=next_node, root=root, edges=tuple(edges))


def make_tree(edges: Iterable[CableEdge], root: int = 0) -> CableTree:
    edges = tuple(edges)
    maximum = max(max(e.parent, e.child) for e in edges)
    return CableTree(n_nodes=maximum + 1, root=root, edges=edges)
