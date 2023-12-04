import pandas as pd
import numpy as np
import os


def filter_locations_into_countries(locations):
    """Practical, but not ideal solution; the data is a total mess, random ',' not corresponding to the given structure in https://clinicaltrials.gov/data-about-studies/csv-download"""
    countries = set()
    for location in locations.split("|"):
        detail_loc = location.split(",")

        first_el = detail_loc[-2].strip()
        second_el = detail_loc[-1].strip()

        country_pair_to_check_both = f"{first_el},{second_el}"

        countries.add(country_pair_to_check_both)

    return "|".join(countries)


class StudiesFilter:
    def __init__(
        self,
        df: pd.DataFrame,
        min_phase=2,
        is_filter_countries=True,
        forbidden_countries_filepath="resources/asian_countries.txt",
    ) -> None:
        self.df = df
        self.min_phase = min_phase
        self.is_filter_countries = is_filter_countries
        self.forbidden_countries_filepath = forbidden_countries_filepath

    def _filter_nan_or_empty(self):
        self.df = self.df.replace(r"^\s*$", np.nan, regex=True)
        self.df = self.df.dropna()

    def _filter_phases(self):
        """We take at least 2nd phase (due to recruitment)"""
        self.df["phases"] = self.df["phases"].astype(str)
        condition = self.df["phases"].str[-1].astype(int) >= 2
        self.df = self.df[condition]

    def _filter_drugs(self):
        """We take drugs only"""
        self.df["interventions"] = self.df["interventions"].astype(str)
        self.df["interventions"] = self.df["interventions"].str.split("|")
        self.df["interventions"] = self.df["interventions"].apply(
            lambda row: [
                intervention.split("DRUG: ", maxsplit=1)[1]
                for intervention in row
                if intervention.startswith("DRUG: ")
            ]
        )
        self.df["interventions"] = self.df["interventions"].apply(
            lambda row: "|".join([intervention for intervention in row])
        )

        self.df = self.df.rename(columns={"interventions": "drugs"})

    def _filter_records_based_on_countries(self, forbidden_countries: list):
        """Because of the messy data in locations, which we remove if all match any of forbidden countries list,
        we need to check if any element of comma separated variable created above is any country in there.
        """
        indices_to_drop = list()
        for index, row in self.df.iterrows():
            if all(
                any(
                    country_to_check in forbidden_countries
                    for country_to_check in country_pair_to_check_both.split(",")
                )
                for country_pair_to_check_both in row["countries_pair_to_check"].split(
                    "|"
                )
            ):
                indices_to_drop.append(index)

        self.df = self.df.drop(indices_to_drop)

    def _filter_countries(self):
        """When all countries in a record are from the given list then the record is removed"""
        base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
        full_path = os.path.join(base_dir, self.forbidden_countries_filepath)
        self.df["locations"] = self.df["locations"].astype(str)

        with open(full_path, "r") as forbidden_countries_file:
            forbidden_countries = forbidden_countries_file.read().splitlines()
            self.df["countries_pair_to_check"] = self.df["locations"].apply(
                filter_locations_into_countries
            )

            self.df["countries_pair_to_check"] = self.df[
                "countries_pair_to_check"
            ].astype(str)

            self._filter_records_based_on_countries(forbidden_countries)

    def filter_df(self):
        self._filter_nan_or_empty()
        self._filter_phases()
        self._filter_drugs()
        if self.is_filter_countries:
            self._filter_countries()
        return self.df
