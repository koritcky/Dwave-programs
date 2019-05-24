from dwave.system.samplers import DWaveSampler
sampler = DWaveSampler(solver={'qpu': True, 'max_anneal_schedule_points__gte': 4})
annealing_range = sampler.properties["annealing_time_range"]
print(annealing_range)
max_slope = 1.0/annealing_range[0]

print("Annealing time range:", annealing_range)
print("Maximum slope:", max_slope)

## Pause shedule

## Draw the pause
# import numpy as np
# from bokeh.plotting import figure, show
# from bokeh.io import output_notebook
# output_notebook()

# shedule = [[0.0, 0.0],[50.0, 0.5], [250.0, 0.5], [300.0, 1.0]]
# print("Schedule: %s" % schedule)
# p = figure(title="Example Anneal Schedule with Pause", x_axis_label='Time [us]', y_axis_label='Annealing Parameter s')
# p.line(*np.array(schedule).T)
# show(p)