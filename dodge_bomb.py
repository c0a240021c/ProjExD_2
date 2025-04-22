import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#練習３:画面外にでないようにする
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRectまたは爆弾Rect
    戻り値:判定結果タプル(横方向判定、縦方向判定)
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True  #横方向、縦方向用の変数
    #横方向判定
    if rct.left < 0 or WIDTH < rct.right:  #画面外だったら
        yoko = False
    #縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom:  #画面外だったら
        tate = False
    return yoko, tate


#演習1:ゲームオーバー時
def gameover(screen: pg.Surface) -> None:
    """
    引数:screen,font
    戻り値:こうかとんと爆弾がぶつかったときに画面を暗くしてGame Overを表示
    """
    font = pg.font.Font(None,80)
    black_img = pg.Surface((WIDTH,HEIGHT))
    kktn_lye = pg.image.load("fig/8.png")
    kktn_lye2 = pg.image.load("fig/8.png")
    black_img.set_alpha(128)  #半透明にする
    txt = font.render("Game Over", True, (255,255,255))  #Game Overと表示。255は色
    screen.blit(black_img, [0,0])
    screen.blit(txt,[400,300])
    screen.blit(kktn_lye, [340,300])
    screen.blit(kktn_lye2, [730,300])
    pg.display.update()
    time.sleep(5)

#演習2:爆弾のサイズと速度の変更
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:

    bb_accs = [a for a in range (1,11)]
    bb_imgs = []
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    return bb_accs,bb_imgs

    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    #練習2:爆弾の表示
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    #練習2:爆弾rctの座標
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    #練習2:爆弾の移動
    vx = +5
    vy = +5


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        #練習4:こうかとんと爆弾の衝突
        if kk_rct.colliderect(bb_rct):
            #演習1:ゲームオーバー関数を呼び出す
            gameover(screen)
            return

        

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        
        kk_rct.move_ip(sum_mv)

        #練習3:画面外にこうかとんがでないようにする
        if check_bound(kk_rct) != (True, True):  #画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #

        #練習2:爆弾の移動

        #練習3:画面外に爆弾がでないようにする
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(kk_img, kk_rct)
        #演習2:爆弾のサイズと速度
        bb_accs , bb_imgs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500,9)]
        bb_img = bb_imgs[min(tmr//500,9)]

        bb_rct.move_ip(avx,vy)
        #練習2:爆弾の表示
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)







if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
