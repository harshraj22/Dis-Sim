import streamlit as st
import requests

st.set_page_config(page_title="Frontend Service", page_icon="🤖")
st.title('Check Image Similarity')

# https://betterprogramming.pub/how-to-make-http-requests-in-streamlit-app-f22a77fd1ed7
with st.form('Image Similarity'):
    img1 = st.file_uploader("Choose img1", type=["png", "jpg", "jpeg"])
    img2 = st.file_uploader("Choose img2", type=["png", "jpg", "jpeg"])

    img_form_submitted = st.form_submit_button("Submit")

if img_form_submitted:
    url = "http://api:8001/submit"
    headers = {"accept": "application/json"}
    files = {"img1": img1, "img2": img2}

    response = requests.post(url, headers=headers, files=files)

    id = response.json()
    st.write(f'Task id:')
    st.code(str(id))





with st.form('Submission Status'):
    task_id = st.text_input('Task Id')
    task_status = st.form_submit_button('Get Status')

if task_status:
    url = f"http://api:8001/status/{task_id}"
    response = requests.get(url)
    status = response.json()
    st.write(f'Status: {status}')





with st.form('Submission result'):
    task_id = st.text_input('Task Id')
    result = st.form_submit_button('Get result')

if result:
    url = f"http://api:8001/result/{task_id}"
    response = requests.get(url)
    result = response.json()
    st.write(f'Similarity result: {result}')