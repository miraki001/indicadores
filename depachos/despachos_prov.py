  conn = st.connection("postgresql", type="sql")
  df1 = conn.query('select anio||mes anio,tintos,blancos,rosados from info_desp_anio_mes_v1;', ttl="0"),

  df2 = df1[0]
 
  st.subheader('Evolución de los despachos por Mes')

  if st.checkbox('Ver datos como tabla'):
    st.write(df)




  option = {
    "dataZoom": [
    {
      "show": 'true',
      "realtime": 'true',
      "start": 0,
      "end": 100,
      "xAxisIndex": [0, 1]
    },
    {
      "type": 'inside',
      "realtime": 'true',
      "start": 30,
      "end": 70,
      "xAxisIndex": [0, 1]
    }
    ],
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df2['anio'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df2['tintos'].to_list(), "type": "line", "name": 'Tintos'},
               {"data": df2['blancos'].to_list(), "type": "line", "name": 'Blancos'},
               {"data": df2['rosados'].to_list(), "type": "line", "name": 'Rosados'},
               ]
  }
  st_echarts(
    options=option, height="400px" ,
  )

    
  st.subheader('Evolución de los despachos por Provincias')
 
  conn = st.connection("postgresql", type="sql")
  dfp = conn.query('select initcap(provincia) provincia from dimprovincia;', ttl="0"),
  dfpv = dfp[0]
  new_row = pd.DataFrame({"provincia": ["Todas"]})
  dfpv = pd.concat([dfpv, new_row], ignore_index=True)

  #st.write(dfpv)
  dfe = conn.query('select subgrupoenvase from dimsubgrupoenvase;', ttl="0"),
  dfev = dfe[0]
  new_row1 = pd.DataFrame({"subgrupoenvase": ["Todos"]})
  dfev = pd.concat([dfev, new_row1], ignore_index=True)


  col1, col2 = st.columns(2)

  with col1:
    prov = st.multiselect(
      "Seleccionar Provincia",dfpv.provincia
    )
    all_options = st.button("Select all options")
    if all_options:
        prov = dfpv.provincia,
    
    #selected_options
  with col2:
    envase = st.multiselect(
        "Seleccionar Tipo de Envase",dfev.subgrupoenvase
    )

  st.write("You selected:", prov)
  #if prov == "Todas":
  qu = 'select año anio,sum(cnt) cnt,provincia,subgrupoenvase from inf_desp_prov group by provincia,año,subgrupoenvase ;'  
  dfpv1 = conn.query(qu, ttl="0"),
  #if prov != "Todas": 
  #  qu = 'select cnt,provincia from inf_desp_prov where provincia =  :prov;'
  #  dfpv1 = conn.query(qu, ttl="0", params={"prov": prov},),
  dfpv1 = dfpv1[0]
  dfpv1 = dfpv1[dfpv1['anio'] > 2010]
  #dfpv1 = dfpv1[dfpv1['provincia'].isin(prov)]
  #st.write(dfpv1)

  df = dfpv1.pivot_table(index='anio', columns='provincia', values='cnt')
  #st.write('df')
  #st.write(df)
  df = df.reset_index() 
  #st.write(df)
  #st.write(df[2021])

  dfpv2 = dfpv1.transpose()
  #st.write(dfpv2)
  #st.write('dfpv2')
  #st.write(dfpv2.transpose())
  ds = dfpv2.transpose(),
  #ds = ds.reset_index() 
  #dfpv2['anio'] = dfpv2['anio'].astype(str)

  #newdf=dfpv2.set_index('anio',inplace=False).rename_axis(None)



  option = {
    "dataZoom": [
    {
      "show": 'true',
      "realtime": 'true',
      "start": 0,
      "end": 100,
      "xAxisIndex": [0, 1]
    },
    {
      "type": 'inside',
      "realtime": 'true',
      "start": 30,
      "end": 70,
      "xAxisIndex": [0, 1]
    }
    ],
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df['anio'].to_list(),
    },
    "yAxis": [{"type": "value"}],
    "series": [
            {
                "name": "Mendoza",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":  df['Mendoza'].to_list(),
            },
            {
                "name": "San Juan",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df['San Juan'].to_list(),
            },
            {
                "name": "La Rioja",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df['La Rioja'].to_list(),
            },
            {
                "name": "Cordoba",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df['Cordoba'].to_list(),
            },
            {
                "name": "Catamarca",
                "type": "line",
                "stack": "cnt",
#                "label": {"show": True, "position": "top"},
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":  df['Catamarca'].to_list(),
            },
            {
                "name": "Buenos Aires",
                "type": "line",
                "stack": "cnt",
#                "label": {"show": True, "position": "top"},
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":df['Buenos Aires'].to_list(),
            },
    ],    
  }

  st_echarts(
    options=option, height="400px" ,
  )

  de = dfpv1.pivot_table(index='anio', columns='subgrupoenvase', values='cnt')
  #de.replace(to_replace=[None], value=0, inplace=True)
  #de = de.fillna(value=np.nan)
  #st.write('antes')
  #de.fillna(0),
  de = de.reset_index() 
  de.round(0)
  de = de.round({'Bag in Box': 0})
  de = de.round({'Botella': 0})
  de = de.round({'Bidon': 0})
  de = de.round({'Multilaminado': 0})
  de = de.round({'Damajuana': 0})
  de = de.round({'Granel': 0})
  de.fillna(0),
  de.round(0)
  #st.write(de)
  #st.write('despues')
  option = {
    "dataZoom": [
    {
      "show": 'true',
      "realtime": 'true',
      "start": 0,
      "end": 100,
      "xAxisIndex": [0, 1]
    },
    {
      "type": 'inside',
      "realtime": 'true',
      "start": 30,
      "end": 70,
      "xAxisIndex": [0, 1]
    }
    ],
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": de['anio'].to_list(),
    },
    "yAxis": [{"type": "value"}],
    "series": [
            {
                "name": "Bag in Box",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":  de['Bag in Box'].to_list(),
            },
            {
                "name": "Bidon",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": de['Bidon'].to_list(),
            },
            {
                "name": "Botella",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": de['Botella'].to_list(),
            },
            {
                "name": "Damajuana",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": de['Damajuana'].to_list(),
            },
            {
                "name": "Granel",
                "type": "line",
                "stack": "cnt",
#                "label": {"show": True, "position": "top"},
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":  de['Granel'].to_list(),
            },
            {
                "name": "Multilaminado",
                "type": "line",
                "stack": "cnt",
#                "label": {"show": True, "position": "top"},
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":de['Multilaminado'].to_list(),
            },
    ],    
  }

  st_echarts(
    options=option, height="400px" ,
  )

  qu1 = 'select name,value from inf_desp_prov_tot ;'  
  data = conn.query(qu1, ttl="0"),
  #st.write(data[0])
  f = data[0].to_json(orient="records")

  #st.write(f)  

  json_obj = json.loads(f)


  st.write(json_obj)  
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
  

  qu2 = 'select anio||mes anio, cnt,producto from inf_desp_prod  ;'  
  prod1 = conn.query(qu2, ttl="0"),
  prod2 = prod1[0]
  #st.write(prod2)
  prod = prod2.pivot_table(index='anio', columns='producto', values='cnt')
  prod = prod.reset_index() 

  prod.round(0)
  prod = prod.round({'Vino Varietal': 0})
  prod = prod.round({'Vinos sin Mencion': 0})
  prod = prod.round({'Espumantes': 0})
  prod = prod.round({'Gasificados': 0})
  prod = prod.round({'Otros Vinos': 0})

  prod.fillna(0),
  prod.round(0)

  st.write(prod)



  option = {
    "dataZoom": [
    {
      "show": 'true',
      "realtime": 'true',
      "start": 0,
      "end": 100,
      "xAxisIndex": [0, 1]
    },
    {
      "type": 'inside',
      "realtime": 'true',
      "start": 30,
      "end": 70,
      "xAxisIndex": [0, 1]
    }
    ],
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": prod['anio'].to_list(),
    },
    "yAxis": [{"type": "value"}],
    "series": [
            {
                "name": "Vino Varietal",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":  prod['Vino Varietal'].to_list(),
            },
            {
                "name": "Vino Sin Mencion",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": prod['Vinos sin Mencion'].to_list(),
            },
            {
                "name": "Espumantes",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": prod['Espumantes'].to_list(),
            },

            {
                "name": "Otros Vinos",
                "type": "line",
                "stack": "cnt",
#                "label": {"show": True, "position": "top"},
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":  prod['Otros Vinos'].to_list(),
            },
    ],    
  }

  st_echarts(
    options=option, height="400px" ,
  )
