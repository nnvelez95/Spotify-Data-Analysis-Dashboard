import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
import numpy as np

def load_enhanced_data():
    # Crear datos más realistas y extensos
    np.random.seed(42)
    
    artists = ['The Weeknd', 'Dua Lipa', 'Bad Bunny', 'Taylor Swift', 'Ed Sheeran', 
               'Billie Eilish', 'The Beatles', 'Rosalía', 'J Balvin', 'Olivia Rodrigo']
    
    genres = {
        'The Weeknd': 'Pop/R&B',
        'Dua Lipa': 'Pop/Dance',
        'Bad Bunny': 'Reggaeton',
        'Taylor Swift': 'Pop',
        'Ed Sheeran': 'Pop/Folk',
        'Billie Eilish': 'Alternative',
        'The Beatles': 'Rock',
        'Rosalía': 'Flamenco/Pop',
        'J Balvin': 'Reggaeton',
        'Olivia Rodrigo': 'Pop/Rock'
    }
    
    data = []
    for i in range(100):  # 100 canciones
        artist = np.random.choice(artists)
        data.append({
            'track_name': f"Canción {i+1}",
            'artist': artist,
            'genre': genres[artist],
            'duration_ms': np.random.randint(180000, 300000),
            'popularity': np.random.randint(70, 100),
            'danceability': round(np.random.uniform(0.3, 0.9), 2),
            'energy': round(np.random.uniform(0.4, 0.95), 2),
            'valence': round(np.random.uniform(0.2, 0.8), 2),
            'acousticness': round(np.random.uniform(0.0, 0.6), 2),
            'tempo': np.random.randint(80, 160),
            'play_count': np.random.randint(10, 100),
            'release_date': (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(data)

def create_enhanced_dashboard(selected_artists, selected_genre, min_popularity):
    df = load_enhanced_data()
    
    # Aplicar filtros
    df_filtered = df.copy()
    
    if selected_artists:
        df_filtered = df_filtered[df_filtered['artist'].isin(selected_artists)]
    
    if selected_genre != "Todos":
        df_filtered = df_filtered[df_filtered['genre'] == selected_genre]
    
    df_filtered = df_filtered[df_filtered['popularity'] >= min_popularity]
    
    # Calcular KPIs
    avg_popularity = df_filtered['popularity'].mean()
    total_tracks = len(df_filtered)
    total_plays = df_filtered['play_count'].sum()
    avg_danceability = df_filtered['danceability'].mean()
    avg_energy = df_filtered['energy'].mean()
    
    kpis_html = f"""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0;">
        <div style="background: #f0f8ff; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; color: #333;">🎵 Canciones</h3>
            <p style="font-size: 24px; font-weight: bold; color: #0066cc;">{total_tracks}</p>
        </div>
        <div style="background: #fff0f5; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; color: #333;">⭐ Popularidad</h3>
            <p style="font-size: 24px; font-weight: bold; color: #cc0066;">{avg_popularity:.0f}</p>
        </div>
        <div style="background: #f0fff0; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; color: #333;">💃 Bailabilidad</h3>
            <p style="font-size: 24px; font-weight: bold; color: #00cc66;">{avg_danceability:.2f}</p>
        </div>
        <div style="background: #fff8f0; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; color: #333;">🔥 Reproducciones</h3>
            <p style="font-size: 24px; font-weight: bold; color: #ff6600;">{total_plays}</p>
        </div>
    </div>
    """
    
    # 1. Gráfico de torta - Distribución por artista
    if not df_filtered.empty:
        artist_counts = df_filtered['artist'].value_counts()
        fig_pie = px.pie(
            values=artist_counts.values,
            names=artist_counts.index,
            title="📊 Distribución por Artista"
        )
    else:
        fig_pie = px.pie(title="No hay datos con los filtros seleccionados")
    
    # 2. Scatter plot - Popularidad vs Bailabilidad
    fig_scatter = px.scatter(
        df_filtered,
        x='danceability',
        y='popularity',
        size='play_count',
        color='artist',
        hover_name='track_name',
        title="🎯 Popularidad vs Bailabilidad",
        size_max=20
    )
    
    # 3. Gráfico de barras - Top canciones por popularidad
    top_tracks = df_filtered.nlargest(10, 'popularity')
    fig_bar = px.bar(
        top_tracks,
        x='popularity',
        y='track_name',
        color='artist',
        orientation='h',
        title="🏆 Top Canciones por Popularidad"
    )
    
    # 4. Heatmap de correlación
    numeric_cols = ['popularity', 'danceability', 'energy', 'valence', 'acousticness', 'tempo', 'play_count']
    corr_matrix = df_filtered[numeric_cols].corr()
    fig_heatmap = px.imshow(
        corr_matrix,
        title="📈 Matriz de Correlación",
        aspect="auto",
        color_continuous_scale="RdBu"
    )
    
    # 5. Radar chart para características de audio (promedio por artista)
    if not df_filtered.empty:
        audio_features = ['danceability', 'energy', 'valence', 'acousticness']
        avg_by_artist = df_filtered.groupby('artist')[audio_features].mean().reset_index()
        
        fig_radar = go.Figure()
        
        for _, row in avg_by_artist.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row[col] for col in audio_features] + [row[audio_features[0]]],
                theta=audio_features + [audio_features[0]],
                fill='toself',
                name=row['artist']
            ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            title="🎼 Características de Audio por Artista"
        )
    else:
        fig_radar = go.Figure()
        fig_radar.update_layout(title="No hay datos para el gráfico de radar")
    
    return (
        kpis_html,
        pio.to_html(fig_pie),
        pio.to_html(fig_scatter),
        pio.to_html(fig_bar),
        pio.to_html(fig_heatmap),
        pio.to_html(fig_radar),
        df_filtered[['track_name', 'artist', 'genre', 'popularity', 'danceability', 'energy', 'play_count']].to_html(classes='table table-striped', index=False)
    )

# Interfaz mejorada de Gradio
with gr.Blocks(theme=gr.themes.Soft(), title="Spotify Advanced Analysis") as demo:
    gr.Markdown("""
    # 🎵 Spotify Advanced Data Analysis Dashboard
    *Análisis completo de tus hábitos de escucha musical*
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🎛️ Panel de Control")
            artist_selector = gr.Dropdown(
                label="Seleccionar Artistas",
                choices=['The Weeknd', 'Dua Lipa', 'Bad Bunny', 'Taylor Swift', 'Ed Sheeran', 
                        'Billie Eilish', 'The Beatles', 'Rosalía', 'J Balvin', 'Olivia Rodrigo'],
                multiselect=True
            )
            
            genre_selector = gr.Dropdown(
                label="Filtrar por Género",
                choices=["Todos", "Pop", "Pop/R&B", "Pop/Dance", "Reggaeton", "Pop/Folk", 
                        "Alternative", "Rock", "Flamenco/Pop", "Pop/Rock"],
                value="Todos"
            )
            
            popularity_slider = gr.Slider(
                minimum=0,
                maximum=100,
                value=70,
                label="Popularidad Mínima"
            )
            
            update_btn = gr.Button("🔄 Actualizar Dashboard", variant="primary")
        
        with gr.Column(scale=3):
            kpis_display = gr.HTML(label="Métricas Principales")
            
            with gr.Row():
                pie_display = gr.HTML(label="Distribución Artistas")
                scatter_display = gr.HTML(label="Popularidad vs Bailabilidad")
            
            with gr.Row():
                bar_display = gr.HTML(label="Top Canciones")
                heatmap_display = gr.HTML(label="Matriz Correlación")
            
            with gr.Row():
                radar_display = gr.HTML(label="Análisis Audio")
            
            with gr.Row():
                table_display = gr.HTML(label="Datos Detallados")
    
    # Conectar el botón
    update_btn.click(
        fn=create_enhanced_dashboard,
        inputs=[artist_selector, genre_selector, popularity_slider],
        outputs=[kpis_display, pie_display, scatter_display, bar_display, heatmap_display, radar_display, table_display]
    )

if __name__ == "__main__":
    demo.launch(share=True)  # share=True te da un link público