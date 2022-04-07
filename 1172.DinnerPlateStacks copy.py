"""
You have an infinite number of stacks arranged in a row and numbered (left to right) from 0, each of the stacks has the same maximum capacity.

Implement the DinnerPlates class:

DinnerPlates(int capacity) Initializes the object with the maximum capacity of the stacks capacity.
void push(int val) Pushes the given integer val into the leftmost stack with a size less than capacity.
int pop() Returns the value at the top of the rightmost non-empty stack and removes it from that stack, and returns -1 if all the stacks are empty.
int popAtStack(int index) Returns the value at the top of the stack with the given index index and removes it from that stack or returns -1 if the stack with that given index is empty.
 

Example 1:

Input
["DinnerPlates", "push", "push", "push", "push", "push", "popAtStack", "push", "push", "popAtStack", "popAtStack", "pop", "pop", "pop", "pop", "pop"]
[[2], [1], [2], [3], [4], [5], [0], [20], [21], [0], [2], [], [], [], [], []]
Output
[null, null, null, null, null, null, 2, null, null, 20, 21, 5, 4, 3, 1, -1]

Explanation: 
DinnerPlates D = DinnerPlates(2);  // Initialize with capacity = 2
D.push(1);
D.push(2);
D.push(3);
D.push(4);
D.push(5);         // The stacks are now:  2  4
                                           1  3  5
                                           ﹈ ﹈ ﹈
D.popAtStack(0);   // Returns 2.  The stacks are now:     4
                                                       1  3  5
                                                       ﹈ ﹈ ﹈
D.push(20);        // The stacks are now: 20  4
                                           1  3  5
                                           ﹈ ﹈ ﹈
D.push(21);        // The stacks are now: 20  4 21
                                           1  3  5
                                           ﹈ ﹈ ﹈
D.popAtStack(0);   // Returns 20.  The stacks are now:     4 21
                                                        1  3  5
                                                        ﹈ ﹈ ﹈
D.popAtStack(2);   // Returns 21.  The stacks are now:     4
                                                        1  3  5
                                                        ﹈ ﹈ ﹈ 
D.pop()            // Returns 5.  The stacks are now:      4
                                                        1  3 
                                                        ﹈ ﹈  
D.pop()            // Returns 4.  The stacks are now:   1  3 
                                                        ﹈ ﹈   
D.pop()            // Returns 3.  The stacks are now:   1 
                                                        ﹈   
D.pop()            // Returns 1.  There are no stacks.
D.pop()            // Returns -1.  There are still no stacks.
 

Constraints:

1 <= capacity <= 2 * 104
1 <= val <= 2 * 104
0 <= index <= 105
At most 2 * 105 calls will be made to push, pop, and popAtStack.

"""
import time

DEBUG = False

