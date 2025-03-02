import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Function to parse log files
def parse_events(log_file):
    events = []
    
    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
            if match:
                time_str = match.group(1)
                event_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                if "SWALLOW CONFIRMED" in line:
                    events.append((event_time, "swallow"))
                elif "POSSIBLE FORGOTTEN PILL" in line:
                    events.append((event_time, "forgotten"))
                elif "MISSED PILL" in line:
                    events.append((event_time, "missed"))
    
    return events

# File paths
log_files = {
    "December": "C:\\Users\\Administrator\\Desktop\\data\\pill_events_202412.log",
    "January": "C:\\Users\\Administrator\\Desktop\\data\\pill_events_202501.log",
    "February": "C:\\Users\\Administrator\\Desktop\\data\\pill_events_202502.log"
}

# Data collection for summary table
summary_data = []

# Loop through each file and generate plots
for month, file_path in log_files.items():
    events = parse_events(file_path)
    df = pd.DataFrame(events, columns=["datetime", "event"])
    df["date"] = df["datetime"].dt.date
    df["hour"] = df["datetime"].dt.hour + df["datetime"].dt.minute / 60.0  # Convert to decimal hours
    
    # Generate scatter plot
    plt.figure(figsize=(12, 6))
    plt.scatter(df[df["event"] == "swallow"]["date"], df[df["event"] == "swallow"]["hour"],
                color='green', label="Swallow Confirmed", alpha=0.6)
    plt.scatter(df[df["event"] == "forgotten"]["date"], df[df["event"] == "forgotten"]["hour"],
                color='orange', label="Possible Forgotten Pill", alpha=0.6)
    plt.scatter(df[df["event"] == "missed"]["date"], df[df["event"] == "missed"]["hour"],
                color='red', label="Missed Pill", alpha=0.6)
    
    plt.xlabel(f"Date ({month})")
    plt.ylabel("Hour of the Day")
    plt.title(f"Pill Events Over {month}")
    plt.xticks(rotation=45)
    plt.yticks(range(0, 25, 2))
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
    
    # Compute statistics for summary table
    total_doses = len(df)
    confirmed_doses = len(df[df["event"] == "swallow"])
    missed_doses = len(df[df["event"] == "missed"])
    forgotten_doses = len(df[df["event"] == "forgotten"])
    correct_medication_rate = (confirmed_doses / total_doses) * 100 if total_doses > 0 else 0
    
    summary_data.append([month, total_doses, confirmed_doses, missed_doses, forgotten_doses, round(correct_medication_rate, 2)])

# Create summary DataFrame
summary_df = pd.DataFrame(summary_data, columns=["Month", "Total Doses", "Confirmed Doses", "Missed Doses", "Forgotten Doses", "Correct Medication\nRate (%)"])

# Plot summary statistics
plt.figure(figsize=(12, 6))
table = plt.table(cellText=summary_df.values,
                  colLabels=summary_df.columns,
                  cellLoc='center', loc='center', bbox=[0, 0, 1, 0.7])

# Increase font size for better readability and adjust column widths
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.5, 1.5)  # Adjust scale for better visibility

# Adjust column widths to avoid text overlap
for i, key in enumerate(summary_df.columns):
    table[0, i].set_text_props(fontsize=12, weight='bold')
    if key in ["Forgotten Doses", "Correct Medication\nRate (%)"]:
        table[0, i].get_text().set_multialignment('center')

plt.axis("off")
plt.title("Medication Summary", fontsize=16, pad=5)
plt.show()

# Display summary table
import ace_tools as tools
tools.display_dataframe_to_user(name="Medication Summary", dataframe=summary_df)

