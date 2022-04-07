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
        return tmp.key
    
    def maxKey(self):
        if self.size == 0:
            return None
        tmp = self.root
        while tmp.right:
            tmp = tmp.right
        return tmp.key
    
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

tree = AVLTree()

while True:
    c = input()
    if c == "i":
        key = int(input())
        # val = int(input())
        tree.insert(key, [])
        # if DEBUG:
        print(tree)
    elif c == "d":
        key = int(input())
        tree.delete(key)
        # if DEBUG:
        print(tree)
    elif c == "v":
        key = int(input())
        val = tree.val(key)
        val.append(1)
        print(tree)
    elif c == 's':
        print(tree.treeSize())

    else:
        break