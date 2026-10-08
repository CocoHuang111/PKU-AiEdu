> 检索摘要：6.006 Introduction to Algorithms（Fall 2011，Undergraduate）的「Readings Binary Search Trees」。页内标题：Readings Binary Search Trees；Simple BST (no balancing)；AVL tree；Testing。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/pages/readings/binary-search-trees/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Readings Binary Search Trees

This page contains various implementations of different Binary Search Trees (BSTs).

### Simple BST (no balancing)

- [bst.py (PY)](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/bst/)
  - Features: insert, find, delete_min, ASCII art
- [bstsize.py (PY)](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/bstsize/)
  - Imports and extends bst.py
  - Augmentation to compute subtree sizes
- [bstsize_r.py](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/bstsize_r/)
  - Recursive version from recitation for computing subtree sizes
  - Features: insert, find, rank, delete

### AVL tree

- [avl.py (PY)](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/avl/)
  - Imports and extends bst.py
  - Features: insert, find, delete_min, ASCII art

### Testing

Both bst.py and avl.py (as well as bstsize.py) can be tested interactively from a UNIX shell as follows:

- python bst.py 10 — do 10 random insertions, printing BST at each step
- python avl.py 10 — do 10 random insertions, printing AVL tree at each step

Alternatively, you can use them from a Python shell as follows:

```
>>> import bst >>> t = bst.BST() >>> print t >>> for i in range(4): ... t.insert(i); ... >>> print t 0 /\ 1 /\ 2 /\ 3 /\ >>> t.delete_min() >>> print t 1 /\ 2 /\ 3 /\
```

```
>>> import avl >>> t = avl.AVL() >>> print t >>> for i in range(4): ... t.insert(i); ... >>> print t 1 / \ 0 2 /\ /\ 3 /\ >>> t.delete_min() >>> print t 2 / \ 1 3 /\ /\
```
