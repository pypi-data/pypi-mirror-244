from cwsapiwrapper.helpers import fetch_response

BASE_URI = 'https://conworkshop.com/api'


class API:
    class Language:
        @staticmethod
        def get_lang(code):
            """
            Returns a dictionary of language attributes
            :param code:
            :return:
            """
            response = fetch_response(f'{BASE_URI}/LANG/{code}')['out']
            if response:
                attributes = {
                    'code': response['CODE'],
                    'name': response['NAME'],
                    'native_name': response['NATIVE_NAME'],
                    'ipa': response['IPA'],
                    'lang_type': (response['TYPE']),
                    'owners': response['OWNERS'],
                    'overview': response['OVERVIEW'],
                    'public': response['PUBLIC'],
                    'status': response['STATUS'],
                    'registered': response['REGISTERED'],
                    'word_count': response['WORD_COUNT'],
                    'karma': response['KARMA']
                }
                return attributes
            else:
                return None

        def get_lang_name(self, code):
            """
            Returns the name of a language
            :param code:
            :return:
            """
            return self.get_lang(code)['name']

        def get_lang_native_name(self, code):
            """
            Returns the native name of a language
            :param code:
            :return:
            """
            return self.get_lang(code)['native_name']

        def get_lang_ipa(self, code):
            """
            Returns the IPA of a language
            :param code:
            :return:
            """
            return self.get_lang(code)['ipa']

        def get_lang_type(self, code):
            """
            Returns the type of language
            :param code:
            :return:
            """
            return self.get_lang(code)['lang_type']

        def get_lang_owners(self, code):
            """
            Returns the owners of a language
            :param code:
            :return:
            """
            return self.get_lang(code)['owners']

        def get_lang_overview(self, code):
            """
            Returns the overview of a language
            :param code:
            :return:
            """
            return self.get_lang(code)['overview']

        def get_lang_public(self, code):
            """
            Returns the public status of a language
            :param code:
            :return:
            """
            return self.get_lang(code)['public']

        def get_lang_status(self, code):
            """
            Returns the status of a language
            :param code:
            :return:
            """
            status_types = {
                '1': 'New',
                '2': 'Progressing',
                '3': 'Completed',
                '4': 'Functional'
            }
            return status_types[self.get_lang(code)['status']]

        def get_lang_registered(self, code):
            """
            Returns the registered date of a language
            :param code:
            :return:
            """
            return self.get_lang(code)['registered']

        def get_lang_word_count(self, code):
            """
            Returns the word count of a language
            :param code:
            :return:
            """
            return self.get_lang(code)['word_count']

        def get_lang_karma(self, code):
            """
            Returns the karma of a language
            :param code:
            :return:
            """
            return self.get_lang(code)['karma']

    class User:
        @staticmethod
        def get_user(cws_id):
            """
            Returns a dictionary of user attributes
            :param cws_id:
            :return:
            """
            response = fetch_response(f'{BASE_URI}/USER/{cws_id}')['out']
            if response:
                attributes = {
                    'uid': response['USER_ID'],
                    'name': response['USER_NAME'],
                    'gender': response['USER_GENDER'],
                    'bio': response['USER_BIO'],
                    'country': response['USER_COUNTRY'],
                    'karma': response['KARMA'],
                }
                return attributes
            else:
                return None

        def get_user_name(self, cws_id):
            """
            Returns the name of a user
            :param cws_id:
            :return:
            """
            return self.get_user(cws_id)['name']

        def get_user_gender(self, cws_id):
            """
            Returns the gender of a user
            :param cws_id:
            :return:
            """
            return self.get_user(cws_id)['gender']

        def get_user_bio(self, cws_id):
            """
            Returns the bio content of a user
            :param cws_id:
            :return:
            """
            return self.get_user(cws_id)['gender']

        def get_user_country(self, cws_id):
            """
            Returns the country of a user
            :param cws_id:
            :return:
            """
            return self.get_user(cws_id)['gender']

        def get_user_karma(self, cws_id):
            """
            Returns the karma of a user
            :param cws_id:
            :return:
            """
            return self.get_user(cws_id)['karma']
