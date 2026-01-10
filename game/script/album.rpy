define build.android_permissions = [
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.READ_MEDIA_IMAGES",
    "android.permission.READ_MEDIA_VIDEO"
]
init python:
    if renpy.android:
        import os
        import shutil
        from jnius import autoclass
        class AlbumManager(object):
            def __init__(self):
                self.PythonSDLActivity = autoclass('org.renpy.android.PythonSDLActivity')
                self.activity = self.PythonSDLActivity.mActivity
                self.last_saved_filename = ""
            def open_gallery(self):
                self.activity.openSystemAlbum()
            def fetch_and_copy_image(self):
                source_path = self.activity.getPickedPath()
                renpy.notify(f"Picked image path: {source_path}")
                
                if not source_path:
                    return None
                target_dir = os.path.join(config.gamedir, "images")
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                original_filename = os.path.basename(source_path)
                dest_filename = "picked_" + original_filename
                target_path = os.path.join(target_dir, dest_filename)

                try:
                    shutil.copy(source_path, target_path)
                    self.last_saved_filename = dest_filename
                    renpy.notify(f"Image copied to: {target_path}")
                    renpy.pause(1.0)
                    return dest_filename
                except Exception as e:
                    renpy.notify("Copy Error: " + str(e))
                    renpy.pause(1.0)
                    return None
            def get_image_name(self):
                return self.last_saved_filename
label album_test:
    "准备调用相册..."
    
    python:
        album = AlbumManager()
        album.open_gallery()
        for pess in build.android_permissions:
            renpy.request_permission(pess)
            renpy.pause(1.5)
    "选照片"
    python:
        img_name = album.fetch_and_copy_image()
    if img_name:
        $ picked_img = "images/" + img_name
        "成功：[img_name]"
        show expression picked_img at truecenter
        "[img_name]"
    else:
        $ renpy.notify("FUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCK")
        "FUCK又失败了"
    jump album_test