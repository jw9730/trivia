INCLUDE_TEST = [1, 2, 3, 4, 5, 6, 7]


# If your implementation runs forever,
# grading does not finish in time. 
# Modify the global variable `INCLUDE_TEST` in 
# `implement_me.py` to select the tests.


class Pointer:
    """
    A pointer that corresponds to a key in a binomial heap.
    """

    def __init(self):
        self.node = None

    def get_key(self):
        """
        Returns the key in the binomial heap that this pointer corresponds to.
        Returns `None` if the key corresponding to this pointer
        is not contained in any binomial heap.

        Works in constant time.

        Returns
        -------
        int or float
            The key in the binomial heap that this pointer corresponds to.
            `None` if the key corresponding to this pointer
            is not contained in any binomial heap.
        """
        if self.node is None:
            return None
        return self.node.key

    def decrease_key(self, new_key):
        """
        Decreases the corresponding key to `new_key` in the binomial heap.
        Internal state of the binomial heap may be altered.
        Its behavior is undefined if the key is strictly less
        than `new_key` or the key is not contained in any binomial heap.

        Works in logarithmic time.

        Parameters
        ----------
        new_key : int or float
        """
        c = self.node
        # assert c is not None
        # assert c.key >= new_key

        c.key = new_key
        while type(c.parent) is not BinomialHeap and c.parent.key > new_key:
            # swap with parent: k, parent, children
            p = c.parent
            # assert c in p.children

            # swap key and ptr
            c.key, p.key = p.key, c.key
            c.ptr.node = p
            p.ptr.node = c
            c.ptr, p.ptr = p.ptr, c.ptr

            # increment c
            c = p

    def get_bh(self):
        # get root of binomial tree
        # get binomial heap object
        e = self.node
        while type(e.parent) is not BinomialHeap:
            e = e.parent
        return e.parent

    def delete_key(self):
        """
        Deletes the corresponding key in the binomial heap.
        Internal structure of the binomial heap may be altered.
        Its behavior is undefined if the key is not contained
        in any binomial heap.

        Works in logarithmic time.
        """
        self.decrease_key(-1e10)
        minkey = self.get_bh().extract_min()
        # assert minkey == -1e10


def is_power_of_two(n):
    return (n != 0) and (n & (n - 1) == 0)


def _merge(l, r):
    """
    :param l: Node() or None
    :param r: Node() or None
    :return: Node(), with r's parent as parent (or None)
    """
    # None-case
    if l is None:
        return r
    if r is None:
        return l

    # merge two Bk
    # assert l.k == r.k
    # print(f"merge trees: degree {l.k}, l {l.key} + r {r.key}")
    if l.key < r.key:
        # swap l and r to maintain heap order
        l, r = r, l
    # merge and update
    r.children.insert(0, l)
    l.parent = r
    # assert l in r.children
    r.k += 1
    # print(f"merge trees: degree {r.k}, merged root key {r.key}")
    return r


def _make_tree(keys):
    # compute k
    # assert is_power_of_two(len(keys))
    k = len(keys).bit_length() - 1

    # if k = 0, make a single-node tree
    if k == 0:
        return Node(key=keys[0])

    # recursively make two k-1 trees
    l_keys = keys[0:2 ** (k - 1)]
    r_keys = keys[2 ** (k - 1):]
    # assert len(l_keys) == len(r_keys)

    # recursively make k-1 trees and merge
    l = _make_tree(l_keys)
    r = _make_tree(r_keys)
    return _merge(l, r)


class Node:
    def __init__(self, key=None, parent=None):
        self.k = 0
        self.key = key
        self.parent = parent  # Node() or BinomialHeap()
        self.children = list()
        self.ptr = None


def _find(k, roots):
    for root in roots:
        if root.k == k:
            return root
    return None


def _step(k, l, r, carry):
    """
    :param k: int
    :param l: None or Node() with BinomialHeap() as parent
    :param r: None or Node() with BinomialHeap() as parent
    :param carry: None or Node()
    :return: (current, carry)
    """
    # l + r
    current = _merge(l, r)
    if current is None:
        # l and r was None
        # if carry is not None:
        #     assert carry.k == k
        return carry, None
    if current.k == k + 1:
        # l + r overflow
        return carry, current
    # l + r no overflow
    # assert current.k == k

    # l + r + carry
    current = _merge(current, carry)
    if current.k == k + 1:
        # l + r + carry overflow
        return None, current
    # l + r + carry no overflow
    # assert current.k == k
    return current, None


