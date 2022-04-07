"""
You are given two integers, m and k, and a stream of integers. You are tasked to implement a data structure that calculates the MKAverage for the stream.

The MKAverage can be calculated using these steps:

If the number of the elements in the stream is less than m you should consider the MKAverage to be -1. Otherwise, copy the last m elements of the stream to a separate container.
Remove the smallest k elements and the largest k elements from the container.
Calculate the average value for the rest of the elements rounded down to the nearest integer.
Implement the MKAverage class:

MKAverage(int m, int k) Initializes the MKAverage object with an empty stream and the two integers m and k.
void addElement(int num) Inserts a new element num into the stream.
int calculateMKAverage() Calculates and returns the MKAverage for the current stream rounded down to the nearest integer.
 

Example 1:

Input
["MKAverage", "addElement", "addElement", "calculateMKAverage", "addElement", "calculateMKAverage", "addElement", "addElement", "addElement", "calculateMKAverage"]
[[3, 1], [3], [1], [], [10], [], [5], [5], [5], []]
Output
[null, null, null, -1, null, 3, null, null, null, 5]

Explanation
MKAverage obj = new MKAverage(3, 1); 
obj.addElement(3);        // current elements are [3]
obj.addElement(1);        // current elements are [3,1]
obj.calculateMKAverage(); // return -1, because m = 3 and only 2 elements exist.
obj.addElement(10);       // current elements are [3,1,10]
obj.calculateMKAverage(); // The last 3 elements are [3,1,10].
                          // After removing smallest and largest 1 element the container will be [3].
                          // The average of [3] equals 3/1 = 3, return 3
obj.addElement(5);        // current elements are [3,1,10,5]
obj.addElement(5);        // current elements are [3,1,10,5,5]
obj.addElement(5);        // current elements are [3,1,10,5,5,5]
obj.calculateMKAverage(); // The last 3 elements are [5,5,5].
                          // After removing smallest and largest 1 element the container will be [5].
                          // The average of [5] equals 5/1 = 5, return 5
 

Constraints:

3 <= m <= 105
1 <= k*2 < m
1 <= num <= 105
At most 105 calls will be made to addElement and calculateMKAverage.
"""

DEBUG = False

