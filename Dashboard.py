import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Solar Analytics Dashboard",
    page_icon="🌞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #FF6B00, #FF4500);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .info-box {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #FF6B00;
        margin: 1rem 0;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(90deg, #FF6B00, #FF4500);
    }
    </style>
""", unsafe_allow_html=True)

class SolarDataAnalyzer:
    def __init__(self, data_type):
        self.data_type = data_type
        self.colors = ['#FF6B00', '#FFD700', '#FF4500', '#8B0000', '#FF8C00', 
                      '#FFA500', '#FF6347', '#DC143C', '#B22222', '#CD5C5C']
        
        self.start_year = 1750
        self.end_year = 2025
        
        self.config = self._get_solar_config()
        
    def _get_solar_config(self):
        configs = {
            "sunspots": {
                "base_value": 50,
                "cycle_years": 11.0,
                "amplitude": 100,
                "trend": "cyclique",
                "unit": "Nombre de Wolf",
                "description": "Taches solaires - Cycle de 11 ans",
                "icon": "🌑",
                "color": "#FF6B00"
            },
            "solar_flux": {
                "base_value": 120,
                "cycle_years": 11.0,
                "amplitude": 40,
                "trend": "cyclique",
                "unit": "SFU",
                "description": "Flux solaire à 10.7 cm",
                "icon": "📡",
                "color": "#FFD700"
            },
            "solar_wind": {
                "base_value": 400,
                "cycle_years": 11.0,
                "amplitude": 200,
                "trend": "cyclique",
                "unit": "km/s",
                "description": "Vitesse du vent solaire",
                "icon": "💨",
                "color": "#00BFFF"
            },
            "solar_irradiance": {
                "base_value": 1361,
                "cycle_years": 11.0,
                "amplitude": 1.5,
                "trend": "stable",
                "unit": "W/m²",
                "description": "Irradiance solaire totale",
                "icon": "☀️",
                "color": "#FF4500"
            },
            "solar_rotation": {
                "base_value": 27,
                "cycle_years": 11.0,
                "amplitude": 2,
                "trend": "variable",
                "unit": "jours",
                "description": "Période de rotation solaire",
                "icon": "🔄",
                "color": "#8A2BE2"
            },
            "solar_inclination": {
                "base_value": 7.25,
                "cycle_years": 11.0,
                "amplitude": 0.5,
                "trend": "stable",
                "unit": "degrés",
                "description": "Inclinaison de l'axe solaire",
                "icon": "📐",
                "color": "#FF69B4"
            },
            "solar_magnetic": {
                "base_value": 0,
                "cycle_years": 22.0,
                "amplitude": 100,
                "trend": "cyclique",
                "unit": "µT",
                "description": "Champ magnétique solaire",
                "icon": "🧲",
                "color": "#00FF7F"
            },
            "solar_activity": {
                "base_value": 50,
                "cycle_years": 11.0,
                "amplitude": 80,
                "trend": "cyclique",
                "unit": "Index",
                "description": "Indice général d'activité",
                "icon": "⚡",
                "color": "#FF6347"
            },
            "default": {
                "base_value": 100,
                "cycle_years": 11.0,
                "amplitude": 50,
                "trend": "cyclique",
                "unit": "Unités",
                "description": "Données solaires génériques",
                "icon": "🌞",
                "color": "#FFFFFF"
            }
        }
        return configs.get(self.data_type, configs["default"])
    
    def generate_solar_data(self):
        dates = pd.date_range(start=f'{self.start_year}-01-01', 
                             end=f'{self.end_year}-12-31', freq='Y')
        
        data = {'Year': [date.year for date in dates]}
        data['Base_Value'] = self._simulate_solar_cycle(dates)
        data['Solar_Minimum'] = self._simulate_solar_minima(dates)
        data['Solar_Maximum'] = self._simulate_solar_maxima(dates)
        data['Cycle_Phase'] = self._simulate_cycle_phase(dates)
        data['Secular_Trend'] = self._simulate_secular_trend(dates)
        data['Grand_Minima'] = self._simulate_grand_minima(dates)
        data['Magnetic_Reversal'] = self._simulate_magnetic_reversal(dates)
        data['Smoothed_Value'] = self._simulate_smoothed_data(dates)
        data['Monthly_Variation'] = self._simulate_monthly_variation(dates)
        data['Annual_Variation'] = self._simulate_annual_variation(dates)
        data['Solar_Index'] = self._simulate_solar_index(dates)
        data['Activity_Level'] = self._simulate_activity_level(dates)
        data['Predicted_Value'] = self._simulate_predicted_data(dates)
        
        df = pd.DataFrame(data)
        self._add_solar_events(df)
        return df
    
    def _simulate_solar_cycle(self, dates):
        base_value = self.config["base_value"]
        cycle_years = self.config["cycle_years"]
        amplitude = self.config["amplitude"]
        
        values = []
        for i, date in enumerate(dates):
            year = date.year
            phase = (year - self.start_year) % cycle_years
            cycle_value = np.sin(2 * np.pi * phase / cycle_years)
            
            if self.config["trend"] == "cyclique":
                value = base_value + amplitude * cycle_value
            elif self.config["trend"] == "stable":
                value = base_value + amplitude * 0.1 * cycle_value
            else:
                value = base_value + amplitude * 0.5 * cycle_value
            
            noise = np.random.normal(0, amplitude * 0.1)
            values.append(value + noise)
        return values
    
    def _simulate_solar_minima(self, dates):
        minima = []
        for i, date in enumerate(dates):
            year = date.year
            cycle_phase = (year - self.start_year) % 11.0
            
            if 10.5 <= cycle_phase <= 11.0 or 0 <= cycle_phase <= 0.5:
                min_factor = 0.3
            elif 10.0 <= cycle_phase <= 10.5 or 0.5 <= cycle_phase <= 1.0:
                min_factor = 0.7
            else:
                min_factor = 1.0
            minima.append(min_factor)
        return minima
    
    def _simulate_solar_maxima(self, dates):
        maxima = []
        for i, date in enumerate(dates):
            year = date.year
            cycle_phase = (year - self.start_year) % 11.0
            
            if 4.5 <= cycle_phase <= 6.5:
                max_factor = 1.0
            elif 4.0 <= cycle_phase <= 4.5 or 6.5 <= cycle_phase <= 7.0:
                max_factor = 0.9
            else:
                max_factor = 0.5
            maxima.append(max_factor)
        return maxima
    
    def _simulate_cycle_phase(self, dates):
        phases = []
        for date in dates:
            year = date.year
            phase = (year - self.start_year) % 11.0 / 11.0
            phases.append(phase)
        return phases
    
    def _simulate_secular_trend(self, dates):
        trends = []
        for i, date in enumerate(dates):
            year = date.year
            if year < 1800:
                trend = 0.9
            elif 1800 <= year < 1900:
                trend = 0.95 + 0.0005 * (year - 1800)
            elif 1900 <= year < 2000:
                trend = 1.0 + 0.001 * (year - 1900)
            else:
                trend = 1.05
            trends.append(trend)
        return trends
    
    def _simulate_grand_minima(self, dates):
        minima_effect = []
        for date in dates:
            year = date.year
            if 1645 <= year <= 1715:
                factor = 0.3
            elif 1790 <= year <= 1820:
                factor = 0.7
            elif 2008 <= year <= 2009:
                factor = 0.8
            else:
                factor = 1.0
            minima_effect.append(factor)
        return minima_effect
    
    def _simulate_magnetic_reversal(self, dates):
        reversals = []
        for date in dates:
            year = date.year
            magnetic_phase = (year - self.start_year) % 22.0
            
            if 10.5 <= magnetic_phase <= 11.5 or 21.5 <= magnetic_phase <= 22.0:
                reversal = 1
            else:
                reversal = 0
            reversals.append(reversal)
        return reversals
    
    def _simulate_smoothed_data(self, dates):
        base_cycle = self._simulate_solar_cycle(dates)
        smoothed = []
        for i in range(len(base_cycle)):
            start_idx = max(0, i - 6)
            end_idx = min(len(base_cycle), i + 7)
            window = base_cycle[start_idx:end_idx]
            smoothed.append(np.mean(window))
        return smoothed
    
    def _simulate_monthly_variation(self, dates):
        variations = []
        for date in dates:
            month = date.month
            seasonal_variation = 0.1 * np.sin(2 * np.pi * (month - 1) / 12)
            variations.append(1 + seasonal_variation)
        return variations
    
    def _simulate_annual_variation(self, dates):
        variations = []
        for i, date in enumerate(dates):
            year = date.year
            annual_variation = 0.05 * np.sin(2 * np.pi * (year - self.start_year) / 5.5)
            variations.append(1 + annual_variation)
        return variations
    
    def _simulate_solar_index(self, dates):
        indices = []
        base_cycle = self._simulate_solar_cycle(dates)
        secular_trend = self._simulate_secular_trend(dates)
        
        for i in range(len(dates)):
            index = (base_cycle[i] * 0.7 + secular_trend[i] * self.config["base_value"] * 0.3)
            indices.append(index)
        return indices
    
    def _simulate_activity_level(self, dates):
        activity_levels = []
        base_cycle = self._simulate_solar_cycle(dates)
        min_val = min(base_cycle)
        max_val = max(base_cycle)
        
        for value in base_cycle:
            activity = 100 * (value - min_val) / (max_val - min_val)
            activity_levels.append(activity)
        return activity_levels
    
    def _simulate_predicted_data(self, dates):
        predictions = []
        base_cycle = self._simulate_solar_cycle(dates)
        secular_trend = self._simulate_secular_trend(dates)
        
        for i, date in enumerate(dates):
            year = date.year
            current_value = base_cycle[i]
            trend_factor = secular_trend[i]
            
            if year > 2020:
                years_since_2020 = year - 2020
                uncertainty = 0.02 * years_since_2020
                prediction = current_value * trend_factor * (1 + np.random.normal(0, uncertainty))
            else:
                prediction = current_value
            predictions.append(prediction)
        return predictions
    
    def _add_solar_events(self, df):
        for i, row in df.iterrows():
            year = row['Year']
            
            if year == 1859:
                df.loc[i, 'Activity_Level'] *= 1.5
                df.loc[i, 'Solar_Index'] *= 1.3
            elif year == 1947:
                df.loc[i, 'Base_Value'] *= 1.2
            elif year == 1958:
                df.loc[i, 'Base_Value'] *= 1.3
                df.loc[i, 'Activity_Level'] = min(100, df.loc[i, 'Activity_Level'] * 1.4)
            elif year == 1989:
                df.loc[i, 'Activity_Level'] *= 1.2
            elif year == 2003:
                df.loc[i, 'Base_Value'] *= 1.15
                df.loc[i, 'Activity_Level'] *= 1.25
            elif year == 2012:
                df.loc[i, 'Base_Value'] *= 1.1
            
            if 1645 <= year <= 1715:
                df.loc[i, 'Base_Value'] *= 0.3
                df.loc[i, 'Activity_Level'] *= 0.4
            elif 1790 <= year <= 1820:
                df.loc[i, 'Base_Value'] *= 0.6
                df.loc[i, 'Activity_Level'] *= 0.7

# Interface principale Streamlit
def main():
    # En-tête
    st.markdown('<div class="main-header"><h1>🌞 Solar Analytics Dashboard</h1><p>Analyse avancée des données solaires (1750-2025)</p></div>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/b/b4/The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Ob.jpg", 
                 use_container_width=True)
        st.title("⚙️ Configuration")
        
        # Sélection du type de données
        solar_data_types = [
            "sunspots", "solar_flux", "solar_wind", "solar_irradiance",
            "solar_rotation", "solar_inclination", "solar_magnetic", "solar_activity"
        ]
        
        selected_type = st.selectbox(
            "Type de données solaires",
            solar_data_types,
            format_func=lambda x: {
                "sunspots": "🌑 Taches solaires",
                "solar_flux": "📡 Flux solaire",
                "solar_wind": "💨 Vent solaire",
                "solar_irradiance": "☀️ Irradiance solaire",
                "solar_rotation": "🔄 Rotation solaire",
                "solar_inclination": "📐 Inclinaison",
                "solar_magnetic": "🧲 Champ magnétique",
                "solar_activity": "⚡ Activité générale"
            }[x]
        )
        
        # Initialisation de l'analyseur
        analyzer = SolarDataAnalyzer(selected_type)
        
        # Période d'analyse
        st.subheader("📅 Période d'analyse")
        col1, col2 = st.columns(2)
        with col1:
            start_year = st.number_input("Début", 1750, 2020, 1750)
        with col2:
            end_year = st.number_input("Fin", 1751, 2025, 2025)
        
        analyzer.start_year = start_year
        analyzer.end_year = end_year
        
        # Options d'affichage
        st.subheader("🎨 Options d'affichage")
        show_grid = st.checkbox("Afficher la grille", True)
        show_events = st.checkbox("Afficher les événements", True)
        
        # Bouton de génération
        if st.button("🔄 Générer les données", use_container_width=True):
            st.session_state['generate'] = True
        
        st.markdown("---")
        st.info("📊 Données simulées basées sur les cycles solaires réels")
    
    # Génération des données
    if 'generate' not in st.session_state:
        st.session_state['generate'] = True
    
    if st.session_state['generate']:
        with st.spinner("🌞 Génération des données solaires en cours..."):
            analyzer = SolarDataAnalyzer(selected_type)
            analyzer.start_year = start_year
            analyzer.end_year = end_year
            df = analyzer.generate_solar_data()
            st.session_state['df'] = df
            st.session_state['analyzer'] = analyzer
            st.session_state['generate'] = False
    
    df = st.session_state.get('df', None)
    analyzer = st.session_state.get('analyzer', None)
    
    if df is not None and analyzer is not None:
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            current_value = df['Base_Value'].iloc[-1]
            st.metric(
                f"{analyzer.config['icon']} Valeur actuelle",
                f"{current_value:.1f} {analyzer.config['unit']}",
                f"{(current_value/df['Base_Value'].mean()-1)*100:.1f}% vs moyenne"
            )
        
        with col2:
            max_value = df['Base_Value'].max()
            max_year = df.loc[df['Base_Value'].idxmax(), 'Year']
            st.metric(
                "📈 Maximum historique",
                f"{max_value:.1f} {analyzer.config['unit']}",
                f"en {int(max_year)}"
            )
        
        with col3:
            min_value = df['Base_Value'].min()
            min_year = df.loc[df['Base_Value'].idxmin(), 'Year']
            st.metric(
                "📉 Minimum historique",
                f"{min_value:.1f} {analyzer.config['unit']}",
                f"en {int(min_year)}"
            )
        
        with col4:
            activity_current = df['Activity_Level'].iloc[-1]
            st.metric(
                "⚡ Niveau d'activité",
                f"{activity_current:.1f}%",
                f"Phase: {df['Cycle_Phase'].iloc[-1]:.2f}"
            )
        
        # Graphiques principaux avec Plotly
        st.markdown("---")
        
        # Graphique 1: Cycle solaire principal
        fig1 = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Cycle Solaire Principal', 'Activité Historique', 
                          'Minima et Maxima', 'Tendances Séculaires'),
            specs=[[{'secondary_y': False}, {'secondary_y': False}],
                   [{'secondary_y': False}, {'secondary_y': False}]]
        )
        
        # Cycle principal
        fig1.add_trace(
            go.Scatter(x=df['Year'], y=df['Base_Value'], 
                      name='Valeur de base', line=dict(color=analyzer.config['color'], width=2)),
            row=1, col=1
        )
        
        # Activité historique
        fig1.add_trace(
            go.Scatter(x=df['Year'], y=df['Activity_Level'],
                      name='Niveau d\'activité', fill='tozeroy',
                      line=dict(color='#FF4500')),
            row=1, col=2
        )
        
        # Minima et maxima
        fig1.add_trace(
            go.Scatter(x=df['Year'], y=df['Solar_Minimum'],
                      name='Minimum', line=dict(color='#1E90FF')),
            row=2, col=1
        )
        fig1.add_trace(
            go.Scatter(x=df['Year'], y=df['Solar_Maximum'],
                      name='Maximum', line=dict(color='#FF6347')),
            row=2, col=1
        )
        
        # Tendances
        fig1.add_trace(
            go.Scatter(x=df['Year'], y=df['Secular_Trend'],
                      name='Tendance séculaire', line=dict(color='#FFD700')),
            row=2, col=2
        )
        fig1.add_trace(
            go.Scatter(x=df['Year'], y=df['Grand_Minima'],
                      name='Grands minima', line=dict(color='#00BFFF')),
            row=2, col=2
        )
        
        fig1.update_layout(height=800, showlegend=True, 
                          template='plotly_dark',
                          title_text=f"Analyse détaillée - {analyzer.config['description']}")
        
        if show_grid:
            fig1.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # Deuxième rangée de graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique: Données brutes vs lissées
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df['Year'], y=df['Base_Value'],
                                      name='Données brutes', line=dict(color='#FF6347', width=1)))
            fig2.add_trace(go.Scatter(x=df['Year'], y=df['Smoothed_Value'],
                                      name='Données lissées', line=dict(color='#00FF7F', width=3)))
            
            fig2.update_layout(
                title="Données brutes vs lissées (moyenne mobile 13 mois)",
                xaxis_title="Année",
                yaxis_title=analyzer.config['unit'],
                template='plotly_dark',
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            # Graphique: Inversions magnétiques
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=df['Year'], y=df['Magnetic_Reversal'],
                                      name='Inversions magnétiques',
                                      fill='tozeroy', line=dict(color='#8A2BE2', width=2)))
            
            fig3.update_layout(
                title="Inversions du champ magnétique solaire (cycle de 22 ans)",
                xaxis_title="Année",
                yaxis_title="État magnétique",
                template='plotly_dark',
                height=400
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        # Troisième rangée
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique: Indice solaire composite
            fig4 = go.Figure()
            fig4.add_trace(go.Scatter(x=df['Year'], y=df['Solar_Index'],
                                      name='Indice composite',
                                      line=dict(color='#FF69B4', width=2)))
            
            fig4.update_layout(
                title="Indice solaire composite",
                xaxis_title="Année",
                yaxis_title="Valeur de l'indice",
                template='plotly_dark',
                height=400
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        with col2:
            # Graphique: Prédictions
            fig5 = go.Figure()
            fig5.add_trace(go.Scatter(x=df['Year'], y=df['Base_Value'],
                                      name='Historique', line=dict(color='#FF6347', width=2)))
            fig5.add_trace(go.Scatter(x=df['Year'], y=df['Predicted_Value'],
                                      name='Projections', line=dict(color='#00FFFF', width=2, dash='dash')))
            
            # Ligne de séparation historique/prédiction
            fig5.add_vline(x=2020, line_dash="dot", line_color="yellow",
                          annotation_text="Début prédictions")
            
            fig5.update_layout(
                title="Données historiques et projections futures",
                xaxis_title="Année",
                yaxis_title=analyzer.config['unit'],
                template='plotly_dark',
                height=400
            )
            st.plotly_chart(fig5, use_container_width=True)
        
        # Analyse statistique
        st.markdown("---")
        st.subheader("📊 Analyse statistique approfondie")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("**📈 Statistiques descriptives**")
            stats_df = df[['Base_Value', 'Activity_Level', 'Solar_Index']].describe()
            st.dataframe(stats_df.style.format("{:.2f}"))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("**🔄 Analyse des cycles**")
            
            # Détection des cycles
            from scipy import signal
            values = df['Base_Value'].values
            peaks, _ = signal.find_peaks(values, distance=5)
            
            st.metric("Nombre de cycles détectés", len(peaks))
            if len(peaks) > 1:
                avg_cycle = np.mean(np.diff(df['Year'].iloc[peaks]))
                st.metric("Durée moyenne du cycle", f"{avg_cycle:.1f} ans")
            
            # Corrélations
            corr_matrix = df[['Base_Value', 'Activity_Level', 'Solar_Index', 
                            'Secular_Trend']].corr()
            st.write("**Matrice de corrélation:**")
            st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm'))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("**🎯 Événements majeurs**")
            
            events_data = {
                "Année": [1859, 1958, 2003, 2012],
                "Événement": ["Éruption Carrington", "Cycle 19 (Max)", "Éruptions Halloween", "Tempête manquée"],
                "Impact": ["+50% activité", "+40% activité", "+25% activité", "+10% activité"]
            }
            events_df = pd.DataFrame(events_data)
            st.dataframe(events_df, use_container_width=True)
            
            st.write("**Grands minima:**")
            minima_data = {
                "Période": ["1645-1715", "1790-1820", "2008-2009"],
                "Nom": ["Minimum Maunder", "Minimum Dalton", "Minimum moderne"],
                "Réduction": ["-70%", "-40%", "-20%"]
            }
            minima_df = pd.DataFrame(minima_data)
            st.dataframe(minima_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Visualisation avancée
        st.markdown("---")
        st.subheader("🔍 Visualisations avancées")
        
        tab1, tab2, tab3 = st.tabs(["📈 Distribution", "🔄 Phase space", "📊 Heatmap"])
        
        with tab1:
            fig6 = go.Figure()
            fig6.add_trace(go.Histogram(x=df['Base_Value'], nbinsx=50,
                                        name='Distribution', marker_color=analyzer.config['color']))
            fig6.update_layout(
                title=f"Distribution des valeurs - {analyzer.config['description']}",
                xaxis_title=analyzer.config['unit'],
                yaxis_title="Fréquence",
                template='plotly_dark',
                bargap=0.1
            )
            st.plotly_chart(fig6, use_container_width=True)
        
        with tab2:
            fig7 = go.Figure()
            fig7.add_trace(go.Scatter(x=df['Base_Value'], y=df['Activity_Level'],
                                      mode='markers', marker=dict(
                                          size=8,
                                          color=df['Year'],
                                          colorscale='Viridis',
                                          showscale=True,
                                          colorbar=dict(title="Année")
                                      ),
                                      text=df['Year'],
                                      name='Phase space'))
            fig7.update_layout(
                title="Espace des phases: Valeur vs Activité",
                xaxis_title=analyzer.config['unit'],
                yaxis_title="Niveau d'activité (%)",
                template='plotly_dark'
            )
            st.plotly_chart(fig7, use_container_width=True)
        
        with tab3:
            # Heatmap des corrélations
            corr_columns = ['Base_Value', 'Solar_Minimum', 'Solar_Maximum', 
                           'Secular_Trend', 'Activity_Level', 'Solar_Index']
            corr_matrix = df[corr_columns].corr()
            
            fig8 = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmin=-1, zmax=1,
                text=corr_matrix.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 10}
            ))
            fig8.update_layout(
                title="Matrice de corrélation",
                template='plotly_dark',
                height=500
            )
            st.plotly_chart(fig8, use_container_width=True)
        
        # Export des données
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger les données (CSV)",
                data=csv,
                file_name=f"solar_{selected_type}_data_{start_year}_{end_year}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Aperçu des données
            with st.expander("👀 Aperçu des données"):
                st.dataframe(df.head(10), use_container_width=True)
                st.write(f"**Dimensions:** {df.shape[0]} lignes, {df.shape[1]} colonnes")
        
        with col3:
            # Métadonnées
            with st.expander("ℹ️ Métadonnées"):
                st.write(f"**Type de données:** {analyzer.config['description']}")
                st.write(f"**Unité:** {analyzer.config['unit']}")
                st.write(f"**Période:** {start_year} - {end_year}")
                st.write(f"**Cycle solaire:** {analyzer.config['cycle_years']} ans")
                st.write(f"**Tendance:** {analyzer.config['trend']}")

if __name__ == "__main__":
    main()
