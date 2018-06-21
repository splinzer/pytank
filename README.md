# PYTANK

Pytank是一个面向python程序员的坦克游戏。

Pytank is a tank game for python coder

用你写的代码控制坦克来和别人代码控制的坦克进行战斗，决出更出色的坦克控制代码。

You will write a python code to control your tank and fight with your enemies.

## 如何启动 how to start

在终端运行以下命令，就可以看到坦克开始战斗了（内置了2个坦克控制代码）：

run below commad in terminal to start a pytank game (there are two tank code already):

> bash run.bash

## 运行环境 enviroment

- python 3.6

- ubuntu 16.04 LTS（目前仅在此平台上进行了测试 only tested on this system）

## 游戏玩法 how to play

首先打开client/tank/目录，这里看到的tankAI_*.py就是用来控制坦克的代码。
你可以以此为模板进行修改，你只需要修改以下2点：
1. 在on_start方法里，通过以下形式为自己的坦克命名

   > self.set_name('Tom')

2. 在on_update方法里，实现自己的坦克控制代码。
on_update方法提供的battle参数提供了不断更新的战场对象（默认0.1秒更新一次）。通过判断战场的状况来控制你坦克的行为。

## 坦克控制代码
AI类用于控制坦克的移动、攻击，你应该在这个类里实现所有坦克的控制逻辑

    - on_update方法的第二个参数battle对象专门用于获取战场信息，该对象结构如下：

        battle─┬───width（战场宽度）
               │
               ├───height（战场高度）
               │
               │
               │ （坦克对象列表）
               ├───tanks[0]─┬───id（唯一编号）
               │            ├───type（物体类型，共2种：tank、bullet）
               │            ├───width（坦克高度）
               │            ├───height（坦克高度）
               │            ├───x（x坐标）
               │            ├───y（y坐标）
               │            ├───status（当前状态，共3种：STATUS_DEAD、STATUS_STOP、STATUS_MOVING）
               │            ├───block（为True表示当前被阻挡了，可能碰到了障碍物或碰到了战场边界）
               │            ├───life（剩余血量）
               │            ├───ammo(剩余弹药）
               │            ├───oil（剩余油量）
               │
               │  （子弹对象列表）
               ├───bullets[0]─┬───id（唯一编号）
               │              ├───type（物体类型，共2种：tank、bullet）
               │              ├───x（x坐标）
               │              ├───y（y坐标）
               │              ├───owner_id（发射该子弹的坦克id）
               └


    - 方法：提供了以下方法用于控制坦克进行战斗（详见方法注释）：

        start_move    向指定方向持续移动
        stop_move     停止移动
        start_fire    使用指定武器开火
        hold_fire     停止射击

    - 状态：坦克
        STATUS_DEAD 死亡状态，该状态的物体无法移动，且状态不再发生变化
        STATUS_STOP 停止状态，除非状态被重置其他状态，否则物体会一直保持静止不动
        STATUS_MOVING 移动中状态，除非碰撞到物体或边界，该状态的物体会一直按照其方向移动

    注意，在一次update函数调用中，tank的同一种状态如果发生多次变化，则以最后一次状态为准
    ./tank目录专用于存放坦克AI程序，系统会自从该目录导入坦克AI程序，请确保所有逻辑都放在一个文件中