class AVLTree:
    class Node:
        def __init__(self, val):
            self.parent = None
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

    def insertAt(self, node: Node, val: int):
        # update height
        if node is None:
            node = self.Node(val)
            return node

        if val < node.val:
            node.left = self.insertAt(node.left, val)
            node.height = self.calHeight(node)
            if node.left:
                node.left.parent = node
        else:
            node.right = self.insertAt(node.right, val)
            node.height = self.calHeight(node)
            if node.right:
                node.right.parent = node
        if DEBUG:
            print(node.val, " bf: ", self.balanceFactor(node),
                    " left: ", node.left.val if node.left else -1,
                    " left height: ", node.left.height if node.left else -1,
                    " lelf bf:", self.balanceFactor(node.left),
                    " right: ", node.right.val if node.right else -1,
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

    def deleteAt(self, node: Node, val: int):
        #  modify parent
        #  update height
        if node is None:
            return None
        if val < node.val:
            node.left = self.deleteAt(node.left, val)
            node.height = self.calHeight(node)
            if node.left:
                node.left.parent = node

        elif val > node.val:
            node.right = self.deleteAt(node.right, val)
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
                    print("node.right:", node.right.val if node.right else -1)
                p = self.leftMostNode(node.right)
                node.val = p.val
                if DEBUG:
                    print("1. p:", p.val, "2. p.parent:", p.parent.val)
                if p.parent == node:
                    node.right = p.right
                    if p.right:
                        p.right.parent = node
                    p = node
                else:
                    if DEBUG:
                        print("HERE - remove leftMost")
                        print("p.parent: ", p.parent.val)
                
                    p.parent.left = p.right
                    if p.right:
                        p.right.parent = p.parent
                    p = p.parent
                    while p != node:
                        p.height = self.calHeight(p)
                        parent = p.parent

                        if DEBUG:
                            print("p:", p.val, "p.parent:", parent.val)
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
            return self.toString(node.left) + " " + str(node.val) + "(" + str(node.height) + ")" \
                 + " " + self.toString(node.right)
        elif node.left:
            return self.toString(node.left) + " " + str(node.val) + "(" + str(node.height) + ")"
        elif node.right:
            return str(node.val) + "(" + str(node.height) + ")" + " " + self.toString(node.right)
        else:
            return str(node.val) + "(" + str(node.height) + ")"

    def __str__(self):
        # return str(self.root.val) + " - " + self.toString(self.root)
        return str(self.size) + " - " + self.toString(self.root)
    
    def insert(self, val):
        self.root = self.insertAt(self.root, val)
        self.size += 1
    
    def delete(self, val):
        self.root = self.deleteAt(self.root, val)

    def minVal(self):
        if self.size == 0:
            return None
        tmp = self.root
        while tmp.left:
            tmp = tmp.left
        return tmp.val
    
    def maxVal(self):
        if self.size == 0:
            return None
        tmp = self.root
        while tmp.right:
            tmp = tmp.right
        return tmp.val

    def containAt(self, node, val):
        if node is None:
            return False
        if val < node.val:
            return self.containAt(node.left, val)
        elif val > node.val:
            return self.containAt(node.right, val)
        else:
            return True

    def contain(self, val):
        return self.containAt(self.root, val)

    # def size(self):
    #     return self.size



class MKAverage:

    def __init__(self, m: int, k: int):
        self.leftTree = AVLTree()
        self.middleTree = AVLTree()
        self.rightTree = AVLTree()
        self.middleSum = 0
        self.stream = []
        self.m = m
        self.k = k

    def addElement(self, num: int) -> None:
        self.stream.append(num)
        # if len(self.stream) > self.m:
        #     oldest = self.stream.pop(0)

        if self.leftTree.size < self.k:
            self.leftTree.insert(num)
        elif self.rightTree.size < self.k:
            maxLeft = self.leftTree.maxVal()
            if maxLeft <= num:
                self.rightTree.insert(num)
            else:
                self.leftTree.delete(maxLeft)
                self.leftTree.insert(num)
                self.rightTree.insert(maxLeft)
        else:
            if self.middleTree.size < self.m - 2 * self.k:
                maxLeft = self.leftTree.maxVal()
                minRight = self.rightTree.minVal()
                if num < maxLeft:
                    self.leftTree.delete(maxLeft)
                    self.leftTree.insert(num)
                    self.middleTree.insert(maxLeft)
                    self.middleSum += maxLeft
                elif num <= minRight:
                    self.middleTree.insert(num)
                    self.middleSum += num
                else:
                    self.rightTree.delete(minRight)
                    self.rightTree.insert(num)
                    self.middleTree.insert(minRight)
                    self.middleSum += minRight
            else:
                oldest = self.stream.pop(0)
                minMiddle = self.middleTree.minVal()
                maxMiddle = self.middleTree.maxVal()
                if num < minMiddle:
                    self.leftTree.insert(num)

                    if self.leftTree.contain(oldest):
                        self.leftTree.delete(oldest)
                        
                    elif self.middleTree.contain(oldest):
                        self.middleTree.delete(oldest)

                        maxLeft = self.leftTree.maxVal()
                        self.leftTree.delete(maxLeft)
                        self.middleTree.insert(maxLeft)
                        self.middleSum += (maxLeft - oldest)
                    else:
                        self.rightTree.delete(oldest)

                        maxLeft = self.leftTree.maxVal()
                        self.leftTree.delete(maxLeft)
                        self.middleTree.insert(maxLeft)

                        maxMiddle = self.middleTree.maxVal()
                        self.middleTree.delete(maxMiddle)

                        self.middleSum += (maxLeft - maxMiddle)
                        self.rightTree.insert(maxMiddle)
                        
                elif num <= maxMiddle:
                    self.middleTree.insert(num)

                    if self.leftTree.contain(oldest):
                        self.leftTree.delete(oldest)
                        minMiddle = self.middleTree.minVal()
                        self.middleTree.delete(minMiddle)
                        self.leftTree.insert(minMiddle)
                        self.middleSum += (num - minMiddle)

                    elif self.middleTree.contain(oldest):
                        self.middleTree.delete(oldest)

                        self.middleSum += (num - oldest)

                    else:
                        self.rightTree.delete(oldest)

                        maxMiddle = self.middleTree.maxVal()
                        self.middleTree.delete(maxMiddle)
                        self.rightTree.insert(maxMiddle)

                        self.middleSum += (num - maxMiddle)


                else:
                    self.rightTree.insert(num)

                    if self.leftTree.contain(oldest):
                        self.leftTree.delete(oldest)

                        minRight = self.rightTree.minVal()
                        self.rightTree.delete(minRight)

                        self.middleTree.insert(minRight)
                        minMiddle = self.middleTree.minVal()
                        self.middleTree.delete(minMiddle)

                        self.leftTree.insert(minMiddle)
                        self.middleSum += (minRight - minMiddle)

                    elif self.middleTree.contain(oldest):
                        self.middleTree.delete(oldest)
                        minRight = self.rightTree.minVal()
                        self.rightTree.delete(minRight)
                        self.middleTree.insert(minRight)

                        self.middleSum  += (minRight - oldest)                      

                    else:
                        self.rightTree.delete(oldest)

    def calculateMKAverage(self) -> int:
        if len(self.stream) < self.m:
            return -1
        return self.middleSum // (self.m - self.k * 2)
        


# Your MKAverage object will be instantiated and called as such:
# obj = MKAverage(m, k)
# obj.addElement(num)
# param_2 = obj.calculateMKAverage()
ops = ["MKAverage", "addElement", "addElement", "calculateMKAverage", "addElement", "calculateMKAverage", "addElement", "addElement", "addElement", "calculateMKAverage"]
vals = [[3, 1], [3], [1], [], [10], [], [5], [5], [5], []]

obj = MKAverage(vals[0][0], vals[0][1])
for i in range(1, len(ops)):
    if ops[i] == "addElement":
        obj.addElement(vals[i][0])
    else:
        print(obj.calculateMKAverage())