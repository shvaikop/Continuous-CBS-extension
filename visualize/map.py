import xml.etree.ElementTree as ET
import networkx as nx
import numpy as np
from abc import ABC, abstractmethod
from pathlib import Path
import pdb


class Agent:
    """
    Class holding attributes of an agent.
    """
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
        self.graph = None
        self.coords = None
        self._parse_map(map_file_path)
        pdb.set_trace()

    def _parse_map(self, map_file_path: Path):
        self.graph = nx.read_graphml(map_file_path)
        coords = nx.get_node_attributes(self.graph, 'coords')
        self.coords = {node: tuple(map(float, coord.split(','))) for node, coord in coords.items()}
