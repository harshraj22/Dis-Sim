import streamlit as st
import requests

st.set_page_config(page_title="Frontend Service", page_icon="🤖", initial_sidebar_state="collapsed")
st.title('Check Image Similarity')


if 'token' not in st.session_state:
    st.session_state['token'] = None

if st.session_state.token is None:
    # Registration form
    with st.expander('Register New User'):
        with st.form('Register'):
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            confirm_password = st.text_input('Confirm Password', type='password')
            register = st.form_submit_button('Register')
            if register:
                if password == confirm_password:
                    r = requests.post('http://auth:8019/register', json={'username': username, 'password': password})
                    if r.status_code == 201:
                        st.success('Registration successful')
                    else:
                        st.error('Registration failed')
                else:
                    st.error('Passwords do not match')

    with st.form('Authenticate'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        authenticate = st.form_submit_button('Login')
        if authenticate:
            r = requests.post('http://auth:8019/login', json={'username': username, 'password': password})

            if r.status_code == 200:
                st.success('Login successful')
                st.session_state['token'] = r.json()['token']
            else:
                st.error('Login failed')

if st.session_state.token is not None:
    # https://betterprogramming.pub/how-to-make-http-requests-in-streamlit-app-f22a77fd1ed7
    with st.form('Image Similarity'):
        img1 = st.file_uploader("Choose img1", type=["png", "jpg", "jpeg"])
        img2 = st.file_uploader("Choose img2", type=["png", "jpg", "jpeg"])

        img_form_submitted = st.form_submit_button("Submit")

    if img_form_submitted:
        url = "http://api:8001/submit"
        headers = {"accept": "application/json", 'Authorization': f'Bearer {st.session_state.token}'}
        files = {"img1": img1, "img2": img2}

        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            id = response.json()
            st.success(f'Task id:')
            st.code(str(id))
        else:
            st.error(response.text)




    with st.form('Submission Status'):
        task_id = st.text_input('Task Id')
        task_status = st.form_submit_button('Get Status')

    if task_status:
        url = f"http://api:8001/status/{task_id}"
        response = requests.get(url)

        if response.status_code == 200:
            status = response.json()
            if status == 'SUCCESS':
                st.success(f'Status: {status}')
            elif status == 'PENDING':
                st.info(f'Status: {status}')
            else:
                st.error(f'Status: {status}')
        else:
            st.error(response.text)




    with st.form('Submission result'):
        task_id = st.text_input('Task Id')
        result = st.form_submit_button('Get result')

    if result:
        url = f"http://api:8001/result/{task_id}"
        response = requests.get(url)
        result = response.json()
        st.write(f'Similarity result: {result}')

        # if response.status_code == 200:
    with st.form('Feedback'):
        task_id = st.text_input('Task Id')
        feedback_response = st.checkbox('Is the result accurate?')
        submit_feedback = st.form_submit_button('Submit Feedback')

    if submit_feedback:
        feedback_url = f"http://api:8001/feedback/"
        feedback_response_data = {"task_id": task_id, "response": bool(feedback_response)}
        feedback_headers = {"accept": "application/json", 'Authorization': f'Bearer {st.session_state.token}'}

        feedback_response = requests.post(feedback_url, headers=feedback_headers, json=feedback_response_data)
        print(f'Feedback response: {feedback_response}')

        if feedback_response.status_code == 200:
            st.success('Feedback submitted successfully')
        else:
            st.error('Failed to submit feedback')