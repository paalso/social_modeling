import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np


class InterbreedingVisualizer:
    def __init__(self, population):
        self.population = population
        self.history = self.population.history

    def plot_all(self):
        genetic_data = self._get_genetic_data()

        fig = plt.figure(figsize=(15, 10))
        spec = fig.add_gridspec(3, 2, height_ratios=[2, 2, 3])  # Увеличьте значения во втором ряду
        plt.tight_layout(pad=2.0)
        plt.subplots_adjust(hspace=0.4)

        # Ряд 1, столбец 1: график роста населения
        ax1 = fig.add_subplot(spec[0, 0])
        
        male_history = [item['male_count'] for item in self.population.history]
        female_history = [item['female_count'] for item in self.population.history]
        years = range(1, self.population.elapsed_years + 1)
        
        ax1.plot(years, male_history[1:], label='Male Population', linestyle='--', color='blue')
        ax1.plot(years, female_history[1:], label='Female Population', linestyle='-', color='red')
        ax1.set_title('Population Growth (Male vs Female) Over Time')
        ax1.set_xlabel('Years')
        ax1.set_ylabel('Population Size')
        ax1.grid(True)
        ax1.legend()
        ax1.set_ylim(bottom=0)

        # Ряд 1, столбец 2: демографическая пирамида
        ax2 = fig.add_subplot(spec[0, 1])

        male_ages = [human.age for human in self.population.members if human.gender == 'male']
        female_ages = [human.age for human in self.population.members if human.gender == 'female']

        age_bins = np.arange(0, max(male_ages + female_ages) + 5, 5)
        male_counts, _ = np.histogram(male_ages, bins=age_bins)
        female_counts, _ = np.histogram(female_ages, bins=age_bins)

        age_labels = [f'{age_bins[i]}-{age_bins[i + 1] - 1}' for i in range(len(age_bins) - 1)]

        male_counts = -male_counts

        y_positions = np.arange(len(age_labels))
        
        ax2.barh(y_positions, male_counts, color='blue', alpha=0.7, label='Men')
        ax2.barh(y_positions, female_counts, color='pink', alpha=0.7, label='Women')

        ax2.set_yticks(y_positions)
        ax2.set_yticklabels(age_labels)
        ax2.set_yticklabels(age_labels, fontsize=8)  # Уменьшить шрифт
        ax2.set_xlabel('Population Count')
        ax2.set_title('Demographic Pyramid')
        ax2.legend()

        ax2.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{abs(int(x))}'))
        ax2.grid(axis='x', linestyle='--', alpha=0.7)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        # Ряд 2, столбец 1: Динамика доли и стандартного отклонения по расам
        ax3 = fig.add_subplot(spec[1, 0])

        green_means = [item['green_mean'] for item in self.population.history]
        brown_means = [item['brown_mean'] for item in self.population.history]
        green_std_devs = [item['green_std_dev'] for item in self.population.history]
        brown_std_devs = [item['brown_std_dev'] for item in self.population.history]

        ax3.plot(years, green_means[1:], label='Average Green Proportion', linestyle='-', color='green')
        ax3.plot(years, brown_means[1:], label='Average Brown Proportion', linestyle='-', color='brown')

        ax3.plot(years, green_std_devs[1:], label='Green Std Dev', linestyle='--', color='darkgreen')
        ax3.plot(years, brown_std_devs[1:], label='Brown Std Dev', linestyle='--', color='darkred')

        ax3.set_title('Racial Proportion & Standard Deviation Over Time')
        ax3.set_xlabel('Years')
        ax3.set_ylabel('Proportion / Std Dev')
        ax3.grid(True)
        ax3.legend()
        ax3.set_ylim(bottom=0)

        # Ряд 2, столбец 2: Box Plot для генетического распределения
        ax4 = fig.add_subplot(spec[1, 1])
        ax4.boxplot([genetic_data[0], genetic_data[1]], patch_artist=True,
                    boxprops=dict(facecolor='lightgreen', color='green'),
                    medianprops=dict(color='red'))
        ax4.set_title('Genetic Composition')
        ax4.set_xticklabels(['Green', 'Brown'])
        ax4.set_ylabel('Proportion')
        ax4.grid(axis='y', linestyle='--', alpha=0.7)

        # Третий ряд, Stacked Bar Chart на всю ширину
        ax5 = fig.add_subplot(spec[2, :])  # Объединяем две колонки
        sort_order = np.argsort(genetic_data[0])[::-1]  # По убыванию компонента 'green'
        genetic_data_sorted = genetic_data[:, sort_order]
        indices_sorted = np.arange(len(self.population.members))

        ax5.bar(indices_sorted, genetic_data_sorted[0], label='Green', color='green', alpha=0.7)
        ax5.bar(indices_sorted, genetic_data_sorted[1], bottom=genetic_data_sorted[0], label='Brown', color='brown', alpha=0.7)
        ax5.set_title('Genetic Composition')
        ax5.set_xlabel('Individuals (sorted by % Green)')
        ax5.set_ylabel('Proportion')
        ax5.legend()
        ax5.grid(axis='y', linestyle='--', alpha=0.7)

        plt.show()

    # Age Distribution
    def plot_age_distribution(self):
        ages = [human.age for human in self.population.members]
        plt.hist(ages, bins=12, color='gray', alpha=0.8)
        plt.title('Age Distribution')
        plt.xlabel('Age (years)')
        plt.ylabel('Frequency')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    # Population Growth (Male vs Female)
    def plot_population_growth(self):
        male_history = [item['male_count'] for item in self.population.history]
        female_history = [item['female_count'] for item in self.population.history]
        print(male_history)
        print(female_history)

        if not male_history or not female_history:
            print('Нет данных о росте населения.')
            return

        years = range(1, self.population.elapsed_years + 1)
        plt.plot(years, male_history[1:], label='Male Population', linestyle='--', color='blue')
        plt.plot(years, female_history[1:], label='Female Population', linestyle='-', color='red')
        plt.title('Population Growth (Male vs Female) Over Time')
        plt.xlabel('Years')
        plt.ylabel('Population Size')
        plt.grid(True)
        plt.legend()
        plt.ylim(bottom=0)
        plt.show()

    # Age Distribution by Gender
    def plot_age_distribution_by_gender(self):
        male_ages = [human.age for human in self.population.members if human.gender == 'male']
        female_ages = [human.age for human in self.population.members if human.gender == 'female']
        plt.hist(
            [male_ages, female_ages],
            bins=12,
            label=['Men', 'Women'],
            color=['blue', 'pink'],
            alpha=0.8
        )
        plt.legend()
        plt.title('Age Distribution by Gender')
        plt.xlabel('Age (years)')
        plt.ylabel('Frequency')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    # Stacked Bar Chart for Genetic Composition
    def plot_genetic_composition(self):
        genetic_data = self._get_genetic_data()

        sort_order = np.argsort(genetic_data[0])[::-1]  # По убыванию компонента 'green'
        genetic_data_sorted = genetic_data[:, sort_order]
    
        indices_sorted = np.arange(len(self.population.members))
    
        plt.bar(indices_sorted, genetic_data_sorted[0], label='Green', color='green', alpha=0.7)
        plt.bar(
            indices_sorted,
            genetic_data_sorted[1],
            bottom=genetic_data_sorted[0],
            label='Brown',
            color='brown',
            alpha=0.7
        )
        plt.title('Genetic Composition')
        plt.xlabel('Individuals (sorted by % Green)')
        plt.ylabel('Proportion')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()
    
    # Box Plot for Genetic Distribution
    def plot_genetic_distribution(self):
        genetic_data = self._get_genetic_data()

        plt.boxplot(
            [genetic_data[0], genetic_data[1]],
            tick_labels=['Green', 'Brown'],
            patch_artist=True,
            boxprops=dict(facecolor='lightgreen', color='green'),
            medianprops=dict(color='red')
        )
        plt.title('Genetic Composition')
        plt.ylabel('Proportion')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    # Violin Plot for Genetic Distribution
    def plot_violin(self):
        genetic_data = self._get_genetic_data()
        
        fig, ax = plt.subplots()
        ax.violinplot(genetic_data, showmedians=True)
        
        ax.set_title('Genetic Composition (Violin Plot)')
        ax.set_xticks([1, 2])
        ax.set_xticklabels(['Green', 'Brown'])
        ax.set_ylabel('Proportion')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def _get_genetic_data(self):
        genetic_data = np.array(
            [[human.genotype.get('green', 0), human.genotype.get('brown', 0)]
             for human in self.population.members]
        ).T
        return genetic_data

    def plot_demographic_pyramid(self):
        male_ages = [human.age for human in self.population.members if human.gender == 'male']
        female_ages = [human.age for human in self.population.members if human.gender == 'female']

        age_bins = np.arange(0, max(male_ages + female_ages) + 5, 5)
        male_counts, _ = np.histogram(male_ages, bins=age_bins)
        female_counts, _ = np.histogram(female_ages, bins=age_bins)

        age_labels = [f'{age_bins[i]}-{age_bins[i + 1] - 1}' for i in range(len(age_bins) - 1)]

        male_counts = -male_counts

        fig, ax = plt.subplots(figsize=(10, 6))
        y_positions = np.arange(len(age_labels))

        ax.barh(y_positions, male_counts, color='blue', alpha=0.7, label='Men')
        ax.barh(y_positions, female_counts, color='pink', alpha=0.7, label='Women')

        ax.set_yticks(y_positions)
        ax.set_yticklabels(age_labels)
        ax.set_xlabel('Population Count')
        ax.set_title('Demographic Pyramid')
        ax.legend()

        ax.grid(axis='x', linestyle='--', alpha=0.7)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        plt.show()
