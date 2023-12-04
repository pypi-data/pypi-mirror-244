from log_analyzer_cwj import logAnalyzer
from log_analyzer_cwj import innerRule

def start(_ruleFile):
    print('------------start---------------')
    logAnalyzer.log_analyze(_ruleFile)


def prepare(eventDict, startFlag):
    return innerRule.prepare(eventDict, startFlag)