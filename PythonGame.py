import pygame
import random
import os
import time

#参数
FPS=60
WIDTH=400
HEIGH=600
LIFE=5
SCORE=0
MAXSCORE=0
BULLETSNUM=100
CANNONSUM=3
DEFSUM=2
WAIT_TIME=0.5
CURDEFPER=0
PAUSE=0

#颜色
COLOR_WHITE=(246,246,246)
COLOR_BLACK=(0,0,0)
COLOR_GREEN=(0,255,0)
COLOR_RED=(255,0,0)
COLOR_BLUE=(0,0,255)
COLOR_PINK=(241,124,150)

#游戏初始化和视窗
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGH))
pygame.display.set_caption("hello world")
clock=pygame.time.Clock()#创建时间管理对象
#文件读取
f=open('score.txt','a+')
position = f.seek(0, 0)
strscore=f.readline()
if len(strscore)>0:
    MAXSCORE=int(strscore)
else :
    MAXSCORE=0
f.close()



#载入图片
background_img=pygame.image.load(os.path.join("img","background.png")).convert()#背景
player_img=pygame.image.load(os.path.join("img","player.png")).convert()#玩家
def_img=pygame.image.load(os.path.join("img","def.png")).convert()#防护罩
deficon_img=pygame.image.load(os.path.join("img","defico.png")).convert()#防护罩实例
life_img=pygame.image.load(os.path.join("img","life.png")).convert()#生命
cannon_img=pygame.image.load(os.path.join("img","reward2.png")).convert()#炮弹
#游戏图标
pygame.display.set_icon(cannon_img)
rock_img=[]#敌人
for i in range(2):
    name = ''.join(['rock',str(i),'.png'])
    rock_img.append(pygame.image.load(os.path.join("img",name)).convert())
bullet_img=pygame.image.load(os.path.join("img","bullet.png")).convert()#子弹
reward_img=[]#掉落奖励
for i in range(4):
    name = ''.join(['reward',str(i),'.png'])
    reward_img.append(pygame.image.load(os.path.join("img",name)).convert())
#爆炸
expl_anim={}
expl_anim['lg']=[]
expl_anim['sm']=[]
expl_anim['ov']=[]
expl_anim['kn']=[]
expl_anim['bk']=[]
expl_img=[]
for i in range(1,10):
    name = ''.join(['exp',str(i),'.png'])
    img=pygame.image.load(os.path.join("img",name)).convert()
    img.set_colorkey((236,240,249))
    expl_anim['lg'].append(pygame.transform.scale(img,(90,90)))
    expl_anim['sm'].append(pygame.transform.scale(img,(30,30)))
    name = ''.join(['pexp',str(i),'.png'])
    img=pygame.image.load(os.path.join("img",name)).convert()
    img.set_colorkey((236,240,249))
    expl_anim['ov'].append(pygame.transform.scale(img,(120,120)))
    name = ''.join(['knockexp',str(i),'.png'])
    img=pygame.image.load(os.path.join("img",name)).convert()
    img.set_colorkey((246,246,246))
    expl_anim['kn'].append(pygame.transform.scale(img,(30,30)))
    name = ''.join(['breakexp',str(i),'.png'])
    img=pygame.image.load(os.path.join("img",name)).convert()
    img.set_colorkey((246,246,246))
    expl_anim['bk'].append(pygame.transform.scale(img,(120,120)))

