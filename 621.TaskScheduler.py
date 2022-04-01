"""
Given a characters array tasks, representing the tasks a CPU needs to do, where each letter represents a different task. Tasks could be done in any order. Each task is done in one unit of time. For each unit of time, the CPU could complete either one task or just be idle.

However, there is a non-negative integer n that represents the cooldown period between two same tasks (the same letter in the array), that is that there must be at least n units of time between any two same tasks.

Return the least number of units of times that the CPU will take to finish all the given tasks.

 

Example 1:

Input: tasks = ["A","A","A","B","B","B"], n = 2
Output: 8
Explanation: 
A -> B -> idle -> A -> B -> idle -> A -> B
There is at least 2 units of time between any two same tasks.
Example 2:

Input: tasks = ["A","A","A","B","B","B"], n = 0
Output: 6
Explanation: On this case any permutation of size 6 would work since n = 0.
["A","A","A","B","B","B"]
["A","B","A","B","A","B"]
["B","B","B","A","A","A"]
...
And so on.
Example 3:

Input: tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2
Output: 16
Explanation: 
One possible solution is
A -> B -> C -> A -> D -> E -> A -> F -> G -> A -> idle -> idle -> A -> idle -> idle -> A
 

Constraints:

1 <= task.length <= 104
tasks[i] is upper-case English letter.
The integer n is in the range [0, 100].
"""
from typing import List
import heapq


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        minUnits = 0
        prioDict = {"A": 25, "B": 24, "C": 23, "D": 22, "E": 21, "F": 20, "G": 19, "H": 18, "I": 17,
                    "J": 16, "K": 15, "L": 14, "M": 13, "N": 12, "O": 11, "P": 10, "Q": 9, "R": 8,
                    "S": 7, "T": 6, "U": 5, "V": 4, "W": 3, "X": 2, "Y": 1, "Z": 0}
        freqDict = {}
        for t in tasks:
            if t in freqDict:
                freqDict[t] += 1
            else:
                freqDict[t] = 1

        freqQueue = []
        for t in freqDict:
            heapq.heappush(freqQueue, (-((freqDict[t] << 5) + prioDict[t]), t))
        
        while len(freqQueue) > 0:
            prio, topTask = heapq.heappop(freqQueue)
            freq = (-prio) >> 5
            minUnits += freq + (freq - 1) * n
            for i in range(freq-1):
                if len(freqQueue) == 0:
                    break
                tmpQueue = []
                for j in range(n):
                    if len(freqQueue) == 0:
                        break
                    nextPrior, nextTask = heapq.heappop(freqQueue)
                    nextFreq = (-nextPrior) >> 5
                    nextFreq -= 1
                    if nextFreq > 0:
                        tmpQueue.append((-((nextFreq << 5) + prioDict[nextTask]), nextTask))
                # push back tmpQueue
                for x in tmpQueue:
                    heapq.heappush(freqQueue, x)

        return minUnits


sol = Solution()
print(sol.leastInterval(["A", "A", "A", "B", "B", "B"], 2))
print(sol.leastInterval(["A", "A", "A", "B", "B", "B"], 0))
print(sol.leastInterval(["A", "A", "A", "A", "A",
      "A", "B", "C", "D", "E", "F", "G"], 2))
