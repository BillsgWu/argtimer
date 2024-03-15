import pygame
import time
pygame.init()
resources = {"FiraCode 40":pygame.font.Font("FiraCode-Regular.ttf",40),
             "FiraCode Bold 100":pygame.font.Font("FiraCode-Medium.ttf",100),
             "FiraCode Bold 300":pygame.font.Font("FiraCode-Medium.ttf",300),
             "ding":pygame.mixer.Sound("ding.mp3")}
def test():
    pass
def main(acolor=[0,128,255],bcolor=[255,128,0],dtime=2.0,tbuf=0.5,discolor=[80,80,80],window=None):
    screen = pygame.display.set_mode([0,0],flags=pygame.FULLSCREEN|pygame.DOUBLEBUF)
    size = screen.get_size()
    screen.fill([0,0,0])
    pygame.display.update()
    keepgoing = True
    clock = pygame.time.Clock()
    user = 0
    atime = dtime
    atimel = dtime
    abuf = tbuf
    btime = dtime
    btimel = dtime
    bbuf = tbuf
    t0 = time.time()
    status = 2
    cnt = 0
    while keepgoing:
        cnt += 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepgoing = False
                elif event.key == pygame.K_SPACE:
                    if status == 0:
                        status = 3
                        atimel = atime
                        t0 = time.time()
                    elif status == 1:
                        status = 2
                        btimel = btime
                        t0 = time.time()
        if status == 0:
            atime = atimel + t0 - time.time()
            if atime < 0:
                t0 = time.time()
                status = 3
                atime = atimel = 0
        elif status == 1:
            btime = btimel + t0 - time.time()
            if btime < 0:
                t0 = time.time()
                status = 2
                btime = btimel = 0
        elif status == 2:
            abuf = tbuf + t0 - time.time()
            if abuf < 0:
                t0 = time.time()
                status = 0
                abuf = tbuf
                resources["ding"].play()
        elif status == 3:
            bbuf = tbuf + t0 - time.time()
            if bbuf < 0:
                t0 = time.time()
                status = 1
                bbuf = tbuf
                resources["ding"].play()
        if atime == 0 and btime == 0:
            resources["ding"].play()
            keepgoing = False
        screen.fill([0,0,0])
        ats = resources["FiraCode Bold 300"].render("%.1f"%atime,True,acolor if status == 0 else discolor)
        bts = resources["FiraCode Bold 300"].render("%.1f"%btime,True,bcolor if status == 1 else discolor)
        abus = resources["FiraCode Bold 100"].render("%.2f"%abuf,True,acolor if status == 2 else discolor)
        bbus = resources["FiraCode Bold 100"].render("%.2f"%bbuf,True,bcolor if status == 3 else discolor)
        screen.blit(ats,[(size[0]/2-ats.get_width())/2,200])
        screen.blit(bts,[(size[0]/2-bts.get_width())/2 + size[0]/2,200])
        screen.blit(abus,[(size[0]/2-abus.get_width())/2,500])
        screen.blit(bbus,[(size[0]/2-bbus.get_width())/2 + size[0]/2,500])
        if window and cnt % 10 == 0:
            window.repaint()
        pygame.display.update()
        clock.tick(60)
    pygame.display.quit()
    time.sleep(1)
if __name__ == "__main__":
    main()