class AVLTree:
    class Node:
        def __init__(self, key, val):
            self.parent = None
            self.key = key
            self.val = val
            self.left = None
            self.right = None
            self.height = 1

    def __init__(self):
        self.root = None
        self.size = 0

    def calHeight(self, node: Node):
        if node is None:
            return 0

        if node.left and node.right:
            if node.left.height < node.right.height:
                return node.right.height + 1
            else:
                return node.left.height + 1
        elif node.left:
            return node.left.height + 1
        elif node.right:
            return node.right.height + 1
        else:
            return 1
    
    def balanceFactor(self, node: Node):
        if node is None:
            return 0
        
        if node.left and node.right:
            return node.left.height - node.right.height
        elif node.left:
            return node.left.height
        elif node.right:
            return -node.right.height
        else:
            return 0

    def llRotate(self, node: Node):
        if DEBUG: 
            print("llRotate")
        # update height
        p = node
        lp = p.left

        p.left = lp.right
        p.height = self.calHeight(p)
        if lp.right:
            lp.right.parent = p

        lp.right = p
        lp.height = self.calHeight(lp)
        p.parent = lp

        lp.parent = None
        return lp
    
    def rrRotate(self, node: Node):
        if DEBUG:
            print("rrRotate")
        # update height
        p = node
        rp = p.right

        p.right = rp.left
        p.height = self.calHeight(p)
        if rp.left:
            rp.left.parent = p

        rp.left = p
        rp.height = self.calHeight(rp)
        p.parent = rp

        rp.parent = None
        return rp

    def rlRotate(self, node: Node):
        if DEBUG:
            print("rlRotate")
        # update height
        p = node
        rp = p.right
        lrp = rp.left

        rp.left = lrp.right
        rp.height = self.calHeight(rp)
        if lrp.right:
            lrp.right.parent = rp

        lrp.right = rp
        lrp.height = self.calHeight(lrp)
        rp.parent = lrp

        p.right = lrp.left
        p.height = self.calHeight(p)
        if lrp.left:
            lrp.left.parent = p

        lrp.left = p
        lrp.height = self.calHeight(lrp)
        p.parent = lrp

        lrp.parent = None
        return lrp

    def lrRotate(self, node: Node):
        if DEBUG:
            print("lrRotate")
        # update height
        p = node
        lp = p.left
        rlp = lp.right

        lp.right = rlp.left
        lp.height = self.calHeight(lp)
        if rlp.left:
            rlp.left.parent = lp

        rlp.left = lp
        rlp.height = self.calHeight(rlp)
        lp.parent = rlp

        p.left = rlp.right
        p.height = self.calHeight(p)
        if rlp.right:
            rlp.right.parent = p

        rlp.right = p
        rlp.height = self.calHeight(rlp)
        p.parent = rlp

        rlp.parent = None
        return rlp

    def insertAt(self, node: Node, key, val):
        # update height
        if node is None:
            node = self.Node(key, val)
            return node

        if key < node.key:
            node.left = self.insertAt(node.left, key, val)
            node.height = self.calHeight(node)
            if node.left:
                node.left.parent = node
        else:
            node.right = self.insertAt(node.right, key, val)
            node.height = self.calHeight(node)
            if node.right:
                node.right.parent = node
        if DEBUG:
            print(node.key, " bf: ", self.balanceFactor(node),
                    " left: ", node.left.key if node.left else -1,
                    " left height: ", node.left.height if node.left else -1,
                    " lelf bf:", self.balanceFactor(node.left),
                    " right: ", node.right.key if node.right else -1,
                    " right height: ", node.right.height if node.right else -1,
                    " right bf: ", self.balanceFactor(node.right))

        if self.balanceFactor(node) == 2 and self.balanceFactor(node.left) >= 0:
            node = self.llRotate(node)
        elif self.balanceFactor(node) == 2 and self.balanceFactor(node.left) == -1:
            node = self.lrRotate(node)
        elif self.balanceFactor(node) == -2 and self.balanceFactor(node.right) <= 0:
            node = self.rrRotate(node)
        elif self.balanceFactor(node) == -2 and self.balanceFactor(node.right) == 1:
            node = self.rlRotate(node)
        
        return node
    
    def leftMostNode(self, node: Node):
        if node is None:
            return None
        while node.left:
            node = node.left
        return node

    def deleteAt(self, node: Node, key):
        #  modify parent
        #  update height
        if node is None:
            return None
        if key < node.key:
            node.left = self.deleteAt(node.left, key)
            node.height = self.calHeight(node)
            if node.left:
                node.left.parent = node

        elif key > node.key:
            node.right = self.deleteAt(node.right, key)
            node.height = self.calHeight(node)
            if node.right:
                node.right.parent = node

        else:
            self.size -= 1
            if node.left is None:
                node = node.right
                if node:
                    node.parent = None
                return node
            elif node.right is None:
                node = node.left
                if node:
                    node.parent = None
                return node
            else:
                if DEBUG:
                    print("node.right:", node.right.key if node.right else -1)
                p = self.leftMostNode(node.right)
                node.key = p.key
                node.val = p.val
                if DEBUG:
                    print("1. p:", p.key, "2. p.parent:", p.parent.key)
                if p.parent == node:
                    node.right = p.right
                    if p.right:
                        p.right.parent = node
                    p = node
                else:
                    if DEBUG:
                        print("HERE - remove leftMost")
                        print("p.parent: ", p.parent.key)
                
                    p.parent.left = p.right
                    if p.right:
                        p.right.parent = p.parent
                    p = p.parent
                    while p != node:
                        p.height = self.calHeight(p)
                        parent = p.parent

                        if DEBUG:
                            print("p:", p.key, "p.parent:", parent.key)
                        if self.balanceFactor(p) == -2 and self.balanceFactor(p.right) <= 0:
                            p = self.rrRotate(p)
                        elif self.balanceFactor(p) == -2 and self.balanceFactor(p.right) == 1:
                            p = self.rlRotate(p)

                        if parent != node:
                            parent.left = p
                        else:
                            parent.right = p
                        if p:
                            p.parent = parent
                        p = parent

        node.height = self.calHeight(node)
        #  rebalance node
        if self.balanceFactor(node) == 2 and self.balanceFactor(node.left) >= 0:
            node = self.llRotate(node)
        elif self.balanceFactor(node) == 2 and self.balanceFactor(node.left) == -1:
            node = self.lrRotate(node)
        if self.balanceFactor(node) == -2 and self.balanceFactor(node.right) <= 0:
            node = self.rrRotate(node)
        elif self.balanceFactor(node) == -2 and self.balanceFactor(node.right) == 1:
            node = self.rlRotate(node)

        return node

    def toString(self, node: Node):
        if node is None:
            return ""
        if node.left and node.right:
            return self.toString(node.left) + " " + \
                "(" + str(node.key) + "-" + str(node.val) + ")" + \
                "(" + str(node.height) + ")" + " " + self.toString(node.right)
        elif node.left:
            return self.toString(node.left) + " " + \
                "(" + str(node.key) + "-" + str(node.val) + ")" + \
                "(" + str(node.height) + ")"
        elif node.right:
            return "(" + str(node.key) + "-" + str(node.val) + ")" + \
                "(" + str(node.height) + ")" + " " + self.toString(node.right)
        else:
            return "(" + str(node.key) + "-" + str(node.val) + ")" + \
                "(" + str(node.height) + ")"

    def __str__(self):
        # return str(self.root.val) + " - " + self.toString(self.root)
        return str(self.size) + " - " + self.toString(self.root)
    
    def insert(self, key, val):
        self.root = self.insertAt(self.root, key, val)
        self.size += 1
    
    def delete(self, key):
        self.root = self.deleteAt(self.root, key)
    
    def minKey(self):
        if self.size == 0:
            return None
        tmp = self.root
        while tmp.left:
            tmp = tmp.left
        return tmp.key, tmp.val
    
    def maxKey(self):
        if self.size == 0:
            return None
        tmp = self.root
        while tmp.right:
            tmp = tmp.right
        return tmp.key, tmp.val
    
    def containAt(self, node, key):
        if node is None:
            return False
        if key < node.key:
            return self.containAt(node.left, key)
        elif key > node.key:
            return self.containAt(node.right, key)
        else:
            return True
    
    def valAt(self, node, key):
        if node is None:
            return None
        if key < node.key:
            return self.valAt(node.left, key)
        elif key > node.key:
            return self.valAt(node.right, key)
        else:
            return node.val
    
    def val(self, key):
        return self.valAt(self.root, key)

    def contain(self, key):
        return self.containAt(self.root, key)

    def treeSize(self):
        return self.size