#载入音乐
#音效初始化
pygame.mixer.init()
shoot_sound=pygame.mixer.Sound(os.path.join("sound","shoot.wav"))#射击
shoot_cannon_sound=pygame.mixer.Sound(os.path.join("sound","shoot_cannon.wav"))#炮弹射击
attacked_sound=pygame.mixer.Sound(os.path.join("sound","attacked.wav"))#受到攻击
over_sound=pygame.mixer.Sound(os.path.join("sound","over.wav"))#结束音乐
death_sound=pygame.mixer.Sound(os.path.join("sound","death.wav"))#敌人死亡
heart_sound=pygame.mixer.Sound(os.path.join("sound","heart.wav"))#获得爱心
lackbullet_sound=pygame.mixer.Sound(os.path.join("sound","lackbullet.wav"))#没有子弹
installbullet_sound=pygame.mixer.Sound(os.path.join("sound","installbullet.wav"))#获得子弹
installcannon_sound=pygame.mixer.Sound(os.path.join("sound","installcannon.wav"))#获得炮弹
defstart_sound=pygame.mixer.Sound(os.path.join("sound","defstart.wav"))#启动防护罩
knock_sound=pygame.mixer.Sound(os.path.join("sound","knock.wav"))#撞击防护罩
break_sound=pygame.mixer.Sound(os.path.join("sound","break.wav"))#防护罩碎裂

background_sound=pygame.mixer.music.load(os.path.join("sound","background.wav"))#背景音乐

pygame.mixer.music.set_volume(0.3)

#方法
font_name=pygame.font.match_font('arial',1,1)#获取字体类型
def draw_text(surf,text,size,color,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)

def draw_init(SCORE):
    screen.blit(background_img,(0,0))#目标，位置
    draw_text(screen,'HELLO    WORLD!',40,COLOR_BLACK,WIDTH/2,HEIGH/2-80)
    draw_text(screen,''.join(['HIGHEST SCORE:',str(MAXSCORE)]),30,COLOR_BLACK,WIDTH/2,HEIGH/2-15)
    draw_text(screen,''.join(['CURRY SCORE:',str(SCORE)]),30,COLOR_BLACK,WIDTH/2,HEIGH/2+15)
    draw_text(screen,'Press KeyPad Enter To Start!',20,COLOR_BLACK,WIDTH/2,HEIGH-30)
    
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)#一秒钟之內最多执行十次，限制刷新次数
    #取得输入
        for event in pygame.event.get():#该方法返回用户输入的所有时间，形式为列表
            if event.type == pygame.QUIT:
                pygame.quit()
                f.close()
                return True
            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_KP_ENTER:
                    waiting=False
                    return False
#类声明
#玩家
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(60,60))
        self.image.set_colorkey(COLOR_WHITE)#将指定色变透明
        self.rect=self.image.get_rect()#将角色包装为矩形框用于定位
        self.radius=25
        #圆形辅助
        #pygame.draw.circle(self.image,COLOR_RED,self.rect.center,self.radius)
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HEIGH-10
        self.speedx=10
        self.life=LIFE
        self.bullet_num=BULLETSNUM
        self.cannon_num=CANNONSUM
        self.def_num=DEFSUM
        self.isdef=0
        self.isempty=1
    
    def update(self):
        #操控
        key_pressed=pygame.key.get_pressed()#按键输入
        if key_pressed[pygame.K_RIGHT] and self.rect.right<WIDTH:
            self.rect.x+=self.speedx
        if key_pressed[pygame.K_LEFT] and self.rect.left>0:
            self.rect.x-=self.speedx
    #攻击
    def shoot(self):
        if self.bullet_num>0:
            bullet=Bullet(self.rect.centerx,self.rect.top,-10)
            self.bullet_num-=1
            all_sprites.add(bullet)
            bullets_sprites.add(bullet)
            shoot_sound.play()
        else:
            lackbullet_sound.play()

    #炮弹攻击
    def shoot2(self):
        if self.cannon_num>0:
            cannon=Cannon(self.rect.centerx,self.rect.top,100,-4)
            self.cannon_num-=1
            all_sprites.add(cannon)
            bullets_sprites.add(cannon)
            shoot_cannon_sound.play()
        else:
            lackbullet_sound.play()

    #启动防御
    def defend(self):
        if self.def_num>0 and self.isdef==0:
            self.def_num-=1
            defstart_sound.play()
            defend=Def(player)
            CURDEFPER=100
            all_sprites.add(defend)
            bullets_sprites.add(defend)#防护罩事件
            self.isdef=1
        else:
            lackbullet_sound.play()
