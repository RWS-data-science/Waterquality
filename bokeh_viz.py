import pickle
import pandas as pd
import numpy as np
import math

from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.models import HoverTool
from bokeh.models.widgets import Select
from bokeh.layouts import WidgetBox, row, column
from bokeh.io import show, curdoc, output_notebook

with open('eijs_metrics.p','rb') as f:
    metric_dict = pickle.load(f)

with open('eijs_predictions.p','rb') as f:
    prediction_dict = pickle.load(f)

with open('eijs_targets.p','rb') as f:
    target_dict = pickle.load(f)

with open('lob_metrics.p','rb') as f:
    metric_dict = {**metric_dict, **pickle.load(f)}

with open('lob_predictions.p','rb') as f:
    prediction_dict = {**prediction_dict, **pickle.load(f)}

with open('lob_targets.p','rb') as f:
    target_dict = {**target_dict, **pickle.load(f)}

def make_data(location, parameter):
    '''
    Create a dataframe with the measured and predicted values of the parameter at a given location.
    
    Args:
        - location (str): one of the available location
        - parameter (str): one of the parameters measured and predicted at that location
        
    Returns:
        - ColumnDataSource object for bokeh
    '''
    
    outDF = pd.DataFrame(prediction_dict[location][parameter])
    outDF.columns = ['modeled_values']
    
    outDF['measured_values'] = target_dict[location][parameter]
    outDF = outDF[target_dict[location].index.min():target_dict[location].index.max()]
    
    outDF['string_date'] = outDF.index.map(lambda x: x.strftime('%d %b %Y'))
    
    return ColumnDataSource(outDF)
    

def make_plot(src, location, parameter):
    '''
    Using the input data created by make_data, make a line plot.
    
    Args:
        - src (ColumnDataSource): output of make_data()
        - location (str): location of the src
        - parameter (str): parameters of the src (the raw version thereof, including the underscores)
        
    Returns:
        - bokeh figure
    '''
    
    top =max(np.nanmax(src.data['measured_values']),np.nanmax(src.data['modeled_values']))
    top = 1.2*top

    # create a new plot with a title and axis labels
    try:
        p = figure(title='{0} at {1} (accuracy {2:.2f}%, R2 {3:.2f}%)'.format(parameter.split('_')[0].capitalize(), 
                                                                              location, 
                                                                              100*metric_dict[location].loc[parameter,'acc'],
                                                                              100*metric_dict[location].loc[parameter,'r2']),
                   x_axis_label='', 
                   y_axis_label='{0} ({1})'.format(*parameter.split('_')[:-1]), 
                   x_axis_type='datetime',
                   y_range=(0., top))
    except:
        p = figure(title='{0} at {1} (missing metrics due to data issues)'.format(parameter.split('_')[0].capitalize(), 
                                                                              location),
                   x_axis_label='', 
                   y_axis_label='{0} ({1})'.format(*parameter.split('_')[:-1]), 
                   x_axis_type='datetime',
                   y_range=(0., top))
    
    # p.line(source=src, x='datetime', y='Measured values', 
    #        legend='Measurement', line_width=2, line_color='#1f77b4')
    p.circle(source=src, x='datetime', y='measured_values', 
             legend='Measured values', color='#1f77b4', size=10)

    p.line(source=src, x='datetime', y='modeled_values', 
           line_width=2, line_color='#ff7f0e')
    p.circle(source=src, x='datetime', y='modeled_values', 
             legend='Modeled values', color='#ff7f0e', size=7)
    
    hover = HoverTool(tooltips=[('Date', '@string_date'),
                                ('Measured value', '@measured_values'), \
                                ('Modeled value', '@modeled_values')])    
    p.add_tools(hover)
    
    return p

def make_metric_data(location):
    outDF = metric_dict[location].dropna().copy()
    outDF['acc'] = 100*outDF['acc']
    outDF['r2'] = 100*outDF['r2']

    return ColumnDataSource(outDF)