class DinnerPlates:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.empty = AVLTree()
        self.notFull = AVLTree()
        self.full = AVLTree()
        self.size = 0
        # self.stacks = []

    def push(self, val: int) -> None:
        if self.notFull.treeSize() > 0:
            key, stack = self.notFull.minKey()
            if self.empty.treeSize() == 0:
                stack.append(val)
                if len(stack) == self.cap:
                    self.notFull.delete(key)
                    self.full.insert(key, stack)
            else:
                key2, stack2 = self.empty.minKey()
                if key2 > key:
                    stack.append(val)
                    if len(stack) == self.cap:
                        self.notFull.delete(key)
                        self.full.insert(key, stack)
                else:
                    stack2.append(val)
                    if len(stack2) == self.cap:
                        self.empty.delete(key2)
                        self.full.insert(key2, stack2)             

        elif self.empty.treeSize() > 0:
            key2, stack2 = self.empty.minKey()
            stack2.append(val)
            if len(stack2) == self.cap:
                self.empty.delete(key2)
                self.full.insert(key2, stack2)
        else:
            stack = [val]
            # self.stacks.append(stack)
            if len(stack) < self.cap:
                self.notFull.insert(self.size, stack)
            else:
                self.full.insert(self.size, stack)

            self.size += 1
        

    def pop(self) -> int:
        top = -1
        if self.notFull.treeSize() > 0:
            key, stack = self.notFull.maxKey()
            if self.full.treeSize() == 0:
                top = stack.pop()
                if len(stack) == 0:
                    self.notFull.delete(key)
                    self.empty.insert(key, stack)
            else:
                key2, stack2 = self.full.maxKey()
                if key > key2:
                    top = stack.pop()
                    if len(stack) == 0:
                        self.notFull.delete(key)
                        self.empty.insert(key, stack)
                else:
                    top = stack2.pop()
                    self.full.delete(key2)
                    if len(stack2) == 0:
                        self.empty.insert(key2, stack2)
                    else:
                        self.notFull.insert(key2, stack2)
                    
        elif self.full.treeSize() > 0:
            key2, stack2 = self.full.maxKey()
            top = stack2.pop()
            self.full.delete(key2)
            if len(stack2) == 0:
                self.empty.insert(key2, stack2)
            else:
                self.notFull.insert(key2, stack2)

        return top


    def popAtStack(self, index: int) -> int:
        top = -1
        stack = self.full.val(index)
        if stack is not None:
            top = stack.pop()
            self.full.delete(index)
            if len(stack) == 0:
                self.empty.insert(index, stack)
            else:
                self.notFull.insert(index, stack)
        else:
            stack = self.notFull.val(index)
            if stack is not None:
                top = stack.pop()
                if len(stack) == 0:
                    self.notFull.delete(index)
                    self.empty.insert(index, stack)

        return top


