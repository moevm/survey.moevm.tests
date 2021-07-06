from selenium.common.exceptions import NoSuchElementException


def find(func, *args):
    try:
        return func(*args)
    except NoSuchElementException:
        return None


class finish_page:
    def __init__(self, driver, season):
        self.url_match = "finish"
        self.season = season
        self.driver = driver
        self.site_path = "http://" + season + ".survey.moevm.info/"

    def get_final_text(self):
        tag = 'h3'
        find_func = self.driver.find_element_by_tag_name
        h3 = find(find_func, tag)
        if h3 is None:
            return None
        final_text = h3.text
        if final_text is None:
            return None
        else:
            return final_text

