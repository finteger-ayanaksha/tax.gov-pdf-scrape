import pandas as pd

# Creating the data
data = {
    "Value": [
        "Notifying Jurisdictions",
        "Notified Agreements",
        "Matched Agreements",
        "One-Way Agreements",
        "Waiting Agreements"
    ],
    "Total Type": [
        104,
        "2,977 (4,943 with duplication)",
        "1,966 (3,932 with duplication)",
        217,
        794
    ],
    "Total Number as of the Selected Date": [
        104,
        "2,977 (4,943 with duplication)",
        "1,966 (3,932 with duplication)",
        217,
        794
    ],
    "Total Number as of Today": [
        104,
        "2,977 (4,943 with duplication)",
        "1,966 (3,932 with duplication)",
        217,
        794
    ]
}

# Creating a DataFrame
df = pd.DataFrame(data)

# Saving to an Excel file
file_path = "/mnt/data/agreements_data.xlsx"
df.to_excel(file_path, index=False)

# Providing the download link
file_path
