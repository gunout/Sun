import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SolarDataAnalyzer:
    def __init__(self, data_type):
        self.data_type = data_type
        self.colors = ['#FF6B00', '#FFD700', '#FF4500', '#8B0000', '#FF8C00', 
                      '#FFA500', '#FF6347', '#DC143C', '#B22222', '#CD5C5C']
        
        self.start_year = 1750  # Début des observations solaires modernes
        self.end_year = 2025
        
        # Configuration spécifique pour chaque type de données solaires
        self.config = self._get_solar_config()
        
    def _get_solar_config(self):
        """Retourne la configuration spécifique pour chaque type de données solaires"""
        configs = {
            "sunspots": {
                "base_value": 50,
                "cycle_years": 11.0,
                "amplitude": 100,
                "trend": "cyclique",
                "unit": "Nombre de Wolf",
                "description": "Taches solaires - Cycle de 11 ans"
            },
            "solar_flux": {
                "base_value": 120,
                "cycle_years": 11.0,
                "amplitude": 40,
                "trend": "cyclique",
                "unit": "SFU (Solar Flux Units)",
                "description": "Flux solaire à 10.7 cm"
            },
            "solar_wind": {
                "base_value": 400,
                "cycle_years": 11.0,
                "amplitude": 200,
                "trend": "cyclique",
                "unit": "km/s",
                "description": "Vitesse du vent solaire"
            },
            "solar_irradiance": {
                "base_value": 1361,
                "cycle_years": 11.0,
                "amplitude": 1.5,
                "trend": "stable",
                "unit": "W/m²",
                "description": "Irradiance solaire totale (TSI)"
            },
            "solar_rotation": {
                "base_value": 27,
                "cycle_years": 11.0,
                "amplitude": 2,
                "trend": "variable",
                "unit": "jours",
                "description": "Période de rotation solaire"
            },
            "solar_inclination": {
                "base_value": 7.25,
                "cycle_years": 11.0,
                "amplitude": 0.5,
                "trend": "stable",
                "unit": "degrés",
                "description": "Inclinaison de l'axe solaire"
            },
            "solar_magnetic": {
                "base_value": 0,
                "cycle_years": 22.0,  # Cycle magnétique complet
                "amplitude": 100,
                "trend": "cyclique",
                "unit": "Microteslas",
                "description": "Champ magnétique solaire"
            },
            "solar_activity": {
                "base_value": 50,
                "cycle_years": 11.0,
                "amplitude": 80,
                "trend": "cyclique",
                "unit": "Index d'activité",
                "description": "Indice général d'activité solaire"
            },
            # Configuration par défaut
            "default": {
                "base_value": 100,
                "cycle_years": 11.0,
                "amplitude": 50,
                "trend": "cyclique",
                "unit": "Unités",
                "description": "Données solaires génériques"
            }
        }
        
        return configs.get(self.data_type, configs["default"])
    
    def generate_solar_data(self):
        """Génère des données solaires simulées basées sur les cycles solaires réels"""
        print(f"🌞 Génération des données solaires pour {self.config['description']}...")
        
        # Créer une base de données annuelle
        dates = pd.date_range(start=f'{self.start_year}-01-01', 
                             end=f'{self.end_year}-12-31', freq='Y')
        
        data = {'Year': [date.year for date in dates]}
        
        # Données principales basées sur les cycles solaires
        data['Base_Value'] = self._simulate_solar_cycle(dates)
        data['Solar_Minimum'] = self._simulate_solar_minima(dates)
        data['Solar_Maximum'] = self._simulate_solar_maxima(dates)
        data['Cycle_Phase'] = self._simulate_cycle_phase(dates)
        
        # Variations à long terme
        data['Secular_Trend'] = self._simulate_secular_trend(dates)
        data['Grand_Minima'] = self._simulate_grand_minima(dates)
        data['Magnetic_Reversal'] = self._simulate_magnetic_reversal(dates)
        
        # Données dérivées
        data['Smoothed_Value'] = self._simulate_smoothed_data(dates)
        data['Monthly_Variation'] = self._simulate_monthly_variation(dates)
        data['Annual_Variation'] = self._simulate_annual_variation(dates)
        
        # Indices solaires complémentaires
        data['Solar_Index'] = self._simulate_solar_index(dates)
        data['Activity_Level'] = self._simulate_activity_level(dates)
        data['Predicted_Value'] = self._simulate_predicted_data(dates)
        
        df = pd.DataFrame(data)
        
        # Ajouter des événements solaires historiques
        self._add_solar_events(df)
        
        return df
    
    def _simulate_solar_cycle(self, dates):
        """Simule le cycle solaire principal (11 ans)"""
        base_value = self.config["base_value"]
        cycle_years = self.config["cycle_years"]
        amplitude = self.config["amplitude"]
        
        values = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Cycle solaire de base
            phase = (year - self.start_year) % cycle_years
            cycle_value = np.sin(2 * np.pi * phase / cycle_years)
            
            # Ajustement pour différents types de données
            if self.config["trend"] == "cyclique":
                value = base_value + amplitude * cycle_value
            elif self.config["trend"] == "stable":
                value = base_value + amplitude * 0.1 * cycle_value
            else:
                value = base_value + amplitude * 0.5 * cycle_value
            
            # Bruit naturel
            noise = np.random.normal(0, amplitude * 0.1)
            values.append(value + noise)
        
        return values
    
    def _simulate_solar_minima(self, dates):
        """Simule les périodes de minimum solaire"""
        minima = []
        for i, date in enumerate(dates):
            year = date.year
            cycle_phase = (year - self.start_year) % 11.0
            
            # Minimum solaire autour des années de transition
            if 10.5 <= cycle_phase <= 11.0 or 0 <= cycle_phase <= 0.5:
                min_factor = 0.3
            elif 10.0 <= cycle_phase <= 10.5 or 0.5 <= cycle_phase <= 1.0:
                min_factor = 0.7
            else:
                min_factor = 1.0
            
            minima.append(min_factor)
        
        return minima
    
    def _simulate_solar_maxima(self, dates):
        """Simule les périodes de maximum solaire"""
        maxima = []
        for i, date in enumerate(dates):
            year = date.year
            cycle_phase = (year - self.start_year) % 11.0
            
            # Maximum solaire autour du milieu du cycle
            if 4.5 <= cycle_phase <= 6.5:
                max_factor = 1.0
            elif 4.0 <= cycle_phase <= 4.5 or 6.5 <= cycle_phase <= 7.0:
                max_factor = 0.9
            else:
                max_factor = 0.5
            
            maxima.append(max_factor)
        
        return maxima
    
    def _simulate_cycle_phase(self, dates):
        """Simule la phase du cycle solaire (0-1)"""
        phases = []
        for date in dates:
            year = date.year
            phase = (year - self.start_year) % 11.0 / 11.0
            phases.append(phase)
        
        return phases
    
    def _simulate_secular_trend(self, dates):
        """Simule les tendances séculaires (variations à long terme)"""
        trends = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Tendance séculaire sur plusieurs siècles
            if year < 1800:
                trend = 0.9  # Période pré-moderne
            elif 1800 <= year < 1900:
                trend = 0.95 + 0.0005 * (year - 1800)  # Augmentation progressive
            elif 1900 <= year < 2000:
                trend = 1.0 + 0.001 * (year - 1900)  # Période moderne
            else:
                trend = 1.05  # Période contemporaine
            
            trends.append(trend)
        
        return trends
    
    def _simulate_grand_minima(self, dates):
        """Simule les grands minima solaires (comme le Minimum de Maunder)"""
        minima_effect = []
        for date in dates:
            year = date.year
            
            # Minimum de Maunder (1645-1715)
            if 1645 <= year <= 1715:
                factor = 0.3
            # Minimum de Dalton (1790-1820)
            elif 1790 <= year <= 1820:
                factor = 0.7
            # Minimum moderne (2008-2009)
            elif 2008 <= year <= 2009:
                factor = 0.8
            else:
                factor = 1.0
            
            minima_effect.append(factor)
        
        return minima_effect
    
    def _simulate_magnetic_reversal(self, dates):
        """Simule les inversions du champ magnétique solaire (cycle de 22 ans)"""
        reversals = []
        for date in dates:
            year = date.year
            magnetic_phase = (year - self.start_year) % 22.0
            
            # Inversion magnétique autour des maximums
            if 10.5 <= magnetic_phase <= 11.5 or 21.5 <= magnetic_phase <= 22.0:
                reversal = 1  # Inversion en cours
            else:
                reversal = 0  # Champ stable
            
            reversals.append(reversal)
        
        return reversals
    
    def _simulate_smoothed_data(self, dates):
        """Simule des données lissées (moyenne mobile sur 13 mois)"""
        base_cycle = self._simulate_solar_cycle(dates)
        
        smoothed = []
        for i in range(len(base_cycle)):
            # Moyenne mobile centrée sur 13 points (≈13 mois)
            start_idx = max(0, i - 6)
            end_idx = min(len(base_cycle), i + 7)
            window = base_cycle[start_idx:end_idx]
            smoothed.append(np.mean(window))
        
        return smoothed
    
    def _simulate_monthly_variation(self, dates):
        """Simule les variations mensuelles"""
        variations = []
        for date in dates:
            # Variation saisonnière simulée
            month = date.month
            seasonal_variation = 0.1 * np.sin(2 * np.pi * (month - 1) / 12)
            variations.append(1 + seasonal_variation)
        
        return variations
    
    def _simulate_annual_variation(self, dates):
        """Simule les variations annuelles"""
        variations = []
        for i, date in enumerate(dates):
            year = date.year
            # Variation annuelle basée sur l'activité solaire
            annual_variation = 0.05 * np.sin(2 * np.pi * (year - self.start_year) / 5.5)
            variations.append(1 + annual_variation)
        
        return variations
    
    def _simulate_solar_index(self, dates):
        """Simule un indice solaire composite"""
        indices = []
        base_cycle = self._simulate_solar_cycle(dates)
        secular_trend = self._simulate_secular_trend(dates)
        
        for i in range(len(dates)):
            # Indice composite pondéré
            index = (base_cycle[i] * 0.7 + 
                    secular_trend[i] * self.config["base_value"] * 0.3)
            indices.append(index)
        
        return indices
    
    def _simulate_activity_level(self, dates):
        """Simule le niveau d'activité solaire (0-100)"""
        activity_levels = []
        base_cycle = self._simulate_solar_cycle(dates)
        
        min_val = min(base_cycle)
        max_val = max(base_cycle)
        
        for value in base_cycle:
            # Normalisation entre 0 et 100
            activity = 100 * (value - min_val) / (max_val - min_val)
            activity_levels.append(activity)
        
        return activity_levels
    
    def _simulate_predicted_data(self, dates):
        """Simule des données prédites (projection future)"""
        predictions = []
        base_cycle = self._simulate_solar_cycle(dates)
        secular_trend = self._simulate_secular_trend(dates)
        
        for i, date in enumerate(dates):
            year = date.year
            current_value = base_cycle[i]
            trend_factor = secular_trend[i]
            
            if year > 2020:  # Période de prédiction
                # Ajouter une incertitude croissante
                years_since_2020 = year - 2020
                uncertainty = 0.02 * years_since_2020
                prediction = current_value * trend_factor * (1 + np.random.normal(0, uncertainty))
            else:
                prediction = current_value
            
            predictions.append(prediction)
        
        return predictions
    
    def _add_solar_events(self, df):
        """Ajoute des événements solaires historiques significatifs"""
        for i, row in df.iterrows():
            year = row['Year']
            
            # Événements solaires historiques
            if year == 1859:
                # Éruption de Carrington
                df.loc[i, 'Activity_Level'] *= 1.5
                df.loc[i, 'Solar_Index'] *= 1.3
            
            elif year == 1947:
                # Cycle solaire 18 - très fort
                df.loc[i, 'Base_Value'] *= 1.2
            
            elif year == 1958:
                # Cycle solaire 19 - le plus fort enregistré
                df.loc[i, 'Base_Value'] *= 1.3
                df.loc[i, 'Activity_Level'] = min(100, df.loc[i, 'Activity_Level'] * 1.4)
            
            elif year == 1989:
                # Tempête solaire qui a affecté le Québec
                df.loc[i, 'Activity_Level'] *= 1.2
            
            elif year == 2003:
                # Éruptions d'Halloween
                df.loc[i, 'Base_Value'] *= 1.15
                df.loc[i, 'Activity_Level'] *= 1.25
            
            elif year == 2012:
                # Tempête solaire manquée de justesse
                df.loc[i, 'Base_Value'] *= 1.1
            
            # Grands minima historiques
            if 1645 <= year <= 1715:
                # Minimum de Maunder
                df.loc[i, 'Base_Value'] *= 0.3
                df.loc[i, 'Activity_Level'] *= 0.4
            
            elif 1790 <= year <= 1820:
                # Minimum de Dalton
                df.loc[i, 'Base_Value'] *= 0.6
                df.loc[i, 'Activity_Level'] *= 0.7
    
    def create_solar_analysis(self, df):
        """Crée une analyse complète des données solaires"""
        plt.style.use('dark_background')  # Fond sombre pour l'astronomie
        fig = plt.figure(figsize=(20, 28))
        
        # 1. Cycle solaire principal
        ax1 = plt.subplot(5, 2, 1)
        self._plot_solar_cycle(df, ax1)
        
        # 2. Activité solaire historique
        ax2 = plt.subplot(5, 2, 2)
        self._plot_historical_activity(df, ax2)
        
        # 3. Comparaison minima/maxima
        ax3 = plt.subplot(5, 2, 3)
        self._plot_minima_maxima(df, ax3)
        
        # 4. Tendances séculaires
        ax4 = plt.subplot(5, 2, 4)
        self._plot_secular_trends(df, ax4)
        
        # 5. Phase du cycle
        ax5 = plt.subplot(5, 2, 5)
        self._plot_cycle_phase(df, ax5)
        
        # 6. Données lissées
        ax6 = plt.subplot(5, 2, 6)
        self._plot_smoothed_data(df, ax6)
        
        # 7. Niveau d'activité
        ax7 = plt.subplot(5, 2, 7)
        self._plot_activity_level(df, ax7)
        
        # 8. Inversions magnétiques
        ax8 = plt.subplot(5, 2, 8)
        self._plot_magnetic_reversals(df, ax8)
        
        # 9. Indice solaire composite
        ax9 = plt.subplot(5, 2, 9)
        self._plot_solar_index(df, ax9)
        
        # 10. Prédictions et projections
        ax10 = plt.subplot(5, 2, 10)
        self._plot_predictions(df, ax10)
        
        plt.suptitle(f'Analyse des Données Solaires: {self.config["description"]} ({self.start_year}-{self.end_year})', 
                    fontsize=16, fontweight='bold', color='white')
        plt.tight_layout()
        plt.savefig(f'solar_{self.data_type}_analysis.png', dpi=300, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        plt.show()
        
        # Générer les insights
        self._generate_solar_insights(df)
    
    def _plot_solar_cycle(self, df, ax):
        """Plot du cycle solaire principal"""
        ax.plot(df['Year'], df['Base_Value'], label='Valeur de base', 
               linewidth=2, color='#FF6B00', alpha=0.9)
        
        ax.set_title(f'Cycle Solaire Principal - {self.config["description"]}', 
                    fontsize=12, fontweight='bold', color='white')
        ax.set_ylabel(self.config["unit"], color='#FF6B00')
        ax.tick_params(axis='y', labelcolor='#FF6B00')
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        
        # Ajouter des annotations pour les cycles
        for year in range(1750, 2026, 11):
            if year in df['Year'].values:
                ax.axvline(x=year, alpha=0.3, color='yellow', linestyle='--')
                ax.text(year, ax.get_ylim()[1]*0.9, f'Cycle', 
                       rotation=90, color='yellow', alpha=0.7, fontsize=8)
    
    def _plot_historical_activity(self, df, ax):
        """Plot de l'activité solaire historique"""
        ax.fill_between(df['Year'], df['Base_Value'], alpha=0.7, 
                       color='#FF4500', label='Activité solaire')
        
        ax.set_title('Activité Solaire Historique', fontsize=12, fontweight='bold', color='white')
        ax.set_ylabel(self.config["unit"], color='#FF4500')
        ax.set_xlabel('Année', color='white')
        ax.tick_params(axis='y', labelcolor='#FF4500')
        ax.tick_params(axis='x', labelcolor='white')
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        
        # Marquer les événements importants
        events = {
            1859: 'Éruption\nCarrington',
            1958: 'Cycle 19\nMax',
            2003: 'Éruptions\nHalloween',
            2012: 'Tempête\nmanquée'
        }
        
        for year, label in events.items():
            if year in df['Year'].values:
                y_val = df.loc[df['Year'] == year, 'Base_Value'].values[0]
                ax.annotate(label, xy=(year, y_val), xytext=(year, y_val*1.2),
                           arrowprops=dict(arrowstyle='->', color='yellow'),
                           color='yellow', fontsize=8, ha='center')
    
    def _plot_minima_maxima(self, df, ax):
        """Plot des minima et maxima solaires"""
        ax.plot(df['Year'], df['Solar_Minimum'], label='Périodes de minimum', 
               color='#1E90FF', alpha=0.7)
        ax.plot(df['Year'], df['Solar_Maximum'], label='Périodes de maximum', 
               color='#FF6347', alpha=0.7)
        
        ax.set_title('Minima et Maxima Solaires', fontsize=12, fontweight='bold', color='white')
        ax.set_ylabel('Facteur d\'amplitude', color='white')
        ax.legend()
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_secular_trends(self, df, ax):
        """Plot des tendances séculaires"""
        ax.plot(df['Year'], df['Secular_Trend'], label='Tendance séculaire', 
               linewidth=2, color='#FFD700')
        ax.plot(df['Year'], df['Grand_Minima'], label='Grands minima', 
               linewidth=2, color='#00BFFF')
        
        ax.set_title('Tendances Séculaires et Grands Minima', fontsize=12, fontweight='bold', color='white')
        ax.set_ylabel('Facteur multiplicatif', color='white')
        ax.legend()
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_cycle_phase(self, df, ax):
        """Plot de la phase du cycle solaire"""
        scatter = ax.scatter(df['Year'], df['Cycle_Phase'], c=df['Cycle_Phase'], 
                           cmap='hsv', alpha=0.7, s=20)
        
        ax.set_title('Phase du Cycle Solaire (0-1)', fontsize=12, fontweight='bold', color='white')
        ax.set_ylabel('Phase du cycle', color='white')
        ax.set_xlabel('Année', color='white')
        plt.colorbar(scatter, ax=ax, label='Phase')
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_smoothed_data(self, df, ax):
        """Plot des données lissées"""
        ax.plot(df['Year'], df['Base_Value'], label='Données brutes', 
               alpha=0.5, color='#FF6347')
        ax.plot(df['Year'], df['Smoothed_Value'], label='Données lissées (13 mois)', 
               linewidth=2, color='#00FF7F')
        
        ax.set_title('Données Brutes vs Lissées', fontsize=12, fontweight='bold', color='white')
        ax.set_ylabel(self.config["unit"], color='white')
        ax.legend()
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_activity_level(self, df, ax):
        """Plot du niveau d'activité solaire"""
        ax.fill_between(df['Year'], df['Activity_Level'], alpha=0.6, 
                       color='#FF4500', label='Niveau d\'activité')
        ax.plot(df['Year'], df['Activity_Level'], color='#FF8C00', alpha=0.8)
        
        ax.set_title('Niveau d\'Activité Solaire (0-100)', fontsize=12, fontweight='bold', color='white')
        ax.set_ylabel('Niveau d\'activité', color='white')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_magnetic_reversals(self, df, ax):
        """Plot des inversions magnétiques"""
        ax.fill_between(df['Year'], df['Magnetic_Reversal'], alpha=0.6, 
                       color='#8A2BE2', label='Inversion magnétique')
        
        ax.set_title('Inversions du Champ Magnétique Solaire', fontsize=12, fontweight='bold', color='white')
        ax.set_ylabel('État magnétique', color='white')
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['Stable', 'Inversion'])
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_solar_index(self, df, ax):
        """Plot de l'indice solaire composite"""
        ax.plot(df['Year'], df['Solar_Index'], label='Indice solaire composite', 
               linewidth=2, color='#FF69B4')
        
        ax.set_title('Indice Solaire Composite', fontsize=12, fontweight='bold', color='white')
        ax.set_ylabel('Valeur de l\'indice', color='white')
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _plot_predictions(self, df, ax):
        """Plot des prédictions et projections"""
        ax.plot(df['Year'], df['Base_Value'], label='Données historiques', 
               color='#FF6347', alpha=0.7)
        ax.plot(df['Year'], df['Predicted_Value'], label='Projections', 
               linewidth=2, color='#00FFFF', linestyle='--')
        
        ax.axvline(x=2020, color='yellow', linestyle=':', alpha=0.7, label='Début des prédictions')
        
        ax.set_title('Données Historiques et Projections Futures', fontsize=12, fontweight='bold', color='white')
        ax.set_ylabel(self.config["unit"], color='white')
        ax.legend()
        ax.grid(True, alpha=0.2, color='white')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
    
    def _generate_solar_insights(self, df):
        """Génère des insights analytiques sur les données solaires"""
        print(f"🌞 INSIGHTS ANALYTIQUES - {self.config['description']}")
        print("=" * 70)
        
        # 1. Statistiques de base
        print("\n1. 📊 STATISTIQUES FONDAMENTALES:")
        avg_value = df['Base_Value'].mean()
        max_value = df['Base_Value'].max()
        min_value = df['Base_Value'].min()
        current_value = df['Base_Value'].iloc[-1]
        
        print(f"Valeur moyenne: {avg_value:.2f} {self.config['unit']}")
        print(f"Valeur maximale: {max_value:.2f} {self.config['unit']}")
        print(f"Valeur minimale: {min_value:.2f} {self.config['unit']}")
        print(f"Valeur actuelle: {current_value:.2f} {self.config['unit']}")
        
        # 2. Analyse des cycles
        print("\n2. 🔄 ANALYSE DES CYCLES SOLAIRES:")
        cycle_length = self.config["cycle_years"]
        n_cycles = (self.end_year - self.start_year) / cycle_length
        
        print(f"Durée du cycle: {cycle_length} années")
        print(f"Nombre de cycles observés: {n_cycles:.1f}")
        print(f"Type de tendance: {self.config['trend']}")
        
        # 3. Activité récente
        print("\n3. 📈 ACTIVITÉ RÉCENTE:")
        recent_data = df[df['Year'] >= 2000]
        avg_recent = recent_data['Base_Value'].mean()
        trend_recent = (recent_data['Base_Value'].iloc[-1] / 
                       recent_data['Base_Value'].iloc[0] - 1) * 100
        
        print(f"Moyenne depuis 2000: {avg_recent:.2f} {self.config['unit']}")
        print(f"Évolution depuis 2000: {trend_recent:+.1f}%")
        
        # 4. Événements majeurs
        print("\n4. ⚡ ÉVÉNEMENTS SOLAIRES MARQUANTS:")
        print("• 1859: Éruption de Carrington - plus grande tempête géomagnétique")
        print("• 1958: Cycle 19 - maximum solaire le plus intense enregistré")
        print("• 2003: Éruptions d'Halloween - perturbations importantes")
        print("• 2012: Tempête solaire manquée de justesse la Terre")
        print("• 1645-1715: Minimum de Maunder - petit âge glaciaire")
        print("• 1790-1820: Minimum de Dalton - baisse d'activité")
        
        # 5. Caractéristiques cycliques
        print("\n5. 🔁 CARACTÉRISTIQUES CYCLIQUES:")
        phase_current = df['Cycle_Phase'].iloc[-1]
        activity_current = df['Activity_Level'].iloc[-1]
        
        print(f"Phase actuelle du cycle: {phase_current:.2f}")
        print(f"Niveau d'activité actuel: {activity_current:.1f}%")
        
        if phase_current < 0.25:
            print("→ Début de cycle - activité croissante")
        elif phase_current < 0.75:
            print("→ Maximum solaire - activité élevée")
        else:
            print("→ Fin de cycle - activité décroissante")
        
        # 6. Projections futures
        print("\n6. 🔮 PROJECTIONS FUTURES:")
        predicted_growth = ((df['Predicted_Value'].iloc[-1] / 
                           df['Base_Value'].iloc[-1]) - 1) * 100
        
        print(f"Tendance projetée: {predicted_growth:+.1f}%")
        print("Cycle 25: Modéré à faible (prévisions actuelles)")
        print("Cycle 26: Incertain - dépend de l'évolution magnétique")
        
        # 7. Implications scientifiques
        print("\n7. 🎯 IMPLICATIONS SCIENTIFIQUES:")
        if self.data_type == "sunspots":
            print("• Indicateur clé de l'activité solaire")
            print("• Correlation avec le climat terrestre")
            print("• Impact sur les communications radio")
        
        elif self.data_type == "solar_wind":
            print("• Influence sur la magnétosphère terrestre")
            print("• Cause des aurores polaires")
            print("• Risque pour les satellites")
        
        elif self.data_type == "solar_irradiance":
            print("• Principal facteur du climat terrestre")
            print("• Variations affectent le bilan énergétique")
            print("• Important pour les énergies renouvelables")
        
        print("• Surveillance essentielle pour la météo spatiale")
        print("• Impact sur les technologies modernes")
        print("• Importance pour l'exploration spatiale")

