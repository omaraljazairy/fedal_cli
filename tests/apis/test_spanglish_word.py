from fedal_cli.apis.spanglish import word
from fedal_cli.services.logger import get_logger
from fedal_cli.services.requester import make_request
from click.testing import CliRunner
from unittest import TestCase
import random

logger = get_logger(loggername='spanglish')


class TestSpanglishWord(TestCase):


    def setUp(self):
        """ runs before any test """

        logger.debug("setUp")

        self.random_number = random.randint(1,101)
        logger.debug("random_number generated: %s", self.random_number)
        word = 'test'.__add__(str(self.random_number))
        word_en = 'test_en_'.__add__(str(self.random_number))
        category = 'Entertainment'
        language = 'EN'
        
        params = {
            'word': word,
            'word_en': word_en,
            'category': category,
            'language': language,
        }

        api = ('spanglish', 'word')

        response = make_request(api=api, action='POST', **params)
        status_code = response.status_code
            
        if status_code == 201:
            content = response.json()
            self.word_id = content['id']

            logger.debug("word_id created: %d", self.word_id)

        else:
            content = response.text
            self.word_id = 1
            

        logger.debug("response status_code: %s", status_code)
        logger.debug("word response content: %s", content)



    def test_word_dict(self):
        """ test if the word module has a funcs dict with 5 objects """

        word_funcs = getattr(word, 'funcs')
        logger.debug("word funcs are: {}".format(word_funcs))

        self.assertEqual(type(word_funcs), dict)
        self.assertTrue(len(word_funcs), 5)


    def test_get_words(self):
        """ making a call to the get_words will exit successfully with code 0 """

        get_words = getattr(word, 'get_words')
        runner = CliRunner()
        result = runner.invoke(get_words, [])

        logger.debug("result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)



    def test_get_word(self):
        """ pass the word_id as an argument and gets the word details. it will exit with code 0 """

        get_word = getattr(word, 'get_word')

        runner = CliRunner()
        result = runner.invoke(get_word, ['--word_id', self.word_id])

        logger.debug("result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)
        


    def test_add_word(self):
        """ 
        provide all the parameters required to create a word and expect the script
        to exit with code 0.
        """

        add_word = getattr(word, 'add_word')

        random_number = random.randint(100,999)
        logger.debug("random_number generated: %s", random_number)

        word_es = 'test'.__add__(str(random_number))
        word_en = 'test_en_'.__add__(str(random_number))
        category = 'Entertainment'
        language = 'EN'

        runner = CliRunner()
        result = runner.invoke(add_word, ['--word', word_es, '--word_en', word_en, '--category', category, '--language', language])

        logger.debug("result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)
        
        

    def test_update_word(self):
        """ try to update the word_en and expect to exit with code 0 """

        update_word = getattr(word, 'update_word')

        logger.debug("word_id generated for this test: {}".format(self.word_id))
        
        runner = CliRunner()
        result = runner.invoke(update_word, ['--word_id', int(self.word_id), '--word', 'blbl', '--word_en', 'bmbm', '--category', 'Greeting', '--language', 'EN'])

        logger.debug("update result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)
        

    def test_delete_word(self):
        """ try to delete the word with id 1 and expect to exit with code 0 """

        delete_word = getattr(word, 'delete_word')

        runner = CliRunner()
        result = runner.invoke(delete_word, ['--word_id', str(self.word_id)])

        logger.debug("delete result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)

        
    def tearDown(self):
        """ runs after every test """

        logger.debug("tearDown")
        args_params = (str(self.word_id),)
        api = ('spanglish', 'word')
        response = make_request(*args_params, api=api, action='DELETE', **{})
        status_code = response.status_code
        logger.debug("response status_code: %s", status_code)

