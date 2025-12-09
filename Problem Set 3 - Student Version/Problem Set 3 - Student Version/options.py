# This file contains the options that you should modify to solve Question 2

def question2_1():
    # low discount factor
    # no noise short 
    return {
        "noise": 0,
        "discount_factor": 0.1,
        "living_reward": -0.1
    }

def question2_2():
    # low discount factor
    # high noise
    # tried discount_factor 0.1 fail
    return {
        "noise": 0.2,
        "discount_factor": 0.2,
        "living_reward": -0.1
        }

def question2_3():
    # far ->high discount
    # short no noise
    return {
        "noise": 0,
        "discount_factor": 0.7,
        "living_reward": -0.3
    }

def question2_4():
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.1
    }

def question2_5():
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": 1.0
    }

def question2_6():
   # tried living_reward -10 fail 
    return {
        "noise": 0.1,
        "discount_factor": 1,
        "living_reward": -20.0
    }