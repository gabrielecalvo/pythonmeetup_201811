import folium

def create_glasgow_map_from_fsa_data(df):
    m = folium.Map(
        location=[55.863823, -4.267681],
        zoom_start=12,
        tiles='cartodbpositron'
    )

    rating_color={
        'fhis_awaiting_inspection_en-GB': 'gray',
        'fhis_improvement_required_en-GB': 'red',
        'fhis_pass_en-GB': 'yellow',
        'fhis_pass_and_eat_safe_en-GB': 'green',
    }

    for _, row in df.iterrows():   
        info_txt = "<b>{}</b><br>(<i>{}</i>, {})".format(row.BusinessName.replace("'", "`"), row.RatingValue, row.RatingDate)
        folium.Circle(
            radius=3,
            location=[row.Latitude, row.Longitude],
            tooltip=info_txt,
            color='black',
            weight=0.5,
            fill_opacity=0.8,
            fill_color=rating_color[row.RatingKey],
            fill=True,
        ).add_to(m)

    m.save('food_safety.html')
    print("Saved :)")