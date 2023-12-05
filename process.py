import glob
import pandas as pd


def main():
    process_csv()


def process_csv():
    df_all = []
    for file in glob.glob("input/*.csv"):
        df = pd.read_csv(file)
        # Split dataframe into 2 columns -> k, v
        df = df["kolom:waarde"].str.split(":", expand=True)
        df.columns = ["Key", "Value"]
        df["Key"] = df["Key"].str.strip().str.lower().str.replace(" ", "")
        df["Value"] = df["Value"].str.strip()

        # Split full name into first and last name
        full_name = df[df["Key"] == "naam"]["Value"].str.split(" ", n=1, expand=True)
        first_name = pd.DataFrame(
            {"Key": ["first_name"], "Value": [full_name[0].iloc[0]]}
        )
        if full_name.shape[1] > 1 and pd.notna(full_name.iloc[0, 1]):
            last_name = pd.DataFrame(
                {"Key": ["last_name"], "Value": [full_name[1].iloc[0]]}
            )
        else:
            last_name = pd.DataFrame({"Key": ["last_name"], "Value": [""]})

        # Split address into street and house_number
        address = df[df["Key"] == "adres"]["Value"].str.extract(r"^(.*\D)(\d*)")
        street = pd.DataFrame({"Key": ["street"], "Value": [address[0].iloc[0]]})
        house_number = pd.DataFrame(
            {"Key": ["house_number"], "Value": [address[1].iloc[0]]}
        )

        # Remove aggregates and concat parts
        df = df.drop(df[df["Key"] == "naam"].index)
        df = df.drop(df[df["Key"] == "adres"].index)
        df = pd.concat([df, first_name])
        df = pd.concat([df, last_name])
        df = pd.concat([df, street])
        df = pd.concat([df, house_number])

        # Get column labels from first column, values from second column
        df = df.transpose()
        df.columns = df.iloc[0]
        df = df.drop(df.index[0])

        df_all.append(df)

    df = pd.concat(df_all, ignore_index=True)
    df.rename(
        columns={
            "gsm": "phone_number",
            "e-mailadres": "email",
            "functie": "responsibilities",
            "studies/job": "education_occupation",
            "hobby's": "hobbies",
            "lievelingskleur": "fav_color",
            "favorietechiro-activiteit": "fav_activity",
            "favorietechirolied": "fav_song",
            "leukstekamp": "fav_camp",
            "lievelingsmuziek": "fav_music_genre",
            "lievelingsfilmof-boek": "fav_film_book",
            "aantaljarenindechiro": "years_active",
            "reedsleidinggeweestvan": "prev_groups",
            "verjaardag": "birth_date",
        },
        inplace=True,
    )

    # Transform birthday format from dd/mm/yyyy to yyyy-mm-dd
    df.loc[:, "birth_date"] = df.loc[:, "birth_date"].apply(transform_date)
    print(df)
    df.to_csv("output/output.csv")


def transform_date(date: str) -> str:
    day, month, year = date.split("/")
    return "{y}-{m}-{d}".format(y=year, m=month, d=day)


if __name__ == "__main__":
    main()