def main():
    """Fonction principale pour l'analyse des données solaires"""
    # Types de données solaires disponibles
    solar_data_types = [
        "sunspots", "solar_flux", "solar_wind", "solar_irradiance",
        "solar_rotation", "solar_inclination", "solar_magnetic", "solar_activity"
    ]
    
    print("🌞 ANALYSE DES DONNÉES NUMÉRIQUES DU SOLEIL (1750-2025)")
    print("=" * 65)
    
    # Demander à l'utilisateur de choisir un type de données
    print("Types de données solaires disponibles:")
    for i, data_type in enumerate(solar_data_types, 1):
        analyzer_temp = SolarDataAnalyzer(data_type)
        print(f"{i}. {analyzer_temp.config['description']}")
    
    try:
        choix = int(input("\nChoisissez le numéro du type de données à analyser: "))
        if choix < 1 or choix > len(solar_data_types):
            raise ValueError
        selected_type = solar_data_types[choix-1]
    except (ValueError, IndexError):
        print("Choix invalide. Sélection des taches solaires par défaut.")
        selected_type = "sunspots"
    
    # Initialiser l'analyseur
    analyzer = SolarDataAnalyzer(selected_type)
    
    # Générer les données
    solar_data = analyzer.generate_solar_data()
    
    # Sauvegarder les données
    output_file = f'solar_{selected_type}_data_1750_2025.csv'
    solar_data.to_csv(output_file, index=False)
    print(f"💾 Données sauvegardées: {output_file}")
    
    # Aperçu des données
    print("\n👀 Aperçu des données:")
    print(solar_data[['Year', 'Base_Value', 'Activity_Level', 'Solar_Index']].head())
    
    # Créer l'analyse
    print("\n📈 Création de l'analyse des données solaires...")
    analyzer.create_solar_analysis(solar_data)
    
    print(f"\n✅ Analyse des données {analyzer.config['description']} terminée!")
    print(f"📊 Période: {analyzer.start_year}-{analyzer.end_year}")
    print("🌡️ Données: Cycles solaires, activité, tendances, prédictions")

if __name__ == "__main__":
    main()