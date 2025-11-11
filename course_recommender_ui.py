import pandas as pd
import streamlit as st
import requests

FASTAPI_URL = "https://mist460-course-recommender-apis-kenney.azurewebsites.net"

def fetch_data(endpoint : str, params : dict, method: str = "get") -> pd.DataFrame:
    if method == "get":
        response = requests.get(f"{FASTAPI_URL}/{endpoint}", params=params)
    elif method == "post":
        response = requests.post(f"{FASTAPI_URL}/{endpoint}", params=params)
    else:
        st.error(f"Unsupported HTTP method: {method}")
        return None

if response.status_code == 200:
    payload = response.json()
    rows = payload.get("data", [])
    df = pd.DataFrame(rows)
    return df

else:
    st.error(f"Error fetching data: {response.status_code}")
    return None

#create a sidebar with a dropdown to select the API endpoint
st.sidebar.title("Course Recommender Functionalities")
api_endpoint = st.sidebar.selectbox(
    "api endpoint",
    [
        "validate user",
        "find_current_semester_course_offerings",
        "find_prerequisites",
        "check_if_student_has_taken_all_prerequisites_for_course",
        "enroll_student_in_course_offering",
        "get_student_enrolled_course_offerings",
        "drop_student_from_course_offering"
    ]
)

if api_endpoint == "validate_user":
    st.header("Validate User")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Validate"):
        df = fetch_data("validate_user", {"username": username, "password": password})
        if df is not None:
            st.success("User validated successfully!")
        else:
            st.error("Invalid username or password.")

elif api_endpoint == "find_current_semester_course_offerings":
    st.header("Find Current Semester Course Offerings")
    df = fetch_data("find_current_semester_course_offerings", {})
    if df is not None:
        st.dataframe(df)
    else:
        st.error("Failed to fetch course offerings.")

elif api_endpoint == "find_prerequisites":
    st.header("Find Prerequisites for a Course")
    course_id = st.text_input("Course ID")
    if st.button("Find Prerequisites"):
        df = fetch_data("find_prerequisites", {"course_id": course_id})
        if df is not None:
            st.dataframe(df)
        else:
            st.error("Failed to fetch prerequisites.")

elif api_endpoint == "check_if_student_has_taken_all_prerequisites_for_course":
    st.header("Check if Student has Taken all Prerequisites for a Course")
    student_id = st.text_input("Student ID")
    course_id = st.text_input("Course ID")
    if st.button("Check Prerequisites"):
        df = fetch_data("check_if_student_has_taken_all_prerequisites_for_course", {"student_id": student_id, "course_id": course_id})
        if df is not None:
            st.dataframe(df)
        else:
            st.error("Failed to check prerequisites.")

elif api_endpoint == "enroll_student_in_course_offering":
    st.header("Enroll Student in Course Offering")
    student_id = st.text_input("Student ID")
    course_offering_id = st.text_input("Course Offering ID")
    if st.button("Enroll"):
        df = fetch_data("enroll_student_in_course_offering", {"student_id": student_id, "course_offering_id": course_offering_id}, method="post")
        if df is not None:
            st.success("Student enrolled successfully!")
        else:
            st.error("Failed to enroll student.")

elif api_endpoint == "get_student_enrolled_course_offerings":
    st.header("Get Student Enrolled Course Offerings")
    student_id = st.text_input("Student ID")
    if st.button("Get Enrollments"):
        df = fetch_data("get_student_enrolled_course_offerings", {"student_id": student_id})
        if df is not None:
            st.dataframe(df)
        else:
            st.error("Failed to fetch enrolled course offerings.")

elif api_endpoint == "drop_student_from_course_offering":
    st.header("Drop Student from Course Offering")
    student_id = st.text_input("Student ID")
    course_offering_id = st.text_input("Course Offering ID")
    if st.button("Drop"):
        df = fetch_data("drop_student_from_course_offering", {"student_id": student_id, "course_offering_id": course_offering_id}, method="post")
        if df is not None:
            st.success("Student dropped from course offering successfully!")
        else:
            st.error("Failed to drop student from course offering.")

