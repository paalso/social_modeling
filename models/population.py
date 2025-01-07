import copy
import math
import numpy as np
import random
from .human import Human


class Population:
    def __init__(self, population_settings):
        self.members = []
        self.elapsed_years = 0
        self.history = []
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
        self._save_yearly_statistics()

    def evolve(self, years):
        self.elapsed_years += years
        for _ in range(years):
            self._simulate_year()

    @property
    def stat(self):
        '''
        Возвращает статистику о популяции.
        :return: Словарь с ключами на английском языке.
        '''
        if not self.members:
            return {
                'elapsed_years': self.elapsed_years,
                'population_size': 0,
                'annual_growth_rate_percent': None,
                'min_age': None,
                'max_age': None,
                'average_age': None,
                'gender_ratio': None,
                'green_mean': None,
                'green_std_dev': None,
                'brown_mean': None,
                'brown_std_dev': None,
            }

        last_year_data = self.history[-1]

        population_size = last_year_data['male_count'] + last_year_data['female_count']
        if self.elapsed_years > 0:
            initial_population_size = (
                self.history[0]['male_count'] + self.history[0]['female_count']
            )
            annual_growth_rate = math.log(
                population_size / initial_population_size
            ) / self.elapsed_years
            annual_growth_rate_percent = round(annual_growth_rate * 100, 3)
        else:
            annual_growth_rate_percent = None

        return {
            'elapsed_years': self.elapsed_years,
            'population_size': population_size,
            'annual_growth_rate_percent': annual_growth_rate_percent,
            'min_age': min(human.age for human in self.members),
            'max_age': max(human.age for human in self.members),
            'average_age':
                round(sum(human.age for human in self.members) / len(self.members), 1),
            'gender_ratio': {
                'male': last_year_data['male_count'],
                'female': last_year_data['female_count'],
                'male_per_female_ratio': (
                    round(last_year_data['male_count'] / last_year_data['female_count'], 1)
                    if last_year_data['female_count'] > 0 else 'N/A'
                ),
            },
            'green_mean': round(last_year_data['green_mean'], 2),
            'green_std_dev': round(last_year_data['green_std_dev'], 2),
            'brown_mean': round(last_year_data['brown_mean'], 2),
            'brown_std_dev': round(last_year_data['brown_std_dev'], 2),
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
        self._save_yearly_statistics()

    def _save_yearly_statistics(self):
        male_ages = [human.age for human in self.members if human.gender == 'male']
        female_ages = [human.age for human in self.members if human.gender == 'female']

        green_concentrations = [human.genotype['green'] for human in self.members]
        brown_concentrations = [human.genotype['brown'] for human in self.members]

        year_stats = {
            'year': self.history[-1]['year'] + 1 if self.history else 0,
            'male_count': len(male_ages),
            'female_count': len(female_ages),
            'average_male_age': sum(male_ages) / len(male_ages) if male_ages else None,
            'average_female_age': sum(female_ages) / len(female_ages) if female_ages else None,
            'green_mean': sum(green_concentrations) / len(green_concentrations),
            'green_std_dev': np.std(green_concentrations),
            'brown_mean': sum(brown_concentrations) / len(brown_concentrations),
            'brown_std_dev': np.std(brown_concentrations),
        }

        self.history.append(year_stats)

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
        return f'Population(size={self.get_population_size()})'

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
