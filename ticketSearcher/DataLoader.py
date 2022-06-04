import json
import urllib.request
from urllib.error import URLError


class DataLoader:
    def __init__(self):
        self.link_form = (
            "https://api.rasp.yandex.net/v3.0/search/?apikey={api_key}" +
            "&format=json" +
            "&from={from_code}" +
            "&to={to_code}" +
            "&lang=ru_RU" +
            "&date={date}" +
            "&transport_types=plane" +
            "&system=iata"
        )

    def load(self, api_key, from_code, to_code, date):
        """Загрузка данных о рейсах"""

        link = self.link_form.format(
            api_key=api_key,
            from_code=from_code,
            to_code=to_code,
            date=date
        )

        try:
            with urllib.request.urlopen(link) as page:
                response = json.loads(page.read().decode('utf-8'))
        except URLError as error:
            print(error)
            return

        return response['segments']

