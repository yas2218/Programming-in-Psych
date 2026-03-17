##go no go

#Hi, I’m trying to adapt a GO/NOGO protocol from Price et al., 2016. Food-specific response inhibition,
#dietary restraint and snack intake in lean and overweight/obese adults.
#The task consists in 50 trials (40 go and 10 no-go). During go trials the 
#subject should press a key as fast as possible. During no-go trials, no key should be pressed. 
#Each trial is composed by an image presented for 750ms and was separated by a blank screen for 500 ms 
#and preceded by a fixation cross for 500 ms. The sequence of go/nogo stimuli are predetermined. 
#Two set of images are used: 10 go images (each one is presented 4 times) and 10 no-go images 
#(each one is presented one time). Image order should be randomized across subjects.
# we are going to change for anorexia nervosa intervention

import pandas as pd
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim, Rect, TextBox, DotStim
from psychopy.core import Clock, quit, wait
from psychopy.event import Mouse
from psychopy.hardware.keyboard import Keyboard
from psychopy import event, data
import random

exp_info = {'participant_nr': '', 'age': '21'}
dlg = DlgFromDict(exp_info)

p_name= exp_info['participant_nr']

# Initialize a fullscreen window with my monitor (HD format) size
# and my monitor specification called "samsung" from the monitor center
win = Window(size=(1200, 800), fullscr=False)
kb = Keyboard()

# Also initialize a mouse, although we're not going to use it
mouse = Mouse(visible=False)

#Instruction Screen
instr_text = (
    "Instructions:\n"
    "You will see images of food surrounded by a border.\n"
    "If the border is Green (go), press the spacebar as fast as possible.\n"
    "if the border is Red (no-go), do not press any key.\n\n"
    "press any key to start."
)
instructions = TextStim(win, text=instr_text, height=0.08)
instructions.draw()
win.flip()
event.waitKeys()

# Initialize a (global) clock
clock = Clock()
f_list = f"/Users/yassaghafi/Downloads/HF_LF_60.csv"
foods = pd.read_csv(f_list)
hf = foods[foods['fat']==1]
lf = foods[foods['fat']==0]
lf = lf.sample(frac=0.4)
hf = hf.sample(frac=0.4)
trial_foods = pd.concat([lf, lf, lf, hf]).sample(frac=1).reset_index(drop=True)
cue_border = Rect(win, width=1.1, height=1.1, lineWidth=10)
kb=Keyboard()

trial_foods['participant_response'] = ""
trial_foods['rt'] = ""

for i in range(0,len(trial_foods)):
    trial=trial_foods.iloc[i]
    fixation = TextStim(win, "+")
    fixation.draw()
    win.flip()
    wait(0.5)
    path = "/Users/yassaghafi/Downloads/Food-Choice-Task-main/stimuli/" + trial.food
    im = ImageStim(win, path, size=(1.0, 1.0))
    if trial.fat==1:
        correct_action = "nogo"
        cue_border.lineColor = 'red'
    else: 
        correct_action = "go"
        cue_border.lineColor = 'green'
   
    t_clock = Clock()
    kb.clock.reset()
    response = "nogo"
    rt = "NA"
    
    while t_clock.getTime() < .75:
        cue_border.draw()
        im.draw()
        win.flip()
        
        keys = kb.getKeys(['space','escape'], waitRelease=False)
        if keys:
            resp = keys[0].name
            if resp == 'escape':
                win.close()
                quit()
            else:
                response = "go"
                rt = keys[0].rt

    win.flip()
    wait(.5)
    trial_foods['response']=response
    trial_foods['rt']= rt

trial_foods.to_csv(f"{p_name}_gonogo_results.csv", index=False)

## tasks
# 1. figure out what is happening in the task & add instructions
# 2. we need to add go-nogo! How would we do that?

    
