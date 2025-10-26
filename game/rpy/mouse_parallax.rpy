init python:
    import pygame
    import math
    
    # 倾角传感器管理器
    class TiltSensorManager:
        def __init__(self):
            self.pitch = 0.0  # 俯仰角（前后翻动）
            self.roll = 0.0   # 横滚角（左右倾斜）
            self.yaw = 0.0    # 偏航角（左右转动）
            self.initialized = False
            self.sensor_listener = None
            self.sensor_manager = None
            self.accel_values = [0, 0, 0]  # 加速度传感器
            self.magnetic_values = [0, 0, 0]  # 地磁传感器
            # 尝试初始化传感器
            self.init_sensors()
        def init_sensors(self):
            try:
                # Android相关
                import jnius
                PythonActivity = jnius.autoclass('org.renpy.android.PythonSDLActivity')
                Context = jnius.autoclass('android.content.Context')
                Sensor = jnius.autoclass('android.hardware.Sensor')
                SensorManager = jnius.autoclass('android.hardware.SensorManager')
                activity = PythonActivity.mActivity
                self.sensor_manager = activity.getSystemService(Context.SENSOR_SERVICE)
                # 加速度传感器和地磁传感器
                self.accelerometer = self.sensor_manager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
                self.magnetometer = self.sensor_manager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD)    
                if self.accelerometer is None or self.magnetometer is None:
                    print("设备缺少必要的传感器")
                    return
                class SensorListener(jnius.PythonJavaClass):
                    __javainterfaces__ = ['android/hardware.SensorEventListener']
                    def __init__(self, manager, **kwargs):
                        super(SensorListener, self).__init__(**kwargs)
                        self.manager = manager
                    @jnius.java_method('(Landroid/hardware/SensorEvent;)V')
                    def onSensorChanged(self, event):
                        # 根据传感器类型存储数据
                        if event.sensor.getType() == Sensor.TYPE_ACCELEROMETER:
                            self.manager.accel_values = [event.values[0], event.values[1], event.values[2]]
                        elif event.sensor.getType() == Sensor.TYPE_MAGNETIC_FIELD:
                            self.manager.magnetic_values = [event.values[0], event.values[1], event.values[2]]
                        # 计算倾角
                        self.manager.calculate_orientation()
                    @jnius.java_method('(Landroid/hardware/Sensor;I)V')
                    def onAccuracyChanged(self, sensor, accuracy):
                        pass
                self.sensor_listener = SensorListener(self)
                self.sensor_manager.registerListener(
                    self.sensor_listener,
                    self.accelerometer,
                    SensorManager.SENSOR_DELAY_GAME
                )
                self.sensor_manager.registerListener(
                    self.sensor_listener,
                    self.magnetometer,
                    SensorManager.SENSOR_DELAY_GAME
                )
                self.initialized = True
                print("倾角传感器初始化成功")
                
            except Exception as e:
                print(f"无法初始化倾角传感器: {e}")
                self.initialized = False
        
        def calculate_orientation(self):
            """根据加速度和地磁数据计算设备方向"""
            try:
                import jnius
                SensorManager = jnius.autoclass('android.hardware.SensorManager')
                # 计算旋转矩阵
                R = [0] * 9
                I = [0] * 9
                success = SensorManager.getRotationMatrix(R, I, self.accel_values, self.magnetic_values)
                if success:
                    # 获方向数据
                    orientation = [0] * 3
                    SensorManager.getOrientation(R, orientation)
                    # 转换为角都（弧度转角度）
                    self.yaw = math.degrees(orientation[0])   # 偏航角（左右转动）
                    self.pitch = math.degrees(orientation[1]) # 俯仰角（前后翻动）
                    self.roll = math.degrees(orientation[2])  # 横滚角（左右倾斜）                 
            except Exception as e:
                print(f"计算方向时出错: {e}")
        
        def stop(self):
            if self.sensor_manager and self.sensor_listener:
                try:
                    self.sensor_manager.unregisterListener(self.sensor_listener)
                except:
                    pass
    
    # 创建全局倾角传感器管理器
    tilt_sensor_manager = None
    if renpy.variant("mobile") and not (renpy.variant("pc") or renpy.variant("web")):
        tilt_sensor_manager = TiltSensorManager()
    
    # 老马出品的视差
    class TrackCursor(renpy.Displayable):
        def __init__(self, child, paramod=1.0, sensitivity=0.5, threshold=5.0, 
                    flip_sensitivity=1.0, dead_zone=10.0, **kwargs):
            super(TrackCursor, self).__init__()
            # 图片
            self.child = child
            # 移动参数
            self.paramod = paramod
            # 灵敏度控制
            self.sensitivity = sensitivity * 1.5
            # 倾斜阈值（度），超过此值才开始移动
            self.threshold = threshold
            # 翻转灵敏度（控制翻转方向的影响程度）
            self.flip_sensitivity = flip_sensitivity
            # 死区角度（度），在此范围内不响应翻转
            self.dead_zone = dead_zone
            
            # 输入数据
            self.input_x = 0
            self.input_y = 0
            # 渲染坐标
            self.x = 0
            self.y = 0
            # 时间轴
            self.old_time = 0
            self.delta_time = 0
            # 尺寸
            self.child_width = 0
            self.child_height = 0
            # 自适应渲染检查
            self.size_initialized = False
            
            # 判断平台
            self.is_mobile = renpy.variant("mobile") and not (renpy.variant("pc") or renpy.variant("web"))
            
            # 基准角度（初始位置）
            self.base_yaw = 0  
            self.base_pitch = 0 
            self.calibrated = False
            
            # 翻转状态跟踪
            self.last_flip_direction = 0  # 0: 未翻转, 1: 正向翻转, -1: 反向翻转
        
        def event(self, ev, x, y, st):
            if not self.is_mobile and ev.type == pygame.MOUSEMOTION:
                # 计算鼠标相对于屏幕中心的偏移量
                center_x = config.screen_width / 150
                center_y = config.screen_height / 5.5
                offset_x = (x - center_x) / self.paramod
                offset_y = (y - center_y) / self.paramod
                
                self.input_x = offset_x
                self.input_y = offset_y
            elif ev.type == pygame.MOUSEBUTTONDOWN and self.is_mobile:
                self.calibrate_sensors()
        
        def calibrate_sensors(self):
            """校准传感器，设置当前姿态为基准"""
            if tilt_sensor_manager and tilt_sensor_manager.initialized:
                self.base_yaw = tilt_sensor_manager.yaw
                self.base_pitch = tilt_sensor_manager.pitch
                self.calibrated = True
                print(f"传感器已校准: yaw={self.base_yaw}, pitch={self.base_pitch}")
        
        def calculate_flip_direction(self, angle_diff):
            """计算翻转方向并应用死区"""
            if abs(angle_diff) < self.dead_zone:
                return 0  # 在死区内，不响应
            
            # 计算翻转方向（1: 正向, -1: 反向）
            direction = 1 if angle_diff > 0 else -1
            
            # 如果翻转方向改变，应用翻转灵敏度
            if direction != self.last_flip_direction:
                self.last_flip_direction = direction
                return angle_diff * self.flip_sensitivity
            
            return angle_diff
        
        # 渲染显示对象
        def render(self, width, height, st, at):
            # 首次渲染时初始化子对象尺寸
            if not self.size_initialized:
                child_render = renpy.render(self.child, width, height, st, at)
                self.child_width, self.child_height = child_render.get_size()
                self.size_initialized = True
            
            render = renpy.Render(width, height)
            
            # 计算渲染间隔
            if self.old_time == 0:
                self.old_time = st
            self.delta_time = st - self.old_time
            self.old_time = st
            
            # 根据平台获取输入数据
            if self.is_mobile and tilt_sensor_manager and tilt_sensor_manager.initialized:
                if not self.calibrated:
                    self.calibrate_sensors()
                
                # 计算相对于基准的角度差异
                yaw_diff = tilt_sensor_manager.yaw - self.base_yaw
                pitch_diff = tilt_sensor_manager.pitch - self.base_pitch
                
                # 处理偏航角（左右转动）的360度跳变问题
                if yaw_diff > 180:
                    yaw_diff -= 360
                elif yaw_diff < -180:
                    yaw_diff += 360
                
                # 应用翻转方向检测和死区
                yaw_diff = self.calculate_flip_direction(yaw_diff)
                pitch_diff = self.calculate_flip_direction(pitch_diff)
                
                if abs(yaw_diff) > self.threshold:
                    # 偏航角（左右转动）控制左右移动
                    self.input_x = yaw_diff * self.sensitivity
                else:
                    self.input_x = 0

                if abs(pitch_diff) > self.threshold:
                    # 俯仰角（前后翻动）控制上下移动
                    self.input_y = pitch_diff * self.sensitivity
                else:
                    self.input_y = 0
                    
            elif not self.is_mobile:
                pass
            else:
                self.input_x = 0
                self.input_y = 0
            
            # 缓动公式
            self.x += (self.input_x - self.x) * 1.5 * self.delta_time * abs(self.paramod)
            self.y += (self.input_y - self.y) * 1.5 * self.delta_time * abs(self.paramod)
            
            draw_x = (width - self.child_width) / 2 + self.x
            draw_y = (height - self.child_height) / 2 + self.y        
            obj_render = renpy.render(self.child, width, height, st, at)
            render.blit(obj_render, (draw_x, draw_y))
            renpy.redraw(self, 0)
            return render

# image sky = TrackCursor(renpy.displayable("sky.png"), paramod=-25, sensitivity=1.0, flip_sensitivity=1.5, dead_zone=5.0)
# image mount = TrackCursor(renpy.displayable("mount.png"), paramod=-15, sensitivity=1.0, flip_sensitivity=1.2, dead_zone=8.0)

# paramod          # 移动幅度参数（PC）
# sensitivity      # 基本灵敏度
# threshold       # 倾斜阈值（度）超过这个角度才会发生偏转
# flip_sensitivity  # 翻转灵敏度
# dead_zone         # 死区角度（度）在这个角度范围内需要偏转threshold才会相应偏转，在这个范围外翻转任意角度都会偏转
