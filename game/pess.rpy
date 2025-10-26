init python:
    if renpy.android:
        import jnius
        from jnius import cast
        from jnius import autoclass
        import os
        
        # 相机和相册管理器
        class PhotoManager:
            def __init__(self):
                self.PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                self.Context = autoclass('android.content.Context')
                self.Intent = autoclass('android.content.Intent')
                self.Uri = autoclass('android.net.Uri')
                self.File = autoclass('java.io.File')
                self.Environment = autoclass('android.os.Environment')
                self.MediaStore = autoclass('android.provider.MediaStore')
                self.ContentResolver = self.PythonActivity.mActivity.getContentResolver()
                self.mActivity = self.PythonActivity.mActivity
                
                # 请求码
                self.REQUEST_IMAGE_CAPTURE = 1
                self.REQUEST_IMAGE_PICK = 2
                
                # 临时文件路径
                self.temp_photo_path = None
            
            def take_photo(self):
                """调用相机拍照"""
                try:
                    # 创建临时文件
                    storage_dir = self.Environment.getExternalStoragePublicDirectory(self.Environment.DIRECTORY_PICTURES)
                    temp_file = self.File(storage_dir, "temp_photo.jpg")
                    self.temp_photo_path = temp_file.getAbsolutePath()
                    
                    # 创建拍照Intent
                    intent = self.Intent(self.MediaStore.ACTION_IMAGE_CAPTURE)
                    photo_uri = autoclass('android.support.v4.content.FileProvider').getUriForFile(
                        self.mActivity,
                        self.mActivity.getPackageName() + ".provider",
                        temp_file
                    )
                    intent.putExtra(self.MediaStore.EXTRA_OUTPUT, photo_uri)
                    intent.addFlags(self.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    
                    # 启动相机
                    self.mActivity.startActivityForResult(intent, self.REQUEST_IMAGE_CAPTURE)
                    return True
                except Exception as e:
                    print(f"拍照失败: {e}")
                    return False
            
            def pick_photo(self):
                """从相册选择照片"""
                try:
                    intent = self.Intent(self.Intent.ACTION_PICK)
                    intent.setType("image/*")
                    self.mActivity.startActivityForResult(intent, self.REQUEST_IMAGE_PICK)
                    return True
                except Exception as e:
                    print(f"选择照片失败: {e}")
                    return False
            
            def on_activity_result(self, requestCode, resultCode, data):
                """处理Activity返回结果"""
                if resultCode == self.mActivity.RESULT_OK:
                    if requestCode == self.REQUEST_IMAGE_CAPTURE:
                        # 处理拍照结果
                        return self.handle_camera_result()
                    elif requestCode == self.REQUEST_IMAGE_PICK:
                        # 处理相册选择结果
                        return self.handle_pick_result(data)
                return None
            
            def handle_camera_result(self):
                """处理相机返回的照片"""
                if self.temp_photo_path and os.path.exists(self.temp_photo_path):
                    # 将照片复制到游戏目录
                    game_dir = os.path.join(renpy.config.gamedir, "images")
                    if not os.path.exists(game_dir):
                        os.makedirs(game_dir)
                    
                    dest_path = os.path.join(game_dir, "image_test.jpg")
                    with open(self.temp_photo_path, 'rb') as src, open(dest_path, 'wb') as dst:
                        dst.write(src.read())
                    
                    # 清理临时文件
                    os.remove(self.temp_photo_path)
                    self.temp_photo_path = None
                    
                    return "image_test"
                return None
            
            def handle_pick_result(self, data):
                """处理相册选择的照片"""
                try:
                    if data and data.getData():
                        uri = data.getData()
                        
                        # 从URI获取文件路径
                        cursor = self.ContentResolver.query(uri, None, None, None, None)
                        if cursor and cursor.moveToFirst():
                            display_name_index = cursor.getColumnIndex(self.MediaStore.Images.Media.DISPLAY_NAME)
                            display_name = cursor.getString(display_name_index)
                            cursor.close()
                            
                            # 读取图片数据
                            input_stream = self.ContentResolver.openInputStream(uri)
                            game_dir = os.path.join(renpy.config.gamedir, "images")
                            if not os.path.exists(game_dir):
                                os.makedirs(game_dir)
                            
                            dest_path = os.path.join(game_dir, "image_choice.jpg")
                            with open(dest_path, 'wb') as f:
                                while True:
                                    chunk = input_stream.read(1024)
                                    if not chunk:
                                        break
                                    f.write(chunk)
                            input_stream.close()
                            
                            return "image_choice"
                except Exception as e:
                    print(f"处理选择照片失败: {e}")
                return None
        
        # 创建全局照片管理器
        photo_manager = PhotoManager()
    
    else:
        photo_manager = None

# 修改权限测试label
label permission_test:
    "权限调用测试"
    "调用储存权限"
    $ renpy.request_permission("android.permission.MANAGE_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.READ_EXTERNAL_STORAGE")

    "调用相机权限"
    $ renpy.request_permission("android.permission.CAMERA")
    
    "权限调用检查"
    if renpy.check_permission("android.permission.MANAGE_EXTERNAL_STORAGE") and renpy.check_permission("android.permission.READ_EXTERNAL_STORAGE"):
        "储存权限已获得"
    else:
        "储存权限未获得"
    
    if renpy.check_permission("android.permission.CAMERA"):
        "相机权限已获得"
    else:
        "相机权限未获得"
    
    # 照片处理流程
    "开始照片处理"
    
    # 拍照
    "正在调用相机..."
    $ camera_success = False
    if photo_manager:
        $ camera_success = photo_manager.take_photo()
    
    if camera_success:
        "请拍照..."
        # 等待拍照完成（这里需要实际的事件处理）
        $ image_test_result = photo_manager.handle_camera_result()
    else:
        $ image_test_result = None
    
    # 选择照片
    "正在打开相册..."
    $ pick_success = False
    if photo_manager:
        $ pick_success = photo_manager.pick_photo()
    
    if pick_success:
        "请选择照片..."
        # 等待选择完成（这里需要实际的事件处理）
        $ image_choice_result = photo_manager.handle_pick_result(None)
    else:
        $ image_choice_result = None
    
    # 显示结果
    if image_test_result or image_choice_result:
        if image_test_result:
            scene expression image_test_result
            "显示拍摄的照片"
        if image_choice_result:
            scene expression image_choice_result
            "显示选择的照片"
    else:
        "没有对象"
    
    return
