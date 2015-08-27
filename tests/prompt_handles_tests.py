__author__ = 'ioparaskev'

from unittest import TestCase, mock
import prompt_handles


def mock_input(func):
        def mock_input_builtin(*args):
            with mock.patch('builtins.input', return_value=args[-1]):
                return func(*args)
        return mock_input_builtin
        # return mock.patch('builtins.input', return_value=answer)


class TestPromptWrapper(TestCase):
    def setUp(self):
        question = 'Test ?'
        self.prompt = prompt_handles.PromptWrapper(question)

    @mock_input
    def get_mocked_answer(self, mocked_ans):
        return self.prompt.get_prompt_answer()

    def test_get_prompt_answer_anything(self):
        answer = self.get_mocked_answer('1')
        self.assertEqual('1', answer)

    def test_get_prompt_answer_only_nums_wrong_aswer(self):
        self.prompt.set_restrictions(answer_restrictions='num')
        answer = self.get_mocked_answer('tt')
        self.assertEqual(None, answer)

    def test_get_prompt_answer_only_nums_correct_aswer(self):
        self.prompt.set_restrictions(answer_restrictions='num')
        answer = self.get_mocked_answer('123')
        self.assertEqual('123', answer)

    def test_get_prompt_answer_only_alpha_wrong_aswer(self):
        self.prompt.set_restrictions(answer_restrictions='alpha')
        answer = self.get_mocked_answer('12asd')
        self.assertEqual(None, answer)

    def test_get_prompt_answer_only_alpha_correct_aswer(self):
        self.prompt.set_restrictions(answer_restrictions='alpha')
        answer = self.get_mocked_answer('asd')
        self.assertEqual('asd', answer)

    def test_get_prompt_answer_only_alphanumeric_wrong_aswer(self):
        self.prompt.set_restrictions(answer_restrictions='alphanum')
        answer = self.get_mocked_answer('12asd_')
        self.assertEqual(None, answer)

    def test_get_prompt_answer_only_alphanum_correct_aswer(self):
        self.prompt.set_restrictions(answer_restrictions='alphanum')
        answer = self.get_mocked_answer('asd123')
        self.assertEqual('asd123', answer)

