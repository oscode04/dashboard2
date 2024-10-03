import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

bikeRent_df = pd.read_csv('hour.csv')

bikeRent_df['day_type'] = bikeRent_df.apply(lambda row: 'Holiday' if row['holiday'] == 1 
                                            else ('Work Day' if row['workingday'] == 1 else 'Weekend'), axis=1)

st.title("Rent Bike Analysis Dashboard")

st.sidebar.header("Filter Options")

season_options = st.sidebar.multiselect(
    'Select season(s) to view:',
    options=bikeRent_df['season'].unique(),
    default=bikeRent_df['season'].unique()
)

hour = st.sidebar.slider("Select the hour of the day:", min_value=0, max_value=23, value=(0, 23))

filtered_data = bikeRent_df[(bikeRent_df['season'].isin(season_options)) & (bikeRent_df['hr'].between(hour[0], hour[1]))]

if st.sidebar.checkbox("Show raw data"):
    st.write(filtered_data)

# Tabs for "Season" and "Day Type"
tab1, tab2 = st.tabs(["Season Analysis", "Day Type Analysis"])

# Tab 1: Season Analysis
with tab1:
    st.header("Average Rentals by Season")
    
    # Filter data based on season selection
    filtered_season_data = bikeRent_df[bikeRent_df['season'].isin(season_options)]

    # Visualization for season
    if len(season_options) > 0:
        avg_casual_registered_season = filtered_season_data.groupby('season')[['casual', 'registered']].mean().reset_index()
        
        # Plot bar chart for casual and registered users by season
        fig, ax = plt.subplots(figsize=(10, 5))
        avg_casual_registered_season.plot(kind='bar', x='season', y=['casual', 'registered'], ax=ax, color=['blue', 'green'])
        plt.title("Average Rentals by Season")
        plt.xlabel("Season (1=Spring, 2=Summer, 3=Fall, 4=Winter)")
        plt.ylabel("Average Number of Rentals")
        st.pyplot(fig)
    
    # Summary Statistics for Season
    st.subheader("Summary Statistics (Season)")
    st.write(filtered_season_data[['casual', 'registered']].describe())

    # ANOVA Test for Season
    st.subheader("ANOVA Test for Season")
    if len(season_options) == 4:
        anova_casual_season = stats.f_oneway(
            filtered_season_data[filtered_season_data['season'] == 1]['casual'],
            filtered_season_data[filtered_season_data['season'] == 2]['casual'],
            filtered_season_data[filtered_season_data['season'] == 3]['casual'],
            filtered_season_data[filtered_season_data['season'] == 4]['casual']
        )
        st.write(f"ANOVA for Casual Users by Season: F-statistic = {anova_casual_season.statistic:.5f}, p-value = {anova_casual_season.pvalue:.5f}")
        
        anova_registered_season = stats.f_oneway(
            filtered_season_data[filtered_season_data['season'] == 1]['registered'],
            filtered_season_data[filtered_season_data['season'] == 2]['registered'],
            filtered_season_data[filtered_season_data['season'] == 3]['registered'],
            filtered_season_data[filtered_season_data['season'] == 4]['registered']
        )
        st.write(f"ANOVA for Registered Users by Season: F-statistic = {anova_registered_season.statistic:.5f}, p-value = {anova_registered_season.pvalue:.5f}")
    else:
        st.warning("ANOVA test for season requires exactly 4 seasons. Please select all 4 seasons.")

# Tab 2: Day Type Analysis
with tab2:
    st.header("Average Rentals by Day Type")

    # Sidebar for day type filter
    day_type_options = st.sidebar.multiselect(
        'Select day type(s) to view:',
        options=['Work Day', 'Weekend', 'Holiday'],
        default=['Work Day', 'Weekend', 'Holiday']
    )

    # Filter data based on day type selection
    filtered_day_type_data = bikeRent_df[bikeRent_df['day_type'].isin(day_type_options)]

    # Visualization for day type
    if len(day_type_options) > 0:
        avg_casual_registered_day_type = filtered_day_type_data.groupby('day_type')[['casual', 'registered']].mean().reset_index()

        # Plot bar chart for casual and registered users by day type
        fig, ax = plt.subplots(figsize=(10, 5))
        avg_casual_registered_day_type.plot(kind='bar', x='day_type', y=['casual', 'registered'], ax=ax, color=['blue', 'green'])
        plt.title("Average Rentals by Day Type")
        plt.xlabel("Day Type")
        plt.ylabel("Average Number of Rentals")
        st.pyplot(fig)

    # Summary Statistics for Day Type
    st.subheader("Summary Statistics (Day Type)")
    st.write(filtered_day_type_data[['casual', 'registered']].describe())

    # ANOVA Test for Day Type
    st.subheader("ANOVA Test for Day Type")
    if len(day_type_options) == 3:
        anova_casual_day_type = stats.f_oneway(
            filtered_day_type_data[filtered_day_type_data['day_type'] == 'Work Day']['casual'],
            filtered_day_type_data[filtered_day_type_data['day_type'] == 'Weekend']['casual'],
            filtered_day_type_data[filtered_day_type_data['day_type'] == 'Holiday']['casual']
        )
        st.write(f"ANOVA for Casual Users by Day Type: F-statistic = {anova_casual_day_type.statistic:.5f}, p-value = {anova_casual_day_type.pvalue:.5f}")
        
        anova_registered_day_type = stats.f_oneway(
            filtered_day_type_data[filtered_day_type_data['day_type'] == 'Work Day']['registered'],
            filtered_day_type_data[filtered_day_type_data['day_type'] == 'Weekend']['registered'],
            filtered_day_type_data[filtered_day_type_data['day_type'] == 'Holiday']['registered']
        )
        st.write(f"ANOVA for Registered Users by Day Type: F-statistic = {anova_registered_day_type.statistic:.5f}, p-value = {anova_registered_day_type.pvalue:.5f}")
    else:
        st.warning("ANOVA test for day type requires all 3 types (Work Day, Weekend, Holiday). Please select all day types.")