class BinomialHeap:
    """
    A binomial heap that stores keys of type `int` and `float`.
    Keys can be inserted and deleted. It is allowed to have duplicate keys.
    """

    def __init__(self):
        """
        Creates an empty binomial heap.

        Works in constant time.
        """
        self.roots = list()

    def insert(self, key):
        """
        Inserts a key to this binomial heap.

        Works in logarithmic time.

        Parameters
        ----------
        key : int or float

        Returns
        -------
        Pointer
            A pointer that corresponds to the inserted key.
        """
        bh = BinomialHeap()
        node = Node(key=key, parent=bh)
        bh.roots = [node]

        # print(f"insert: current roots {[(root.k, root.key) for root in self.roots]}, to-merge roots {[(root.k, root.key) for root in bh.roots]}")

        self.merge(bh)

        # print(f"insert: result bh roots {[(root.k, root.key) for root in self.roots]}")

        p = Pointer()
        p.node = node
        node.ptr = p
        return p

    def peek_min(self):
        """
        Peeks, but does not delete, the minimum key in the
        binomial heap. If there are multiple minimum keys,
        returns any one of them. If there are no keys,
        returns `None`.

        Works in logarithmic time.

        Returns
        -------
        int or float
            The minimum key in the binomial heap.
        """
        if len(self.roots) == 0:
            return None
        # print(f"current roots: {[node.key for node in self.roots]}")
        return min([node.key for node in self.roots])

    def extract_min(self):
        """
        Extracts the minimum key from the binomial heap.
        Extracted key is deleted from the binomial heap.
        If there are multiple minimum keys,
        extracts any one of them. If there are no keys,
        returns `None`.

        Works in logarithmic time.

        Returns
        -------
        int or float
            The minimum key in the binomial heap. `None` if
            the binomal heap is empty.
        """
        if len(self.roots) == 0:
            return None

        # print(f"extract-min: roots {[(root.k, root.key) for root in self.roots]}")

        min_root = min(self.roots, key=lambda x: x.key)
        self.roots.remove(min_root)
        assert min_root not in self.roots

        # invalidate pointer
        if min_root.ptr is not None:
            min_root.ptr.node = None
            min_root.ptr = None

        bh = BinomialHeap()
        bh.roots = min_root.children[::-1]
        for node in min_root.children:
            assert node.parent == min_root
            node.parent = bh

        if len(bh.roots) != 0:
            self.merge(bh)

        return min_root.key

    def merge(self, bh):
        """
        Merges two binomial heaps, `self` and `bh`.
        Keys contained in `bh` are merged into `self`.
        All pointers that correspond to the keys in `bh` are maintaind.
        After execution of this method, all behaviors of `bh` are undefined.

        Works in logarithmic time.

        Parameters
        ----------
        bh : BinomialHeap
        """
        if len(self.roots + bh.roots) == 0:
            new_roots = list()
            self.roots = new_roots
            return

        max_k = max(self.roots + bh.roots, key=lambda x: x.k).k

        # print(f"merge: self trees {[(root.k, root.key) for root in self.roots]}, bh trees {[(root.k, root.key) for root in bh.roots]}, max degree {max_k}")

        new_roots = list()
        carry = None
        for k in range(max_k + 1):
            b1 = _find(k, self.roots)
            b2 = _find(k, bh.roots)
            # detach from previous BH
            if b1 is not None:
                self.roots.remove(b1)
                b1.parent = None
            if b2 is not None:
                bh.roots.remove(b2)
                b2.parent = None

            # print(f"merge: iteration {k}, b1 {b1}, b2 {b2}, carry {carry}")

            # compute current and carry
            current, carry = _step(k, b1, b2, carry)

            # print(f"merge: iteration {k}, current {current}, carry {carry}")

            if current is not None:
                assert current.k == k
                current.parent = self
                new_roots.append(current)
                # print(f"merge: merged roots extended to {new_roots}")

        # handle last carry
        if carry is not None:
            assert carry.k == max_k + 1
            carry.parent = self
            new_roots.append(carry)
            # print(f"merge: merged roots extended to {new_roots}")

        self.roots = new_roots
