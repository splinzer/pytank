# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午7:33


class BattleObject():
    """物体类"""
    # 物体状态
    # STATUS_DEAD 死亡状态，该状态的物体无法移动，且状态不再发生变化
    # STATUS_STOP 停止状态，除非状态被重置其他状态，否则物体会一直保持静止不动
    # STATUS_MOVING 移动中状态，除非碰撞到物体或边界，该状态的物体会一直按照其方向移动
    STATUS_DEAD = 2
    STATUS_STOP = 3
    STATUS_MOVING = 4

    MAX_VELOCITY = 5

    DIRECTION_UP = 1
    DIRECTION_DOWN = 2
    DIRECTION_LEFT = 3
    DIRECTION_RIGHT = 4

    def __init__(self, width: int = 64, height: int = 64, x: int = 0, y: int = 0):
        """
        初始化
        :param width: 宽度
        :param height: 高度
        :param x: x坐标（以右上角为原点，向左为x轴）
        :param y: y坐标（以右上角为原点，向下为y轴）
        """
        # id是物体的唯一标识
        self.id = 'rectobject'
        self.type = 'rectobject'
        self.width = width
        self.height = height
        # 所在战场
        self.battlefield = None
        self.battlefield_id = None
        # self.weapon_type = 'BattleObject'
        # 以左上角为坐标基准点
        self.x = x
        self.y = y
        # 默认方向向上
        self.direction = self.DIRECTION_UP
        # 默认速度最大
        self.velocity = self.MAX_VELOCITY
        # 自毁延迟次数,表示物体状态变为dead后循环几次再销毁，这里的循环是指update被调用的次数
        # 将要销毁的物体，我们需要一次性告知客户端某个物体已经销毁，而后为了精简服务器与客户端通信的数据长度，
        # 服务器以后下发的数据中将不再包含已销毁物体的任何信息，
        # 这个延时的目的是让服务器能够有时间把物体销毁的消息传给客户端
        self.countdown = 1
        # 是否已被摧毁
        self.dead = False

        # 为True表示当前被阻挡了，可能碰到了障碍物或碰到了战场边界
        self.block = False

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity: int):
        self.velocity = velocity

    def get_direction(self):
        return self.direction

    def set_direction(self, direction: int):
        self.direction = direction

    def get_name(self):
        return self.id

    def set_position(self, x: int, y: int):
        """
        设置位置
        :param x: x坐标
        :param y: y坐标
        :return: None
        """
        self.x = x
        self.y = y

    def get_position(self):
        """
        返回坐标
        :return: 坐标(x,y)
        """
        return self.x, self.y

    def is_collide(self, obj, other_obj):
        """
        计算所有物体之间是否有位置重叠，有则视为发生碰撞
        :param obj:要检测的物体
        :param other_obj:要检测的物体
        :return: 布尔值，检测到碰撞返回True
        """
        obj_position = obj.get_position()
        other_obj_position = other_obj.get_position()
        x1 = obj_position[0]
        y1 = obj_position[1]
        x2 = other_obj_position[0]
        y2 = other_obj_position[1]

        width = obj.width if x1 < x2 else other_obj.width
        height = obj.height if y1 < y2 else other_obj.height

        if abs(x1 - x2) <= width and abs(y1 - y2) <= height:
            return True
        else:
            return False

    def move_step(self, direction: int, velocity: int = 5):
        """
        按照指定方向和速度移动一次
        :param direction:移动方向
        :param velocity:移动速度
        :return:新坐标（Point类型）
        """
        x = self.x
        y = self.y
        # if velocity > self.MAX_VELOCITY:
        #     velocity = self.MAX_VELOCITY
        if direction == self.DIRECTION_UP:
            y -= velocity
        elif direction == self.DIRECTION_DOWN:
            y += velocity
        elif direction == self.DIRECTION_LEFT:
            x -= velocity
        elif direction == self.DIRECTION_RIGHT:
            x += velocity
        # print(self.name, x, y)
        self.set_position(x, y)
        # 每走一步进行一次越界检测
        self.limit_bound()
        # 每走一步进行一次碰撞检测


    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def stop(self):
        self.set_status(self.STATUS_STOP)


    def suicide(self):
        """
        自杀函数，物体销毁时调用该方法进行清理。
        本来该方法中有callback参数作为回调函数，用于销毁rectobject对象，
        由于添加callback函数会导致Manager无法序列化，报错：Can't pickle local object
        所以暂时取消该参数
        :return:
        """
        # self.die_callback = callback
        self.dead = True

    def __destroy(self):
        """
        自毁函数，当self.countdown为零时触发.会自动调用，不要手动调用
        :return:
        """
        # 从共享列表中清除
        self.battlefield.remove_object(self)

        del self


    def __del__(self):
        pass

    def limit_bound(self, delta = 7) -> bool:
        """
        检测对象是否到达战场边沿，是的话将对象的阻塞状态设置为True
        :param delta:定义偏移量，如果对象碰到边界，则按照该偏移量反弹，目的是避免物体被困住。
        :return:布尔值，在战场边沿为True
        """

        pass

    def update(self):
        # 自毁倒计时计数
        if self.dead:
            if self.countdown <= 0:
                self.__destroy()
                return
            self.countdown -= 1
        if self.status == self.STATUS_MOVING:

            self.move_step(self.direction, self.velocity)
            # if self.is_on_edge():
            #     self.stop()
            # else:
            #     self.move_step(self.direction, self.velocity)
