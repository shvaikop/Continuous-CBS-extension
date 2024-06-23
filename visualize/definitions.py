#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from pathlib import Path
from collections import namedtuple
from typing import List
import pdb

class Agent:
    def __init__(self, radius):
        self.radius = radius

class MapBase(ABC):
    @abstractmethod
    def __init__(self, map_file_path: Path):
        pass

    @abstractmethod
    def _parse_map(self, map_file_path: Path):
        pass

class GridMap(MapBase):
    def __init__(self, map_file_path: Path):
        self.map_type = None
        self.width = None
        self.height = None
        self.grid = None
        self._parse_map(map_file_path)

    def _parse_map(self, map_file_path: Path):
        map = ET.parse(map_file_path)
        root = map.getroot()
        self.map_type = root.find('./map/type').text
        self.width = int(root.find('./map/width').text)
        self.height = int(root.find('./map/height').text)

        self.grid = np.zeros((self.height, self.width))
        for i, row in enumerate(root.findall('./map/grid/row')):
            self.grid[i] = [int(cell) for cell in row.text.split()]

    def __str__(self):
        return f"GridMap({self.map_type}, width: {self.width}, height: {self.height})"

    def __repr__(self):
        return f"{self.__str__()}\n{self.grid}"


class RoadMap(MapBase):
    def __init__(self, map_file_path: Path):
        raise NotImplementedError

    def _parse_map(self, map_file_path: Path):
        raise NotImplementedError

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

    def _parse_entry(self, entry: ET.Element):
        radius = float(entry.get('radius'))
        start_id = int(entry.get('start_id'))
        goal_id = int(entry.get('goal_id'))
        return RoadmapTask.Entry(Agent(radius), start_id, goal_id)

class PlanSection:
    def __init__(self, start_i, start_j, goal_i, goal_j, duration):
        self.start_i = start_i
        self.start_j = start_j
        self.goal_i = goal_i
        self.goal_j = goal_j
        self.duration = duration

class AgentPlan:
    def __init__(self, agent: Agent, sections: List[PlanSection]):
        self.agent = agent
        self.sections = sections

class SolutionBase(ABC):
    def __init__(self, task: TaskBase, solution_file_path: Path):
        self.task = task
        self.cpu_time = None
        self.flowtime = None
        self.makespan = None
        self.solution = self._parse_solution(solution_file_path)

    @abstractmethod
    def _time_type(self, time: str):
        pass

    @abstractmethod
    def _coord_type(self, coord: str):
        pass

    def _parse_solution(self, solution_file_path: Path):
        solution = ET.parse(solution_file_path)
        root = solution.getroot()
        log = root.find('./log')
        summary = log.find('./summary')
        self.cpu_time = float(summary.get('time'))
        self.flowtime = self._time_type(summary.get('flowtime'))
        self.makespan = self._time_type(summary.get('makespan'))
        
        num_agents = self.task.get_num_agents()
        plan = [None for _ in range(num_agents)]
        for entry in log.findall('./agent'):
            agent_id = int(entry.get('number'))
            agent = self.task.get_agent(agent_id)
            plan_sections = self._parse_plan(entry.find('./path'))
            plan[agent_id] = AgentPlan(agent, plan_sections)
        return plan

    def _parse_plan(self, plan: ET.Element) -> List[PlanSection]:
        agent_plan = []
        for section in plan.findall('./section'):
            sec_num = int(section.get('number'))
            assert len(agent_plan) == sec_num, "Plan section numbers should be contiguous"
            agent_plan.append(PlanSection(start_i=self._coord_type(section.get('start_i')),
                                          start_j=self._coord_type(section.get('start_j')),
                                          goal_i=self._coord_type(section.get('goal_i')),
                                          goal_j=self._coord_type(section.get('goal_j')),
                                          duration=self._time_type(section.get('duration'))))
        return agent_plan

class GridSolution(SolutionBase):
    def _time_type(self, time):
        return int(time)

    def _coord_type(self, coord):
        return int(coord)

class RoadmapSolution(SolutionBase):
    def _time_type(self, time):
        return float(time)

    def _coord_type(self, coord):
        return float(coord)
            
        
        
        
