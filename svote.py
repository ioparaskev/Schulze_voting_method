__author__ = 'ioparaskev'

from collections import OrderedDict
from prompt_handles import PromptWrapper


class Voter(object):
    def __init__(self, name):
        self.__name = name
        self.preference = None

    def set_preference(self, pref):
        self.preference = pref

    @property
    def name(self):
        return self.__name


class SchulzeVoter(Voter):
    def __init__(self, name, preferences):
        super(SchulzeVoter, self).__init__(name)
        self.preferences = preferences
        self.preferences_ranked = {preference: len(self.preferences)
                                   for preference in self.preferences}

    def set_rank(self, pref, rank):
        if rank > len(self.preferences) or rank < 1:
            rank = len(self.preferences)
        self.preferences_ranked[pref] = rank
        # self.update_preference_order()

    def update_preference_order(self):
        self.preferences_ranked = OrderedDict(
            sorted(self.preferences_ranked.items(),
                   key=lambda t: t[1]))

    def get_ranked_preferences(self):
        return self.preferences_ranked.keys()

    def get_rank_for_preference(self, preference):
        try:
            return self.preferences_ranked[preference]
        except ValueError:
            return len(self.preferences)


class SchulzeVoting(object):
    def __init__(self, candidates, voters):
        self.candidates = candidates
        self.voters = self.create_voters(voters)
        self.candidate_prompts = dict()
        self.prefs = None
        self.preference_matrix = None
        self.pairwise_dict = None

    def create_voters(self, names):
        voters = []
        for name in names:
            voters.append(SchulzeVoter(name, self.candidates))
        return tuple(voters)

    def create_prompts(self):
        candidate_prompts = dict()
        for candidate in self.candidates:
            question = self.set_question(candidate)
            vote_prompt = PromptWrapper(question, answer_type_restriction='num')
            candidate_prompts[candidate] = vote_prompt
        self.candidate_prompts = candidate_prompts

    def set_question(self, candidate):
        max_rank = len(self.candidates) - 1
        return 'Enter a rank between 1 - {max_rank} for {cand}\n' \
               'Enter 0 to declare indifference\n' \
               'Rank: '.format(max_rank=max_rank, cand=candidate)

    def run_voting(self):
        voters = self.voters[:]
        for voter in voters:
            print('Time for {0} to vote...'.format(voter.name))
            for candidate, vote_prompt in self.candidate_prompts.items():
                pref = vote_prompt.get_prompt_answer()
                voter.set_rank(candidate, pref)

        self.voters = tuple(voters)

    def voter_vote_pair_sequence(self, pair, voter):
        first_candidate = pair.split(':')[0]
        second_candidate = pair.split(':')[1]
        return voter.get_rank_for_preference(
            first_candidate) < voter.get_rank_for_preference(second_candidate)

    def get_voters_for_pair(self, pair):
        voters = 0
        for voter in self.voters:
            if self.voter_vote_pair_sequence(pair, voter):
                voters += 1
        return voters

    def craft_pair(self, first_candidate, second_candidate):
        return '{0}:{1}'.format(first_candidate, second_candidate)

    def set_pairwise_preference_matrix(self):
        pairwise_dict = dict()
        for cand in self.candidates:
            pairwise_dict[cand] = dict()
            pairwise_dict[cand][cand] = 0
            for cand2 in (x for x in self.candidates if x != cand):
                pair = self.craft_pair(cand, cand2)
                pairwise_dict[cand][cand2] = self.get_voters_for_pair(pair)

        self.pairwise_dict = pairwise_dict

    def set_strongest_paths(self):
        strongest = dict(self.pairwise_dict)
        for cand in self.pairwise_dict.keys():
            strongest[cand] = dict()
            for cand2 in (x for x in self.pairwise_dict.keys() if x != cand):
                if self.pairwise_dict[cand][cand2] > self.pairwise_dict[cand2][cand]:
                    strongest[cand][cand2] = self.pairwise_dict[cand][cand2]
                else:
                    strongest[cand][cand2] = 0

        for cand in self.pairwise_dict.keys():
            for cand2 in (x for x in self.pairwise_dict.keys() if x !=cand):
                if cand is not cand2:
                    for cand3 in (x for x in self.pairwise_dict.keys() if x not in (cand, cand2)):
                        strongest[cand2][cand3] = max(strongest[cand2][cand3],
                                                      min(strongest[cand2][cand], strongest[cand][cand3]))
        return strongest

    def get_winner(self):
        self.set_pairwise_preference_matrix()
        c = self.set_strongest_paths()
        strongest = None
        for cand in self.candidates:
            strongest = cand
            for cand2 in (x for x in self.candidates if x != cand):
                if c[cand][cand2] < c[cand2][cand]:
                    strongest = cand2

        return strongest


if __name__ == '__main__':
    pass