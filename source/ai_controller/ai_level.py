'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Oct 11, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

from time import sleep
import time
import math
import jsonpickle
from pathfinder import Pathfinder
from message import Message

class AiLevel:
    """
    The AI level of the AI controller.  This level performs the pathfinding on the world and
    generates the commands for the robot to execute.

    Args:
        options (dict): The dictionary containing the program settings.

    Attributes:
        options (dict): The dictionary containing the program settings.
        keep_running (bool): Boolean that keeps the main event loop running.
        connections (dict): A dictionary that maps the program levels to their respective queues.
    """

    def __init__(self, options):
        self.options = options
        self.keep_running = True
        self.connections = {}
        self.world_model = None

    def ai_level_main(self, ai_input, mov_input, main_input):
        """
        The main event loop of the movement level.  The loop checks for messages to the level,
        interprets the message, and performs the appropriate action.

        Args:
            ai_input (Queue): The queue for receiving messages in the AI level.
            mov_input (Queue): The queue for sending messages to the movement level.
            main_input (Queue): The queue for sending messages to the main level.
        """

        self.connections['AI_LEVEL'] = ['running', ai_input, None]
        self.connections['MOV_LEVEL'] = ['running', mov_input, None]
        self.connections['MAIN_LEVEL'] = ['running', main_input, None]

        main_input.put(Message('AI_LEVEL', 'MAIN_LEVEL', 'info', {
            'message': 'AI_LEVEL is running'
        }))

        # Infinite loop to keep the process running
        while self.keep_running:
            try:
                # Get items from input queue until it is not empty
                while not self.connections["AI_LEVEL"][1].empty():

                    message = self.connections["AI_LEVEL"][1].get()

                    # make sure the message is a Message object
                    if isinstance(message, Message):

                        # Appropriately process the message depending on its category
                        if message.category == 'command':
                            self.process_command(message)

                        # relay message to destination
                        if message.destination != "AI_LEVEL":
                            relay_to = self.connections[message.destination][1]

                            relay_to.put(message)

                        elif self.options['DUMP_MSGS_TO_MAIN']:
                            main_input.put(message)

                # Do rest of stuff

                sleep(self.options["AI_LOOP_SLEEP_INTERVAL"])

            except Exception as err:
                # Catch all exceptions and log them.
                self.connections["MAIN_LEVEL"][1].put(Message('AI_LEVEL', 'MAIN_LEVEL', 'error', {
                    'message': str(err)
                }))

                # Raise the exception again so it isn't lost.
                if self.options["RAISE_ERRORS_AFTER_CATCH"]:
                    raise

    def process_command(self, message):
        """
        The command processor of the AI level.  It processes messages categorized as
        "commands".

        Args:
            message (Message): The message object to be processed.
        """

        if message.data['directive'] == 'generate-plan':
            # Parse out the world model
            world = jsonpickle.decode(message.data['args'])

            self.connections["MAIN_LEVEL"][1].put(Message('AI_LEVEL', 'MAIN_LEVEL', 'info', {
                'message':"Path requested for world:\n" + world.to_string()
            }))

            # Get the moves
            start_time = time.time()
            robot_moves = self.generate_moves(world)

            # Log the AI result
            self.connections["MAIN_LEVEL"][1].put(Message('AI_LEVEL', 'MAIN_LEVEL', 'info', {
                'message':"Pathfinding took " + str((time.time()-start_time)/60) +
                          " minutes\nMoves: " + str(robot_moves)
            }))

            if robot_moves is None:
                self.connections["MOV_LEVEL"][1].put(Message('AI_LEVEL', 'MOV_LEVEL', 'command', {
                    'message': "Nothing left to move",
                    'directive': "no-plan"
                }))
            else:
                self.connections["MOV_LEVEL"][1].put(Message('AI_LEVEL', 'MOV_LEVEL', 'command', {
                    'message': "Plan generated for single robot",
                    'directive': "execute-plan",
                    'args': robot_moves
                }))

        elif message.data['directive'] == 'shutdown' and message.origin == 'MAIN_LEVEL':
            # the level has been told to shutdown.  Kill all the children!!!
            # Loop over the child processes and shut them shutdown

            self.connections["MAIN_LEVEL"][1].put(Message('AI_LEVEL', 'MAIN_LEVEL', 'info', {
                'message': 'Shutting down AI_LEVEL'
            }))

            # End the com_level
            self.keep_running = False

    def robot_goal_assignment(self, world_grid):
        """
        Assigns robots to the goal that is nearest to them.

        Args:
            world (Tile[][]): A 2D array containing the current world state.
        """
        goal_positions = [] # [(goal_x, goal_y)]
        robot_and_position = [] # [(robot_number, (robot_x, robot_y))]
        robot_and_goal = [] # [(robot_number, (goal_x, goal_y))]

        for row in range(self.options["ARENA_SIZE"]):
            for col in range(self.options["ARENA_SIZE"]):
                if world_grid[row][col].goal is True:
                    goal_positions.append(world_grid[row][col].position)
                if world_grid[row][col].occupied is not None:
                    robot_and_position.append((world_grid[row][col].occupied.robot_number,
                                               world_grid[row][col].position))

        # Loop over the goals
        for goal_index, goal in enumerate(goal_positions):

            # The farthest away a robot can possibly be
            closest_distance = float("inf")

            # Loop over each robot for the goal
            for index, entry in enumerate(robot_and_position):
                if entry is None:
                    continue

                dist = math.hypot(entry[1][0] - goal[0],   # x2 - x1
                                  entry[1][1] - goal[1])   # y2 - y1

                if dist < closest_distance:
                    closest_robot = entry[0]
                    ele_with_robot = index
                    closest_distance = dist

            # We have compared all robots, now assign the winner to the goal
            robot_and_goal.append((closest_robot, goal))

            robot_and_position[ele_with_robot] = None
            goal_positions[goal_index] = None

        return robot_and_goal

    def generate_moves(self, world):
        """
        Generates the moves to get the robot to a goal state.  It is iterative and can handle
        robots in batches.  The more robots per iteration, the slower the processing.

        Args:
            world (Arena): The object containing the current state of the world.
        """
        robot_and_goal = self.robot_goal_assignment(world.grid)

        robot_goals = []

        for index, entry in enumerate(robot_and_goal):
            robot_goals.append(entry)
            # Process if it has hit the necesssary iterations or if it is the last robot
            if(len(robot_goals) % self.options["ROBOTS_PLANNED_PER_ITERATION"] == 0
               or index == len(robot_and_goal) - 1):
                pathfinder = Pathfinder(self.options, world.grid, robot_goals)
                robot_goals = []
                robot_moves = pathfinder.start_algorithm()
                if len(robot_moves) > 0:
                    return robot_moves
        return None
