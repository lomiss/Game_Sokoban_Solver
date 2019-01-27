# _*_ coding:utf-8 _*_
__author__ = 'lomiss'
__data__ = '2018/12/12 9:10'


class BFS:
    def __init__(self, level, col=10):
        '''
        ' '空地 #墙 $箱子 .终点 @人
        +人在终点 *箱子在终点
        :param level
        :param col: 地图的宽度，由于设定为10，默认为10
        '''
        self.level = level
        # start和end 表示开始的状态，结束的状态
        # start只有' ', '#', '$', '@'。
        # end只有' ', '.'，' '表示其他。
        self.start = ''
        self.end = ''
        self.col = col
        # paths记录最短路径(可能有多条)
        self.paths = []
        # len记录最短路径长度
        self.len = -1

    def pre(self):
        '''
        1.获得start状态和end状态
        2.获得人的位置ppos
        '''
        # 现在只需要把start状态中的'$'位置移动到end状态中的'.'位置即满足条件
        start_dict = {'.': ' ', '+': '@', '*': '$'}
        end_dict = {'.': '.', '+': '.', '*': '.'}
        for x in self.level:
            self.start += start_dict.get(x, x)
            self.end += end_dict.get(x, ' ')
        assert '$' in self.start, '关卡中没有箱子？'
        # ppos表示'@'(人)的位置
        self.ppos = self.start.find('@')
        assert self.ppos != -1, '关卡中没有人？'

    def is_ok(self, start):
        '''
        如果start中的'$'(箱子)都移动到end的'.'(终点)即为游戏结束
        '''
        return ('$', ' ') not in zip(start, self.end)

    def BFS(self):
        '''
        BFS获得最短路径保存到paths中
        '''
        # 4个方向，小写代表只是人移动，大写表示人推着箱子一起移动
        dirs = [[-self.col, 'u', 'U'], [self.col, 'd', 'D'], [1, 'r', 'R'], [-1, 'l', 'L']]
        # 把开始的状态进入队列(list模拟)，状态包括字符串表示的当前状态、当前的路径、当前人的位置
        states = [[self.start, '', self.ppos]]
        # 访问集合，访问过的状态(字符串)不再访问
        visi = set()
        visi.add(self.start)
        # 保护机制，设置边界，超过1000步就退出
        s_len = 1000
        while states:
            start, path, ppos = states.pop(0)
            if len(path) > s_len:
                break
            # 当寻找了一个路径时就break，BFS一般结果是最短路径
            if self.is_ok(start):
                if self.len == -1 or len(path) == self.len:
                    self.paths.append(path)
                    self.len = len(path)
                break

            for dir in dirs:
                # '@'下一个的状态的位置
                cpos = ppos + dir[0]
                # '@'下一个的下一个的状态的位置
                npos = cpos + dir[0]
                if start[cpos] == '$' and start[npos] == ' ':
                    # 人和箱子一起推动，start中连着的状态为'@' '$' ' '。推完之后start变为' ' '@' '$'
                    # python中字符串不可更改，于是把字符串变成list更改状态后再转换为字符串
                    digits = list(start)
                    digits[ppos], digits[cpos], digits[npos] = ' ', '@', '$'
                    new_start = ''.join(digits)
                    if new_start not in visi:
                        visi.add(new_start)
                        states.append([new_start, path + dir[2], cpos])
                elif start[cpos] == ' ':
                    # 人动箱子不动，start中连着的状态为'@',' '。
                    digits = list(start)
                    digits[ppos], digits[cpos] = ' ', '@'
                    new_start = ''.join(digits)
                    if new_start not in visi:
                        visi.add(new_start)
                        states.append([new_start, path + dir[1], cpos])

    def gen_shortest_paths(self):
        self.pre()
        self.BFS()
        return self.paths