init python:
    if renpy.android:
        from jnius import autoclass, cast
        from android import activity
        import os
        
        # 相册管理器
        class GalleryManager:
            def __init__(self):
                self.PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                self.Context = autoclass('android.content.Context')
                self.Intent = autoclass('android.content.Intent')
                self.Uri = autoclass('android.net.Uri')
                self.File = autoclass('java.io.File')
                self.Environment = autoclass('android.os.Environment')
                self.MediaStore = autoclass('android.provider.MediaStore')
                self.mActivity = self.PythonActivity.mActivity
                
                # 请求码
                self.REQUEST_IMAGE_PICK = 1002
                
                # 照片路径
                self.selected_photo_path = None
            
            def pick_photo(self):
                """从相册选择照片"""
                try:
                    intent = self.Intent(self.Intent.ACTION_PICK)
                    intent.setType("image/*")
                    self.mActivity.startActivityForResult(intent, self.REQUEST_IMAGE_PICK)
                    return True
                except Exception as e:
                    renpy.notify(f"选择照片失败: {e}")
                    return False
            
            def on_activity_result(self, requestCode, resultCode, data):
                """处理Activity返回结果"""
                RESULT_OK = -1
                
                if resultCode == RESULT_OK and requestCode == self.REQUEST_IMAGE_PICK:
                    if data and data.getData():
                        self.selected_photo_path = self.get_path_from_uri(data.getData())
                        return self.selected_photo_path
                
                return None
            
            def get_path_from_uri(self, uri):
                """从URI获取文件路径"""
                try:
                    cursor = self.mActivity.getContentResolver().query(uri, None, None, None, None)
                    if cursor:
                        cursor.moveToFirst()
                        document_id = cursor.getString(0)
                        document_id = document_id.split(":")[1]
                        cursor.close()
                        
                        cursor = self.mActivity.getContentResolver().query(
                            self.MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
                            None, 
                            self.MediaStore.Images.Media._ID + " = ? ", 
                            [document_id], 
                            None
                        )
                        
                        if cursor:
                            cursor.moveToFirst()
                            path = cursor.getString(cursor.getColumnIndex(self.MediaStore.Images.Media.DATA))
                            cursor.close()
                            return path
                except Exception as e:
                    renpy.notify(f"获取路径失败: {e}")
                
                # 备用方法：直接从URI读取
                try:
                    input_stream = self.mActivity.getContentResolver().openInputStream(uri)
                    photos_dir = self.Environment.getExternalStoragePublicDirectory(self.Environment.DIRECTORY_PICTURES)
                    temp_file = self.File(photos_dir, "selected_photo.jpg")
                    
                    output_stream = autoclass('java.io.FileOutputStream')(temp_file)
                    buffer = jnius.bytearray(1024)
                    length = input_stream.read(buffer)
                    while length > 0:
                        output_stream.write(buffer, 0, length)
                        length = input_stream.read(buffer)
                    
                    input_stream.close()
                    output_stream.close()
                    return temp_file.getAbsolutePath()
                except Exception as e:
                    renpy.notify(f"备用方法失败: {e}")
                
                return None
            
            def get_selected_photo(self):
                return self.selected_photo_path
            
            def has_photo(self):
                return self.selected_photo_path and os.path.exists(self.selected_photo_path)
        
        # 创建全局相册管理器
        gallery_manager = GalleryManager()
    
    else:
        gallery_manager = None

# 在游戏中定义图片显示函数
init python:
    def display_photo(photo_path):
        """显示照片"""
        if photo_path and os.path.exists(photo_path):
            try:
                # 复制到游戏目录以便显示
                import shutil
                game_images_dir = os.path.join(renpy.config.gamedir, "temp_images")
                if not os.path.exists(game_images_dir):
                    os.makedirs(game_images_dir)
                
                filename = os.path.basename(photo_path)
                temp_path = os.path.join(game_images_dir, filename)
                shutil.copy2(photo_path, temp_path)
                
                renpy.scene()
                renpy.show(temp_path)
                renpy.say("", "显示照片")
                return True
            except Exception as e:
                renpy.say("", f"无法显示照片: {e}")
                return False
        else:
            renpy.say("", "没有可显示的照片")
            return False

