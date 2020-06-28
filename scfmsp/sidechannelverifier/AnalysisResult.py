from enum import Enum


class AnalysisResult(Enum):
    SUCCESS = 0
    INFORMATION_LEAK = 1
    TIMING_LEAK = 2
    LOOP_ON_SECRET_DATA = 3
    NEMISIS_VULNERABILITY = 4
