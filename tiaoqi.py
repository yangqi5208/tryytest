# 跳棋 (Chinese Checkers) 简易实现
# 这个版本使用文本终端交互，适合在命令行下跑。

import random

class ChineseCheckers:
    def __init__(self, size=7):
        self.size = size
        self.board = self._make_board()

    def _make_board(self):
        # 简化6角星为一个7x7矩阵（实际不完整）
        # 0: 空位, 1: 玩家1棋子, 2: 玩家2棋子
        b = [[0]*self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if i < 2 and j < 2:  # 起点1区
                    b[i][j] = 1
                elif i >= self.size-2 and j >= self.size-2:  # 起点2区
                    b[i][j] = 2
        return b

    def draw(self):
        print('  ' + ' '.join(str(i) for i in range(self.size)))
        for i, row in enumerate(self.board):
            print(str(i) + ' ' + ' '.join(str(x) for x in row))

    def valid_moves(self, x, y):
        if self.board[x][y] == 0:
            return []
        dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1)]
        moves = []
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == 0:
                moves.append((nx, ny))
            # 跳跃
            jx, jy = x+2*dx, y+2*dy
            if 0 <= jx < self.size and 0 <= jy < self.size and self.board[nx][ny] != 0 and self.board[jx][jy] == 0:
                moves.append((jx, jy))
        return moves

    def move(self, x,y,nx,ny):
        self.board[nx][ny] = self.board[x][y]
        self.board[x][y] = 0

    def check_win(self):
        # 简化胜利条件：对方起点区域被填满
        p1 = all(self.board[i][j] == 1 for i in range(self.size-2, self.size) for j in range(self.size-2, self.size))
        p2 = all(self.board[i][j] == 2 for i in range(0,2) for j in range(0,2))
        if p1:
            return 1
        if p2:
            return 2
        return 0


if __name__ == '__main__':
    game = ChineseCheckers()
    player = 1
    while True:
        game.draw()
        print(f"当前玩家: {player}")
        try:
            piece = input('选择棋子(格式 x y) 或 q 退出: ').strip()
            if piece.lower() == 'q':
                print('游戏结束')
                break
            x, y = map(int, piece.split())
            if not (0 <= x < game.size and 0 <= y < game.size) or game.board[x][y] != player:
                print('无效棋子，请重新选择')
                continue
            moves = game.valid_moves(x,y)
            if not moves:
                print('该棋子无可用移动')
                continue
            print('可移动到:', moves)
            tx, ty = map(int, input('目标坐标 x y: ').split())
            if (tx,ty) not in moves:
                print('无效移动点')
                continue
            game.move(x,y,tx,ty)
            winner = game.check_win()
            if winner:
                game.draw()
                print(f'玩家 {winner} 获胜！')
                break
            player = 1 if player == 2 else 2
        except Exception as e:
            print('输入有误:', e)
            continue
