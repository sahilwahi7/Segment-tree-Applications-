class Node(object):
    def __init__(self, start, end):
        self.start = start                 #creating a segment tree node
        self.end = end
        self.total = 0
        self.left = None
        self.right = None
        

class NumArray(object):
    def __init__(self, nums):
        def createTree(nums, l, r):
            if l > r:
                return None
                
            if l == r:     #if we reach the range==1 then we stop tree growth
                n = Node(l, r)
                n.total = nums[l]    # assign value to the node
                return n
            
            mid = (l + r) // 2
            
            root = Node(l, r)
             
            #recursively build the Segment tree
            root.left = createTree(nums, l, mid)    #left half of tree
            root.right = createTree(nums,mid+1, r)  # right half of tree
            root.total = root.left.total + root.right.total  # storing the range sum till the point
                
            return root
        
        self.root = createTree(nums, 0, len(nums)-1)
            
    def update(self, i, val):
        def updateVal(root, i, val):  # i is the point and val is tha value to be updated
            if root.start == root.end:
                root.total = val
                return val   # if range is 1 just update the value at that node
        
            mid = (root.start + root.end) // 2
            
            #If the index is less than the mid, that leaf must be in the left subtree
            if i <= mid:
                updateVal(root.left, i, val)   
                
            #Otherwise, the right subtree
            else:
                updateVal(root.right, i, val)
            
            #Propogate the changes after recursive call returns
            root.total = root.left.total + root.right.total
            
            return root.total
        
        return updateVal(self.root, i, val)

    def sumRange(self, i, j):
        def rangeSum(root, i, j):
            
            #case1 and 2 are of full overlap and case3 is of partial overlap
            
            #If the range exactly matches the root, we already have the sum
            if root.start == i and root.end == j:
                return root.total
            
            mid = (root.start + root.end) // 2
            
            #If end of the range is less than the mid, the entire interval lies
            #in the left subtree
            #case1
            if j <= mid:
                return rangeSum(root.left, i, j)
            
            #If start of the interval is greater than mid, the entire inteval lies
            #in the right subtree
            #case2
            elif i >= mid + 1:
                return rangeSum(root.right, i, j)
            
            #Otherwise, the interval is split. So we calculate the sum recursively,
            #by splitting the interval
            #case3
            else:
                return rangeSum(root.left, i, mid) + rangeSum(root.right, mid+1, j)
        
        return rangeSum(self.root, i, j)
