from clues import Anagram, Definition, Container, Deletion, Hidden, Homophone, Reversal
from solutions import DoubleSolution
from clue_sources import Combination
from string_conversion import StringConversion
from cry_strings import split_tokens

class CryFactory:
    """
    A factory class for creating various types of cryptic crossword clues and solutions.

    >>> from string_conversion import StringConversion
    >>> factory = CryFactory()
    >>> split_factory = CryFactory(StringConversion(split_tokens))

    >>> factory.anagram('shredded corset', 'shredded <fodder>', 'corset', 'ESCORT')
    Anagram(clue='shredded corset', indicator='shredded <fodder>', fodder='corset', answer='ESCORT')

    >>> split_factory.anagram('shredded corset', 'shredded <fodder>', 'corset', 'ESCORT')
    Anagram(clue='s|h|r|e|d|d|e|d| |c|o|r|s|e|t', indicator='s|h|r|e|d|d|e|d| |<fodder>', fodder='c|o|r|s|e|t', answer='ESCORT')

    >>> factory.definition('Chaperone', 'ESCORT')
    Definition(clue='Chaperone', answer='ESCORT')

    >>> split_factory.definition('Chaperone', 'ESCORT')
    Definition(clue='C|h|a|p|e|r|o|n|e', answer='ESCORT')

    >>> factory.container('PAL outside of U', '<outer_left><outer_right> outside of <inner>', 'PA', 'L', 'U', 'PAUL')
    Container(clue='PAL outside of U', indicator='<outer_left><outer_right> outside of <inner>', outer_left='PA', outer_right='L', inner='U', answer='PAUL')

    >>> split_factory.container('PAL outside of U', '<outer_left><outer_right> outside of <inner>', 'PA', 'L', 'U', 'PAUL')
    Container(clue='P|A|L| |o|u|t|s|i|d|e| |o|f| |U', indicator='<outer_left>|<outer_right>| |o|u|t|s|i|d|e| |o|f| |<inner>', outer_left='P|A', outer_right='L', inner='U', answer='PAUL')

    >>> factory.deletion('Beheaded STAR', 'Beheaded <delete><keep>', 'TAR', 'S', None, 'TAR')
    Deletion(clue='Beheaded STAR', indicator='Beheaded <delete><keep>', keep='TAR', delete='S', deletion=None, answer='TAR')

    >>> split_factory.deletion('Beheaded STAR', 'Beheaded <delete><keep>', 'TAR', 'S', None, 'TAR')
    Deletion(clue='B|e|h|e|a|d|e|d| |S|T|A|R', indicator='B|e|h|e|a|d|e|d| |<delete>|<keep>', keep='T|A|R', delete='S', deletion=None, answer='TAR')

    >>> factory.hidden('Found ermine, deer hides', '<left><hidden><right> hides', 'Found ', 'ermine, d', 'eer', 'ERMINED')
    Hidden(clue='Found ermine, deer hides', indicator='<left><hidden><right> hides', left='Found ', hidden='ermine, d', right='eer', answer='ERMINED')

    >>> split_factory.hidden('Found ermine, deer hides', '<left><hidden><right> hides', 'Found ', 'ermine, d', 'eer', 'ERMINED')
    Hidden(clue='F|o|u|n|d| |e|r|m|i|n|e|,| |d|e|e|r| |h|i|d|e|s', indicator='<left>|<hidden>|<right>| |h|i|d|e|s', left='F|o|u|n|d| ', hidden='e|r|m|i|n|e|,| |d', right='e|e|r', answer='ERMINED')

    >>> factory.homophone('We hear PAIR', 'We hear <sound_alike>', 'PAIR', 'PARE')
    Homophone(clue='We hear PAIR', indicator='We hear <sound_alike>', sound_alike='PAIR', answer='PARE')

    >>> split_factory.homophone('We hear PAIR', 'We hear <sound_alike>', 'PAIR', 'PARE')
    Homophone(clue='W|e| |h|e|a|r| |P|A|I|R', indicator='W|e| |h|e|a|r| |<sound_alike>', sound_alike='P|A|I|R', answer='PARE')

    >>> factory.reversal('Returned lager', 'Returned <fodder>', 'lager', 'REGAL')
    Reversal(clue='Returned lager', indicator='Returned <fodder>', fodder='lager', answer='REGAL')

    >>> split_factory.reversal('Returned lager', 'Returned <fodder>', 'lager', 'REGAL')
    Reversal(clue='R|e|t|u|r|n|e|d| |l|a|g|e|r', indicator='R|e|t|u|r|n|e|d| |<fodder>', fodder='l|a|g|e|r', answer='REGAL')

    >>> factory.double_solution(
    ...     'Not seeing window covering',
    ...     '_____',
    ...     factory.definition('Not seeing', 'BLIND'),
    ...     factory.definition('window covering', 'BLIND'),
    ...     'BLIND'
    ... )
    DoubleSolution(clue='Not seeing window covering', answer_pattern='_____', solution1=Definition(clue='Not seeing', answer='BLIND'), solution2=Definition(clue='window covering', answer='BLIND'), answer='BLIND')

    >>> split_factory.double_solution(
    ...     'Not seeing window covering',
    ...     '_____',
    ...     split_factory.definition('Not seeing', 'BLIND'),
    ...     split_factory.definition('window covering', 'BLIND'),
    ...     'BLIND'
    ... )
    DoubleSolution(clue='N|o|t| |s|e|e|i|n|g| |w|i|n|d|o|w| |c|o|v|e|r|i|n|g', answer_pattern='_|_|_|_|_', solution1=Definition(clue='N|o|t| |s|e|e|i|n|g', answer='BLIND'), solution2=Definition(clue='w|i|n|d|o|w| |c|o|v|e|r|i|n|g', answer='BLIND'), answer='BLIND')

    >>> factory.combination(
    ...     'Returned beer',
    ...     'Returned ',
    ...     factory.definition('beer', 'LAGER'),
    ...     '',
    ...     'Returned LAGER'
    ... )
    Combination(input='Returned beer', prefix='Returned ', combined=Definition(clue='beer', answer='LAGER'), suffix='', output='Returned LAGER')

    >>> split_factory.combination(
    ...     'Returned beer',
    ...     'Returned ',
    ...     split_factory.definition('beer', 'LAGER'),
    ...     '',
    ...     'Returned LAGER'
    ... )
    Combination(input='R|e|t|u|r|n|e|d| |b|e|e|r', prefix='R|e|t|u|r|n|e|d| ', combined=Definition(clue='b|e|e|r', answer='LAGER'), suffix='', output='R|e|t|u|r|n|e|d| |L|A|G|E|R')
    """

    def __init__(self, string_conversion: StringConversion = None):
        if string_conversion is None:
            string_conversion = StringConversion(lambda x: x)
        self.conv = string_conversion

    def anagram(self, clue, indicator, fodder, answer):
        return Anagram(
            self.conv.convert_clue_source(clue),
            self.conv.convert_indicator_pattern_str(indicator),
            self.conv.convert_indicator_part_str(fodder),
            answer
        )

    def definition(self, clue, answer):
        return Definition(self.conv.convert_clue_source(clue), answer)

    def container(self, clue, indicator, outer_left, outer_right, inner, answer):
        return Container(
            self.conv.convert_clue_source(clue),
            self.conv.convert_indicator_pattern_str(indicator),
            self.conv.convert_indicator_part_str(outer_left),
            self.conv.convert_indicator_part_str(outer_right),
            self.conv.convert_indicator_part_str(inner),
            answer
        )

    def deletion(self, clue, indicator, keep, delete, deletion, answer):
        return Deletion(
            self.conv.convert_clue_source(clue),
            self.conv.convert_indicator_pattern_str(indicator),
            self.conv.convert_indicator_part(keep),
            self.conv.convert_indicator_part(delete),
            self.conv.convert_indicator_part_str(deletion) if deletion is not None else None,
            answer
        )

    def hidden(self, clue, indicator, left, hidden, right, answer):
        return Hidden(
            self.conv.convert_clue_source(clue),
            self.conv.convert_indicator_pattern_str(indicator),
            self.conv.convert_indicator_part_str(left),
            self.conv.convert_indicator_part_str(hidden),
            self.conv.convert_indicator_part_str(right),
            answer
        )

    def homophone(self, clue, indicator, sound_alike, answer):
        return Homophone(
            self.conv.convert_clue_source(clue),
            self.conv.convert_indicator_pattern_str(indicator),
            self.conv.convert_indicator_part_str(sound_alike),
            answer
        )

    def reversal(self, clue, indicator, fodder, answer):
        return Reversal(
            self.conv.convert_clue_source(clue),
            self.conv.convert_indicator_pattern_str(indicator),
            self.conv.convert_indicator_part_str(fodder),
            answer
        )

    def double_solution(self, clue, answer_pattern, solution1, solution2, answer):
        return DoubleSolution(
            self.conv.convert_clue_str(clue),
            self.conv.convert_answer_pattern_str(answer_pattern),
            solution1,
            solution2,
            answer
        )

    def combination(self, input, prefix, combined, suffix, output):
        return Combination(
            self.conv.convert_clue_str(input),
            self.conv.convert_clue_str(prefix),
            combined,
            self.conv.convert_clue_str(suffix),
            self.conv.convert_clue_str(output)
        )