init python:
    import os
    import time
    
    class GalleryPhoto:
        def __init__(self):
            self.selected_image = None
            self.permissions_granted = False
        
        def request_all_permissions(self):
            """请求所有需要的权限"""
            if not renpy.android:
                return True
                
            permissions_granted = True
            for permission in build.android_permissions:
                if not renpy.check_permission(permission):
                    result = renpy.request_permission(permission)
                    if not result:
                        permissions_granted = False
            
            self.permissions_granted = permissions_granted
            return permissions_granted
        
        def check_all_permissions(self):
            """检查所有权限状态"""
            if not renpy.android:
                return True
                
            for permission in build.android_permissions:
                if not renpy.check_permission(permission):
                    return False
            return True
        
        def open_gallery(self):
            """使用SDL打开相册选择图片"""
            if not renpy.android:
                return False
                
            try:
                # 使用SDL的Android Activity打开相册
                activity = renpy.android.get_activity()
                if activity:
                    # 清除之前的图片选择
                    activity.clearSelectedImage()
                    # 打开相册
                    activity.openGallery()
                    return True
                return False
            except Exception as e:
                renpy.notify(f"打开相册失败: {e}")
                return False
        
        def get_selected_image(self):
            """获取选择的图片路径"""
            if not renpy.android:
                return self.selected_image
                
            try:
                # 从SDL Activity获取选择的图片路径
                activity = renpy.android.get_activity()
                if activity:
                    path = activity.getSelectedImagePath()
                    if path and path != "":
                        self.selected_image = path
                return self.selected_image
            except Exception as e:
                renpy.notify(f"获取图片路径失败: {e}")
                return self.selected_image
        
        def copy_image_to_internal(self, source_path):
            """将图片复制到内部存储以便Ren'Py使用"""
            try:
                import shutil
                # 获取内部存储路径
                internal_dir = renpy.config.gamedir
                dest_dir = os.path.join(internal_dir, "user_images")
                os.makedirs(dest_dir, exist_ok=True)
                
                # 生成唯一文件名
                filename = "selected_image_" + str(int(time.time())) + os.path.splitext(source_path)[1]
                dest_path = os.path.join(dest_dir, filename)
                
                # 复制文件
                shutil.copy2(source_path, dest_path)
                return dest_path
            except Exception as e:
                renpy.notify(f"复制图片失败: {e}")
                return source_path
        
        def wait_for_image_selection(self, timeout=30):
            """等待图片选择完成"""
            if not renpy.android:
                return False
                
            start_time = time.time()
            while time.time() - start_time < timeout:
                # 检查是否有图片被选择
                if self.get_selected_image():
                    return True
                # 等待一段时间再检查
                renpy.pause(0.5)
            
            return False
    
    # 创建全局实例
    gallery = GalleryPhoto()

# 相册测试流程
label gallery_test:
    "正在初始化相册功能..."
    
    # 检查权限
    if gallery.check_all_permissions():
        "权限检查通过"
        jump open_gallery
    else:
        "需要请求权限"
        jump request_permissions

label request_permissions:
    "正在请求必要的权限..."
    
    $ success = gallery.request_all_permissions()
    
    if success:
        "权限请求已发送"
        # 等待用户响应
        $ renpy.pause(2.0)
        
        # 再次检查权限
        if gallery.check_all_permissions():
            "权限已授予"
            jump open_gallery
        else:
            "部分权限未被授予"
            jump permission_failed
    else:
        "权限请求失败"
        jump permission_failed

label permission_failed:
    "权限获取失败，可能无法使用完整功能"
    
    menu:
        "继续尝试（可能无法使用完整功能）":
            jump open_gallery
        "返回":
            return

label open_gallery:
    "正在打开相册..."
    
    $ success = gallery.open_gallery()
    
    if not success:
        "无法打开相册"
        return
    
    "请在相册中选择一张图片..."
    
    # 等待图片选择
    $ selection_success = gallery.wait_for_image_selection()
    
    if selection_success:
        jump image_selected
    else:
        "选择超时或用户取消了选择"
        return

# 图片选择成功标签
label image_selected:
    $ selected_path = gallery.get_selected_image()
    
    if not selected_path:
        "没有选择图片"
        return
    
    "图片选择成功！"
    "文件路径: [selected_path]"
    
    # 尝试将图片复制到内部存储
    $ internal_path = gallery.copy_image_to_internal(selected_path)
    
    # 在Ren'Py中显示图片
    python:
        try:
            # 将图片添加到Ren'Py的图像库
            renpy.image("selected_image", internal_path)
            renpy.notify("图片已加载成功！")
            load_success = True
        except Exception as e:
            renpy.notify("加载图片时出错: " + str(e))
            load_success = False
    
    if not load_success:
        "图片加载失败，请重新选择"
        return
    
    scene black
    show selected_image at truecenter with dissolve
    "这是您选择的图片！"
    
    menu:
        "使用此图片作为背景":
            $ persistent.selected_background = internal_path
            "图片已设置为背景！"
            jump show_background
            
        "重新选择图片":
            jump gallery_test

# 显示背景标签
label show_background:
    if persistent.selected_background:
        scene expression persistent.selected_background
    else:
        scene black
    
    "这个场景使用了您选择的图片作为背景"
    "测试完成！"
    return
