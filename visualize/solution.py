import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from task import *


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
        self.flowtime = float(summary.get('flowtime'))
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
                                          duration=float(section.get('duration'))))
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