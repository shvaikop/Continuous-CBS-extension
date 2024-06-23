import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from pathlib import Path
from collections import namedtuple


class Agent:
    """
    Class holding attributes of an agent.
    """
    def __init__(self, radius):
        self.radius = radius


class TaskBase(ABC):
    def __init__(self, task_file_path: Path):
        self.entries = self._parse_task(task_file_path)

    def _parse_task(self, task_file_path: Path):
        task = ET.parse(task_file_path)
        root = task.getroot()
        entries = []
        for entry in root.findall('./agent'):
            entries.append(self._parse_entry(entry))
        return entries

    @abstractmethod
    def _parse_entry(self, entry):
        pass

    def get_num_agents(self):
        return len(self.entries)

    def get_agent(self, id: int):
        return self.entries[id].agent


class GridTask(TaskBase):
    Entry = namedtuple('Entry', ['agent', 'start_i', 'start_j', 'goal_i', 'goal_j'])

    def _parse_entry(self, entry: ET.Element):
        radius = float(entry.get('radius'))
        start_i = int(entry.get('start_i'))
        start_j = int(entry.get('start_j'))
        goal_i = int(entry.get('goal_i'))
        goal_j = int(entry.get('goal_j'))
        return GridTask.Entry(Agent(radius), start_i, start_j, goal_i, goal_j)


class RoadmapTask(TaskBase):
    Entry = namedtuple('Entry', ['agent', 'start_id', 'goal_id'])
    
    class Entry:
        def __init__(self, agent, start_id, goal_id):
            self.agent = agent
            self.start_id = start_id
            self.goal_id = goal_id

        def get_start_id_str(self):
            return 'n' + str(self.start_id)

        def get_goal_id_str(self):
            return 'n' + str(self.goal_id)

    def _parse_entry(self, entry: ET.Element):
        radius = float(entry.get('radius', 0.4))
        start_id = int(entry.get('start_id'))
        goal_id = int(entry.get('goal_id'))
        return RoadmapTask.Entry(Agent(radius), start_id, goal_id)