def make_metric_plot(metric_src, location):
    a = figure(plot_height=200, title='R2 (higher is better)',
               y_axis_label='R2 (%)', x_range=list(metric_src.data['index']),
               tools='ypan,ywheel_zoom,reset', active_scroll='ywheel_zoom')
    a.vbar(source=metric_src, x='index', top='r2', width=0.9)
    a.xaxis.major_label_text_font_size = '0pt'

    hover = HoverTool(tooltips=[('Parameter', '@index'),
                                ('Accuracy', '@r2')], 
                      mode='vline')    
    a.add_tools(hover)


    b = figure(plot_height=200, title='Mean square error (lower is better)',
               y_axis_label='MSE', x_range=list(metric_src.data['index']),
               tools='ypan,ywheel_zoom,reset', active_scroll='ywheel_zoom')
    b.vbar(source=metric_src, x='index', top='mse', width=0.9)
    b.xaxis.major_label_text_font_size = '0pt'

    hover = HoverTool(tooltips=[('Parameter', '@index'),
                                ('MSE', '@mse')],
                      mode='vline')    
    b.add_tools(hover)

    c = figure(plot_height=350, title='Mean accuracy (higher is better)',
               y_axis_label='Mean accuracy (%)', x_range=list(metric_src.data['index']),
               tools='ypan,ywheel_zoom,reset', active_scroll='ywheel_zoom')
    c.vbar(source=metric_src, x='index', top='acc', width=0.9)
    c.xaxis.major_label_orientation = math.pi/4

    hover = HoverTool(tooltips=[('Parameter', '@index'),
                                ('R2', '@acc')],
                      mode='vline')    
    c.add_tools(hover)

    d = column(a,b,c)

    return d

def update_plot(attr, old, new):
    loc = location_dropdown.value
    par = parameter_dropdown.value
    
    new_src = make_data(loc, par)
    
    src.data.update(new_src.data)
    
    new_p = make_plot(new_src, loc, par)
    
    p.title.update(text=new_p.title.text)
    p.y_range.update(end=new_p.y_range.end)
    p.yaxis[0].update(axis_label=new_p.yaxis[0].axis_label)


def update_parameter_dropdown(attr, old, new):
    location = location_dropdown.value
    new_pars = [(i, '{0} ({1}, {2})'.format(*i.split('_'))) for i in target_dict[location].columns]
    
    parameter_dropdown.update(options=new_pars, value=new_pars[0][0])

def update_parameter_dropdown(attr, old, new):
    location = location_dropdown.value
    new_pars = [(i, '{0} ({1}, {2})'.format(*i.split('_'))) for i in target_dict[location].columns]

    parameter_dropdown.update(options=new_pars, value=new_pars[0][0])

def update_metric_plot(attr,old,new):
    loc = location_dropdown.value

    new_metric_src = make_metric_data(loc)

    metric_src.data.update(new_metric_src.data)

    new_d = make_metric_plot(new_metric_src, loc)

    for i in range(3):
        q.children[i].x_range.update(factors=new_d.children[i].x_range.factors)

locs = [(l, l) for l in metric_dict.keys()]
location_dropdown = Select(title="Location:", value=locs[0][0], options=locs)

location_dropdown.on_change('value', update_parameter_dropdown)
location_dropdown.on_change('value', update_metric_plot)

pars = [(col, '{0} ({1}, {2})'.format(*col.split('_'))) for col in target_dict[locs[0][0]].columns]
parameter_dropdown = Select(title="Parameter:", value=pars[0][0], options=pars)

parameter_dropdown.on_change('value', update_plot)

# Put controls in a single element
controls = WidgetBox(location_dropdown, 
                     parameter_dropdown)

src = make_data(location_dropdown.value, 
                parameter_dropdown.value)

p = make_plot(src, location_dropdown.value, 
              parameter_dropdown.value)

metric_src = make_metric_data(location_dropdown.value)

q = make_metric_plot(metric_src, location_dropdown.value)

intermediate = column(controls,p)

# Create a row layout
layout = row(intermediate, q)
# layout = row(controls, p, q)

curdoc().add_root(layout)

#show(layout)#,p)
