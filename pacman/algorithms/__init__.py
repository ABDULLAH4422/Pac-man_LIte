"""
Algorithms Package for Pac-Man Lite
ECE 2103: Data Structures & Algorithms
Implements BFS, DFS, A*, and Sorting algorithms using the custom DSA structures.
"""

from .bfs import bfs_search
from .dfs import dfs_search
from .astar import astar_search
from .sorting import quick_sort, merge_sort

__all__ = [
    'bfs_search',
    'dfs_search',
    'astar_search',
    'quick_sort',
    'merge_sort'
]