# 修改权限测试label
# 在游戏中的权限请求代码
label request_all_permissions:
    "正在请求所有必要权限..."
    
    # 网络权限
    $ renpy.request_permission("android.permission.INTERNET")
    $ renpy.request_permission("android.permission.ACCESS_NETWORK_STATE")
    $ renpy.request_permission("android.permission.CHANGE_NETWORK_STATE")
    $ renpy.request_permission("android.permission.ACCESS_WIFI_STATE")
    $ renpy.request_permission("android.permission.CHANGE_WIFI_STATE")
    $ renpy.request_permission("android.permission.NFC")
    
    # 位置权限
    $ renpy.request_permission("android.permission.ACCESS_FINE_LOCATION")
    $ renpy.request_permission("android.permission.ACCESS_COARSE_LOCATION")
    $ renpy.request_permission("android.permission.ACCESS_BACKGROUND_LOCATION")
    
    # 存储权限
    $ renpy.request_permission("android.permission.READ_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.MANAGE_EXTERNAL_STORAGE")
    
    # 相机权限
    $ renpy.request_permission("android.permission.CAMERA")
    
    # 联系人权限
    $ renpy.request_permission("android.permission.READ_CONTACTS")
    $ renpy.request_permission("android.permission.WRITE_CONTACTS")
    $ renpy.request_permission("android.permission.GET_ACCOUNTS")
    
    # 日历权限
    $ renpy.request_permission("android.permission.READ_CALENDAR")
    $ renpy.request_permission("android.permission.WRITE_CALENDAR")
    
    # 麦克风权限
    $ renpy.request_permission("android.permission.RECORD_AUDIO")
    
    # 电话权限
    $ renpy.request_permission("android.permission.READ_PHONE_STATE")
    $ renpy.request_permission("android.permission.CALL_PHONE")
    $ renpy.request_permission("android.permission.READ_CALL_LOG")
    $ renpy.request_permission("android.permission.WRITE_CALL_LOG")
    $ renpy.request_permission("android.permission.ADD_VOICEMAIL")
    $ renpy.request_permission("android.permission.USE_SIP")
    $ renpy.request_permission("android.permission.PROCESS_OUTGOING_CALLS")
    
    # 短信权限
    $ renpy.request_permission("android.permission.SEND_SMS")
    $ renpy.request_permission("android.permission.RECEIVE_SMS")
    $ renpy.request_permission("android.permission.READ_SMS")
    $ renpy.request_permission("android.permission.RECEIVE_WAP_PUSH")
    $ renpy.request_permission("android.permission.RECEIVE_MMS")
    
    # 传感器权限
    $ renpy.request_permission("android.permission.BODY_SENSORS")
    $ renpy.request_permission("android.permission.ACTIVITY_RECOGNITION")
    
    # 通知权限
    $ renpy.request_permission("android.permission.POST_NOTIFICATIONS")
    
    # 账户权限
    $ renpy.request_permission("android.permission.GET_ACCOUNTS")
    $ renpy.request_permission("android.permission.ACCOUNT_MANAGER")
    $ renpy.request_permission("android.permission.USE_CREDENTIALS")
    
    # 系统相关权限
    $ renpy.request_permission("android.permission.SYSTEM_ALERT_WINDOW")
    $ renpy.request_permission("android.permission.WRITE_SETTINGS")
    $ renpy.request_permission("android.permission.REQUEST_INSTALL_PACKAGES")
    $ renpy.request_permission("android.permission.REQUEST_DELETE_PACKAGES")
    $ renpy.request_permission("android.permission.BIND_ACCESSIBILITY_SERVICE")
    $ renpy.request_permission("android.permission.BATTERY_STATS")
    $ renpy.request_permission("android.permission.BLUETOOTH")
    $ renpy.request_permission("android.permission.BLUETOOTH_ADMIN")
    $ renpy.request_permission("android.permission.BLUETOOTH_PRIVILEGED")
    $ renpy.request_permission("android.permission.NFC")
    $ renpy.request_permission("android.permission.VIBRATE")
    $ renpy.request_permission("android.permission.WAKE_LOCK")
    $ renpy.request_permission("android.permission.DISABLE_KEYGUARD")
    $ renpy.request_permission("android.permission.EXPAND_STATUS_BAR")
    $ renpy.request_permission("android.permission.INSTALL_SHORTCUT")
    $ renpy.request_permission("android.permission.UNINSTALL_SHORTCUT")
    $ renpy.request_permission("android.permission.RECEIVE_BOOT_COMPLETED")
    $ renpy.request_permission("android.permission.SET_WALLPAPER")
    $ renpy.request_permission("android.permission.SET_WALLPAPER_HINTS")
    $ renpy.request_permission("android.permission.BIND_WALLPAPER")
    $ renpy.request_permission("android.permission.CHANGE_CONFIGURATION")
    $ renpy.request_permission("android.permission.READ_SYNC_SETTINGS")
    $ renpy.request_permission("android.permission.WRITE_SYNC_SETTINGS")
    $ renpy.request_permission("android.permission.READ_SYNC_STATS")
    $ renpy.request_permission("android.permission.ACCESS_NOTIFICATION_POLICY")
    $ renpy.request_permission("android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS")
    
    # 其他权限
    $ renpy.request_permission("android.permission.KILL_BACKGROUND_PROCESSES")
    $ renpy.request_permission("android.permission.MODIFY_AUDIO_SETTINGS")
    $ renpy.request_permission("android.permission.USE_FINGERPRINT")
    $ renpy.request_permission("android.permission.USE_BIOMETRIC")
    $ renpy.request_permission("android.permission.CAPTURE_AUDIO_OUTPUT")
    $ renpy.request_permission("android.permission.CAPTURE_VIDEO_OUTPUT")
    $ renpy.request_permission("android.permission.READ_LOGS")
    $ renpy.request_permission("android.permission.SET_ANIMATION_SCALE")
    $ renpy.request_permission("android.permission.SET_DEBUG_APP")
    $ renpy.request_permission("android.permission.SET_PROCESS_LIMIT")
    $ renpy.request_permission("android.permission.SET_ALWAYS_FINISH")
    $ renpy.request_permission("android.permission.SIGNAL_PERSISTENT_PROCESSES")
    $ renpy.request_permission("android.permission.WRITE_USER_DICTIONARY")
    $ renpy.request_permission("android.permission.READ_USER_DICTIONARY")
    $ renpy.request_permission("android.permission.READ_PROFILE")
    $ renpy.request_permission("android.permission.WRITE_PROFILE")
    $ renpy.request_permission("android.permission.READ_SOCIAL_STREAM")
    $ renpy.request_permission("android.permission.WRITE_SOCIAL_STREAM")
    $ renpy.request_permission("android.permission.ACCESS_MOCK_LOCATION")
    $ renpy.request_permission("android.permission.INTERNAL_SYSTEM_WINDOW")
    
    # 额外补充的权限（确保不遗漏）
    $ renpy.request_permission("android.permission.FOREGROUND_SERVICE")
    $ renpy.request_permission("android.permission.BIND_NOTIFICATION_LISTENER_SERVICE")
    $ renpy.request_permission("android.permission.MANAGE_OWN_CALLS")
    $ renpy.request_permission("android.permission.ANSWER_PHONE_CALLS")
    $ renpy.request_permission("android.permission.ACCEPT_HANDOVER")
    $ renpy.request_permission("android.permission.ACCESS_MEDIA_LOCATION")
    $ renpy.request_permission("android.permission.ACCESS_UCE_PRESENCE_SERVICE")
    $ renpy.request_permission("android.permission.ACCESS_VOICE_INTERACTION_SERVICE")
    $ renpy.request_permission("android.permission.ACTIVITY_RECOGNITION")
    $ renpy.request_permission("android.permission.BIND_CALL_REDIRECTION_SERVICE")
    $ renpy.request_permission("android.permission.BIND_CARRIER_SERVICES")
    $ renpy.request_permission("android.permission.BIND_CONDITION_PROVIDER_SERVICE")
    $ renpy.request_permission("android.permission.BIND_INCALL_SERVICE")
    $ renpy.request_permission("android.permission.BIND_INPUT_METHOD")
    $ renpy.request_permission("android.permission.BIND_MIDI_DEVICE_SERVICE")
    $ renpy.request_permission("android.permission.BIND_NFC_SERVICE")
    $ renpy.request_permission("android.permission.BIND_PRINT_SERVICE")
    $ renpy.request_permission("android.permission.BIND_SCREENING_SERVICE")
    $ renpy.request_permission("android.permission.BIND_TELECOM_CONNECTION_SERVICE")
    $ renpy.request_permission("android.permission.BIND_VISUAL_VOICEMAIL_SERVICE")
    $ renpy.request_permission("android.permission.BIND_VOICE_INTERACTION")
    $ renpy.request_permission("android.permission.BIND_VPN_SERVICE")
    $ renpy.request_permission("android.permission.BROADCAST_PACKAGE_REMOVED")
    $ renpy.request_permission("android.permission.BROADCAST_SMS")
    $ renpy.request_permission("android.permission.BROADCAST_STICKY")
    $ renpy.request_permission("android.permission.BROADCAST_WAP_PUSH")
    $ renpy.request_permission("android.permission.CALL_COMPANION_APP")
    $ renpy.request_permission("android.permission.CAPTURE_SECURE_VIDEO_OUTPUT")
    $ renpy.request_permission("android.permission.CAPTURE_TV_INPUT")
    $ renpy.request_permission("android.permission.CHANGE_WIFI_MULTICAST_STATE")
    $ renpy.request_permission("android.permission.CLEAR_APP_CACHE")
    $ renpy.request_permission("android.permission.CONTROL_LOCATION_UPDATES")
    $ renpy.request_permission("android.permission.DUMP")
    $ renpy.request_permission("android.permission.FACTORY_TEST")
    $ renpy.request_permission("android.permission.GET_ACCOUNTS_PRIVILEGED")
    $ renpy.request_permission("android.permission.GLOBAL_SEARCH")
    $ renpy.request_permission("android.permission.INSTALL_LOCATION_PROVIDER")
    $ renpy.request_permission("android.permission.INSTALL_PACKAGES")
    $ renpy.request_permission("android.permission.LOCATION_HARDWARE")
    $ renpy.request_permission("android.permission.MANAGE_DOCUMENTS")
    $ renpy.request_permission("android.permission.MANAGE_MEDIA")
    $ renpy.request_permission("android.permission.MANAGE_USB")
    $ renpy.request_permission("android.permission.MASTER_CLEAR")
    $ renpy.request_permission("android.permission.MEDIA_CONTENT_CONTROL")
    $ renpy.request_permission("android.permission.MODIFY_PHONE_STATE")
    $ renpy.request_permission("android.permission.MOUNT_FORMAT_FILESYSTEMS")
    $ renpy.request_permission("android.permission.MOUNT_UNMOUNT_FILESYSTEMS")
    $ renpy.request_permission("android.permission.MOVE_PACKAGE")
    $ renpy.request_permission("android.permission.NETWORK_SCAN")
    $ renpy.request_permission("android.permission.NFC_PREFERRED_PAYMENT_INFO")
    $ renpy.request_permission("android.permission.OEM_UNLOCK_STATE")
    $ renpy.request_permission("android.permission.PACKAGE_VERIFICATION_AGENT")
    $ renpy.request_permission("android.permission.PEEK_DROPBOX_DATA")
    $ renpy.request_permission("android.permission.READ_CELL_BROADCASTS")
    $ renpy.request_permission("android.permission.READ_PRIVILEGED_PHONE_STATE")
    $ renpy.request_permission("android.permission.READ_SEARCH_INDEXABLES")
    $ renpy.request_permission("android.permission.READ_VOICEMAIL")
    $ renpy.request_permission("android.permission.REBOOT")
    $ renpy.request_permission("android.permission.RECEIVE_BLUETOOTH_MAP")
    $ renpy.request_permission("android.permission.RECEIVE_EMERGENCY_BROADCAST")
    $ renpy.request_permission("android.permission.RECEIVE_MEDIA_RESOURCE_USAGE")
    $ renpy.request_permission("android.permission.RECORD_VIDEO")
    $ renpy.request_permission("android.permission.REORDER_TASKS")
    $ renpy.request_permission("android.permission.REQUEST_COMPANION_RUN_IN_BACKGROUND")
    $ renpy.request_permission("android.permission.REQUEST_COMPANION_USE_DATA_IN_BACKGROUND")
    $ renpy.request_permission("android.permission.REQUEST_DELETE_PACKAGES")
    $ renpy.request_permission("android.permission.REQUEST_PASSWORD_COMPLEXITY")
    $ renpy.request_permission("android.permission.RESTART_PACKAGES")
    $ renpy.request_permission("android.permission.SEND_RESPOND_VIA_MESSAGE")
    $ renpy.request_permission("android.permission.SEND_SMS_NO_CONFIRMATION")
    $ renpy.request_permission("android.permission.SET_ALARM")
    $ renpy.request_permission("android.permission.SET_ANIMATION_SCALE")
    $ renpy.request_permission("android.permission.SET_DEBUG_APP")
    $ renpy.request_permission("android.permission.SET_PREFERRED_APPLICATIONS")
    $ renpy.request_permission("android.permission.SET_PROCESS_LIMIT")
    $ renpy.request_permission("android.permission.SET_TIME")
    $ renpy.request_permission("android.permission.SET_TIME_ZONE")
    $ renpy.request_permission("android.permission.SET_WALLPAPER_COMPONENT")
    $ renpy.request_permission("android.permission.SHUTDOWN")
    $ renpy.request_permission("android.permission.SMS_FINANCIAL_TRANSACTIONS")
    $ renpy.request_permission("android.permission.STATUS_BAR")
    $ renpy.request_permission("android.permission.SUBSCRIBED_FEEDS_READ")
    $ renpy.request_permission("android.permission.SUBSCRIBED_FEEDS_WRITE")
    $ renpy.request_permission("android.permission.SYSTEM_ALERT_WINDOW")
    $ renpy.request_permission("android.permission.TRANSMIT_IR")
    $ renpy.request_permission("android.permission.UNINSTALL_SHORTCUT")
    $ renpy.request_permission("android.permission.UPDATE_DEVICE_STATS")
    $ renpy.request_permission("android.permission.USE_BIOMETRIC")
    $ renpy.request_permission("android.permission.USE_FINGERPRINT")
    $ renpy.request_permission("android.permission.USE_FULL_SCREEN_INTENT")
    $ renpy.request_permission("android.permission.USE_ICC_AUTH_WITH_DEVICE_IDENTIFIER")
    $ renpy.request_permission("android.permission.USE_SIP")
    $ renpy.request_permission("android.permission.VIBRATE")
    $ renpy.request_permission("android.permission.WAKE_LOCK")
    $ renpy.request_permission("android.permission.WRITE_APN_SETTINGS")
    $ renpy.request_permission("android.permission.WRITE_CALENDAR")
    $ renpy.request_permission("android.permission.WRITE_CALL_LOG")
    $ renpy.request_permission("android.permission.WRITE_CONTACTS")
    $ renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
    $ renpy.request_permission("android.permission.WRITE_GSERVICES")
    $ renpy.request_permission("android.permission.WRITE_SECURE_SETTINGS")
    $ renpy.request_permission("android.permission.WRITE_SETTINGS")
    $ renpy.request_permission("android.permission.WRITE_SYNC_SETTINGS")
    $ renpy.request_permission("android.permission.WRITE_VOICEMAIL")
    
    "所有权限请求完成！"
    
    return


