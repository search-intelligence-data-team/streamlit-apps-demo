from bs4 import BeautifulSoup 

#import leafmap

import streamlit.components.v1 as components
import streamlit as st

st.set_page_config(
    page_title = 'Demo Apps'
)

st.title('Index Page')
st.sidebar.success('Select a page.')

m = leafmap.Map(center=[51, 0], zoom=5)

map_html = m.to_html()
#print(map_html)

map_html2 = str(BeautifulSoup(map_html).find('body'))[6:-7]
#print(map_html2)

st.markdown('<h2>something</h2>', unsafe_allow_html=True)
#st.markdown(map_html2, unsafe_allow_html=True)
m.to_streamlit(width=400, height=700)
#st.pydeck_chart(m)

components.html(map_html)

st.markdown('<h2>something else</h2>', unsafe_allow_html=True)
#print(type(map_html))