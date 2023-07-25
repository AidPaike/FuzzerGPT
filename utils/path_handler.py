from pathlib import Path
from datetime import datetime
from utils.logger import CustomLogger
import logging


class PathHandler:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.path_handler_log = self.project_root / "log" / "path_handler.log"
        self.logger = CustomLogger(log_level=logging.DEBUG, log_file=self.path_handler_log)

    def get_absolute_path(self, relative_path):
        abs_path = self.project_root / relative_path
        # 获取文件所在的文件夹路径
        folder_path = abs_path.parent
        # 判断文件夹是否存在
        if folder_path.is_dir():
            return abs_path
        else:
            self.logger.log(f"Warning: The path '{relative_path}' does not exist. Using a fallback path.",
                            log_level=logging.DEBUG)
            # 使用企业级日志命名方式：在文件名中加上日期时间
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            abs_path = self.project_root / "log" / f"fallback_file_{now}.txt"
            self.logger.log(f"Using a fallback path '{abs_path}'.", log_level=logging.DEBUG)
        return abs_path


# 示例使用：
if __name__ == "__main__":
    path_handler = PathHandler()

    # 日志文件路径
    log_file_path = path_handler.get_absolute_path("logs/app.log")
    print(log_file_path)

    # # 数据文件路径
    # data_file_path = path_handler.get_absolute_path("data/data.csv")
    # print(data_file_path)
    #
    # # 其他文件或目录的路径
    # other_path = path_handler.get_absolute_path("path_to_other_file_or_directory")
    # print(other_path)
    # path_handler = PathHandler()
    #
    # # 日志文件路径
    # log_file_path = path_handler.get_absolute_path("logs/app.log")
    # print(log_file_path)
    #
    # # 不存在的路径，使用备用路径
    # non_existing_path = path_handler.get_absolute_path("non_existing_folder")
    # print(non_existing_path)
