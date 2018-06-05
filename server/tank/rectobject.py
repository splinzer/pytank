# coding:utf8
# @author : Guoxi
# @email  : splinzer@gmail.com
# @time   : 2018 下午7:33


class RectObject():
    """物体类"""
    # 物体状态
    # STATUS_READY 就绪状态
    # STATUS_DEAD 死亡状态，该状态的物体无法移动，且状态不再发生变化
    # STATUS_STOP 停止状态，除非状态被重置其他状态，否则物体会一直保持静止不动
    # STATUS_MOVING 移动中状态，除非碰撞到物体或边界，该状态的物体会一直按照其方向移动
    STATUS_READY = 1
    STATUS_DEAD = 2
    STATUS_STOP = 3
    STATUS_MOVING = 4

    MAX_VELOCITY = 5

    DIRECTION_UP = 1
    DIRECTION_DOWN = 2
    DIRECTION_LEFT = 3
    DIRECTION_RIGHT = 4

    def __init__(self, width: int, height: int, x: int = 0, y: int = 0):
        """
        初始化
        :param name: 名称
        :param width: 宽度
        :param height: 高度
        :param x: x坐标（以右上角为原点，向左为x轴）
        :param y: y坐标（以右上角为原点，向下为y轴）
        """
        self.id = 'rectobject'
        self.id = None
        self.width = width
        self.height = height
        # self.weapon_type = 'RectObject'
        # 以左上角为坐标基准点
        self.x = x
        self.y = y
        # 默认方向向上
        self.direction = self.DIRECTION_UP
        # 默认速度最大
        self.velocity = self.MAX_VELOCITY
        # 自毁延时,状态变为STATUS_DEAD后多久删除自己，这里的值不是一个时间，而是update的次数
        self.countdown = 1

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

    def get_center(self):
        x = self.x + self.width // 2
        y = self.y + self.height // 2
        return x, y

    def isCollide(self, obj, other_obj):
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
        if velocity > self.MAX_VELOCITY:
            velocity = self.MAX_VELOCITY
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

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def stop(self):
        self.set_status(self.STATUS_STOP)

    def ready(self):
        self.set_status(self.STATUS_READY)
    # 自杀函数，callback是回调函数，用于销毁rectobject对象
    def die(self, callback):
        self.die_callback = callback
        self.set_status(self.STATUS_DEAD)

    # 自毁函数，只有当self.countdown为零时触发.会自动调用，不要手动调用
    def __destroy(self):
        self.die_callback(self)
        del self

    def __del__(self):
        pass

    def update(self):
        # 自毁倒计时计数
        if self.status == self.STATUS_DEAD:
            if self.countdown <= 0:
                self.__destroy()
                return
            self.countdown -= 1

        # print('status:{},STATUS_MOVING:{}'.format(self.status,STATUS_MOVING))
        if self.status == self.STATUS_MOVING:
            self.move_step(self.direction, self.velocity)
