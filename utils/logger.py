import logging


class CustomLogger:
    def __init__(self, log_level=logging.INFO, log_file="error.log", terminal_output=True, file_output=True):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')
        if terminal_output:
            # 设置终端输出处理器
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            self.logger.addHandler(console_handler)

        if file_output and log_file:
            # 设置文件输出处理器（如果配置了log_file）
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)

    def set_log_level(self, log_level):
        self.logger.setLevel(log_level)

    def log(self, message, log_level=logging.INFO):
        self.logger.log(log_level, message)


# 示例使用：
if __name__ == "__main__":
    from path_handler import PathHandler
    path_handler = PathHandler()

    # 创建日志对象
    log_file_path = path_handler.get_absolute_path("log/logger_test.log")
    logger = CustomLogger(log_level=logging.DEBUG, log_file=log_file_path, terminal_output=True, file_output=True)
    # 输出日志信息
    logger.log("这是一条DEBUG级别的日志信息", log_level=logging.DEBUG)
    logger.log("这是一条INFO级别的日志信息")
    logger.log("这是一条WARNING级别的日志信息", log_level=logging.WARNING)
    logger.log("这是一条ERROR级别的日志信息", log_level=logging.ERROR)