#最高值图例
class Highscore(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(30,30))
        self.image.set_colorkey(COLOR_WHITE)#将指定色变透明
        self.rect=self.image.get_rect()#将角色包装为矩形框用于定位
        self.rect.x=x
        self.rect.y=y  
#血条
class Life(pygame.sprite.Sprite):
    def __init__(self,num):
        pygame.sprite.Sprite.__init__(self)
        #绘制血量
        self.image=pygame.transform.scale(life_img,(30,30))
        self.image.set_colorkey(COLOR_WHITE)#将指定色变透明
        self.rect=self.image.get_rect()#将角色包装为矩形框用于定位
        self.rect.x=WIDTH-self.rect.width*num
        self.rect.y=0
#敌人
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img=random.choice(rock_img)
        if img==rock_img[0]:
            self.image=pygame.transform.scale(img,(90,90))
            self.image.set_colorkey((255,255,255))#将指定色变透明
            self.radius=40
        else :
            self.image=pygame.transform.scale(img,(50,50))
            self.image.set_colorkey((246,246,246))#将指定色变透明
            self.radius=20
        self.rect=self.image.get_rect()#将角色包装为矩形框用于定位
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=0
        self.speedy=random.randrange(1,6)
        self.speedx=random.randrange(-2,2)

    def update(self):
        #下落
        self.rect.x+=self.speedx
        if self.rect.left<=0 or self.rect.right>=WIDTH:#碰到边界则反向
            self.speedx=-self.speedx
            self.image=pygame.transform.flip(self.image,True,False)
        self.rect.y+=self.speedy 
            
        if self.rect.bottom>=HEIGH:
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.rect.y=0
            self.speedy=random.randrange(1,6)
            self.speedx=random.randrange(-2,2)
