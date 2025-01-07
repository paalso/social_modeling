from dataclasses import dataclass


@dataclass
class Human:
    gender: str
    genotype: dict
    age: int
    number_of_children: int = 0

    def die(self):
        del self

    def __repr__(self):
        self_repr = f'Human(gender={self.gender}, ' \
                    f'genotype={self.genotype}, age={self.age})'
        if self.gender == 'female' and self.number_of_children > 0:
            self_repr = f'{self_repr}, ' \
                        f'number of children: {self.number_of_children}'
        return self_repr
