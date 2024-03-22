import time

class HistoryItem:
    def __init__(self, action, actor=None):
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.action = action
        self.actor = actor

    def __str__(self):
        if self.actor:
            return f"[{self.timestamp}] {self.actor}: {self.action}"
        else:
            return f"[{self.timestamp}] {self.action}"

class History:
    def __init__(self):
        self.actions = []

    def add_action(self, action, actor=None):
        history_item = HistoryItem(action, actor)
        self.actions.append(history_item)

    def display_history(self):
        sorted_actions = sorted(self.actions, key=lambda x: x.timestamp)
        for item in sorted_actions:
            print(item)

    def clear_history(self):
        self.actions = []