#!/usr/bin/env python
# coding:utf-8


import tempfile
import threading
import win32file
import win32con
import os

#典型临时文件所在目录
dirs_to_monitor = ['C:\\Windows\\Temp', tempfile.gettempdir()]

#文件修改对应的常量
FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

def start_monitor(path_to_watch):

    #为每一个监控器创建线程
    FILE_LIST_DIRECTORY = 0x0001

    h_directory = win32file.CreateFile(
        path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARED_READ | win32con.FILE_SHARED_WRITE | win32con.FILE_SHARED_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    while True:
        try:
            results = win32file.ReadDirectoryChangesW(
                h_directory,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
            )

            for action, file_name in results:
                full_filename = os.path.join(path_to_watch, file_name)

                if action == FILE_CREATED:
                    print("[ + ] Created %s" % full_filename)
                elif action == FILE_DELETED:
                    print("[ - ] Deleted %s" % full_filename)
                elif action == FILE_MODIFIED:
                    print("[ * ] Modified %s" % full_filename)
                    # 输出文件内容
                    print("[vvv] Dumping contents...")
                    try:
                        # 打开文件读数据
                        fd = open(full_filename, "rb")
                        contents = fd.read()
                        fd.close()
                        print(contents)
                        print("[^^^] Dump complete.")
                    except:
                        print("[!!!] Failed.")
                # 重命名哪个文件
                elif action == FILE_RENAMED_FROM:
                    print("[ > ] Renamed from: %s" % full_filename)
                # 重命名后的文件名是?
                elif action == FILE_RENAMED_TO:
                    print("[ < ] Renamed to: %s" % full_filename)
                else:
                    print("[???] Unknown: %s" % full_filename)

        except:
            pass

for path in dirs_to_monitor:
    monitor_thread = threading.Thread(target=start_monitor, args=(path, ))
    print("Monitoring to the path %s " % path)
    monitor_thread.start()





