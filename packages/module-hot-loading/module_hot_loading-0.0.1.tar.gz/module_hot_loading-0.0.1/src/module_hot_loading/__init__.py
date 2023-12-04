import time
import sys
import os
import importlib
from threading import Event, Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, path, main_module_path, interval=5, only_import_exist=True):
        '''
        main_module_name: __main__的文件名
        interval: 监听间隔
        only_import_exist: 只导入sys.modules里已经存在的
        '''
        super().__init__()
        self.path = path
        self.interval = interval
        self.main_module_path = os.path.abspath(self._driver_upper(main_module_path))
        self.only_import_exist = only_import_exist
        self.timer = None
        self.snapshot = DirectorySnapshot(path)
    
    def on_any_event(self, event):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.interval, self.checkSnapshot)
        self.timer.start()
    
    def checkSnapshot(self):
        snapshot = DirectorySnapshot(self.path)
        diff = DirectorySnapshotDiff(self.snapshot, snapshot)
        self.snapshot = snapshot
        self.timer = None
        for i in dir(diff):
            if i.startswith('_'):
                continue
            deal_func = getattr(self, f"_deal_{i}")
            deal_arg = getattr(diff, i)
            deal_func(deal_arg)
        
    def _deal_files_created(self, files):
        '''当文件是新创建时，导入新创建的文件'''
        for file in files:
            if not file.endswith('.py'):
                continue
            print(f'监听到文件{file}创建，开始导入模块')
            module_name = self._path_to_module_name(file)
            self._load_module(module_name)

    def _deal_files_modified(self, files):
        '''当文件被修改时，重新导入模块'''
        for file in files:
            if not file.endswith('.py'):
                continue
            print(f'监听到文件{file}修改，开始导入模块')
            module_name = self._path_to_module_name(file)
            module = self._load_module(module_name)

    def _deal_files_deleted(self, files):
        '''当文件被删除时，删除模块'''
        for file in files:
            if not file.endswith('.py'):
                continue
            print(f'监听到文件{file}删除，开始删除模块')
            module_name = self._path_to_module_name(file)
            self._del_module(module_name)
    
    def _deal_files_moved(self, files):
        '''当文件移动时，删除之前的模块并重新导入'''
        for ofile, nfile in files:
            print(f'监听到文件{ofile}移动到{nfile}，开始删除旧模块导入新模块')
            if ofile.endswith('.py'):
                module_name = self._path_to_module_name(ofile)
                self._del_module(module_name)
            if nfile.endswith('.py'):
                module_name = self._path_to_module_name(nfile)
                self._load_module(module_name)

    def _deal_dirs_modified(self, files):
        '''目录修改不处理'''

    def _deal_dirs_deleted(self, files):
        '''目录删除不处理'''

    def _deal_dirs_created(self, files):
        '''目录创建不处理'''

    def _deal_dirs_moved(self, files):
        '''目录移动不处理'''
    
    def _load_module(self, module_name):
        if not module_name:
            return
        module = None
        if sys.modules.get(module_name):
            module = importlib.reload(sys.modules[module_name])
        else:
            if not self.only_import_exist:
                module = importlib.import_module(module_name)
        print(f"导入模块({module_name})成功，模块: {module}")
        return module

    def _del_module(self, module_name):
        if not module_name:
            return
        if sys.modules.get(module_name):
            del sys.modules[module_name]
    
    def _driver_upper(self, path:str):
        new_path = path[0].upper() + path[1:]
        return new_path

    def _path_to_module_name(self, path):       
        '''路径转模块名'''
        child_directory = self._driver_upper(os.path.abspath(path))
        module_name = None
        # 如果是__main__则不加载
        if child_directory == self.main_module_path:
            print("当前模块为__main__，无法重新加载", child_directory)
            return
        for _path in sys.path:
            parent_directory = self._driver_upper(os.path.abspath(_path))
            if os.path.commonprefix([parent_directory + os.sep, child_directory]) == parent_directory + os.sep:
                relative_path = os.path.relpath(child_directory, parent_directory)
                module_name = relative_path.strip(os.sep).strip('.py').replace(os.sep, ".").replace('.__init__', "")
        return module_name
    
       
def monitor_dir(path:str, event:Event, main_module_path, interval=2, only_import_exist=True):
    '''
    path: 要监听的目录
    event: 停止监听的标识
    main_module_path: __main__的绝对路径'''
    observer = Observer()
    event_handler = FileEventHandler(path, main_module_path, interval, only_import_exist)
    observer.schedule(event_handler, path, True)
    observer.start()
    while event.is_set(): 
        time.sleep(1) 
    observer.stop()  

