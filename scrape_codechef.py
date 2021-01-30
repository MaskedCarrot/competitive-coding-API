import re
import requests
from bs4 import BeautifulSoup
import json
from constants import *


class CodechefUserData:

    def __init__(self, username=None):
        self.__username = username
        url = CODECHEF_URL + self.__username
        self.__page = requests.get(url)
        self.__soup = BeautifulSoup(self.__page.text, 'html.parser')

    def get_basic_details(self):
        '''function to get basic user details'''

        soup = self.__soup

        result = {'status': STATE_PENDING}

        try:
            rating = soup.find('div', class_='rating-number').text

            stars = soup.find('span', class_='rating').text

            highest_rating_container = soup.find('div', class_='rating-header')
            highest_rating = highest_rating_container.find_next(
                'small').text.split()[-1].rstrip(')')

            rating_ranks_container = soup.find('div', class_='rating-ranks')
            rating_ranks = rating_ranks_container.find_all('a')

            global_rank = rating_ranks[0].strong.text
            country_rank = rating_ranks[1].strong.text

            rating_table = soup.find('table', class_='rating-table')

            rating_table_rows = rating_table.find_all('td')

            try:
                long_challenge = {'rating': int(rating_table_rows[1].text),
                                  'global_rank': int(rating_table_rows[2].a.hx.text),
                                  'country_rank': int(rating_table_rows[3].a.hx.text)}

            except ValueError:
                long_challenge = {'rating': int(rating_table_rows[1].text),
                                  'global_rank': rating_table_rows[2].a.hx.text,
                                  'country_rank': rating_table_rows[3].a.hx.text}

            try:
                cook_off = {'rating': int(rating_table_rows[5].text),
                            'global_rank': int(rating_table_rows[6].a.hx.text),
                            'country_rank': int(rating_table_rows[7].a.hx.text)}
            except ValueError:
                cook_off = {'rating': int(rating_table_rows[5].text),
                            'global_rank': rating_table_rows[6].a.hx.text,
                            'country_rank': rating_table_rows[7].a.hx.text}

            try:
                lunch_time = {'rating': int(rating_table_rows[9].text),
                              'global_rank': int(rating_table_rows[10].a.hx.text),
                              'country_rank': int(rating_table_rows[11].a.hx.text)}

            except ValueError:
                lunch_time = {'rating': int(rating_table_rows[9].text),
                              'global_rank': rating_table_rows[10].a.hx.text,
                              'country_rank': rating_table_rows[11].a.hx.text}

            problem_solved_section = soup.find(
                'section', class_='rating-data-section problems-solved')

            no_solved = problem_solved_section.find_all('h5')

            fully_solved = re.findall('\d+', no_solved[0].text)[0]

            partially_solved = re.findall(
                '\d+', no_solved[1].text)[0]

            result['status'] = STATE_PASS

            result['username'] = self.__username

            result['long_challenge'] = long_challenge
            result['cook_off'] = cook_off
            result['lunch_time'] = lunch_time

            result['fully_solved'] = int(fully_solved)
            result['partially_solved'] = int(partially_solved)

            result['stars'] = stars
            result['rating'] = int(rating)
            result['highest_rating'] = int(highest_rating)
            result['country_rank'] = int(country_rank)
            result['global_rank'] = int(global_rank)

        except:
            result = {'status':  STATE_ERROR_INVALID_USER}
        finally:
            return result

    def get_contests_details(self):
        '''function to get contests details in which user participated.'''

        page = self.__page
        soup = self.__soup

        result = {'status': STATE_PENDING}

        try:
            start_ind = page.text.find('[', page.text.find('all_rating'))
            end_ind = page.text.find(']', start_ind) + 1

            next_opening_brack = page.text.find('[', start_ind+1)
            while next_opening_brack < end_ind:
                end_ind = page.text.find(']', end_ind+1) + 1
                next_opening_brack = page.text.find('[', next_opening_brack+1)

            all_rating = json.loads(page.text[start_ind: end_ind])
            for rating_contest in all_rating:
                rating_contest.pop('color')

            problem_solved_section = soup.find(
                'section', class_='rating-data-section problems-solved')

            no_solved = problem_solved_section.find_all('h5')

            categories = problem_solved_section.find_all('article')

            fully_solved = {'count': re.findall('\d+', no_solved[0].text)[0]}
            for category in categories[0].find_all('p'):
                category_name = category.find('strong').text[:-1]
                fully_solved[category_name] = []

                for prob in category.find_all('a'):
                    fully_solved[category_name].append({'name': prob.text,
                                                        'link': 'https://www.codechef.com' + prob['href']})

            partially_solved = {'count': re.findall(
                '\d+', no_solved[1].text)[0]}
            for category in categories[1].find_all('p'):
                category_name = category.find('strong').text[:-1]
                partially_solved[category_name] = []

                for prob in category.find_all('a'):
                    partially_solved[category_name].append({'name': prob.text,
                                                            'link': 'https://www.codechef.com' + prob['href']})

            result['status'] = STATE_PASS

            result['username'] = self.__username

            result['all_rating'] = all_rating
            result['fully_solved'] = fully_solved
            result['partially_solved'] = partially_solved

        except:
            result = {'status': STATE_ERROR_INVALID_USER}
        finally:
            return result

    def get_personal_details(self):
        '''function to get personal details of user'''

        soup = self.__soup

        result = {'status': STATE_PENDING}

        try:
            header_containers = soup.find_all('header')
            name = header_containers[1].find('h2').text

            user_details_section = soup.find('section', class_='user-details')
            user_details_list = user_details_section.find_all('li')

            result['status'] = STATE_PASS
            result['name'] = name
            result['username'] = self.__username
            result['country'] = user_details_list[1].text.split(
                ':')[-1].strip()
            result['state'] = user_details_list[2].text.split(':')[-1].strip()
            result['city'] = user_details_list[3].text.split(':')[-1].strip()
            result['identity'] = user_details_list[4].text.split(
                ':')[-1].strip()
            result['organization'] = user_details_list[5].text.split(
                ':')[-1].strip()

        except:
            result = {'status': STATE_ERROR_INVALID_USER}

        finally:
            return result


def get_friends_details_basic(array_of_friends):
    '''get basic details of all friends of a user'''

    result = {'status': STATE_PENDING}
    try:
        for friend in array_of_friends:
            friends_details = CodechefUserData(friend)
            result[friend] = friends_details.get_basic_details()
    except:
        result = {'state': STATE_ERROR_IN_CODECHEF_FRIENDS}
    finally:
        return result


if __name__ == '__main__':
    ans = get_friends_details_basic(['maskedcarrot'])
    print(ans)
