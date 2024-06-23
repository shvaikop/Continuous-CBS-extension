#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, CheckButtons
import random
from map import *
from task import *
from solution import *
import pdb

def generate_contrasting_colors(n):
    # Predefined list of contrasting colors
    predefined_colors = [
        "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF",
        "#800000", "#008000", "#000080", "#808000", "#800080", "#008080",
        "#C0C0C0", "#FFA500", "#A52A2A", "#DEB887", "#5F9EA0", "#7FFF00",
        "#D2691E", "#6495ED"
    ]
    
    # If n is less than the number of predefined colors, return the first n colors
    if n <= len(predefined_colors):
        return predefined_colors[:n]
    
    # Otherwise, use all predefined colors and generate additional random colors
    colors = predefined_colors.copy()
    while len(colors) < n:
        colors.append("#{:06x}".format(random.randint(0, 0xFFFFFF)))
    
    return colors

class GridVisualizer:
    def __init__(self, grid_map: GridMap, grid_task: GridTask, solution: GridSolution):
        self.grid_map = grid_map
        self.grid_task = grid_task
        self.solution = solution
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.anim_running = False
        self.step_mode = False
        self.step = 0

        self.init_plot()
        self.create_widgets()
        self.create_animation()
        plt.show()

    def init_plot(self):
        self.ax.set_xlim(0, self.grid_map.width)
        self.ax.set_ylim(0, self.grid_map.height)
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_xticks(np.arange(0, self.grid_map.width + 1, 1))
        self.ax.set_yticks(np.arange(0, self.grid_map.height + 1, 1))
        self.ax.grid(True)
        self.ax.invert_yaxis()

        # Plot the grid cells
        for i in range(self.grid_map.height):
            for j in range(self.grid_map.width):
                if self.grid_map.grid[i, j] == 1:
                    self.ax.add_patch(plt.Rectangle((j, i), 1, 1, color='black'))

        # Initialize agent positions and colors
        self.agents = []
        self.agent_colors = generate_contrasting_colors(len(self.grid_task.entries))
        for i, entry in enumerate(self.grid_task.entries):
            start_i, start_j = entry.start_i, entry.start_j
            goal_i, goal_j = entry.goal_i, entry.goal_j
            radius = entry.agent.radius
            color = (self.agent_colors[i])
            agent_circle = Circle((start_j + 0.5, start_i + 0.5), radius, color=color, alpha=0.5)
            goal_circle = Circle((goal_j + 0.5, goal_i + 0.5), 0.1, color=color, alpha=0.3)
            self.ax.add_patch(agent_circle)
            self.ax.add_patch(goal_circle)
            self.agents.append(agent_circle)

    def create_widgets(self):
        # Buttons for control
        axstart = plt.axes([0.85, 0.7, 0.1, 0.075])
        axpause = plt.axes([0.85, 0.6, 0.1, 0.075])
        axresume = plt.axes([0.85, 0.5, 0.1, 0.075])
        axrestart = plt.axes([0.85, 0.4, 0.1, 0.075])

        self.bstart = Button(axstart, 'Start')
        self.bpause = Button(axpause, 'Pause')
        self.bresume = Button(axresume, 'Resume')
        self.brestart = Button(axrestart, 'Reset')

        self.bstart.on_clicked(self.start)
        self.bpause.on_clicked(self.pause)
        self.bresume.on_clicked(self.resume)
        self.brestart.on_clicked(self.reset)

    def create_animation(self):
        self.anim = FuncAnimation(self.fig, self.animate, frames=self.solution.makespan * 10, interval=100, blit=True)

    def interpolate(self, start, end, alpha):
        return start + (end - start) * alpha

    def animate(self, frame):
        if not self.anim_running:
            return self.agents

        if self.step_mode:
            frame = self.step

        for agent_id, agent_plan in enumerate(self.solution.solution):
            circle = self.agents[agent_id]
            sections = agent_plan.sections
            current_frame = frame
            for section in sections:
                duration_frames = section.duration * 10
                if current_frame < duration_frames:
                    alpha = current_frame / duration_frames
                    new_i = self.interpolate(section.start_i, section.goal_i, alpha)
                    new_j = self.interpolate(section.start_j, section.goal_j, alpha)
                    circle.center = (new_j + 0.5, new_i + 0.5)
                    break
                current_frame -= duration_frames
        return self.agents

    def start(self, event):
        self.reset(event)
        self.anim.event_source.start()
        self.anim_running = True

    def pause(self, event):
        if self.anim_running:
            self.anim.event_source.stop()
            self.anim_running = False

    def resume(self, event):
        if not self.anim_running:
            self.anim.event_source.start()
            self.anim_running = True

    def reset(self, event):
        self.anim.event_source.stop()
        self.step = 0
        self.init_plot()
        self.create_animation()
        self.anim_running = False