if 'product_result' not in st.session_state:
    st.session_state.product_result = None

def cambiar_producto_cb(df):
    st.session_state.product_result = filter_by_producto(
        df, st.session_state.txt_searchairlinek)

def filter_by_producto(df, airline):
    #filtered_df = df[df['producto'].str.contains(producto, case=False)]
    filtered_df = df[df['producto'].str]
    unique_producto = filtered_df['producto'].unique()
    return unique_producto


with tab2:
    @st.cache_data
    def query():
        df3 = conn.query('select cantidadlitros lts,anio,mes,provincia,producto,subgrupoenvase,variedad1 from despachos_m  where anio > 2021  ;', ttl="0"),
        return df3
    df3 = query()
    df2 = df3[0]
    #st.write(df2)

    st.markdown(
        """
        <style>
        span[data-baseweb="tag"] {
        background-color: blue !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    

    col1, col2,col3,col4 = st.columns(4)

    with col1:
      with st.popover(label='Producto', use_container_width=True):
            cols = st.columns([2, 1], gap='small')
            with cols[0]:
                st_keyup('Search Producto', key='txt_searchairlinek',
                         on_change=cambiar_producto_cb, args=(df2,),
                         placeholder='type to search')
                st.dataframe(st.session_state.product_result, hide_index=True,
                             use_container_width=True, height=150)

            # Shows airline checkboxes
            for a in df2['producto'].unique():
                st.checkbox(a, value=True, key=a)

    with col2:
        selected_categories = st.multiselect('Productos:', df2['producto'].unique(),placeholder="")
        if selected_categories:
            # Filter the dataframe based on selected categories
            df2 = df2[df2['producto'].isin(selected_categories)]
    with col3:
        selected_prov = st.multiselect('Provincias:', df2['provincia'].unique() ,help=None,placeholder="")
        if selected_prov:
            # Filter the dataframe based on selected categories
            df2 = df2[df2['provincia'].isin(selected_prov)]
    with col4:
        selected_var = st.multiselect('variedad:', df2['variedad1'].unique() ,help=None,placeholder="")
        if selected_var:
            # Filter the dataframe based on selected categories
            df2 = df2[df2['variedad1'].isin(selected_var)]    
            
    pivot_table_basic = df2.pivot_table(
      index='mes', 
      columns='anio',  
      values=['lts'],
      aggfunc='sum'
    )
    
    dfg = pivot_table_basic
    dfg.columns = dfg.columns.droplevel(0)
    dfg = dfg.rename(columns={2022: "2022", 2023: "2023", 2024: "2024",'mes': " mes"})
    #st.write(dfg) 
    
    #pivot_table_basic.columns = pivot_table_basic.columns.droplevel(0)
    pivot_table_basic = pivot_table_basic.reset_index().rename_axis(None, axis=1)
    pivot_table_basic.loc['Total']= pivot_table_basic.sum(numeric_only=True,axis=0)
    pivot_table_basic['2023/2022'] = (1-(pivot_table_basic[2022]/pivot_table_basic[2023]))*100
    pivot_table_basic['2024/2023'] = (1-(pivot_table_basic[2023]/pivot_table_basic[2024]))*100
    pivot_table_basic = pivot_table_basic.rename(columns={2022: "2022", 2023: "2023", 2024: "2024",'mes': " mes"})

    pivot_table_basic = pivot_table_basic.sort_index(axis = 1)


    styled_df = pivot_table_basic.style.applymap(bgcolor_positive_or_negative, subset=['2023/2022','2024/2023']).format(
        {"2022": lambda x : '{:,.0f}'.format(x), 
        "2023": lambda x : '{:,.0f}'.format(x),
        "2024": lambda x : '{:,.0f}'.format(x),
        "2023/2022": lambda x : '{:,.2f} %'.format(x),
        "2024/2023": lambda x : '{:,.2f} %'.format(x),
                                        }
        ,
    thousands='.',
    decimal=',',
    )


    
    
    st.dataframe(styled_df,
      column_config={
        'mes': st.column_config.Column('Key'),
        '2022': st.column_config.Column('2022'),
        '2023': st.column_config.Column('2023'),
        '2024': st.column_config.Column('2024'),
        '2023/2022': st.column_config.Column('2023/2022'),
        '2024/2023': st.column_config.Column('2024/2023')
      },
      width = 600,   
      height = 500,
      hide_index=False)

    dfg = dfg.reset_index().rename_axis(None, axis=1)
    #st.write(dfg)  
    
    #dfg['mes'] = dfg['mes'].astype(str)

    #newdf=dfg.set_index('mes',inplace=False).rename_axis(None)

    option = {
        "dataZoom": [
        {
          "show": 'true',
          "realtime": 'true',
          "start": 0,
          "end": 100,
          "xAxisIndex": [0, 1]
        },
        {
          "type": 'inside',
          "realtime": 'true',
          "start": 30,
          "end": 70,
          "xAxisIndex": [0, 1]
        }
        ],
            "tooltip": {
            "trigger": 'axis',
            "axisPointer": { "type": 'cross' }
        },
        "legend": {},    
        "xAxis": {
            "type": "category",
            "data": dfg['mes'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": dfg['2022'].to_list(), "type": "line", "name": '2022'}
               ,{"data": dfg['2023'].to_list(), "type": "line","name":'2023'}
               ,{"data": dfg['2024'].to_list(), "type": "line","name":'2024'}                   
                  ]
    }
    st_echarts(
        options=option, height="400px" ,
    )
with tab4:
    @st.cache_data
    def query():
        df31 = conn.query('select cantidadlitros lts,anio,mes,provincia,producto,subgrupoenvase,variedad1 from despachos_m  where anio > 2021  ;', ttl="0"),
        return df31
    df31 = query()
    df21 = df31[0]
    desp_prov.despachos_prov(df21)
