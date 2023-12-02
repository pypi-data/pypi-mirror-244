from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from .errors import InvalidCredentialsError


class _Token:
    @staticmethod
    def obtain(login, password) -> str:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)

        wait = WebDriverWait(driver, 4)
        driver.get("https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Ddnevnik.mos.ru%26scope%3Dopenid%2Bprofile%2Bbirthday%2Bcontacts%2Bsnils%2Bblitz_user_rights%2Bblitz_change_password%26redirect_uri%3Dhttps%253A%252F%252Fschool.mos.ru%252Fv3%252Fauth%252Fsudir%252Fcallback%26state%3D")

        login_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login')))
        login_input.send_keys(login)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#password'))).send_keys(password)

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#bind'))).click()
        try:
            # костыль от нестабильности работы сайта
            wait.until(EC.staleness_of(login_input))
            token = wait.until(lambda x: x.get_cookie('aupd_token'))
        except TimeoutException:
            driver.close()
            raise InvalidCredentialsError

        driver.close()
        return token["value"]
