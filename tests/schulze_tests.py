__author__ = 'ioparaskev'

from svote import SchulzeVoting, SchulzeVoter
from unittest import TestCase, mock


class TestSchulzeVoting(TestCase):
    def set_preference(self, voter, pref):
        prf = dict()
        for i, pref in enumerate(pref):
            prf[pref] = i + 1
        voter.preferences_ranked = prf
        return voter

    def setup_schulze(self, num_of_voters, prefs):
        voters = [str(i) for i in range(1, num_of_voters+1)]
        self.prefs = tuple(x for x in prefs)
        self.schulze = SchulzeVoting(self.prefs, voters)

    def set_votes(self, number, preference):
        voters = []
        for i in range(1, number+1):
            voter = SchulzeVoter('', preference)
            voters.append(voter)
        return voters

    def set_wiki_example(self):
        test_voters = []

        test_voters.extend(self.set_votes(5, 'ACBED'))
        test_voters.extend(self.set_votes(5, 'ADECB'))
        test_voters.extend(self.set_votes(8, 'BEDAC'))
        test_voters.extend(self.set_votes(3, 'CABED'))
        test_voters.extend(self.set_votes(7, 'CAEBD'))
        test_voters.extend(self.set_votes(3, 'CBADE'))
        test_voters.extend(self.set_votes(7, 'DCEBA'))
        test_voters.extend(self.set_votes(8, 'EBADC'))
        return test_voters

    def set_wiki_example2(self):
        test_voters = []
        test_voters.extend(self.set_votes(3, 'ABCD'))
        test_voters.extend(self.set_votes(2, 'DABC'))
        test_voters.extend(self.set_votes(2, 'DBCA'))
        test_voters.extend(self.set_votes(2, 'CBDA'))
        return test_voters

    def test_wiki(self):
        self.setup_schulze(45, 'ABCDE')
        self.schulze.voters = self.set_wiki_example()
        winner = self.schulze.get_winner()
        self.assertEqual('E', winner)

    # def test_wiki2(self):
    #     self.setup_schulze(9, 'ABCD')
    #     self.schulze.voters = self.set_wiki_example2()
    #     winner = self.schulze.get_winner()
    #     self.assertEqual('E', winner)