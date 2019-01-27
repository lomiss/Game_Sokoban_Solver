# _*_ coding:utf-8 _*_
__author__ = 'lomiss'
__data__ = '2019/1/1 20:32'
import ctypes
from ctypes import *
ASTAR = ctypes.cdll.LoadLibrary("C:/Users/lenovo/Desktop/sokoban/C_Astar/x64/Release/C_Astar.dll")
BFS = ctypes.cdll.LoadLibrary("C:/Users/lenovo/Desktop/sokoban/C_BFS/x64/Release/C_BFS.dll")
DFS = ctypes.cdll.LoadLibrary("C:/Users/lenovo/Desktop/sokoban/C_DFS/x64/Release/C_DFS.dll")
# level = "##########      ##   .   ##   $   ## .$@$. #####$   #   #.   #   #   ##   ##### "
# level = "   ###       ## # #### ##  ###  ### $      ##   @$ #  #### $###  #  #  #..  # ## ##.# ## #      ##  #     ##   #######   "
# length_level = len(level)
# level = c_wchar_p(level)
# length_solution = BFS.Bfs(level, length_level, 11)
# solution = '#' * length_solution
# solution = c_wchar_p(solution)
# BFS.Get_solution(solution)
# print(solution.value)


class C_algo:
    def __init__(self, level, col):
         self.level = level
         self.col = col

    def C_BFS(self):
        length_level = len(self.level)
        level = c_wchar_p(self.level)
        length_solution = BFS.Bfs(level, length_level, self.col)
        solution = '#' * length_solution
        solution = c_wchar_p(solution)
        BFS.Get_solution(solution)
        return solution.value

    def C_DFS(self):
        length_level = len(self.level)
        level = c_wchar_p(self.level)
        length_solution = DFS.Dfs(level, length_level, self.col)
        solution = '#' * length_solution
        solution = c_wchar_p(solution)
        DFS.Get_solution(solution)
        return solution.value

    def C_Astar(self):
        length_level = len(self.level)
        level = c_wchar_p(self.level)
        length_solution = ASTAR.Astar(level, length_level, self.col)
        solution = '#' * length_solution
        solution = c_wchar_p(solution)
        ASTAR.Get_solution(solution)
        return solution.value
