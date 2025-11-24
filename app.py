import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from music_analyzer import music_analyzer

def create_global_music_dashboard(analysis_type, selected_genres, selected_artists):
    """Dashboard principal de análisis musical global"""
    
    # Cargar datos según el tipo de análisis
    df = music_analyzer.get_global_charts_data()
    
    if analysis_type == "Genre Analysis":
        title = "🌍 Análisis de Géneros Musicales Globales"
    elif analysis_type == "Artist Analysis":
        title = "🎤 Análisis de Artistas Globales"
    else:  # Trend Analysis
        title = "📈 Tendencias Musicales Globales"
    
    # Aplicar filtros
    df_filtered = df.copy()
    
    if selected_genres:
        df_filtered = df_filtered[df_filtered['genre'].isin(selected_genres)]
    
    if selected_artists:
        df_filtered = df_filtered[df_filtered['artist'].isin(selected_artists)]
    
    # KPIs globales
    total_tracks = len(df_filtered)
    avg_popularity = df_filtered['popularity'].mean()
    total_streams = df_filtered['streams_millions'].sum()
    unique_artists = df_filtered['artist'].nunique()
    
    kpis_html = f"""
    <div style="text-align: center; margin: 20px 0;">
        <h2>{title}</h2>
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <h4 style="margin: 0; font-size: 14px;">🎵 Canciones</h4>
            <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{total_tracks}</p>
        </div>
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <h4 style="margin: 0; font-size: 14px;">⭐ Popularidad</h4>
            <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{avg_popularity:.0f}</p>
        </div>
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <h4 style="margin: 0; font-size: 14px;">📊 Streams (M)</h4>
            <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{total_streams:.0f}</p>
        </div>
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <h4 style="margin: 0; font-size: 14px;">🎤 Artistas</h4>
            <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{unique_artists}</p>
        </div>
    </div>
    """
    
    # Visualizaciones según el tipo de análisis
    if analysis_type == "Genre Analysis":
        return genre_analysis(df_filtered, kpis_html)
    elif analysis_type == "Artist Analysis":
        return artist_analysis(df_filtered, kpis_html)
    else:  # Trend Analysis
        return trend_analysis(df_filtered, kpis_html)

def genre_analysis(df_filtered, kpis_html):
    """Análisis por género"""
    # Análisis por género
    genre_stats = df_filtered.groupby('genre').agg({
        'popularity': 'mean',
        'streams_millions': 'sum',
        'danceability': 'mean',
        'energy': 'mean'
    }).reset_index()
    
    fig1 = px.bar(
        genre_stats.sort_values('streams_millions', ascending=True),
        y='genre',
        x='streams_millions',
        title='📊 Streams por Género (Millones)',
        color='genre',
        orientation='h'
    )
    
    # Radar chart de características por género
    features = ['danceability', 'energy', 'valence', 'acousticness']
    fig2 = go.Figure()
    
    genres_to_show = genre_stats['genre'].head(4)  # Mostrar máximo 4 géneros
    
    for genre in genres_to_show:
        genre_data = df_filtered[df_filtered['genre'] == genre]
        if len(genre_data) > 0:
            avg_features = [genre_data[feature].mean() for feature in features]
            fig2.add_trace(go.Scatterpolar(
                r=avg_features + [avg_features[0]],
                theta=features + [features[0]],
                fill='toself',
                name=genre
            ))
    
    fig2.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        title='🎼 Características por Género',
        height=400
    )
    
    return kpis_html, pio.to_html(fig1), pio.to_html(fig2)

def artist_analysis(df_filtered, kpis_html):
    """Análisis por artista"""
    # Análisis por artista
    artist_stats = df_filtered.groupby('artist').agg({
        'popularity': 'mean',
        'streams_millions': 'sum',
        'genre': 'first'
    }).nlargest(12, 'streams_millions').reset_index()
    
    fig1 = px.bar(
        artist_stats,
        x='streams_millions',
        y='artist',
        color='genre',
        title='🏆 Top Artistas por Streams',
        orientation='h',
        height=400
    )
    
    # Scatter plot artistas
    fig2 = px.scatter(
        artist_stats,
        x='popularity',
        y='streams_millions',
        size='streams_millions',
        color='genre',
        hover_name='artist',
        title='📈 Popularidad vs Streams por Artista',
        size_max=30,
        height=400
    )
    
    return kpis_html, pio.to_html(fig1), pio.to_html(fig2)

def trend_analysis(df_filtered, kpis_html):
    """Análisis de tendencias"""
    # Análisis de tendencias
    weekly_trends = df_filtered.groupby('week').agg({
        'popularity': 'mean',
        'streams_millions': 'sum'
    }).reset_index()
    
    fig1 = px.line(
        weekly_trends,
        x='week',
        y='streams_millions',
        title='📈 Evolución Semanal de Streams',
        markers=True,
        height=400
    )
    
    # Distribución de características
    fig2 = px.box(
        df_filtered,
        x='genre',
        y='danceability',
        color='genre',
        title='💃 Distribución de Bailabilidad por Género',
        height=400
    )
    
    return kpis_html, pio.to_html(fig1), pio.to_html(fig2)

def update_artist_options(selected_genres):
    """Actualizar lista de artistas basado en géneros seleccionados"""
    df = music_analyzer.get_global_charts_data()
    
    if selected_genres:
        df_filtered = df[df['genre'].isin(selected_genres)]
        artists = sorted(df_filtered['artist'].unique().tolist())
    else:
        artists = sorted(df['artist'].unique().tolist())
    
    return gr.Dropdown(choices=artists, value=[])

# Interfaz de Gradio SIMPLIFICADA
with gr.Blocks() as demo:
    gr.Markdown("""
    # 🌍 Global Music Trends Analyzer
    **Análisis de tendencias musicales globales y comparativa entre géneros**
    
    *Datos simulados realistas de la industria musical global*
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🎛️ Configuración del Análisis")
            analysis_type = gr.Radio(
                choices=["Genre Analysis", "Artist Analysis", "Trend Analysis"],
                value="Genre Analysis",
                label="Tipo de Análisis"
            )
            
            gr.Markdown("### 🔍 Filtros")
            genre_selector = gr.Dropdown(
                label="Filtrar por Género",
                choices=music_analyzer.genres,
                multiselect=True,
                value=["Pop", "Hip-Hop", "Rock"]
            )
            
            artist_selector = gr.Dropdown(
                label="Filtrar por Artista",
                multiselect=True,
                value=[],
                interactive=True
            )
            
            update_btn = gr.Button("🔄 Generar Análisis", variant="primary")
            
            gr.Markdown("""
            ### 💡 Tipos de Análisis
            - **Genre Analysis**: Comparativa entre géneros musicales
            - **Artist Analysis**: Ranking y análisis de artistas  
            - **Trend Analysis**: Evolución temporal y tendencias
            """)
        
        with gr.Column(scale=3):
            kpis_display = gr.HTML()
            with gr.Row():
                chart1_display = gr.HTML()
            with gr.Row():
                chart2_display = gr.HTML()
    
    # Conectar eventos
    update_btn.click(
        fn=create_global_music_dashboard,
        inputs=[analysis_type, genre_selector, artist_selector],
        outputs=[kpis_display, chart1_display, chart2_display]
    )
    
    # Actualizar artistas cuando cambien los géneros
    genre_selector.change(
        fn=update_artist_options,
        inputs=genre_selector,
        outputs=artist_selector
    )

if __name__ == "__main__":
    print("🚀 Iniciando Global Music Analysis...")
    demo.launch(
        server_name="127.0.0.1", 
        server_port=7860, 
        share=True
    )