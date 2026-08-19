"""评估流水线专用异常。"""


class EvaluationCancelled(Exception):
    """用户主动停止评估任务。"""
