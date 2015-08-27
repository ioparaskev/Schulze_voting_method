__author__ = 'ioparaskev'
import re


class Response(object):
    def __init__(self):
        self.p_ans = tuple()
        self.csens = True
        self.ans_restrict = None
        self.regx = False
        self.str_restriction = lambda x: False

    def set_restrictions(self, case_sensitive=True, possible_answers=tuple(),
                         answer_restrictions=None):
        self.case_sensitive = case_sensitive
        self.possible_answers = possible_answers
        self.answer_restriction = answer_restrictions

    @property
    def case_sensitive(self):
        return self.csens

    @case_sensitive.setter
    def case_sensitive(self, val):
        if val not in (True, False):
            raise ValueError('Only bool values allowed for case sensitive set!')
        self.csens = val

    @property
    def possible_answers(self):
        return self.p_ans

    @possible_answers.setter
    def possible_answers(self, val):
        self.p_ans = val

    @property
    def answer_restriction(self):
        return self.ans_restrict

    @answer_restriction.setter
    def answer_restriction(self, val):
        usual_restrictions = dict(alpha=lambda x: x.isalpha(),
                                  num=lambda x: x.isnumeric(),
                                  alphanum=lambda x: x.isalnum())
        if val in usual_restrictions.keys():
            self.restrictions_match_possible_answers(restriction=usual_restrictions[val])
            self.str_restriction = usual_restrictions[val]
        elif self.is_regex(val):
            self.restrictions_match_possible_answers(regex=val.strip("regex:"))
            self.regx = True
        else:
            raise NotImplementedError('Wrong restriction given\n'
                                      'Use --help to see possible restrictions')

        self.ans_restrict = val

    def is_regex(self, regex_keyword):
        starts_with_keyword = regex_keyword.find("regex:")
        if starts_with_keyword == -1:
            return False
        elif starts_with_keyword > 0:
            raise RuntimeError("To enter a regex you should enter "
                               "'regex:'[regex_expression]")
        return True

    def restrictions_match_possible_answers(self, restriction=None, regex=None):
        err = RuntimeError('Possible answers given do not match restriction')
        if restriction:
            for answer in self.possible_answers:
                if not restriction(answer):
                    raise err
        elif regex:
            pass

    def get_prompt_response(self, question):
        answer = None
        for x in range(3):
            ans = input(question)
            if self.match_restrictions(ans):
                answer = ans
                break

        if not answer:
            raise RuntimeError('Wrong answer given 3 times\nExiting')
        else:
            return answer

    def match_restrictions(self, answer):
        if self.possible_answers:
            if answer not in self.possible_answers:
                return False
            else:
                return True

        if self.answer_restriction:
            if not self.str_restriction(answer):
                return False
            else:
                return True

        return True


class PromptWrapper(object):
    def __init__(self, question, case_sensitive=True, accepted_answers=tuple(),
                 answer_type_restriction=None):
        self.question = question
        self.case_sensitive = case_sensitive
        self.accepted_answers = accepted_answers
        self.answer_type_restriction = answer_type_restriction
        self.response = Response()

    def set_restrictions(self, case_sensitive=True, possible_answers=tuple(),
                         answer_restrictions=None):
        self.response.set_restrictions(case_sensitive, possible_answers,
                                       answer_restrictions)

    def get_prompt_answer(self):
        answer = None
        try:
            answer = self.response.get_prompt_response(self.question)
        except RuntimeError as error:
            print(error)
        finally:
            return answer