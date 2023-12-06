import requests
from bs4 import BeautifulSoup
import re

class FormulaOneParser:
    def __init__(self):
        self.base_url = "https://www.formula1.com/en/results.html/"

    def parse_drivers_data(self, year):
        url = f"{self.base_url}{year}/drivers.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser")

        drivers_data = []
        for table in soup.find_all('table', class_='resultsarchive-table'):
            for row in table.find_all('tr')[1:]:
                driver_info = self._extract_driver_info(row)
                drivers_data.append(driver_info)

        return drivers_data

    def parse_races_data(self, year):
        url = f"{self.base_url}{year}/races.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser")

        races_data = []
        for table in soup.find_all('table', class_='resultsarchive-table'):
            for row in table.find_all('tr')[1:]:
                race_info = self._extract_race_info(row)
                races_data.append(race_info)

        return races_data

    def parse_teams_data(self, year):
        url = f"{self.base_url}{year}/team.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser")

        teams_data = []
        for table in soup.find_all('table', class_='resultsarchive-table'):
            for row in table.find_all('tr')[1:]:
                team_info = self._extract_team_info(row)
                teams_data.append(team_info)

        return teams_data

    def parse_fastest_laps_data(self, year):
        url = f"{self.base_url}{year}/fastest-laps.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser")

        fastest_laps_data = []
        for table in soup.find_all('table', class_='resultsarchive-table'):
            for row in table.find_all('tr')[1:]:
                fastest_lap_info = self._extract_fastest_lap_info(row)
                fastest_laps_data.append(fastest_lap_info)

        return fastest_laps_data

    def _extract_driver_info(self, row):
        position = re.findall(r'<td class="dark">(.*?)</td>', str(row))[0].strip()
        driver_name = re.findall(r'<span class="hide-for-tablet">(.*?)</span>', str(row))[0]
        driver_surname = re.findall(r'<span class="hide-for-mobile">(.*?)</span>', str(row))[0].strip()
        nationality = re.findall(r'<td class="dark semi-bold uppercase">(.*?)</td>', str(row))[0].strip()
        car = re.findall(r'.html">(.*?)</a>', str(row))[0].strip()
        points = re.findall(r'<td class="dark bold">(.*?)</td>', str(row))[0].strip()

        driver_info = {
            "position": position,
            "name": f"{driver_name} {driver_surname}",
            "nationality": nationality,
            "car": car,
            "points": points
        }

        return driver_info

    def _extract_race_info(self, row):
        grandprix = re.findall(r'html">\n {24}(.*?)\n {20}</a>', str(row))[0].strip()
        date = re.findall(r'<td class="dark hide-for-mobile">(.*?)</td>', str(row))[0]
        winner_name = re.findall(r'<span class="hide-for-tablet">(.*?)</span>', str(row))[0]
        winner_surname = re.findall(r'<span class="hide-for-mobile">(.*?)</span>', str(row))[0].strip()
        car = re.findall(r'<td class="semi-bold uppercase">(.*?)</td>', str(row))[0].strip()
        laps = re.findall(r'<td class="bold hide-for-mobile">(.*?)</td>', str(row))[0].strip()

        race_info = {
            "grandprix": grandprix,
            "date": date,
            "winner": f"{winner_name} {winner_surname}",
            "car": car,
            "laps": laps
        }

        return race_info

    def _extract_team_info(self, row):
        position = re.findall(r'<td class="dark">(.*?)</td>', str(row))[0].strip()
        team = re.findall(r'.html">(.*?)</a>\n</td>\n', str(row))[0].strip()
        points = re.findall(r'<td class="dark bold">(.*?)</td>', str(row))[0].strip()

        team_info = {
            "position": position,
            "team": team,
            "points": points
        }

        return team_info

    def _extract_fastest_lap_info(self, row):
        grandprix = re.findall(r'<td class="width30 dark">(.*?)</td>', str(row))[0]
        driver_surname = re.findall(r'<span class="hide-for-mobile">(.*?)</span>', str(row))[0]
        team = re.findall(r'<td class="width25 semi-bold uppercase">(.*?)</td>', str(row))[0].strip()
        lap_time = re.findall(r'<td class="dark bold">(.*?)</td>', str(row))[0]

        fastest_lap_info = {
            "grandprix": grandprix,
            "driver": f"{driver_surname}",
            "team": team,
            "lap_time": lap_time
        }

        return fastest_lap_info


if __name__ == "__main__":
    parser = FormulaOneParser()

    drivers_data = parser.parse_drivers_data(2023)

    print(drivers_data)
