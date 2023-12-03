from abc import ABC, abstractmethod

from game_tools.device.windows_message import MessageSender


class StateMachineBlackboard:
    """
    状态机黑板类
    """

    def __init__(self, hwnd):
        self.screen = None
        self.hwnd = hwnd
        self.msg = MessageSender(hwnd)


class StateStack:
    """
    状态机栈
    """

    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from an empty stack")

    def delete_state(self, item):
        if item in self.items:
            self.items.remove(item)
        else:
            raise IndexError("itme not in the stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("peek from an empty stack")

    def size(self):
        return len(self.items)


class StateMachineManager(ABC):
    """
    状态机管理器
    """

    def __init__(self, blackboard: StateMachineBlackboard):
        # 后进先出
        self.state_stack = StateStack()
        self.blackboard = blackboard

    def push_state(self, state):
        self.state_stack.push(state)

    def delete_state(self, state):
        return self.state_stack.delete_state(state)

    def peek_state(self):
        return self.state_stack.peek()

    def execute(self):
        state = self.peek_state()
        print('state class', state.__class__.__name__)
        # if state.pre_execute(self, self.blackboard):
        if state.execute(self, self.blackboard):
            print('delete_state', state.__class__.__name__)
            self.delete_state(state)

    def send_message(self, msg):
        self.execute_message(msg)

    @abstractmethod
    def execute_message(self, msg):
        pass


class StateMachine(ABC):
    """
    状态机类
    """

    @abstractmethod
    def execute(self, manager: StateMachineManager, blackboard: StateMachineBlackboard) -> bool:
        pass

    def pre_execute(self, manager: StateMachineManager, blackboard: StateMachineBlackboard) -> bool:
        # return self.execute(manager, blackboard)
        flag = True
        try:
            flag = self.execute(manager, blackboard)
        except Exception as e:
            print(e)
        finally:
            return flag