class RoadMapVisualizer:
    def __init__(self, roadmap: RoadMap, roadmap_task, solution):
        self.roadmap = roadmap.graph
        self.roadmap_task = roadmap_task
        self.solution = solution
        self.pos = roadmap.coords
        self.fig, self.ax = plt.subplots()
        self.agents = []
        self.agent_colors = self.generate_colors(len(solution.solution))
        self.init_plot()
        plt.show()
        
    def generate_colors(self, n):
        colors = [
            'red', 'blue', 'green', 'orange', 'purple',
            'brown', 'pink', 'gray', 'olive', 'cyan'
        ]
        if n <= len(colors):
            return colors[:n]
        else:
            return colors + [(np.random.rand(), np.random.rand(), np.random.rand()) for _ in range(n - len(colors))]

    def init_plot(self):
        # Draw the roadmap
        self.pos = nx.spring_layout(self.roadmap, pos=self.pos, iterations=50)  # Spring layout with initial positions

        # Draw the roadmap with small circles for nodes and normal lines for edges
        nx.draw_networkx_nodes(self.roadmap, self.pos, ax=self.ax, node_size=50, node_color='skyblue')
        nx.draw_networkx_edges(self.roadmap, self.pos, ax=self.ax, edge_color='gray')
        
        edge_labels = nx.get_edge_attributes(self.roadmap, 'weight')
        nx.draw_networkx_edge_labels(self.roadmap, self.pos, edge_labels=edge_labels, ax=self.ax)
        
        # Initialize agents
        for idx, section in enumerate(self.roadmap_task.entries):
            # pdb.set_trace()
            start_pos = self.pos[section.get_start_id_str()]
            agent_circle = Circle(start_pos, 0.5, color=self.agent_colors[idx], alpha=0.5)
            self.ax.add_patch(agent_circle)
            self.agents.append(agent_circle)
            
        # Draw goal positions
        for idx, section in enumerate(self.roadmap_task.entries):
            goal_pos = self.pos[section.get_goal_id_str()]
            self.ax.plot(goal_pos[0], goal_pos[1], 'o', color=self.agent_colors[idx])

    def interpolate(self, start, end, alpha):
        return start + (end - start) * alpha

    def animate(self, frame):
        for agent_idx, agent_solution in enumerate(self.solution.solution):
            agent_circle = self.agents[agent_idx]
            sections = agent_solution.sections
            current_frame = frame % len(sections)
            section = sections[current_frame]
            start = (section.start_i, section.start_j)
            goal = (section.goal_i, section.goal_j)
            alpha = (frame % 10) / 10.0
            new_pos = self.interpolate(np.array(start), np.array(goal), alpha)
            agent_circle.center = new_pos
        return self.agents

    def start_animation(self, interval=100):
        ani = FuncAnimation(self.fig, self.animate, frames=range(len(max(self.solution.solution, key=len).sections) * 10), interval=interval, blit=True)
        plt.show()
        

def main():
    parser = argparse.ArgumentParser(description='MAPF solution visualizer')
    parser.add_argument('--type', type=str, help='Type of the map', choices=['grid', 'roadmap'], required=True)
    parser.add_argument('--map', type=Path, help='Path to the xml map file', required=True)
    parser.add_argument('--task', type=Path, help='Path to the xml task file', required=True)
    parser.add_argument('--solution', type=Path, help='Path to the xml solution file', required=True)
    # parser.add_argument('solution', type=str, help='Path to the xml solution file', required=True)
    args = parser.parse_args()

    if args.type == 'grid':
        map = GridMap(args.map)
        task = GridTask(args.task)
        solution = GridSolution(task, args.solution)
        GridVisualizer(map, task, solution)
    elif args.type == 'roadmap':
        map = RoadMap(args.map)
        task = RoadmapTask(args.task)
        solution = RoadmapSolution(task, args.solution)
        vis = RoadMapVisualizer(map, task, solution)
        # vis.start_animation()
    pdb.set_trace()
    return
    # visualize_grid(map, task, solution)
    Visualizer(map, task, solution)
    

    
    


if __name__ == '__main__':
    main()