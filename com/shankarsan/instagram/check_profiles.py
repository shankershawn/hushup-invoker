import sys
import time

import schedule
from retry import retry
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from com.shankarsan.repository.oracle import Connection

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

profiles = sys.argv[1].split(',')
token = sys.argv[2]


def persist_info(insta_driver):
    title = insta_driver.title
    element = insta_driver.find_element(By.XPATH,
                                        '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/'
                                        + 'section/main/div/header/section/ul/li[1]/button/span/span')
    connection = Connection.get_connection_from_pool(token)
    cursor1 = connection.cursor()
    cursor1.execute(statement='MERGE INTO t_instagram_post_counts_f target USING'

                              '( SELECT :profile_url profile_url FROM dual) source '
                              'ON ( target.profile_url = source.profile_url ) '
                              'WHEN MATCHED THEN UPDATE SET post_count = :post_count, profile_title = :profile_title, '
                              'updated_by = :updated_by, '
                              'update_date_time = cast(current_timestamp as timestamp) '
                              'where post_count <> :post_count or profile_title <> :profile_title '
                              'WHEN NOT MATCHED THEN '
                              'INSERT ( target.profile_url, target.profile_title, '
                              'target.post_count, target.created_by, target.updated_by ) '
                              'VALUES ( :profile_url, :profile_title, :post_count, :created_by, :updated_by )',
                    profile_url=insta_driver.current_url, profile_title=title,
                    post_count=int(element.text), updated_by='raspi_script', created_by='raspi_script')

    # print(f'{cursor1.rowcount} rows updated')
    connection.commit()
    # print(f'{title} has {element.text} posts')


@retry(NoSuchElementException, backoff=1.5, delay=1, tries=50)
def invoke_profile(profile, insta_driver):
    insta_driver.get(profile)
    persist_info(insta_driver)


def invoke_profiles():
    [invoke_profile(profile, driver) for profile in profiles]


schedule.every(20).minutes.do(invoke_profiles)
while 1:
    schedule.run_pending()
    time.sleep(1)
