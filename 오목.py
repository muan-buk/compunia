import pygame, sys, math

# 설정
S, C, M = 15, 40, 40
SZ = C * (S - 1) + M * 2
P_SCORES = {"5": 1000000, "4_OPEN": 80000, "4_CLOSE": 30000, "3_OPEN": 10000}

def get_sc(line, p):
    s = "".join(map(str, line))
    opp = "1" if p == 2 else "2"
    p = str(p)
    if p*5 in s: return P_SCORES["5"]
    if f"0{p*4}0" in s: return P_SCORES["4_OPEN"]
    if f"0{p*4}{opp}" in s or f"{opp}{p*4}0" in s: return P_SCORES["4_CLOSE"]
    if f"0{p*3}0" in s: return P_SCORES["3_OPEN"]
    return 0

class Omok:
    def __init__(self, d):
        pygame.init()
        self.scr = pygame.display.set_mode((SZ, SZ))
        pygame.display.set_caption("AI 오목 - R: 다시 시작, Q: 종료")
        self.font = pygame.font.SysFont("malgungothic", 30)
        self.d = d
        self.reset()

    def reset(self):
        self.bd = [[0]*S for _ in range(S)]
        self.turn, self.last, self.game_over = 1, None, False
        self.msg = ""

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
        lines = self.bd + [[self.bd[r][c] for r in range(S)] for c in range(S)]
        for i in range(-S+1, S):
            lines.append([self.bd[r][r-i] for r in range(S) if 0<=r-i<S])
            lines.append([self.bd[r][S-1-r-i] for r in range(S) if 0<=S-1-r-i<S])
        for l in lines:
            ai += get_sc(l, 2); pl += get_sc(l, 1)
        return ai - pl * 4

    def get_m(self):
        mvs = []
        for r in range(S):
            for c in range(S):
                if self.bd[r][c] == 0:
                    if any(self.bd[nr][nc] for nr in range(max(0,r-1),min(S,r+2)) for nc in range(max(0,c-1),min(S,c+2))):
                        mvs.append((r, c))
        return mvs if mvs else [(7,7)]

    def move(self):
        mvs = self.get_m()
        for p in [2, 1]: 
            for r, c in mvs:
                self.bd[r][c] = p
                if self.check(r, c, p): self.bd[r][c] = 0; return (r, c)
                self.bd[r][c] = 0
        best, best_m = -math.inf, None
        mvs.sort(key=lambda x: abs(x[0]-7) + abs(x[1]-7))
        for r, c in mvs[:15]:
            self.bd[r][c] = 2
            v = self.minimax(self.d, -math.inf, math.inf, False)
            self.bd[r][c] = 0
            if v > best: best, best_m = v, (r, c)
        return best_m if best_m else mvs[0]

    def minimax(self, d, a, b, mx):
        if d == 0: return self.ev()
        mvs = self.get_m()[:8]
        for r, c in mvs:
            self.bd[r][c] = 2 if mx else 1
            v = self.minimax(d-1, a, b, not mx)
            self.bd[r][c] = 0
            if mx: a = max(a, v)
            else: b = min(b, v)
            if b <= a: break
        return a if mx else b

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
            
            if self.game_over:
                txt = self.font.render(self.msg + " R:다시 시작, Q:종료", True, (200, 0, 0))
                self.scr.blit(txt, (SZ//2 - 200, 10))
            
            pygame.display.flip()

            if self.turn == 2 and not self.game_over:
                r, c = self.move()
                self.bd[r][c], self.last, self.turn = 2, (r, c), 1
                if self.check(r, c, 2): self.msg, self.game_over = "AI 승리!", True

            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and self.turn == 1 and not self.game_over:
                    c, r = round((e.pos[0]-M)/C), round((e.pos[1]-M)/C)
                    if 0<=r<S and 0<=c<S and not self.bd[r][c]:
                        self.bd[r][c], self.last, self.turn = 1, (r, c), 2
                        if self.check(r, c, 1): self.msg, self.game_over = "플레이어 승리!", True
                if self.game_over and e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r: self.reset()
                    if e.key == pygame.K_q: pygame.quit(); sys.exit()

if __name__ == "__main__":
    d = int(input("난이도 (1~3): ") or 2)
    Omok(d).run()
