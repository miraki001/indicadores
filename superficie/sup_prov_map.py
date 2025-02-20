 f = data[0].to_json(orient="records")

  #st.write(f)  

  json_obj = json.loads(f)


  #st.write(json_obj)  
  raw_data = json_obj



  with open("./data/argentina.json", "r") as f:
        map = Map(
            "Argentina",
            json.loads(f.read()),
        )
  #render_usa,

  
  options = {
        "title": {
            "text": "Despachos por Provincias",
#            "subtext": "Data from www.census.gov",
#            "sublink": "http://www.census.gov/popest/data/datasets.html",
            "left": "right",
        },
        "tooltip": {
            "trigger": "item",
            "showDelay": 0,
            "transitionDuration": 0.2,
#            "formatter": formatter,
        },
        "visualMap": {
            "left": "right",
            "min": 5000,
            "max": 14000000,
            "inRange": {
                "color": [
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ]
            },
            "text": ["High", "Low"],
            "calculable": True,
        },
        "toolbox": {
            "show": True,
            "left": "left",
            "top": "top",
            "feature": {
                "dataView": {"readOnly": False},
                "restore": {},
                "saveAsImage": {},
            },
        },
        "series": [
            {
                "name": "Despachos por Provincias",
                "type": "map",
                "roam": True,
                "map": "Argentina",
                "emphasis": {"label": {"show": True}},
                "data": raw_data,
            }
        ],
  }
  st_echarts(options, map=map)
