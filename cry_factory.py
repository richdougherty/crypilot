from clues import Anagram, Definition, Container, Deletion, Hidden, Homophone, Reversal
from solutions import DoubleSolution
from clue_sources import Combination

class CryFactory:
    """
    A factory class for creating various types of cryptic crossword clues and solutions.

    >>> factory = CryFactory()

    >>> factory.anagram('shredded corset', 'shredded <fodder>', 'corset', 'ESCORT')
    Anagram(clue='shredded corset', indicator='shredded <fodder>', fodder='corset', answer='ESCORT')

    >>> factory.definition('Chaperone', 'ESCORT')
    Definition(clue='Chaperone', answer='ESCORT')

    >>> factory.container('PAL outside of U', '<outer_left><outer_right> outside of <inner>', 'PA', 'L', 'U', 'PAUL')
    Container(clue='PAL outside of U', indicator='<outer_left><outer_right> outside of <inner>', outer_left='PA', outer_right='L', inner='U', answer='PAUL')

    >>> factory.deletion('Beheaded STAR', 'Beheaded <delete><keep>', 'TAR', 'S', None, 'TAR')
    Deletion(clue='Beheaded STAR', indicator='Beheaded <delete><keep>', keep='TAR', delete='S', deletion=None, answer='TAR')

    >>> factory.hidden('Found ermine, deer hides', '<left><hidden><right> hides', 'Found ', 'ermine, d', 'eer', 'ERMINED')
    Hidden(clue='Found ermine, deer hides', indicator='<left><hidden><right> hides', left='Found ', hidden='ermine, d', right='eer', answer='ERMINED')

    >>> factory.homophone('We hear PAIR', 'We hear <sound_alike>', 'PAIR', 'PARE')
    Homophone(clue='We hear PAIR', indicator='We hear <sound_alike>', sound_alike='PAIR', answer='PARE')

    >>> factory.reversal('Returned lager', 'Returned <fodder>', 'lager', 'REGAL')
    Reversal(clue='Returned lager', indicator='Returned <fodder>', fodder='lager', answer='REGAL')

    >>> factory.double_solution(
    ...     'Not seeing window covering',
    ...     '_____',
    ...     factory.definition('Not seeing', 'BLIND'),
    ...     factory.definition('window covering', 'BLIND'),
    ...     'BLIND'
    ... )
    DoubleSolution(clue='Not seeing window covering', answer_pattern='_____', solution1=Definition(clue='Not seeing', answer='BLIND'), solution2=Definition(clue='window covering', answer='BLIND'), answer='BLIND')

    >>> factory.combination(
    ...     'Returned beer',
    ...     'Returned ',
    ...     factory.definition('beer', 'LAGER'),
    ...     '',
    ...     'Returned LAGER'
    ... )
    Combination(input='Returned beer', prefix='Returned ', combined=Definition(clue='beer', answer='LAGER'), suffix='', output='Returned LAGER')
    """

    def anagram(self, clue, indicator, fodder, answer):
        return Anagram(clue, indicator, fodder, answer)

    def definition(self, clue, answer):
        return Definition(clue, answer)

    def container(self, clue, indicator, outer_left, outer_right, inner, answer):
        return Container(clue, indicator, outer_left, outer_right, inner, answer)

    def deletion(self, clue, indicator, keep, delete, deletion, answer):
        return Deletion(clue, indicator, keep, delete, deletion, answer)

    def hidden(self, clue, indicator, left, hidden, right, answer):
        return Hidden(clue, indicator, left, hidden, right, answer)

    def homophone(self, clue, indicator, sound_alike, answer):
        return Homophone(clue, indicator, sound_alike, answer)

    def reversal(self, clue, indicator, fodder, answer):
        return Reversal(clue, indicator, fodder, answer)

    def double_solution(self, clue, answer_pattern, solution1, solution2, answer):
        return DoubleSolution(clue, answer_pattern, solution1, solution2, answer)

    def combination(self, input, prefix, combined, suffix, output):
        return Combination(input, prefix, combined, suffix, output)