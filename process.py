import glob
import pandas as pd


def main():
    process_csv()


def process_csv():
    for file in glob.glob("input/*.csv"):
        df = pd.read_csv(file)
        # Split dataframe into 2 columns -> k, v
        split_data = df["kolom:waarde"].str.split(":", expand=True)
        split_data.columns = ["Key", "Value"]
        split_data["Key"] = (
            split_data["Key"].str.strip().str.lower().str.replace(" ", "")
        )
        split_data["Value"] = split_data["Value"].str.strip()

        # Split full name into first and last name
        full_name = split_data[split_data["Key"] == "naam"]["Value"].str.split(
            " ", n=1, expand=True
        )
        split_data.loc[split_data["Key"] == "naam", "Key"] = "first_name"
        split_data.loc[split_data["Key"] == "first_name", "Value"] = full_name[0]

        # Set last name if provided
        if full_name.shape[1] > 1 and pd.notna(full_name.iloc[0, 1]):
            last_name = full_name.iloc[0, 1]
        else:
            last_name = ""
        last_name_df = pd.DataFrame({"Key": ["last_name"], "Value": [last_name]})
        split_data = pd.concat([split_data, last_name_df])

        print(split_data)


if __name__ == "__main__":
    main()
