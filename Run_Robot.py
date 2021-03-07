import sys, pygame
from Config import Config
import Constants as C
from Robot import Robot
from collision_managment import create_environment, render_environment
import numpy as np
from math import sqrt
import json

#SET THE WEIGHTS JSON STRING AND CHOOSE THE ROOM HERE, THEN RUN
weights = json.loads('[[[0.8221108717535397, -0.4873091326448733, 0.733576336305489, 0.915262463598095, 0.5976895198812369, 0.017964884918109547], [-0.287461618186974, -0.19207028703245355, -0.5998785852859625, 0.13956190272704583, 0.07118748050039048, -0.1285830385276847], [0.8211587660904476, -0.73152003372673, 0.3058708122885221, 0.4034912391215857, 0.9531564289736101, -0.8685788080599028], [-0.9827118815894933, 0.30978867580044733, -0.6982670950468981, 0.5853367932621523, -0.8848529112855008, -0.2702446367005822], [-0.9163352556154305, -0.8892762836864154, 0.6216847012183024, -0.5148966356580433, 0.8327407885131726, -0.030135833601387496], [0.4432604265422331, 0.7923976184876043, 0.8665891593686585, -0.3611484403435745, -0.22705661992970638, 0.29791017950022103], [0.5252423708675562, 0.6009787804244102, 0.06088436233864791, 0.5417428243381524, 0.018131183136862683, 0.4429482771260935], [0.10462705795473837, 0.46902449835124527, -0.6775495956571873, -0.9246363962067581, -0.16072404745928703, -0.0830039978932331], [-0.86824919342792, -0.13695023292785247, -0.37373020418632485, 0.9125230220537939, 0.6594914664539282, -0.6118495133633746], [0.7237266258430046, 0.1558763282998754, -0.6944003830206456, 0.07859093181393084, 0.9496261948469149, -0.15908101568420951], [0.8998029554709652, -0.03332640046323232, -0.021080391913948615, 0.7336642111501226, 0.6248670382134434, 0.6698727098202462], [-0.44705847550527844, -0.4367467699088978, 0.8691050822477422, 0.9146173856089135, -0.612853743721524, -0.2573044976117447], [-0.6347419814645336, -0.29037061151876364, 0.9537911855840313, 0.15515992418936309, 0.6485407645686585, 0.4673913796584095], [0.15591366321012257, 0.25508200820853255, -0.5919479757524091, 0.7569418984928018, -0.08314557681664758, 0.48606505583851156], [-0.5710476674173228, -0.35260063245665507, 0.2587887416184347, -0.2048026537859673, -0.8380086081890601, -0.3657458433083207], [-0.15813751959846267, -0.1348440351169613, 0.12151350796060756, 0.13187654790547176, 0.15049088156997015, 0.8982364783497871], [0.30084456295272877, -0.3180048183558688, -0.7165300079355037, -0.44739956480201015, 0.017964023549830177, 0.2918718983626385], [-0.22737139497197867, -0.6466590141954243, 0.6516360527996978, -0.30047100824407824, -0.8449574462306368, 0.6679461211805515], [-0.6533591340419589, 0.8161884638998804, -0.6154602030555909, 0.4898208744003594, -0.09285799891423885, 0.6333463810558284]], [[-0.5251306123127839, 0.3434134712171206], [0.5612891245089051, -0.8183450943524253], [0.810180584129252, 0.5227783131123134], [0.8346009643661236, 0.9929951126009338], [0.2607337323921166, 0.6893973862845459], [0.6554217898153372, -0.18036891517530895]]]')
room_number = 7

def clear_room(c, R, blackboard):
    cx = round(c[0])
    cy = round(c[1])
    #R = round(R*3.7795) #from mm to px
    for x in range(-R, R):
        for y in range( round(-R*sqrt(1-x*x/(R*R))) , round(R*sqrt(1-x*x/(R*R))) ):
            blackboard[ min(blackboard.shape[0]-1, max(0, cx+x)) ][ min(blackboard.shape[1]-1, max(0, cy+y)) ]=1


config=Config()
env=create_environment(Config.BOARD_SIZE, room_number)
pygame.init()
screen = pygame.display.set_mode(config.BOARD_SIZE)
robot = Robot(config, pygame, screen, config.BOARD_SIZE, env, C.ROBOT_CYAN, [305, 280], 90, config.BALL_SIZE, config.MAX_VELOCITY, weights)
blackboard=np.zeros(config.BOARD_SIZE, dtype='bool')

for tick in range(400): #config.GENERATION_DURATION
    robot.controller_process()
    robot.move()
    clear_room(robot.position, Config.BALL_SIZE, blackboard)
    #update the sensors' measurement
    robot.check_sensors()
    render_environment(screen, pygame, env)
    robot.draw()
    pygame.display.flip()

print('Area covered %:', np.count_nonzero(blackboard)*100/(config.BOARD_SIZE[0]*config.BOARD_SIZE[1]),'%')

