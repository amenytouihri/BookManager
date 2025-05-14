"""Manage reading goals for the current year."""

import streamlit as st
import pandas as pd

def manage_reading_goal(current_year):
    try:
        # Create or read the CSV file
        try:
            goals_df = pd.read_csv('data/reading_goals.csv')
        except FileNotFoundError:
            goals_df = pd.DataFrame(columns=['year', 'goal'])

        # Get current goal if exists
        if not goals_df.empty and current_year in goals_df['year'].values:
            st.session_state.current_goal = goals_df.loc[goals_df['year'] == current_year, 'goal'].values[0]
        # Display current goal
        if st.session_state.current_goal is not None:
            st.write(f"Your {current_year} goal: **{int(st.session_state.current_goal)} books**")

        # Input for new goal
        new_goal = st.number_input(
            f"Set/update your {current_year} reading goal:",
            min_value=1,
            value=int(st.session_state.current_goal) if st.session_state.current_goal else 12,
            step=1,
            key="goal_input"
        )

        if st.button("Save Goal"):
            # Update or add the goal
            if current_year in goals_df['year'].values:
                goals_df.loc[goals_df['year'] == current_year, 'goal'] = new_goal
            else:
                new_row = pd.DataFrame({'year': [current_year], 'goal': [new_goal]})
                goals_df = pd.concat([goals_df, new_row], ignore_index=True)

            # Save to CSV and update session state
            goals_df.to_csv('data/reading_goals.csv', index=False)
            st.session_state.current_goal = new_goal
            st.rerun()  # This forces the UI to update immediately

    except Exception as e:
        st.error(f"An error occurred: {e}")
