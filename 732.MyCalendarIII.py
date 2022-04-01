"""
A k-booking happens when k events have some non-empty intersection (i.e., there is some time that is common to all k events.)

You are given some events [start, end), after each given event, return an integer k representing the maximum k-booking between all the previous events.

Implement the MyCalendarThree class:

MyCalendarThree() Initializes the object.
int book(int start, int end) Returns an integer k representing the largest integer such that there exists a k-booking in the calendar.
 

Example 1:

Input
["MyCalendarThree", "book", "book", "book", "book", "book", "book"]
[[], [10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]
Output
[null, 1, 1, 2, 3, 3, 3]

Explanation
MyCalendarThree myCalendarThree = new MyCalendarThree();
myCalendarThree.book(10, 20); // return 1, The first event can be booked and is disjoint, so the maximum k-booking is a 1-booking.
myCalendarThree.book(50, 60); // return 1, The second event can be booked and is disjoint, so the maximum k-booking is a 1-booking.
myCalendarThree.book(10, 40); // return 2, The third event [10, 40) intersects the first event, and the maximum k-booking is a 2-booking.
myCalendarThree.book(5, 15); // return 3, The remaining events cause the maximum K-booking to be only a 3-booking.
myCalendarThree.book(5, 10); // return 3
myCalendarThree.book(25, 55); // return 3
 

Constraints:

0 <= start < end <= 109
At most 400 calls will be made to book.
"""


class MyCalendarThree:

    def __init__(self):
        self.segments = []

    def book(self, start: int, end: int) -> int:
        # for i in range(len(self.segments)):
        i = 0
        while i < len(self.segments):
            s, e, freq = self.segments[i]
            if end <= s:
                self.segments.insert(i, [start, end, 1])
                start = end
                break
            if start >= e:
                i += 1
                continue
            if start < s:
                if end < e:
                    self.segments[i][0] = end
                    self.segments.insert(i, [s, end, freq+1])
                    self.segments.insert(i, [start, s, 1])
                    start = end
                    break
                elif end == e:
                    self.segments[i][2] = freq + 1
                    self.segments.insert(i, [start, s, 1])
                    start = end
                    break
                else: # if end > e:
                    self.segments[i][2] = freq + 1
                    self.segments.insert(i, [start, s, 1])
                    start = e
                    i += 2
            elif start == s:
                if end < e:
                    self.segments[i][0] = end
                    self.segments.insert(i, [s, end, freq+1])
                    start = end
                    break
                elif end == e:
                    self.segments[i][2] = freq + 1
                    start = end
                    break
                else: # end > e
                    self.segments[i][2] = freq + 1
                    start = e
                    i += 1
            else: # start > s
                if end < e:
                    self.segments[i][0] = end
                    self.segments.insert(i, [start, end, freq+1])
                    self.segments.insert(i, [s, start, freq])
                    start = end
                    break
                elif end == e:
                    self.segments[i][2] = freq + 1
                    self.segments[i][0] = start
                    self.segments.insert(i, [s, start, freq])
                    start = end
                    break
                else: # end > e
                    self.segments[i][0] = start
                    self.segments[i][2] = freq + 1
                    self.segments.insert(i, [s, start, freq])
                    start = e
                    i += 2

        if start < end:
            self.segments.append([start, end, 1])
        
        res = 0
        for seg in self.segments:
            if res < seg[2]:
                res = seg[2]
        return res


# Your MyCalendarThree object will be instantiated and called as such:
# obj = MyCalendarThree()
# param_1 = obj.book(start,end)

ops = ["MyCalendarThree", "book", "book", "book", "book", "book", "book"]
vals = [[], [10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]
outs = [None, 1, 1, 2, 3, 3, 3]

obj = MyCalendarThree()
for i in range(1, len(ops)):
    out = obj.book(vals[i][0], vals[i][1])
    if out != outs[i]:
        print(i, out, "!=", outs[i])




ops = ["MyCalendarThree","book","book","book","book","book","book","book","book","book","book"]
vals = [[],[24,40],[43,50],[27,43],[5,21],[30,40],[14,29],[3,19],[3,14],[25,39],[6,19]]
outs = [None,1,1,2,2,3,3,3,3,4,4]

obj = MyCalendarThree()
for i in range(1, len(ops)):
    out = obj.book(vals[i][0], vals[i][1])
    if out != outs[i]:
        print(i, out, "!=", outs[i])

ops = ["MyCalendarThree","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book"]
vals = [[],[55,69],[43,58],[36,52],[75,86],[65,83],[17,29],[53,66],[72,84],[38,53],[66,79],[71,84],[42,61],[49,65],[4,17],[43,57],[17,31],[35,47],[35,53],[23,36],[41,57],[26,41],[83,97],[18,37],[10,26],[82,97],[25,44],[85,96],[82,98],[15,28],[24,39],[11,25],[50,61],[1,17],[66,81],[62,79],[86,100],[49,68],[63,74],[99,100],[8,24],[11,22],[1,14],[9,23],[15,33],[16,30],[19,33],[60,70],[87,99],[69,79],[18,33],[55,70],[39,49],[53,71],[65,79],[70,84],[77,95],[57,67],[29,47],[88,100],[3,14]]
outs = [None,1,2,2,2,2,2,3,3,3,4,5,5,5,5,6,6,6,7,7,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,11,12,12,12,12,13,13,13,13,13,13,13,13,13,13,13]

obj = MyCalendarThree()
for i in range(1, len(ops)):
    out = obj.book(vals[i][0], vals[i][1])
    print(vals[i], "||", obj.segments, "\n")

    if out != outs[i]:
        print(i, out, "!=", outs[i])
        break