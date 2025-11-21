init python:
    if renpy.android:
        from jnius import autoclass
        from android import activity
        import os
        import time
        
        class StorageManager:
            def __init__(self):
                try:
                    self.PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                    self.mActivity = self.PythonActivity.mActivity
                    self.Environment = autoclass('android.os.Environment')
                    self.Intent = autoclass('android.content.Intent')
                    self.Uri = autoclass('android.net.Uri')
                except Exception as e:
                    renpy.notify(f"存储管理器初始化失败: {e}")
                    renpy.pause(0.5)
            
            def has_all_files_access_permission(self):
                """检查是否拥有所有文件访问权限"""
                try:
                    return self.mActivity.hasAllFilesAccessPermission()
                except Exception as e:
                    renpy.notify(f"检查所有文件访问权限失败: {e}")
                    renpy.pause(0.5)
                    return False
            
            def request_all_files_access_permission(self):
                """请求所有文件访问权限"""
                try:
                    self.mActivity.requestAllFilesAccessPermission()
                    return True
                except Exception as e:
                    renpy.notify(f"请求所有文件访问权限失败: {e}")
                    renpy.pause(0.5)
                    return False
            
            def get_storage_status(self):
                """获取存储权限状态"""
                try:
                    if self.has_all_files_access_permission():
                        return "拥有所有文件访问权限"
                    else:
                        return "无所有文件访问权限"
                except:
                    return "无法检测存储权限状态"
        
        class GalleryManager:
            def __init__(self):
                try:
                    self.PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                    self.mActivity = self.PythonActivity.mActivity
                    self.selected_photo_path = None
                    activity.bind(on_activity_result=self.on_activity_result)
                    self.storage_manager = StorageManager()
                except Exception as e:
                    renpy.notify(f"相册管理器初始化失败: {e}")
                    renpy.pause(0.5)
            
            def pick_photo(self):
                """从相册选择照片"""
                try:
                    # 检查权限
                    if not self.has_required_permissions():
                        renpy.notify("需要存储权限才能访问相册")
                        renpy.pause(0.5)
                        return False
                    
                    self.mActivity.openGallery()
                    return True
                except Exception as e:
                    renpy.notify(f"打开相册失败: {e}")
                    renpy.pause(0.5)
                    return False
            
            def has_required_permissions(self):
                """检查所需权限"""
                try:
                    # 检查基本存储权限
                    read_storage = renpy.check_permission("android.permission.READ_EXTERNAL_STORAGE")
                    write_storage = renpy.check_permission("android.permission.WRITE_EXTERNAL_STORAGE")
                    
                    # 检查所有文件访问权限
                    all_files_access = self.storage_manager.has_all_files_access_permission()
                    
                    return read_storage and write_storage and all_files_access
                except Exception as e:
                    renpy.notify(f"检查权限失败: {e}")
                    renpy.pause(0.5)
                    return False
            
            def request_required_permissions(self):
                """请求所需权限"""
                try:
                    # 请求基本存储权限
                    renpy.request_permission("android.permission.READ_EXTERNAL_STORAGE")
                    renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
                    
                    # 请求所有文件访问权限
                    if not self.storage_manager.has_all_files_access_permission():
                        self.storage_manager.request_all_files_access_permission()
                        return "正在请求所有文件访问权限..."
                    
                    return "所有权限已获取"
                except Exception as e:
                    return f"请求权限失败: {e}"
            
            def on_activity_result(self, requestCode, resultCode, data):
                """处理相册选择结果"""
                RESULT_OK = -1
                if resultCode == RESULT_OK and requestCode == 1001:
                    if data and data.getData():
                        uri = data.getData()
                        self.selected_photo_path = self.mActivity.getPathFromUri(uri)
                        if self.selected_photo_path:
                            renpy.notify("选择成功: " + self.selected_photo_path)
                            renpy.pause(0.5)
                            return True
                renpy.notify("未选择照片")
                renpy.pause(0.5)
                return False
            
            def get_selected_photo(self):
                return self.selected_photo_path
            
            def has_photo(self):
                return self.selected_photo_path and os.path.exists(self.selected_photo_path)
            
            def clear_selection(self):
                self.selected_photo_path = None
        
        try:
            gallery_manager = GalleryManager()
            storage_manager = StorageManager()
        except:
            gallery_manager = None
            storage_manager = None
    else:
        gallery_manager = None
        storage_manager = None

init python:
    def show_photo():
        if not gallery_manager or not gallery_manager.has_photo():
            renpy.notify("没有可显示的照片")
            renpy.pause(0.5)
            return
        photo_path = gallery_manager.get_selected_photo()
        renpy.show_screen("photo_viewer", photo_path)

screen photo_viewer(photo_path):
    modal True
    zorder 200
    add "#000000AA"
    
    frame:
        background Solid("#FFFFFF")
        xalign 0.5
        yalign 0.5
        padding (20, 20, 20, 20)
        
        vbox:
            spacing 20
            
            label "照片预览"
            
            if photo_path and os.path.exists(photo_path):
                add photo_path:
                    fit "contain"
            else:
                text "无法显示照片" color "#FF0000"
            
            text "文件路径: [photo_path]" size 16 color "#666666"
            
            textbutton "关闭" action Hide("photo_viewer")

screen storage_permission_screen():
    tag menu
    
    vbox:
        spacing 20
        align (0.5, 0.5)
        
        label "存储权限管理"
        
        if storage_manager:
            $ storage_status = storage_manager.get_storage_status()
            text "存储权限状态: [storage_status]" xalign 0.5
            
            vbox:
                spacing 10
                xalign 0.5
                
                textbutton "检查权限状态" action Function(renpy.notify, storage_status)
                textbutton "请求所有文件访问权限" action Function(storage_manager.request_all_files_access_permission)
                textbutton "请求基础存储权限" action Function(
                    lambda: [
                        renpy.request_permission("android.permission.READ_EXTERNAL_STORAGE"),
                        renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
                    ]
                )
        
        else:
            text "存储管理器不可用" color "#FF0000" xalign 0.5
        
        textbutton "返回" action Return() xalign 0.5

label permission_test:
    "权限调用测试"
    
    "正在检查权限状态..."
    
    if gallery_manager:
        $ has_permissions = gallery_manager.has_required_permissions()
        if has_permissions:
            "所有必要权限已获取"
        else:
            "需要请求权限"
            $ gallery_manager.request_required_permissions()
            "请按照系统提示授权..."
    else:
        "相册管理器不可用"
    
    "功能测试"
    menu:
        "从相册选择照片":
            if gallery_manager and gallery_manager.pick_photo():
                "请在相册中选择一张照片..."
            else:
                "无法打开相册"
        
        "查看已选照片":
            if gallery_manager and gallery_manager.has_photo():
                $ show_photo()
            else:
                "没有选择的照片"
        
        "存储权限管理":
            call screen storage_permission_screen
        
        "返回":
            return
    
    jump permission_test


