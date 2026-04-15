import pandas as pd
import numpy as np
import streamlit
from streamlit import columns

def fetch_medal_tally(df,year, country):
    medal_df = df.drop_duplicates(subset=['Team','Games','Event','City','Sport','Medal','NOC','Year'])
    flag = 0
    if (year == "Overall" and country == "Overall"):
        temp_df = medal_df
    elif (year != "Overall" and country == "Overall"):
        temp_df = medal_df[medal_df["Year"] == int(year)]
    elif (year == "Overall" and country != "Overall"):
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]
    elif (year != "Overall" and country != "Overall"):
        temp_df = medal_df[(medal_df["Year"] == int(year)) & (medal_df["region"] == country)]
    if flag ==1:
        x = temp_df.groupby("Year")
        x = x.sum()[['Gold','Silver','Bronze']].sort_values("Year", ascending = True).reset_index()
    else:
        x = temp_df.groupby("region")
        x = x.sum()[['Gold','Silver','Bronze']].sort_values("Gold", ascending = False).reset_index()
    x["Total"] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold']   = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['Total']  = x['Total'].astype(int)
    return x

# def medal_tally(df):
#     df.drop_duplicates(subset=['Team', 'Games', 'Event', 'City', 'Sport', 'Medal', 'NOC', 'Year'], inplace=True)
#     medal_tally = df.groupby('region')
#     medal_tally = medal_tally.sum()[['Gold', 'Silver', 'Bronze']].sort_values("Gold", ascending=False).reset_index()
#     medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
#     medal_tally = medal_tally.rename(columns={'region': 'Region'})
#
#     medal_tally['Gold'] = medal_tally['Gold'].astype(int)
#     medal_tally['Silver'] = medal_tally['Silver'].astype(int)
#     medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
#     medal_tally['Total'] = medal_tally['Total'].astype(int)
#     return medal_tally

def country_year_list(df):
    year = df["Year"].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')
    return country, year

def data_over_time(df, col):
    nation_over_time = df.drop_duplicates(["Year", col])
    nation_over_time = nation_over_time["Year"].value_counts().reset_index().sort_values("Year", ascending=True)
    nation_over_time = nation_over_time.rename(columns={"count": col})

    return nation_over_time


def most_successfull_athlete(df, sport):
    if sport == "Overall":
        temp_df = df.dropna(subset=["Medal"])["Name"].value_counts().reset_index()
        temp_df = temp_df.merge(df, left_on="Name", right_on="Name", how="left")[
            ["Name", "count", "region", "Sport"]].drop_duplicates("Name")
    elif sport != "Overall":
        temp_df = df.dropna(subset=["Medal"])["Name"].value_counts().reset_index()
        temp_df = temp_df.merge(df, left_on="Name", right_on="Name", how="left")[
            ["Name", "count", "region", "Sport"]].drop_duplicates("Name")
        temp_df = temp_df[temp_df["Sport"] == sport]
    temp_df = temp_df.rename(columns={"count": "Medal", "region": "Country"})

    return temp_df

def countywise_medal_tally(df, country):
    temp_df = df.dropna(subset=["Medal"]).drop_duplicates(
        ["Team", "NOC", "Year", "City", "Sport", "Event", "Medal", "region"])
    temp_df = temp_df[temp_df["region"] == country]
    temp_df = temp_df["Year"].value_counts().reset_index().sort_values("Year")
    temp_df = temp_df.rename(columns={"count": "Country_medals"})
    return temp_df

def county_sport_heatmap(df,country):
    temp_df = df.dropna(subset=["Medal"]).drop_duplicates(
        ["Team", "NOC", "Year", "City", "Sport", "Event", "Medal", "region"])
    temp_df = temp_df[temp_df["region"] == country]
    temp_df = temp_df.pivot_table(index="Sport", columns="Year", values="Medal", aggfunc="count").fillna(0).astype(int)

    return temp_df


def most_successfull_athlete_countrywise(df, country):
    temp_df = df[df["region"] == country]
    temp_df = temp_df.dropna(subset=["Medal"])["Name"].value_counts().reset_index()
    temp_df = temp_df.merge(df, left_on="Name", right_on="Name", how="left")[
        ["Name", "count", "Sport"]].drop_duplicates("Name")

    return temp_df.head(10)

def age_distribution(df):
    x = df["Age"].dropna()
    x1 = df[df["Medal"] == "Gold"]["Age"].dropna()
    x2 = df[df["Medal"] == "Silver"]["Age"].dropna()
    x3 = df[df["Medal"] == "Bronze"]["Age"].dropna()

    return x,x1,x2,x3

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final