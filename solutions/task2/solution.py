from selenium import webdriver as wd
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import fake_useragent
import csv


# CYRILLIC = {chr(i): 0 for i in range(1040, 1072) if chr(i) not in ("Ъ", "Ь", "Й", "Ы")}
CYRILLIC = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П',
            'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']


class WikiParser:
    """класс для подсчета животных по именам"""
    def __init__(self, url: str = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"):
        svc = wd.ChromeService(executable_path=binary_path)
        options = wd.ChromeOptions()
        user = fake_useragent.UserAgent().random
        options.add_argument(f"user-agent={user}")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.brawser = wd.Chrome(service=svc, options=options)
        self.brawser.get(url=url)

        self.counter_cyrillic = {i: 0 for i in CYRILLIC}

    def manager(self, names_animals: list[str]):
        """
            Разбирает список животных и ведет подсчет в атрибут
            1. если в имени 1 буква - это оглавление
            2. если имя не начинается с латиницы - подсчет окончен
        """
        for animal in names_animals:
            # 1
            if len(animal) == 1:
                continue
            # 2
            if animal[0].upper() not in CYRILLIC:
                return True
            self.counter_cyrillic[animal[0].upper()] += 1

    def parse(self):
        """
            1. Забирает со страницы элемент с животными
            2. Переходит на следующую
        """
        while True:
            # 1
            table = WebDriverWait(self.brawser, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mw-category.mw-category-columns"))
            )
            animals = table.text.split("\n")

            flag = self.manager(animals)
            if flag:
                break

            # 2
            next_page = self.brawser.find_element(By.LINK_TEXT, "Следующая страница")
            next_page.click()

        return self.counter_cyrillic


def writer_csv(animals: dict[str, int]):
    # Запись в CSV файл
    with open('beasts.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['start_name', 'count'])  # Заголовки столбцов
        for key, value in animals.items():
            writer.writerow([key, value])


if __name__ == "__main__":

    parser = WikiParser()
    animals = parser.parse()

    writer_csv(animals)

