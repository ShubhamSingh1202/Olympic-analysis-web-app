import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import preprocessor,helper
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv("noc_regions.csv")

df = preprocessor.preprocess(df, region_df)
st.sidebar.title("Olympic Analysis")
st.sidebar.image("https://substackcdn.com/image/fetch/$s_!Fas9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F29dd3945-540a-45fe-b89c-d38c9e4f365f_1500x1500.jpeg")
st.sidebar.subheader("Medal Analysis")
user_menu = st.sidebar.radio(
    'Select the option',
    ('Medal Analysis', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Analysis':
    st.sidebar.header("Medal Tally")

    country, year = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', year)
    selected_country =st.sidebar.selectbox('Select Counrty', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if (selected_year == "Overall" and selected_country == "Overall"):
        st.title(f"Overall Olympic Medal Tally")
    elif (selected_year != "Overall" and selected_country == "Overall"):
        st.title(f"All Country Performance in {selected_year} Olympic" )
    elif (selected_year == "Overall" and selected_country != "Overall"):
        st.title(f"{selected_country} Performance in Olympic")
    elif (selected_year != "Overall" and selected_country != "Overall"):
        st.title(f"{selected_country} Performance {selected_year} in Olympic")
    st.table(medal_tally)

if user_menu == "Overall Analysis":
    editions = df["Year"].unique().shape[0] -1
    city = df["City"].unique().shape[0]
    events = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    nations = df["region"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]

    st.header("Top Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Total Editions")
        st.subheader(f"-> {editions}")
    with col2:
        st.subheader("Host City")
        st.subheader(f"-> {city}")
    with col3:
        st.subheader("Total Events")
        st.subheader(f"-> {events}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Total Athletes")
        st.subheader(f"-> {athletes}")
    with col2:
        st.subheader("Total Nations")
        st.subheader(f"-> {nations}")
    with col3:
        st.subheader("Total Sports")
        st.subheader(f"-> {sports}")

    st.divider()
    st.title(f"Participating Nation over the time")
    nation_over_time = helper.data_over_time(df,"region")
    fig = px.line(nation_over_time, x= "Year", y= "region")
    st.plotly_chart(fig)

    st.divider()
    st.title(f"Number of Events conducted every Year")
    event_over_time = helper.data_over_time(df,"Event")
    fig = px.line(event_over_time, x= "Year", y= "Event")
    st.plotly_chart(fig)

    st.divider()
    st.title(f"Number of Athletes every Year")
    event_over_time = helper.data_over_time(df,"Name")
    fig = px.line(event_over_time, x= "Year", y= "Name")
    st.plotly_chart(fig)
# st.plotly_chart is used t show the dynamic charts
# st.pyplot is use to show the static graphs
    st.divider()
    st.title(f"Number of Event per Sports every Year")
    # fig, ax = plt.subplots(figsize = (20,20))
    fig = plt.figure(figsize = (20,20))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    x = x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype(int)
    x = sns.heatmap(x, annot=True)
    st.pyplot(fig)

    st.divider()
    st.title("Most Successfull Athletes")
    sports_list = df["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, "Overall")
    select_sports = st.selectbox("Select Sport", sports_list)

    x = helper.most_successfull_athlete(df, select_sports)
    st.table(x)

if user_menu == "Country-wise Analysis":
    st.title("Country wise Analysis")
    st.divider()
    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()
    country = st.sidebar.selectbox("Select Country", country_list)

    temp_df = helper.countywise_medal_tally(df, country)
    x = px.line(temp_df, x= "Year", y= "Country_medals")
    st.header(f"{country} Medal Analysis")
    st.plotly_chart(x)

    st.divider()
    country_heatmap = helper.county_sport_heatmap(df,country)
    fig, ax = plt.subplots(figsize = (20,20))
    ax = sns.heatmap(country_heatmap, annot=True)
    st.header(f"{country} Medals Heatmap Analysis")
    st.pyplot(fig)

    st.divider()
    top10 = helper.most_successfull_athlete_countrywise(df, country)
    st.header(f"{country} Top 10 Athletes")
    st.table(top10)

if user_menu == "Athlete wise Analysis":
    st.title("Athlete wise Analysis")

    st.divider()
    x, x1,x2, x3 = helper.age_distribution(df)
    fig = ff.create_distplot([x,x1,x2,x3],["Overall Age","Gold Medal", "Silver", "Bronze"],show_hist=False, show_rug=False)
    st.header("Age Distribution")
    st.plotly_chart(fig)

    st.divider()
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = df[df ['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.divider()
    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df,x = 'Weight',y= 'Height', hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.divider()
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


