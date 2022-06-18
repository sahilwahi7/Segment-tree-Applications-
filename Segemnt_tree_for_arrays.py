#ranges=[[1,2],[3,4],[3,6]]
#arr=[6,4,3,2,5]
#chararr="abbabbb"

"""
After first iteration the string becomes
chararr=abbabb#    range[1,2]="bb"  -----> not distinct
                   range[3,4]="ab"  -----> Distinct
                   range[3,6]="abb#" -----> Not distinct        cnt=1
                   
After Second interation:
chararr="abba#b#"   range[1,2]="bb"  -----> not distinct
                    range[3,4]="a#"  -----> Distinct            cnt+=1
                    range[3,6]="ab##" -----> distinct

After third iteration range [1,2] stll is not disitnct so cnt+=1

After fourth iteration it becomes all distinct so cnt=4

<------Implementing this with segment tree---->
"""


import collections
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
                n.total = collections.Counter(nums[l:r+1])    # assign value to the node
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
                root.total = collections.Counter(val)
                return collections.Counter(val)   # if range is 1 just update the value at that node
        
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
      
s=NumArray(chararr)   #O(n)   n ----> length of string       ---->creating segment tree object
cnt=0
cnt2=0
for i in arr:       #o(p)    p-----> lenght of array
    s.update(i,"#")  #o(logn) -----> update
    value=[]
    for r in range(len(ranges)):   #O(q) -----q is length if ranges
        l,r=ranges[r] 
        x=s.sumRange(l,r)
        print(x)
        
        for key,val in x.items():
            if key!="#":
                if val==1:
                  cnt+=1
            if key=="#":
              cnt+=1
        if cnt==len(x):
              cnt2+=1
        cnt=0
    if cnt2==len(ranges):
            print(cnt2)
            break
    else:
            cnt2=0
   
            
        
#<----overall time complexity  O(n*p*qlog(n))  ------from brute force it will be O(n*n*p*q)------->
