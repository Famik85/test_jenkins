from web_ui.ui_methods.ui_methods import UIMethods
from settings.project_setting import PROJECT_HOST
from utils.tm_ai_methods import TMMethod

class TestHomePage:

    def test_click_dandruff_in_search_field_with_change_lang(self, page):
        url_en_wikipedia_search = "https://en.wikipedia.org/"
        h1_en_wikipedia_search = "Search"
        url_uk_wikipedia_search = "https://uk.wikipedia.org/"
        h1_uk_wikipedia_search = "Пошук"
        selected_language = "Українська"
        selected_language_icon = "uk"
        ui = UIMethods(page)
        ai = TMMethod()
        ui.general.open_url(PROJECT_HOST)
        ui.homepage.click_dandruff_in_search_field()
        ui.general.check_open_page_with_url_contains(url_en_wikipedia_search)
        ui.general.check_open_page_with_header(h1_en_wikipedia_search)
        ui.general.open_url(PROJECT_HOST)
        opened_list = ui.homepage.click_select_language_icon_in_search_field()
        ui.homepage.select_language_option_in_search_field(opened_list, selected_language)
        ui.homepage.check_icon_select_language(selected_language_icon)
        ui.homepage.click_dandruff_in_search_field()
        ui.general.check_open_page_with_url_contains(url_uk_wikipedia_search)
        ui.general.check_open_page_with_header(h1_uk_wikipedia_search)
        ai.check_content_by_lang(page, 'Ukrainian')

    def test_select_language_main_page(self, page):
        url_en_wikipedia_main_page = "https://en.wikipedia.org/wiki/Main_Page"
        h1_en_wikipedia_main_page = "Welcome to "
        selected_language = "English"
        ui = UIMethods(page)
        ui.general.open_url(PROJECT_HOST)
        ui.homepage.click_lang_under_text_the_free_encyclopedia(selected_language)
        ui.general.check_open_page_with_url_contains(url_en_wikipedia_main_page)
        ui.general.check_open_page_with_header(h1_en_wikipedia_main_page)
        ui.general.open_url(PROJECT_HOST)
        block = ui.homepage.click_button_read_wikipedia_in_your_language()
        ui.homepage.select_language_in_wikipedia_in_your_lang(block, selected_language)
        ui.general.check_open_page_with_url_contains(url_en_wikipedia_main_page)
        ui.general.check_open_page_with_header(h1_en_wikipedia_main_page)

    def test_read_wikipedia_in_your_language_and_click_other_language(self, page):
        url_list_of_wikipedias = "https://meta.wikimedia.org/wiki/List_of_Wikipedias"
        h1_list_of_wikipedias = "List of Wikipedias"
        btn_other_languages = "Other languages"
        ui = UIMethods(page)
        ui.general.open_url(PROJECT_HOST)
        block = ui.homepage.click_button_read_wikipedia_in_your_language()
        ui.homepage.select_language_in_wikipedia_in_your_lang(block, btn_other_languages)
        ui.general.check_open_page_with_url_contains(url_list_of_wikipedias)
        ui.general.check_open_page_with_header(h1_list_of_wikipedias)

    def test_pass_to_page_in_block_download_wikipedia_for_android_or_ios(self, page):
        url_google_play = "https://play.google.com/"
        url_app_store = "https://apps.apple.com/"
        url_list_of_wikipedia_mobile_apps = "https://en.wikipedia.org/wiki/List_of_Wikipedia_mobile_apps"
        h1_list_of_wikipedia_mobile_apps = "List of Wikipedia mobile apps"
        ui = UIMethods(page)
        ui.general.open_url(PROJECT_HOST)
        new_page = ui.homepage.click_mobile_app_icon('android')
        ui = UIMethods(new_page)
        ui.general.check_open_page_with_url_contains(url_google_play)
        ui = UIMethods(page)
        new_page = ui.homepage.click_mobile_app_icon('ios')
        ui = UIMethods(new_page)
        ui.general.check_open_page_with_url_contains(url_app_store)
        ui = UIMethods(page)
        ui.homepage.click_button_download_wikipedia_for_android_or_ios()
        ui.general.check_open_page_with_url_contains(url_list_of_wikipedia_mobile_apps)
        ui.general.check_open_page_with_header(h1_list_of_wikipedia_mobile_apps)

    def test_pass_to_page_by_source_links(self, page):
        sources_dict = {
            'Commons': ('https://commons.wikimedia.org/wiki/Main_Page', 'Commons'),
            'Wikibooks': ('https://www.wikibooks.org/', 'Wikibooks'),
            'Wikiversity': ('https://www.wikiversity.org/', 'Wikiversity'),
            'Wikisource': ('https://wikisource.org/wiki/Wikisource:Main_Page', 'Wikisource'),
            'Meta-Wiki': ('https://meta.wikimedia.org/wiki/Main_Page', 'Meta-Wiki'),
            'Wikivoyage': ('https://www.wikivoyage.org/', 'Wikivoyage'),
            'Wikiquote': ('https://www.wikiquote.org/', 'Wikiquote'),
            'Wikispecies': ('https://species.wikimedia.org/wiki/Main_Page', 'Wikispecies'),
            'Wiktionary': ('https://www.wiktionary.org/', 'Wiktionary'),
            'Wikidata': ('https://www.wikidata.org/wiki/Wikidata:Main_Page', 'Wikidata'),
            'MediaWiki': ('https://www.mediawiki.org/wiki/MediaWiki', 'MediaWiki'),
            'Wikifunctions': ('https://www.wikifunctions.org/wiki/Wikifunctions:Main_Page',
                              'Wikifunctions')}
        ui = UIMethods(page)
        for source, (url, header) in sources_dict.items():
            ui.general.open_url(PROJECT_HOST)
            ui.homepage.click_button_other_projects(source)
            ui.general.check_open_page_with_url_contains(url)
            ui.general.check_open_page_with_text(header)
