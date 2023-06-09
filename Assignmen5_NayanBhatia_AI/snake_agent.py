import numpy as np
import helper
import random

#   This class has all the functions and variables necessary to implement snake game
#   We will be using Q learning to do this

class SnakeAgent:

    #   This is the constructor for the SnakeAgent class
    #   It initializes the actions that can be made,
    #   Ne which is a parameter helpful to perform exploration before deciding next action,
    #   LPC which ia parameter helpful in calculating learning rate (lr) 
    #   gamma which is another parameter helpful in calculating next move, in other words  
    #            gamma is used to blalance immediate and future reward
    #   Q is the q-table used in Q-learning
    #   N is the next state used to explore possible moves and decide the best one before updating
    #           the q-table
    def __init__(self, actions, Ne, LPC, gamma):
        self.actions = actions
        self.Ne = Ne
        self.LPC = LPC
        self.gamma = gamma
        self.reset()

        # Create the Q and N Table to work with
        self.Q = helper.initialize_q_as_zeros()
        self.N = helper.initialize_q_as_zeros()


    #   This function sets if the program is in training mode or testing mode.
    def set_train(self):
        self._train = True

     #   This function sets if the program is in training mode or testing mode.       
    def set_eval(self):
        self._train = False

    #   Calls the helper function to save the q-table after training
    def save_model(self):
        helper.save(self.Q)

    #   Calls the helper function to load the q-table when testing
    def load_model(self):
        self.Q = helper.load()

    #   resets the game state
    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    #   This is a function you should write. 
    #   Function Helper:IT gets the current state, and based on the 
    #   current snake head location, body and food location,
    #   determines which move(s) it can make by also using the 
    #   board variables to see if its near a wall or if  the
    #   moves it can make lead it into the snake body and so on. 
    #   This can return a list of variables that help you keep track of
    #   conditions mentioned above.
    def helper_func(self, state):
        print("IN helper_func")
        EXACT_LOCATION,WALL_NO_HIT=0,0
        TILT_LEFT_SNAKE,TILT_DOWN_SNAKE,WALL_HIT_LEFT,WALL_HIT_DOWN=1,1,1,1
        TILT_RIGHT_SNAKE,TILT_UP_SNAKE,WALL_HIT_RIGHT,WALL_HIT_UP=2,2,2,2
        snake_x_coordinate,snake_y_coordinate,body,food_x_coordinate,food_y_coordinate=state
      

        wall = {"xaxis":WALL_NO_HIT,"y-axis":WALL_NO_HIT}
        food = {"xaxis":WALL_NO_HIT,"y-axis":WALL_NO_HIT}
        snake_collision = []

        if snake_x_coordinate == helper.BOARD_LIMIT_MIN: 
            wall["xaxis"] = WALL_HIT_LEFT
        elif snake_x_coordinate == helper.BOARD_LIMIT_MAX: 
            wall["xaxis"] = WALL_HIT_RIGHT
        else: 
            wall["xaxis"] = WALL_NO_HIT

        if snake_y_coordinate == helper.BOARD_LIMIT_MIN: 
            wall["y-axis"] = WALL_HIT_DOWN
        elif snake_y_coordinate == helper.BOARD_LIMIT_MAX: 
            wall["y-axis"] = WALL_HIT_UP
        else: 
            wall["y-axis"] = WALL_NO_HIT

        if (food_x_coordinate - snake_x_coordinate) > 0: 
            food["xaxis"] = TILT_RIGHT_SNAKE
        elif (food_x_coordinate - snake_x_coordinate) < 0: 
            food["xaxis"] = TILT_LEFT_SNAKE
        else: 
            food["xaxis"] = EXACT_LOCATION


        if (food_y_coordinate - snake_y_coordinate) > 0: 
            food["y-axis"] = TILT_UP_SNAKE
        elif (food_y_coordinate - snake_y_coordinate) < 0: 
            food["y-axis"] = TILT_DOWN_SNAKE
        else: 
            food["y-axis"] = EXACT_LOCATION

        for x, y in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            snake_colide = int([snake_x_coordinate+x, snake_y_coordinate+y] in body)
            snake_collision.append(snake_colide)

        return [*wall.values(),*food.values(),*snake_collision]


    # Computing the reward, need not be changed.
    def compute_reward(self, points, dead):
        if dead:
            return -1
        elif points > self.points:
            return 1
        else:
            return -0.1

    #   This is the code you need to write. 
    #   This is the reinforcement learning agent
    #   use the helper_func you need to write above to
    #   decide which move is the best move that the snake needs to make 
    #   using the compute reward function defined above. 
    #   This function also keeps track of the fact that we are in 
    #   training state or testing state so that it can decide if it needs
    #   to update the Q variable. It can use the N variable to test outcomes
    #   of possible moves it can make. 
    #   the LPC variable can be used to determine the learning rate (lr), but if 
    #   you're stuck on how to do this, just use a learning rate of 0.7 first,
    #   get your code to work then work on this.
    #   gamma is another useful parameter to determine the learning rate.
    #   based on the lr, reward, and gamma values you can update the q-table.
    #   If you're not in training mode, use the q-table loaded (already done)
    #   to make moves based on that.
    #   the only thing this function should return is the best action to take
    #   ie. (0 or 1 or 2 or 3) respectively. 
    #   The parameters defined should be enough. If you want to describe more elaborate
    #   states as mentioned in helper_func, use the state variable to contain all that.
    def agent_action(self, state, points, dead):
        print("IN AGENT_ACTION")

        def update(state,dead,points,previous_state,previous_action):
    
            get_current_state = self.helper_func(state)
            return self.Q[(*self.helper_func(previous_state), previous_action)] + self.LPC / (self.LPC + self.N[(*self.helper_func(previous_state), previous_action)]) * (self.compute_reward(points, dead) + self.gamma * max(self.Q[(*get_current_state, 0)], self.Q[(*get_current_state, 1)], self.Q[(*get_current_state, 2)], self.Q[(*get_current_state, 3)]) - self.Q[(*self.helper_func(previous_state), previous_action)])

        Qvalues = [0] * 4
        if dead:
            previous_state = self.helper_func(self.s)
            self.Q[(*previous_state, self.a)] = update(state, dead, points, self.s, self.a)
            self.reset()
            return
        get_state = self.helper_func(state)
        if self._train and self.s != None and self.a != None:
            previous_state = self.helper_func(self.s)
            new_q = update(state, dead, points, self.s, self.a)
            self.Q[tuple(previous_state)][self.a] = new_q
        for num_action in range(helper.NUM_ACTIONS):
            if self.N[(*get_state, num_action)] < self.Ne:
                Qvalues[num_action] = 1
            else:
                Qvalues[num_action] = self.Q[(*get_state, num_action)]
        self.a = Qvalues.index(max(Qvalues))
        for num_action in range(3, -1, -1):
            if Qvalues[num_action] == max(Qvalues):
                self.a = num_action
                break
        self.N[(*get_state, self.a)] += 1
        self.s,self.points = state,points
        return self.a