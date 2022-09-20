from tinydb import TinyDB, Query
import scipy.interpolate as si
import numpy as np

def init_query_list(db):
    with open('keys.txt') as f:
        keys = f.read().splitlines()
        keys = list(dict.fromkeys(keys))

    with open('blacklist.txt') as f1:
        blacklist_keys = f1.read().splitlines()
        blacklist_keys = list(dict.fromkeys(blacklist_keys))   

    for key in blacklist_keys:
        keys.remove(key)

    for item in db:
        if item['PROCCESS_NUMBER'] in keys:
            keys.remove(item['PROCCESS_NUMBER'])

    return keys

def human_like_mouse_move(action, start_element):
        points = [[6, 2], [3, 2],[0, 0], [0, 2]];
        points = np.array(points)
        x = points[:,0]
        y = points[:,1]

        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, 100)

        x_tup = si.splrep(t, x, k=1)
        y_tup = si.splrep(t, y, k=1)

        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

        x_i = si.splev(ipl_t, x_list)
        y_i = si.splev(ipl_t, y_list)

        startElement = start_element

        action.move_to_element(startElement);
        action.perform();

        c = 5 # change it for more move
        i = 0
        for mouse_x, mouse_y in zip(x_i, y_i):
            action.move_by_offset(mouse_x,mouse_y)
            action.perform()
            i += 1
            if i == c:
                break