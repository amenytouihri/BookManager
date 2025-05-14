# Exceptions in Bookmanger2

## Why Exceptions Were Used
In the Bookmanager2 project, exceptions were implemented to handle unexpected scenarios and ensure the application remains robust and user-friendly without crashing the application. This approach improves the overall reliability and maintainability of the system.


## Example: `reading_goals.py`
In the `reading_goals.py` file, exceptions are used to handle scenarios where user-defined reading goals might be invalid or improperly configured. For instance:

```python

try:
    goals_df = pd.read_csv('data/reading_goals.csv')
except FileNotFoundError:
    goals_df = pd.DataFrame(columns=['year', 'goal'])
```

This example demonstrates how a `FileNotFoundError` exception is used to handle cases where the expected file is missing. By providing a fallback mechanism to create an empty DataFrame, the application ensures continuity and avoids crashes, maintaining a smooth user experience.
