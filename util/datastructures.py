from collections import defaultdict

class DisJointSets():
    def __init__(self, N):
        # Initially, all elements are single element subsets
        self._parents = [node for node in range(N)]
        self._ranks = [1 for _ in range(N)]

    def find(self, u):
        while u != self._parents[u]:
            # path compression technique
            self._parents[u] = self._parents[self._parents[u]]
            u = self._parents[u]
        return u

    def connected(self, u, v):
        return self.find(u) == self.find(v)

    def union(self, u, v):
        # Union by rank optimization
        root_u, root_v = self.find(u), self.find(v)
        if root_u == root_v:
            return True

        # I modified this to have proper rank sizes
        if self._ranks[root_u] > self._ranks[root_v]:
            self._parents[root_v] = root_u
            self._ranks[root_u] += self._ranks[root_v]
        elif self._ranks[root_v] > self._ranks[root_u]:
            self._parents[root_u] = root_v
            self._ranks[root_v] += self._ranks[root_u]
        else:
            self._parents[root_u] = root_v
            self._ranks[root_v] += self._ranks[root_u]
        return False

    join = union

    def n_components(self):
        return sum(parent == i for i, parent in enumerate(self._parents))

    def copy(self):
        new = DisJointSets(len(self._parents))
        new._parents = self._parents[:]
        new._ranks = self._ranks[:]
        return new

    def components(self):
        componentsByRoot = defaultdict(list)
        for i in range(len(self._parents)):
            componentsByRoot[self.find(i)].append(i)
        return componentsByRoot.values()

    def componentRoots(self):
        componentRoots = set()
        for i in range(len(self._parents)):
            componentRoots.add(self.find(i))
        return componentRoots

    def componentSize(self, i):
        return self._ranks[self.find(i)]

    def compressAll(self):
        for i in range(len(self._parents)):
            self.find(i)


class MutableMinHeap:
    def __init__(self):
        self.heap = []
        self.keyIndices = {}
        self.keyValues = {}

    def insert(self, keyVal, element):
        self.heap.append(keyVal)
        self.keyIndices[keyVal] = len(self.heap) - 1
        self.keyValues[keyVal] = element
        self.siftUp(len(self.heap) - 1)

    def top(self):
        return self.heap[0]

    def pop(self) -> tuple:
        out = self.heap[0]
        outValue = self.keyValues[out]
        del self.keyIndices[out]
        del self.keyValues[out]
        # Place last element at index 0.
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        if len(self.heap) > 0:
            self.keyIndices[self.heap[0]] = 0
            self.siftDown(0)
        return out, outValue

    def swap(self, i, j):
        ival, jval = self.heap[i], self.heap[j]
        self.keyIndices[ival] = j
        self.keyIndices[jval] = i
        self.heap[i] = jval
        self.heap[j] = ival

    def siftDown(self, i):
        l = (i + 1) * 2 - 1
        r = (i + 1) * 2
        if l >= len(self.heap):
            return
        else:
            # Obtain the smaller child, and VALUE OF THE LARGEST CHILD
            if r >= len(self.heap):
                b, bval = l, self.keyValues[self.heap[l]]
            else:
                lval = self.keyValues[self.heap[l]]
                rval = self.keyValues[self.heap[r]]
                if lval <= rval:
                    b, bval = l, lval
                else:
                    b, bval = r, rval

            # If needed, swap with smaller child and recurse
            if bval < self.keyValues[self.heap[i]]:
                self.swap(i, b)
                self.siftDown(b)

    def siftUp(self, i):
        if i == 0:
            return

        parent = (i - 1) // 2
        parentVal = self.keyValues[self.heap[parent]]
        if self.keyValues[self.heap[i]] < parentVal:
            self.swap(i, parent)
            self.siftUp(parent)

    def update(self, key, newVal):
        if key not in self.keyValues:
            self.insert(key, newVal)
        else:
            oldVal = self.keyValues[key]
            self.keyValues[key] = newVal
            if newVal < oldVal:
                self.siftUp(self.keyIndices[key])
            elif newVal > oldVal:
                self.siftDown(self.keyIndices[key])

    def update_lower(self, key, newVal):
        if not (key in self.keyValues and self.keyValues[key] <= newVal):
            self.update(key, newVal)

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return str([(key, self.keyValues[key]) for key in self.heap]) + str(self.keyIndices)


# Ring buffer.

class KeyedItem:
    def __init__(self, items, key, negated=False):
        self.items = items
        self.key = key
        self.negated = negated

    def __lt__(self, other):
        return self.key(*self.items).__lt__(other.key(*other.items)) if not self.negated else other.key(
            *other.items).__lt__(self.key(*self.items))

    def __str__(self):
        return str(self.items)

    def __repr__(self):
        return str(self)


class MyCircularDeque:
    def __init__(self, k: int):
        self.buffer = [None] * k
        self.back = 1
        self.front = 0
        self.size = 0
        self.k = k

    def forceInsert(self, value: int):
        if self.isFull():
            self.deleteLast()
        self.insertFront(value)

    def insertFront(self, value: int) -> bool:
        if self.size >= self.k:
            return False
        else:
            self.front = (self.front + 1) % self.k
            self.size += 1
            self.buffer[self.front] = value
            return True

    def insertLast(self, value: int) -> bool:
        if self.size >= self.k:
            return False
        else:
            self.back = (self.back - 1) % self.k
            self.size += 1
            self.buffer[self.back] = value
            return True

    def deleteFront(self) -> bool:
        if self.size == 0:
            return False
        else:
            self.size -= 1
            self.front = (self.front - 1) % self.k
            return True

    def deleteLast(self) -> bool:
        if self.size == 0:
            return False
        else:
            self.size -= 1
            self.back = (self.back + 1) % self.k
            return True

    def getFront(self) -> int:
        if self.size <= 0:
            return -1
        else:
            return self.buffer[self.front]

    def getRear(self) -> int:
        if self.size <= 0:
            return -1
        else:
            return self.buffer[self.back]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size >= self.k

    def __len__(self):
        return self.size

    def __getitem__(self, i):
        # Index from the front.
        if i >= self.size:
            raise IndexError

        return self.buffer[(self.front - i) % self.k]


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        self.root.insert(word)
        # print(self.root)

    def search(self, word: str) -> bool:
        found = self.root.seek(word)
        # print(word, "found", found)
        return found is not None and found.terminal

    def startsWith(self, prefix: str) -> bool:
        # print(prefix, "starts with found", self.root.seek(prefix))
        return self.root.seek(prefix) is not None


class TrieNode:
    def __init__(self):
        self.children = {}
        self.terminal = False

    def insert(self, seq, i=0):
        if i >= len(seq):
            self.terminal = True
        else:
            c = seq[i]
            if c not in self.children:
                self.children[c] = TrieNode()
            self.children[c].insert(seq, i + 1)

    def seek(self, seq, i=0):
        if i >= len(seq):
            return self

        c = seq[i]
        if c in self.children:
            return self.children[c].seek(seq, i + 1)
        else:
            return None

    def __str__(self):
        return "<" + ", ".join(f"{c}:{child}" for c, child in self.children.items()) + "$" * self.terminal + ">"
