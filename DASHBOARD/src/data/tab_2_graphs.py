import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data.loader import load_dataframe
import pkg_resources
import json


file_path1 = pkg_resources.resource_filename('data', 'cleaned_data.json')

df = load_dataframe(file_path1)

with open('/Users/roshan/Documents/DLProjectWork/Fighting-Homelessness-2023/DASHBOARD/src/utils/columns_mapping.json', 'r') as f:
    columns_mapping = json.load(f)


def create_plot(col_name: str, y_axis:str) -> go.Figure:
    tmp = col_name
    #adding column which combines race and sex
    df["Demographic Grouping"] = df[["race", "gender"]].apply("-".join, axis=1)

    fig = go.Figure()
    if col_name in columns_mapping:
        col_name = columns_mapping[col_name]
    

    df1=df.groupby(['Demographic Grouping', col_name]).count()['age'].reset_index(name='counts')
    df1['Total'] = df1.groupby('Demographic Grouping')['counts'].transform('sum')
    df1['Percentage'] = (df1['counts'] / df1['Total']) * 100
    df1['Percentage'] = df1['Percentage'].round(2)

    if y_axis == 'count':
        fig = px.bar(df1, x="Demographic Grouping", y="counts", color=col_name, title="Distribution of "+tmp+" by race and gender (count))")
    elif y_axis == 'percent':
        fig = px.bar(df1, x="Demographic Grouping", y="Percentage", color=col_name, title="Distribution of "+tmp+" by race and gender (percentage))")

    fig.update_layout(bargap=0.5,
                        title_x=0.5,
                        height=600,
                        width=1400,)
    return fig


