import pygame, sys, math

# 설정
S, C, M = 15, 40, 40
SZ = C * (S - 1) + M * 2
# 점수 체계: 연속성(Connectivity)에 더 높은 가중치 부여
P_SCORES = {"5": 1000000, "022220": 80000, "022221": 30000, "02220": 10000, "0220": 1000}

def get_sc(line, p):
    s = "".join(map(str, line))
    opp = "1" if p == 2 else "2"
    p = str(p)
    if p*5 in s: return P_SCORES["5"]
    if f"0{p*4}0" in s: return P_SCORES["022220"] # 열린 4
    if f"0{p*4}{opp}" in s or f"{opp}{p*4}0" in s: return P_SCORES["022221"] # 막힌 4
    if f"0{p*3}0" in s: return P_SCORES["02220"] # 열린 3
    return 0

class Omok:
    def __init__(self, d):
        pygame.init()
        self.scr = pygame.display.set_mode((SZ, SZ))
        self.bd = [[0]*S for _ in range(S)]
        self.turn, self.d, self.last = 1, d, None

    def check(self, r, c, p):
        for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
            cnt = 1
            for d in [1, -1]:
                i = 1
                while 0<=r+dr*i*d<S and 0<=c+dc*i*d<S and self.bd[r+dr*i*d][c+dc*i*d]==p:
                    cnt, i = cnt+1, i+1
            if cnt >= 5: return True
        return False

    def ev(self):
        ai, pl = 0, 0
        # 모든 라인 추출 (가로, 세로, 대각선)
        lines = self.bd + [[self.bd[r][c] for r in range(S)] for c in range(S)]
        for i in range(-S+1, S):
            lines.append([self.bd[r][r-i] for r in range(S) if 0<=r-i<S])
            lines.append([self.bd[r][S-1-r-i] for r in range(S) if 0<=S-1-r-i<S])
        for l in lines:
            ai += get_sc(l, 2); pl += get_sc(l, 1)
        return ai - pl * 4 # 수비 가중치

    def get_m(self):
        mvs = []
        for r in range(S):
            for c in range(S):
                if self.bd[r][c] == 0:
                    # 인접한 1칸 이내에 돌이 있는 곳을 우선 탐색 (한 칸 띄기 방지)
                    dist = 1
                    found = False
                    for dr in range(-dist, dist+1):
                        for dc in range(-dist, dist+1):
                            if 0<=r+dr<S and 0<=c+dc<S and self.bd[r+dr][c+dc] != 0:
                                found = True; break
                        if found: break
                    if found or (r==7 and c==7):
                        # 거리 점수 부여: 중앙 및 기존 돌에 가까울수록 가중치
                        mvs.append((r, c))
        return mvs

    def move(self):
        mvs = self.get_m()
        # [최우선] 즉시 승리/패배 노드 체크 (가장 근접한 수부터)
        for p in [2, 1]: 
            for r, c in mvs:
                self.bd[r][c] = p
                if self.check(r, c, p):
                    self.bd[r][c] = 0
                    return (r, c)
                self.bd[r][c] = 0
        
        # [탐색] 미니맥스
        best, best_m = -math.inf, None
        # 정렬: 중앙에 가까운 수부터 탐색하도록 정렬하여 가지치기 효율 높임
        mvs.sort(key=lambda x: abs(x[0]-7) + abs(x[1]-7))
        
        for r, c in mvs[:15]:
            self.bd[r][c] = 2
            v = self.minimax(self.d, -math.inf, math.inf, False)
            self.bd[r][c] = 0
            if v > best:
                best, best_m = v, (r, c)
        return best_m if best_m else mvs[0]

    def minimax(self, d, a, b, mx):
        if d == 0: return self.ev()
        mvs = self.get_m()[:8]
        if mx:
            for r, c in mvs:
                self.bd[r][c] = 2
                a = max(a, self.minimax(d-1, a, b, False))
                self.bd[r][c] = 0
                if b <= a: break
            return a
        else:
            for r, c in mvs:
                self.bd[r][c] = 1
                b = min(b, self.minimax(d-1, a, b, True))
                self.bd[r][c] = 0
                if b <= a: break
            return b

    def run(self):
        while True:
            self.scr.fill((220,179,92))
            for i in range(S):
                pygame.draw.line(self.scr, 0, [M, M+i*C], [SZ-M, M+i*C])
                pygame.draw.line(self.scr, 0, [M+i*C, M], [M+i*C, SZ-M])
            for r in range(S):
                for c in range(S):
                    if self.bd[r][c]: pygame.draw.circle(self.scr, (0,0,0) if self.bd[r][c]==1 else (255,255,255), [M+c*C, M+r*C], 18)
            if self.last: pygame.draw.circle(self.scr, (255,0,0), [M+self.last[1]*C, M+self.last[0]*C], 5)
            pygame.display.flip()

            if self.turn == 2:
                r, c = self.move()
                self.bd[r][c], self.last, self.turn = 2, (r, c), 1
                if self.check(r, c, 2): print("AI Win!"); break
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and self.turn == 1:
                    c, r = round((e.pos[0]-M)/C), round((e.pos[1]-M)/C)
                    if 0<=r<S and 0<=c<S and not self.bd[r][c]:
                        self.bd[r][c], self.last, self.turn = 1, (r, c), 2
                        if self.check(r, c, 1): print("Player Win!"); self.turn = 0
        pygame.time.wait(3000)

if __name__ == "__main__":
    try:
        d = int(input("난이도 (1:하, 2:중, 3:상): ") or 2)
    except: d = 2
    Omok(d).run()