"""大纲优化流水线专用异常。"""


class SyllabusCancelled(Exception):
    """用户主动停止大纲优化任务。"""
