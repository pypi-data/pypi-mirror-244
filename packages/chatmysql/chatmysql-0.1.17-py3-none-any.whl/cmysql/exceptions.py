
class MDataKGInitError(Exception):
    code = 1001
    message = "MDataKG初始化失败"

class PromptTooLong(Exception):
    code = 1002
    message = "Prompt过长"