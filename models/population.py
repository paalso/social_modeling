import copy
import math
import random
from .human import Human


class Population:
    def __init__(self, population_settings):
        self.members = []
        self.elapsed_years = 0
        self.male_history = []
        self.female_history = []
        self.population_settings = population_settings
        self.birth_probability = self.population_settings['birth_probability']
        self.death_probability = self.population_settings['death_probability']
        self.gender_ratio_at_birth = self.population_settings['gender_ratio_at_birth']
        self.female_fertile_age_range = self.population_settings['fertile_age_range']['female']
        self.male_fertile_age_range = self.population_settings['fertile_age_range']['male']
        self.genetic_components = set(self.population_settings['initial_race_distribution'].keys())

    def generate_population(self, size):
        age_distribution = self.population_settings['initial_age_distribution']
        genetic_distribution = self.population_settings['initial_race_distribution']
        gender_distribution = self.population_settings['gender_ratio_at_birth']

        for _ in range(size):
            # Select age group and random age
            age_group = random.choices(
                population=list(age_distribution.keys()),
                weights=list(age_distribution.values()),
                k=1
            )[0]
            age = random.randint(*age_group)
    
            # Select gender
            gender = random.choices(
                population=list(gender_distribution.keys()),
                weights=list(gender_distribution.values()),
                k=1
            )[0]
    
            # Select genetic component
            genetic_component = random.choices(
                population=list(genetic_distribution.keys()),
                weights=list(genetic_distribution.values()),
                k=1
            )[0]
            other_genetic_component = self.get_other_set_item(
                self.genetic_components, genetic_component
            )
            genotype = {genetic_component: 1.0, other_genetic_component: 0.0}
    
            # Add new human to the population
            self._add_human(Human(gender=gender, genotype=genotype, age=age))

        self.initial_members = copy.deepcopy(self.members)
        self._save_genders_history()

    def evolve(self, years):
        self.elapsed_years += years
        for _ in range(years):
            self._simulate_year()
            self._save_genders_history()

    @property
    def stat(self):
        """
        Возвращает статистику о популяции.
        :return: Словарь с ключами на английском языке.
        """
        annual_growth_rate_percent = None

        if not self.members:
            return {
                'elapsed_years': self.elapsed_years,
                'population_size': 0,
                'growth_rate_percent': annual_growth_rate_percent,
                'min_age': None,
                'max_age': None,
                'average_age': None,
                'gender_ratio': None,
            }
    
        ages = [human.age for human in self.members]
        male_count = self.male_history[-1]
        female_count = self.female_history[-1]
        population_size = len(self.members)
        if self.elapsed_years > 0:
            initial_population_size = \
                self.male_history[0] + self.female_history[0]
            annual_growth_rate = math.log(
                population_size / initial_population_size) / self.elapsed_years
            annual_growth_rate_percent = round(annual_growth_rate * 100, 3)

        return {
            'elapsed_years': self.elapsed_years,
            "population_size": len(self.members),
            'annual_growth_rate_percent': annual_growth_rate_percent,
            "min_age": min(ages),
            "max_age": max(ages),
            "average_age": sum(ages) / len(ages),
            "gender_ratio": {
                "male": male_count,
                "female": female_count,
                "male_per_female_ratio": male_count / female_count if female_count > 0 else 'N/A'
            },
        }

    def _add_human(self, human):
        self.members.append(human)

    def _remove_human(self, human):
        self.members.remove(human)

    def _simulate_year(self):
        self.fertile_males = self._get_fertile_males()
    
        for human in list(self.members):
            human.age += 1
            self._simulate_death(human)
            self._simulate_birth(human)

    def _save_genders_history(self):
        male_count = sum(1 for human in self.members if human.gender == 'male')
        female_count = sum(1 for human in self.members if human.gender == 'female')
        self.male_history.append(male_count)
        self.female_history.append(female_count)

    def _simulate_death(self, human):
        if random.random() < self.death_probability(
            human, self.population_settings['max_age']):
            self._remove_human(human)
            del(human)

    def _simulate_birth(self, human):
        if human.gender == 'male':
            return
        if random.random() < self.birth_probability(
            human, self.female_fertile_age_range):

            father = random.choice(self.fertile_males)   # ПРОМИСКУИТЕТ какой-то позорный ;)

            new_gender = random.choices(
                population=list(self.gender_ratio_at_birth.keys()),
                weights=list(self.gender_ratio_at_birth.values()),
                k=1
            )[0]

            new_genotype = self._combine_genetics(
                human.genotype, father.genotype)

            human.number_of_children += 1

            self._add_human(Human(gender=new_gender, genotype=new_genotype, age=0))

    def _get_fertile_males(self):
        min_male_fertile_age_range, max_male_fertile_age_range = self.male_fertile_age_range
        fertile_males = [
            human for human in self.members
            if human.gender == 'male' and \
                (min_male_fertile_age_range <= human.age <= max_male_fertile_age_range)]
        return fertile_males
    
    def __repr__(self):
        return f"Population(size={self.get_population_size()})"

    @staticmethod
    def _combine_genetics(genotype_1, genotype_2):
        new_genotype = {}
        for genetic_component in genotype_1:
            new_genotype[genetic_component] = \
            (genotype_1[genetic_component] + genotype_2.get(genetic_component, 0)) / 2
        return new_genotype
        
    @staticmethod
    def get_other_set_item(set_, item):
        item_set = set()
        item_set.add(item)
        return (set_ - item_set ).pop()
