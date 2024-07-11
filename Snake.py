import PySimpleGUI as gui
from random import randrange

def draw_figure(x,y,color):
    figure = graph.draw_rectangle((x,y),(x+20,y+20),
             fill_color = color, line_color = color)
    
def draw_snake(tail):
    for xy in tail:
        draw_figure(xy[0],xy[1],"green")
     
def move(tail,direction):
    global x_fr, y_fr, fruit, type_fruits
    last_x,last_y = tail[1]
    
    for i in range(0,len(tail)-1):
        tail[i] = tail[i+1]
        
    x,y = tail[-1]
    if direction == 'Left:37':
        tail[len(tail)-1] = [x-20,y]
    elif direction == 'Right:39':
        tail[len(tail)-1] = [x+20,y]
    elif direction == 'Up:38':
        tail[len(tail)-1] = [x,y-20]
    elif direction == 'Down:40':
        tail[len(tail)-1] = [x,y+20]

    graph.erase()
    fruit = draw_figure(x_fr,y_fr,type_fruits[0])
    draw_snake(tail)
    return [last_x,last_y]

def fruit_is_caught(tail,last_x,last_y):
    global x_fr, y_fr, fruit, score, window
    if len(graph.get_figures_at_location((x_fr,y_fr))) == 2:
            tail.insert(0,[last_x,last_y])
            score += 10
            while len(graph.get_figures_at_location((x_fr,y_fr))) == 2:
                x_fr, y_fr = randrange(1,581,20), randrange(1,581,20)
                graph.relocate_figure(fruit,x_fr,y_fr)
                
    window["score"].update(score)
    
def is_lose(tail):
    for x,y in tail[:len(tail)-1]:
        if x == tail[-1][0] and y == tail[-1][1]:
            return True
    x,y = tail[-1]
    if x > 580 or x < 0 or y > 580 or y < 0:
        return True
    return False
def is_win(tail):
    if len(tail) == 900:
        return True
    return False

def restart():
    global tail, type_fruits, x_fr, y_fr, fruit, direction, score
    tail = [[100+coef,280] for coef in range(0,101,20)]
    
    draw_snake(tail)
    type_fruits = ["red","orange","yellow"]
    x_fr,y_fr = 401,281
    fruit = draw_figure(x_fr,y_fr,type_fruits[0])
    direction = 0
    
    score = 0
    window["score"].update(score)
    
layout = [
       [gui.Graph(
            canvas_size = (602,602),
            graph_bottom_left=(-1,602),
            graph_top_right=(602,-1),
            background_color='white',
            key='graph'
        )],
       [gui.Text("Score"),
        gui.Input(key = "score", size = (12,1), disabled = True)]
    ]
window = gui.Window("Snake", layout, finalize = True, return_keyboard_events = True)
graph = window['graph']
restart()
while True:
    event, values = window.read(timeout = 80)
    if event == gui.WIN_CLOSED:
        break
    else:
        if event == "Left:37" and direction != "Right:39" and direction != 0:
            ##direction != 0 is needed because at the beginning of the game the snake cannot move to the left
            direction = "Left:37"
        elif event == "Right:39" and direction != "Left:37":
            direction = "Right:39"
        elif event == "Up:38" and direction != "Down:40":
            direction = "Up:38"
        elif event == "Down:40" and direction != "Up:38":
            direction = "Down:40"
    if direction != 0:
        last_x, last_y = move(tail,direction)
        if is_win(tail) or is_lose(tail):
            event = window.read()
            graph.erase()
            restart()
            continue
        fruit_is_caught(tail,last_x,last_y)