#掉落奖励
class Reward(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=random.choice(reward_img)
        if img==reward_img[0]:
            self.image=pygame.transform.scale(img,(40,40))
            self.image.set_colorkey((255,255,255))#将指定色变透明
            self.radius=19
        elif img==reward_img[1]:
            self.image=pygame.transform.scale(img,(40,40))
            self.image.set_colorkey((246,246,246))#将指定色变透明
            self.radius=20
        elif img==reward_img[2]:
            self.image=pygame.transform.scale(img,(40,40))
            self.image.set_colorkey((246,246,246))#将指定色变透明
            self.radius=21
        else:
            self.image=pygame.transform.scale(img,(40,40))
            self.image.set_colorkey((84,84,84))#将指定色变透明
            self.radius=22

        self.rect=self.image.get_rect()#将角色包装为矩形框用于定位
        self.rect.centerx=x
        self.rect.centery=y
        self.speedy=3

    def update(self):
        #下落
        if self.rect.bottom>=HEIGH:
            self.kill()#超过边界，自动销毁
        else:
            self.rect.y+=self.speedy
#子弹
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bullet_img,(10,20))
        self.image.set_colorkey(COLOR_BLACK)#将指定色变透明
        self.rect=self.image.get_rect()#将角色包装为矩形框用于定位
        self.rect.x=x
        self.rect.y=y
        self.speedy=speed
        self.type=0

    def update(self):
        #攻击
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()#删除子弹
#炮弹
class Cannon(pygame.sprite.Sprite):
    def __init__(self,x,y,scl,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(cannon_img,(scl,scl))
        self.image.set_colorkey((246,246,246))#将指定色变透明
        self.rect=self.image.get_rect()#将角色包装为矩形框用于定位
        self.rect.centerx=x
        self.rect.bottom=y
        self.speedy=speed
        self.type=1

    def update(self):
        #攻击
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()#删除炮弹
#爆炸
class Explostion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size=size
        self.image=expl_anim[self.size][0]
        self.rect=self.image.get_rect()#将角色包装为矩形框用于定位
        self.rect.center=center
        self.frame=0
        self.last_update=pygame.time.get_ticks()
        self.frame_rate=50

    def update(self):
        #攻击
        now=pygame.time.get_ticks()
        if now-self.last_update>self.frame_rate:
            self.last_update=now
            self.frame+=1
            if self.frame==len(expl_anim[self.size]):
                self.kill()
            else:
                self.image=expl_anim[self.size][self.frame]
                center=self.rect.center
                self.rect=self.image.get_rect()
                self.rect.center=center
#防护罩
class Def(pygame.sprite.Sprite):
    def __init__(self,player):
        pygame.sprite.Sprite.__init__(self)
        #绘制血量
        self.image=pygame.transform.scale(def_img,(90,75))
        self.image.set_colorkey((84,84,84))#将指定色变透明
        self.rect=self.image.get_rect()#将角色包装为矩形框用于定位
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HEIGH-10
        self.life=5
        self.type=2
    def update(self):
        self.rect.centerx=player.rect.centerx
#防护罩图例
class Defico(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #绘制血量
        self.image=pygame.transform.scale(def_img,(30,30))
        self.image.set_colorkey((84,84,84))#将指定色变透明
        self.rect=self.image.get_rect()#将角色包装为矩形框用于定位
        self.rect.x=x
        self.rect.y=y

#初始化
pygame.mixer.music.play(-1)#背景乐播放
show_init=True
running=True


while running:
    if show_init:
        close=draw_init(SCORE)
        if close:
            break
        SCORE=0
        show_init=False

        #实例化类 
        #玩家
        all_sprites=pygame.sprite.Group()
        player=Player()
        all_sprites.add(player)
        #血条
        life_sprites=pygame.sprite.Group()
        names = locals()
        for i in range(1,player.life+1):
            names['n' + str(i) ]=Life(i)
            life_sprites.add(names['n' + str(i) ])
        #子弹图例
        for i in range(3):
            bullet_exm=Bullet(10*i,0,0)
            all_sprites.add(bullet_exm)
        #炮弹图例
        cannon_exm=Cannon(16,55,30,0)
        all_sprites.add(cannon_exm)
        #防护罩图例
        defico_exm=Defico(0,95)
        all_sprites.add(defico_exm)
        #最高值图例
        highscore=Highscore(0,60)
        all_sprites.add(highscore)
        #子弹组
        bullets_sprites=pygame.sprite.Group()
        #敌人组
        rocks_sprites=pygame.sprite.Group()
        for i in range(7):
            rock=Rock()
            all_sprites.add(rock)
            rocks_sprites.add(rock)
        #奖励组
        rewards_sprites=pygame.sprite.Group()

    #无子弹，给空投
    if player.bullet_num==0 and player.cannon_num==0 and player.def_num==0:
        
        if player.isempty==1:
            begintime=pygame.time.get_ticks()#毫秒为单位
            player.isempty=0
        else :
            currtime=pygame.time.get_ticks()
            if currtime-begintime>3000:#三秒施放空投
                for i in range(3):
                    reward=Reward(random.randrange(0,WIDTH-25),0)
                    all_sprites.add(reward)
                    rewards_sprites.add(reward)
                player.isempty=1

    clock.tick(FPS)#一秒钟之內最多执行十次，限制刷新次数
    #输入事件
    for event in pygame.event.get():#该方法返回用户输入的所有时间，形式为列表
        if event.type == pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                player.shoot()#射击事件
            if event.key==pygame.K_q:
                player.shoot2()#射击炮弹事件
            if event.key==pygame.K_e:
                player.defend()#防御事件
            if event.key==pygame.K_ESCAPE:
                PAUSE=1#暂停
    while PAUSE:
        for event in pygame.event.get():#该方法返回用户输入的所有时间，形式为列表
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                PAUSE=0#暂停



    #更新游戏
    all_sprites.update()
    #碰撞
    hits=pygame.sprite.groupcollide(rocks_sprites,bullets_sprites,True,False)#子弹与敌人
    for hit in hits:
        death_sound.play()
        SCORE+=1
        r=Rock()
        rocks_sprites.add(r)
        all_sprites.add(r)
        for b in hits[hit]:
            if b.type==0:#子弹则销毁，炮弹不销毁
                expl=Explostion(hit.rect.center,'sm')
                all_sprites.add(expl)
                b.kill()
            elif b.type==1:#炮弹 
                expl=Explostion(hit.rect.center,'lg')
                all_sprites.add(expl)
            else :#防护罩
                if b.life<1:#破防
                    expl=Explostion(b.rect.center,'bk')
                    all_sprites.add(expl)
                    CURDEFPER=0
                    break_sound.play()
                    b.kill()
                    player.isdef=0
                else:
                    expl=Explostion(hit.rect.center,'kn')
                    all_sprites.add(expl)
                    knock_sound.play()
                    b.life-=1
                    CURDEFPER=b.life*20
        #有几率生成掉落物
        if random.randint(0,7)==3:
            reward=Reward(hit.rect.centerx,hit.rect.centery)
            all_sprites.add(reward)
            rewards_sprites.add(reward)

    hits=pygame.sprite.spritecollide(player,rewards_sprites,False,pygame.sprite.collide_circle)#奖励与玩家
    for hit in hits:
        if hit.radius==20:#爱心
            if player.life<LIFE:
                heart_sound.play()
                player.life+=1
                names['n' + str(player.life) ]=Life(player.life)
                life_sprites.add(names['n' + str(player.life) ])
                j=1
        elif hit.radius==19:#弹药
            if player.bullet_num<BULLETSNUM:
                player.bullet_num=player.bullet_num+10 if player.bullet_num+10<=BULLETSNUM else BULLETSNUM
                installbullet_sound.play()
        elif hit.radius==21:#炮弹
            if player.cannon_num<CANNONSUM:
                player.cannon_num=player.cannon_num+1
                installcannon_sound.play()
        else : #防护罩
            if player.def_num<DEFSUM:
                player.def_num=player.def_num+1
                installcannon_sound.play()
        hit.kill()

    hits=pygame.sprite.spritecollide(player,rocks_sprites,False,pygame.sprite.collide_circle)#敌人与玩家
    for hit in hits:
        hit.kill()        
        if player.life>0:
            attacked_sound.play()
            expl=Explostion(hit.rect.center,'sm')
            all_sprites.add(expl)
            life_sprites.remove(names['n' + str(player.life) ])
            player.life-=1
            q=2
        else:
            if SCORE>MAXSCORE:
                MAXSCORE=SCORE
                f = open('score.txt', 'w+')
                f.write(str(MAXSCORE))#写入最高分
                f.close()
            over_sound.play()
            start_time = time.time()  # remember when we started
            expl=Explostion(player.rect.center,'ov')
            all_sprites.add(expl)
            screen.blit(background_img,(0,0))#目标，位置
            all_sprites.draw(screen)#将元素对象都显示在画面上
            
            while (time.time() - start_time) < WAIT_TIME:
                pygame.display.update()
                1==1
            show_init=True
        r=Rock()
        rocks_sprites.add(r)
        all_sprites.add(r)

    #显示画面
    screen.blit(background_img,(0,0))#目标，位置
    all_sprites.draw(screen)#将元素对象都显示在画面上
    life_sprites.draw(screen)
    draw_text(screen,str(SCORE),30,COLOR_GREEN,WIDTH/2,0)#分数
    draw_text(screen,str(player.bullet_num),20,(181,12,5),45,0)#子弹数目
    draw_text(screen,str(player.cannon_num),20,(181,12,5),45,35)#炮弹数目
    draw_text(screen,str(player.def_num),20,(181,12,5),45,100)#防护罩数目
    draw_text(screen,''.join([str(CURDEFPER),'%']),15,COLOR_BLUE,70,105)#防护罩耐久
    draw_text(screen,str(MAXSCORE),20,(181,12,5),45,70)#最高分数
    
    pygame.display.update()


