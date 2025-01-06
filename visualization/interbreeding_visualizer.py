# visualization/visualizer.py
import matplotlib.pyplot as plt
import numpy as np


class InterbreedingVisualizer:
    def __init__(self, population):
        self.population = population

    def plot_all(self):
        genetic_data = self._get_genetic_data()

        # Создаем подграфики с помощью gridspec
        fig = plt.figure(figsize=(15, 10))
        spec = fig.add_gridspec(3, 2, height_ratios=[2, 2, 3])
        plt.tight_layout(pad=3.0)

        # Первый ряд, график распределения по возрасту
        ax1 = fig.add_subplot(spec[0, 0])
        ax1.hist([human.age for human in self.population.members], bins=12, color="gray", alpha=0.8)
        ax1.set_title('Age Distribution')
        ax1.set_xlabel('Age (years)')
        ax1.set_ylabel('Frequency')
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        # Первый ряд, распределение по возрасту по полу
        ax2 = fig.add_subplot(spec[0, 1])
        male_ages = [human.age for human in self.population.members if human.gender == "male"]
        female_ages = [human.age for human in self.population.members if human.gender == "female"]
        ax2.hist([male_ages, female_ages], bins=12, label=["Men", "Women"], color=["blue", "pink"], alpha=0.8)
        ax2.legend()
        ax2.set_title('Age Distribution by Gender')
        ax2.set_xlabel('Age (years)')
        ax2.set_ylabel('Frequency')
        ax2.grid(axis='y', linestyle='--', alpha=0.7)

        # Второй ряд, график роста населения
        ax3 = fig.add_subplot(spec[1, 0])
        male_history = self.population.male_history
        female_history = self.population.female_history
        years = range(1, self.population.elapsed_years + 1)
        ax3.plot(years, male_history[1:], label="Male Population", linestyle='--', color='blue')
        ax3.plot(years, female_history[1:], label="Female Population", linestyle='-', color='red')
        ax3.set_title("Population Growth (Male vs Female) Over Time")
        ax3.set_xlabel("Years")
        ax3.set_ylabel("Population Size")
        ax3.grid(True)
        ax3.legend()
        ax3.set_ylim(bottom=0)

        # Второй ряд, Box Plot для генетического распределения
        ax4 = fig.add_subplot(spec[1, 1])
        ax4.boxplot([genetic_data[0], genetic_data[1]], patch_artist=True,
                    boxprops=dict(facecolor="lightgreen", color="green"),
                    medianprops=dict(color="red"))
        ax4.set_title('Genetic Composition')
        ax4.set_xticklabels(["Green", "Brown"])
        ax4.set_ylabel('Proportion')
        ax4.grid(axis='y', linestyle='--', alpha=0.7)

        # Третий ряд, Stacked Bar Chart на всю ширину
        ax5 = fig.add_subplot(spec[2, :])  # Объединяем две колонки
        sort_order = np.argsort(genetic_data[0])[::-1]  # По убыванию компонента "green"
        genetic_data_sorted = genetic_data[:, sort_order]
        indices_sorted = np.arange(len(self.population.members))

        ax5.bar(indices_sorted, genetic_data_sorted[0], label="Green", color="green", alpha=0.7)
        ax5.bar(indices_sorted, genetic_data_sorted[1], bottom=genetic_data_sorted[0], label="Brown", color="brown", alpha=0.7)
        ax5.set_title('Genetic Composition')
        ax5.set_xlabel('Individuals (sorted by % Green)')
        ax5.set_ylabel('Proportion')
        ax5.legend()
        ax5.grid(axis='y', linestyle='--', alpha=0.7)

        plt.show()

    # Age Distribution
    def plot_age_distribution(self):
        ages = [human.age for human in self.population.members]
        plt.hist(ages, bins=12, color="gray", alpha=0.8)
        plt.title('Age Distribution')
        plt.xlabel('Age (years)')
        plt.ylabel('Frequency')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    # Population Growth (Male vs Female)
    def plot_population_growth(self):
        male_history = self.population.male_history
        female_history = self.population.female_history

        if not male_history or not female_history:
            print("Нет данных о росте населения.")
            return

        years = range(1, self.population.elapsed_years + 1)

        plt.plot(years, male_history[1:], label="Male Population", linestyle='--', color='blue')
        plt.plot(years, female_history[1:], label="Female Population", linestyle='-', color='red')
        plt.title("Population Growth (Male vs Female) Over Time")
        plt.xlabel("Years")
        plt.ylabel("Population Size")
        plt.grid(True)
        plt.legend()
        plt.ylim(bottom=0)
        plt.show()

    # Age Distribution by Gender
    def plot_age_distribution_by_gender(self):
        male_ages = [human.age for human in self.population.members if human.gender == "male"]
        female_ages = [human.age for human in self.population.members if human.gender == "female"]
        plt.hist(
            [male_ages, female_ages],
            bins=12,
            label=["Men", "Women"],
            color=["blue", "pink"],
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

        sort_order = np.argsort(genetic_data[0])[::-1]  # По убыванию компонента "green"
        genetic_data_sorted = genetic_data[:, sort_order]
    
        indices_sorted = np.arange(len(self.population.members))
    
        plt.bar(indices_sorted, genetic_data_sorted[0], label="Green", color="green", alpha=0.7)
        plt.bar(
            indices_sorted,
            genetic_data_sorted[1],
            bottom=genetic_data_sorted[0],
            label="Brown",
            color="brown",
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
            tick_labels=["Green", "Brown"],
            patch_artist=True,
            boxprops=dict(facecolor="lightgreen", color="green"),
            medianprops=dict(color="red")
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
        ax.set_xticklabels(["Green", "Brown"])
        ax.set_ylabel('Proportion')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def _get_genetic_data(self):
        genetic_data = np.array(
            [[human.genotype.get("green", 0), human.genotype.get("brown", 0)]
             for human in self.population.members]
        ).T
        return genetic_data
