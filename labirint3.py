from pygame import *
 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
    #метод, в котором реализовано управление спрайтом по кнопкам стрелкам клавиатуры
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
 
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
 
    def update(self):
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
        # сначала движение по горизонтали
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: # идем направо, правый край персонажа - вплотную к левому краю стены
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # если коснулись сразу нескольких, то правый край - минимальный из возможных
        elif self.x_speed < 0: # идем налево, ставим левый край персонажа вплотную к правому краю стены
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # если коснулись нескольких стен, то левый край - максимальный
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # идем вниз
            for p in platforms_touched:
                self.y_speed = 0
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: # идем вверх
            for p in platforms_touched:
                self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
                self.rect.top = max(self.rect.top, p.rect.bottom) # выравниваем верхний край по нижним краям стенок, на которые наехали
    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 50)
        bullets.add(bullet)
 
#класс спрайта-врага   
class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
 
  #движение врага
    def update(self):
        if self.rect.x <= 250: #w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.x >= win_width - 100:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
 
# класс спрайта-пули  
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    # движение врага
    def update(self):
        self.rect.x += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.x > win_width+10:
            self.kill()
 
#Создаем окошко
win_width = 1280
win_height = 720
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = (128, 128, 128)#задаем цвет согласно цветовой схеме RGB
 
#создаем группу для стен
barriers = sprite.Group()
 
#создаем группу для пуль
bullets = sprite.Group()
 
#создаем группу для монстров
monsters = sprite.Group()
 
#создаем стены картинки
w1 = GameSprite('wall.jpg',250, 300, 1050, 50) #x,y,sizex,sizey
w2 = GameSprite('wall_v.jpg', 100, 100, 50, 700)
w3 = GameSprite('wall.jpg', 250, 600, 1050, 15)
w4 = GameSprite('wall.jpg', 100,100, 1050, 50)
w5 = GameSprite('wall.jpg', 150,450, 1050, 50)
w6 = GameSprite('wall.jpg', 1050,150, 100, 50)
w7 = GameSprite('wall.jpg', 850,250, 100, 50)
w8 = GameSprite('wall.jpg', 650,150, 100, 50)
w9 = GameSprite('wall.jpg', 450,250, 100, 50)
w10 = GameSprite('wall.jpg', 250,150, 100, 50)

 
#добавляем стены в группу
p=[w1,w2,w3,w4,w5,w6,w7,w8,w9,w10]
barriers.add(p)

 
#создаем спрайты
packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 100, 80, 80)
 
monster1 = Enemy('cyborg.png', win_width - 1, 2, 80, 80, 50)
monster2 = Enemy('cyborg.png', win_width - 20, 230, 80, 80, 5)
monster3 = Enemy('cyborg.png', 100, 120, 80, 80,10)
monster4 = Enemy('cyborg.png', 100, 350, 80, 80,10)
monster5 = Enemy('cyborg.png', 100, 350, 80, 80,15)
monster6 = Enemy('cyborg.png', 100, 350, 80, 80,20)
#добавляем монстра в группу
b=[monster1,monster2,monster3,monster4,monster5,monster6]
monsters.add(b)
#переменная, отвечающая за то, как кончилась игра
finish = False
#игровой цикл
run = True
while run:
    #цикл срабатывает каждую 0.05 секунд
    time.delay(50)
    #перебираем все события, которые могли произойти
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -15
            elif e.key == K_RIGHT:
                packman.x_speed = 15
            elif e.key == K_UP:
                packman.y_speed = -15
            elif e.key == K_DOWN:
                packman.y_speed = 15
            elif e.key == K_SPACE:
                packman.fire()
 
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
 
    #проверка, что игра еще не завершена
    if not finish:
        #обновляем фон каждую итерацию
        window.fill(back)#закрашиваем окно цветом
 
        #запускаем движения спрайтов
        packman.update()
        bullets.update()
 
        #обновляем их в новом местоположении при каждой итерации цикла
        packman.reset()
        #рисуем стены 2
        #w1.reset()
        #w2.reset()
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()
 
        if not(sprite.groupcollide(monsters, bullets, True, True)):
            monsters.update()
            monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
 
        #Проверка столкновения героя с врагом и стенами
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            #вычисляем отношение
            img = image.load('game_over.jpg')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (1280, 720)), (0, 0))
 
        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (1280, 720)), (0, 0))
    display.update()