# Your DinnerPlates object will be instantiated and called as such:
# obj = DinnerPlates(capacity)
# obj.push(val)
# param_2 = obj.pop()
# param_3 = obj.popAtStack(index)

ops = ["DinnerPlates", "push", "push", "push", "push", "push", "popAtStack", "push", "push", "popAtStack", "popAtStack", "pop", "pop", "pop", "pop", "pop"]
vals = [[2], [1], [2], [3], [4], [5], [0], [20], [21], [0], [2], [], [], [], [], []]
outs = [None, None, None, None, None, None, 2, None, None, 20, 21, 5, 4, 3, 1, -1]

obj = DinnerPlates(vals[0][0])

for i in range(1, len(ops)):
    op = ops[i]
    if op == "push":
        assert obj.push(vals[i][0]) == outs[i]
    elif op == "pop":
        assert obj.pop() == outs[i]
    elif op == "popAtStack":
        assert obj.popAtStack(vals[i][0]) == outs[i]






t1 = time.time()
print(len(ops))

obj = DinnerPlates(vals[0][0])

for i in range(1, len(ops)):
    op = ops[i]
    if op == "push":
        obj.push(vals[i][0])
    elif op == "pop":
        obj.pop()
    elif op == "popAtStack":
        obj.popAtStack(vals[i][0])

t2 = time.time()
print(t2 - t1)