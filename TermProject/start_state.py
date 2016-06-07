import pygame
from pygame.locals import *
import time # time 모듈을 import

pygame.init() # pygame 라이브러리 초기화

from data import *
from background import Background

WINDOW_SIZE = (1024, 768) # 윈도우 해상도를 800 X 600으로 초기화
SCREEN = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption('휴게소 맛집 파인더') # 타이틀 바의 텍스트를 조정


TARGET_FPS = 60 # 초당 프레임을 60으로 설정
clock = pygame.time.Clock() # 60 FPS를 맞추기 위한 딜레이를 추가

running = True # 메인 루프 상태 변수



data = Data()
background = Background()


def update():

    background.update()

   # print(pygame.time.Clock.get_fps())

def handle_events():
    global running


    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        data.handle_events(event)

def draw():
    SCREEN.fill(WHITE) # 화면을 하얀색으로 채우기


    background.draw(SCREEN)
    data.draw(SCREEN)

 # 텍스트 객체를 생성! 파리미터 : 텍스트 내용, 안티 앨리어싱 사용 여부, 텍스트 컬러
 #    textSurfaceObj = font20.render("안녕하세요", True, BLUE) # 텍스트 객체를 생성
 #    textRectObj = textSurfaceObj.get_rect() # 텍스트 객체의 출력 위치를 가져온다.
 #    textRectObj.center = (350, 300)  # 텍스트 객체의 중심 좌표를 350, 300으로 설정

 #   SCREEN.blit(textSurfaceObj, textRectObj) # 설정한 위치에 텍스트 객체를 출력

    pygame.display.update() # 화면 업데이트


while running: # 메인 루프

    handle_events()  # 키보드, 마우스등 각종 이벤트가 발생하는 곳
    update()  # 프로그램의 정보를 지속적으로 업데이트 해주는 부분
    draw()  # 이미지나 도형 등 화면에 무언가 출력을 하는 부분

    clock.tick(TARGET_FPS)  # 프레임 수 맞추기
    #print(clock.get_fps())

pygame.quit() # 프로그램 종료