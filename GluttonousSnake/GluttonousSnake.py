import operator
import threading

from enum import Enum
from time import sleep
from car_serial_app import Car_srlapp, MgsType
from rplidar import RPLidar


# 小车状态类型
class State(Enum):
    WAIT = 0
    HEAD = 1
    FOLLOW = 2
    STOP = 3


# 所有需设定的参数：
# 检测状态切换的距离阈值，用于stateControl
Wait2HeadThreshold = 100
Head2FollowThreshold = 100
Follow2StopThreshold = 50

# 目标边界的梯度阈值，用于_get_nearest_target
# 梯度为相邻两个角度的 距离差/角度差
leftGradThreshold = -10
rightGradThreshold = 10

# 不同状态下雷达扫描范围，用于_get_nearest_target
scanned_range = {State.WAIT: (0, 360),
                 State.HEAD: (0, 360),
                 State.FOLLOW: (0, 360)}

# 状态变化检测时间间隔
StateInspectInterval = 0.5

# 头车路径修正时间间隔
HeadPathCorrectionInterval = 1

# 跟随车路径修正时间间隔
FollowPathCorrectionInterval = 1

# 小车速度
TurnSpeed = 85
MoveSpeed = 85

# 小车转向角度偏差阈值(正负乘2）
AngleDeviationThreshold = 5

# 小车转向角度检测间隔
AngleCorrectionInterval = 0.2

threadLock = threading.Lock()


class GluttonousSnake:
    def __init__(self, state = State.WAIT):
        self.state = state
        self.running = True
        self.car_srl = Car_srlapp()
        self.lidar = RPLidar('/dev/ttyUSB0')

    # 状态控制
    def _state_control(self):
        while self.running and self._get_state() is not State.STOP:
            dist, _ = self._get_nearest_target()

            # 加锁避免状态数据同步冲突
            threadLock.acquire()
            if self._get_state() is State.WAIT and dist < Wait2HeadThreshold:
                self.state = State.HEAD
            elif self._get_state() is State.HEAD and dist < Head2FollowThreshold:
                self.state = State.FOLLOW
            elif self._get_state() is State.WAIT and dist < Follow2StopThreshold:
                self.state = State.STOP
            threadLock.release()
            sleep(StateInspectInterval)

    def _wait_main(self):
        while self.running and self._get_state() is State.WAIT:
            pass

    def _head_main(self):
        while self.running and self._get_state() is State.HEAD:
            dest = self._get_nearest_target()
            # 判断是否存在目标,存在则前往，不存在则停止
            # 在state_control外进行了状态切换，代码结构上有缺陷，但性能上更好
            if dest:
                self._go_somewhere(dest)
            else:
                # 加锁避免状态数据同步冲突
                threadLock.acquire()
                self.state = State.STOP
                threadLock.release()
            sleep(HeadPathCorrectionInterval)

    def _follow_main(self):
        while self.running and self._get_state() is State.FOLLOW:
            dest = self._get_nearest_target()

            # 考虑前车停止的碰撞问题，对dest进行修正
            dest = self._follow_dest_correction(dest)

            self._go_somewhere(dest)
            sleep(FollowPathCorrectionInterval)

    def _stop_main(self):
        while self.running and self._get_state() is State.STOP:
            self.car_srl.control(MgsType.CONTROL_STOP)
            self.running = False

    def main(self):
        state_control = threading.Thread(target=self._state_control, args=())

        wait_main = threading.Thread(target=self._wait_main(), args=())
        head_main = threading.Thread(target=self._head_main(), args=())
        follow_main = threading.Thread(target=self._follow_main(), args=())
        stop_main = threading.Thread(target=self._stop_main(), args=())

        threads = {State.HEAD: head_main,
                   State.FOLLOW: follow_main,
                   State.STOP: stop_main}

        cur_state = self._get_state()

        # 如果当前状态为wait，则将wait_main加入threads，便于后续遍历join
        if cur_state is State.WAIT:
            threads[cur_state] = wait_main

        # pre_state用于判断状态切换，以开启新线程
        pre_state = cur_state
        state_control.start()
        threads[pre_state].start()
        while self.running:
            if pre_state is not self._get_state():
                threads[self._get_state()].start()
                pre_state = self._get_state()

        for thread in threads.values():
            thread.join()
        state_control.join()

        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()

    def _get_state(self):
        return self.state

    # 雷达数据获取
    def _get_radar_signal(self):
        scan = next(self.lidar.iter_scans(300, 200))
        radar_signal = {}
        for i in scan:
            radar_signal[i[1]] = i[2]
        return radar_signal

    # 控制小车朝向dest运动
    def _go_somewhere(self, dest):
        _, yaw, _ = self.car_srl.request(MgsType.REQUEST_POSE)

        # yaw的顺逆时针朝向未知，故此处为+或-待定
        yaw_zero = yaw - dest[1]
        self.car_srl.control(MgsType.CONTROL_TURN, TurnSpeed)
        while abs(yaw_zero - yaw) > AngleDeviationThreshold:
            sleep(AngleCorrectionInterval)
            _, yaw, _ = self.car_srl.request(MgsType.REQUEST_POSE)
        self.car_srl.control(MgsType.CONTROL_STOP)
        self.car_srl.control(MgsType.CONTROL_MOVE, MoveSpeed)

    # 获取数据梯度信息
    def _get_grads(self, sorted_signal):
        grads = []
        for index in range(1, len(sorted_signal)):
            delta = sorted_signal[index - 1][0] - sorted_signal[index][0]
            theta = sorted_signal[index - 1][0]
            grad = (sorted_signal[index - 1][1] - sorted_signal[index][1]) / delta
            grads.append((theta, grad))
        return grads

    # 根据梯度信息获取所有目标的角度（左右边界角度的平均值）及距离（目前使用的左边界距离）
    def _get_targets(self, grads, radar_signal):
        targets = []
        temp_boundary = 0
        for i in grads:
            if i[1] < leftGradThreshold and temp_boundary == 0:
                temp_boundary = i[0]
            elif i[1] > rightGradThreshold and temp_boundary != 0:
                targets.append((radar_signal[i[0]], (temp_boundary + i[0])/2))
                temp_boundary = 0
        return targets

    # 返回范围内最近目标的位置信息
    def _get_nearest_target(self):
        # TODO 跨越360~0边界的目标检测还有BUG存在
        radar_signal = self._get_radar_signal()

        # 筛选所需范围的雷达数据
        radar_signal_ranged = {}
        for i in radar_signal:
            if scanned_range[self._get_state()][0] <= i <= scanned_range[self._get_state()][1]:
                radar_signal_ranged[i] = radar_signal[i]

        # 对筛选后的数据进行排序
        sorted_signal = sorted(radar_signal_ranged.items(), key=operator.itemgetter(0))
        grads = self._get_grads(sorted_signal)
        targets = self._get_targets(grads, radar_signal)

        # 考虑搜寻不到目标的情况
        if targets:
            target = min(targets)
        else:
            target = ()
        return target

    # TODO 对跟随目标修正，以避免碰撞
    def _follow_dest_correction(self, dest):
        return dest


if __name__ == '__main__':
    # 根据指令内容初始化state
    # state = State.WAIT
    state = State.HEAD
    gluttonous_snake = GluttonousSnake(state)
    gluttonous_snake.main()
