from model_utils import Choices


class IndexableChoices(Choices):

    def index_of(self, item):
        for i in range(len(self._doubles)):
            if item == self._doubles[i][0]:
                return i
        raise ValueError(f"{item} is not a valid choice.")


DIFFICULTY_CHOICES = IndexableChoices(
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ('expert', 'Expert')
)
NP_CHOICES = Choices(
    ('taroko', 'Taroko National Park'),
    ('sheipa', 'Shei-pa National Park'),
    ('jade', 'Yushan National Park')
)
