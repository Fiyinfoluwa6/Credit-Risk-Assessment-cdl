import os  
import re  
import numpy as np
import math
import pandas as pd
from IPython.display import display_html

def display_side_by_side(*args):
    html_str=''
    for df in args:
        html_str+=df.to_html()
    display_html(html_str.replace('table','table style="display:inline"'),raw=True)
    
def display_crosstab_side_by_side(df, column1, column2):
    # Create the crosstab
    crosstab = pd.crosstab(df[column1], df[column2])
    
    # Calculate the crosstab with percentages
    crosstab_percentage = pd.crosstab(df[column1], df[column2], normalize=True) * 100
    
    # Create a styler object for the crosstab
    styler1 = crosstab.style.background_gradient(cmap='Blues')
     # Calculate the crosstab with percentages
    styler2 =  crosstab_percentage.style.background_gradient(cmap='Blues')
    
    
    # Display the tables side by side
    display_side_by_side(styler1, styler2)

def calculate_woe_iv(dataset, feature, target):
    lst = []
    for i in range(dataset[feature].nunique()):
        val = list(dataset[feature].unique())[i]
        lst.append({
            'Value': val,
            'All': dataset[dataset[feature] == val].count()[feature],
            'Good': dataset[(dataset[feature] == val) & (dataset[target] == 'Good')].count()[feature],
            'Bad': dataset[(dataset[feature] == val) & (dataset[target] == 'Bad')].count()[feature]
        }) 
    dset = pd.DataFrame(lst)
    dset['Distr_Good'] = dset['Good'] / dset['Good'].sum()
    dset['Distr_Bad'] = dset['Bad'] / dset['Bad'].sum()
    dset['WoE'] = np.log(dset['Distr_Good'] / dset['Distr_Bad'])
    dset['NWoE'] = dset.WoE * -1
    dset['WoE%'] = dset.WoE * 100
    dset['NWoE%'] = dset.WoE * -1
    dset = dset.replace({'WoE': {np.inf: 0, -np.inf: 0}})
    dset = dset.replace({'WoE%': {np.inf: 0, -np.inf: 0}})
    dset['IV'] = (dset['Distr_Good'] - dset['Distr_Bad']) * dset['WoE']
    iv = dset['IV'].sum()
    dset = dset.sort_values(by='Value')
    return dset, iv

def calculate_woe_iv(dataset, feature, target):
    lst = []
    for i in range(dataset[feature].nunique()):
        val = list(dataset[feature].unique())[i]
        lst.append({
            'Value': val,
            'All': dataset[dataset[feature] == val].count()[feature],
            'Good': dataset[(dataset[feature] == val) & (dataset[target] == 'Good')].count()[feature],
            'Bad': dataset[(dataset[feature] == val) & (dataset[target] == 'Bad')].count()[feature]
        }) 
    dset = pd.DataFrame(lst)
    dset['Distr_Good'] = dset['Good'] / dset['Good'].sum()
    dset['Distr_Bad'] = dset['Bad'] / dset['Bad'].sum()
    dset['WoE'] = np.log(dset['Distr_Good'] / dset['Distr_Bad'])
    dset['IV'] = (dset['Distr_Good'] - dset['Distr_Bad']) * dset['WoE']
    iv = dset['IV'].sum()
    return iv
