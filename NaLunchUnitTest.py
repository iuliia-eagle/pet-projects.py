from selenium import webdriver
import unittest

#Проверка того, что ссылка на сайт заведения была нажата успешно и страница заведения была загружена
def test_url(url: str):
    chromedriver_path = r"C:\Python38\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(url)
    assert driver.find_element_by_link_text('Сайт заведения')
    driver.find_element_by_link_text('Сайт заведения').click()
    assert "Problem loading page" not in driver.title

test_url("https://www.nalunch.ru/WhereTo/Place/611")