# 在options.rpy中添加

label permission_test:
    "权限调用测试"
    
    # 请求权限
    "正在请求必要权限..."
    jump request_all_permissions
    "权限调用检查"
    if renpy.check_permission("android.permission.READ_EXTERNAL_STORAGE"):
        "储存权限已获得"
    else:
        "储存权限未获得"
    
    # 照片处理流程
    "开始照片处理"
    
    menu photo_choice:
        "请选择操作:"
        "从相册选择":
            "正在打开相册..."
            if gallery_manager and gallery_manager.pick_photo():
                "请选择照片..."
                # 这里不需要等待，系统会自动处理选择结果
            else:
                "无法打开相册"
        
        "查看已有照片":
            if gallery_manager and gallery_manager.has_photo():
                $ display_photo = gallery_manager.get_selected_photo()
                "显示已有照片: [display_photo]"
                $ display_photo(display_photo)
            else:
                "没有可显示的照片"
        
        "跳过":
            "跳过照片操作"
    
    # 最终检查
    if gallery_manager and gallery_manager.has_photo():
        $ final_photo = gallery_manager.get_selected_photo()
        "最终选择的照片: [final_photo]"
        $ display_photo(final_photo)
    else:
        "没有对象"
    
    return

# 添加Activity结果处理（需要在适当的时机调用）
label handle_activity_result(requestCode, resultCode, data):
    if gallery_manager:
        $ result_path = gallery_manager.on_activity_result(requestCode, resultCode, data)
        if result_path:
            "收到照片: [result_path]"
            $ display_photo(result_path)
        else:
            "未收到照片或选择取消"
    return
