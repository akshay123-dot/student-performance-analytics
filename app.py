import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "students.csv"


# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    try:
        return pd.read_csv(FILE_NAME)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "Student_ID", "Name", "Class",
            "Math", "Science", "English"
        ])


# -----------------------------
# SAVE DATA
# -----------------------------
def save_data(df):
    df.to_csv(FILE_NAME, index=False)


# -----------------------------
# DELETE STUDENT
# -----------------------------
def delete_student(df, sid):
    df = df[df["Student_ID"] != sid]
    return df


# -----------------------------
# GRADE FUNCTION
# -----------------------------
def grade(p):
    if p >= 80:
        return "A"
    elif p >= 60:
        return "B"
    elif p >= 40:
        return "C"
    else:
        return "Fail"


# -----------------------------
# PERFORMANCE
# -----------------------------
def performance(df):
    subjects = ["Math", "Science", "English"]

    df["Total"] = df[subjects].sum(axis=1)
    df["Average"] = df[subjects].mean(axis=1)
    df["Percentage"] = (df["Total"] / 300) * 100
    df["Grade"] = df["Percentage"].apply(grade)

    return df


# -----------------------------
# UI START
# -----------------------------
st.title("🎓 Student Performance Analytics System")

df = load_data()

menu = st.sidebar.selectbox(
    "Menu",
    ["View Students", "Add Student", "Delete Student", "Analytics", "Graph"]
)


# -----------------------------
# VIEW STUDENTS
# -----------------------------
if menu == "View Students":
    st.subheader("Student Records")
    st.dataframe(df)


# -----------------------------
# ADD STUDENT
# -----------------------------
elif menu == "Add Student":
    st.subheader("Add Student")

    sid = st.number_input("Student ID", step=1)
    name = st.text_input("Name")
    cls = st.text_input("Class")

    math = st.number_input("Math Marks", step=1)
    science = st.number_input("Science Marks", step=1)
    english = st.number_input("English Marks", step=1)

    if st.button("Add Student"):
        new = pd.DataFrame([{
            "Student_ID": sid,
            "Name": name,
            "Class": cls,
            "Math": math,
            "Science": science,
            "English": english
        }])

        df = pd.concat([df, new], ignore_index=True)
        save_data(df)

        st.success("Student Added Successfully")


# -----------------------------
# DELETE STUDENT
# -----------------------------
elif menu == "Delete Student":
    st.subheader("Delete Student")

    sid = st.number_input("Enter Student ID to Delete", step=1)

    if st.button("Delete Student"):
        if sid in df["Student_ID"].values:
            df = delete_student(df, sid)
            save_data(df)
            st.success("Student Deleted Successfully")
        else:
            st.error("Student Not Found")


# -----------------------------
# ANALYTICS
# -----------------------------
elif menu == "Analytics":
    st.subheader("Analytics")

    if len(df) > 0:
        df = performance(df)

        st.write(df)

        st.write("Top Students")
        st.dataframe(df.sort_values("Percentage", ascending=False).head(5))

        st.write("Weak Students")
        st.dataframe(df[df["Percentage"] < 40])

        st.write("Subject Average")
        st.write(df[["Math", "Science", "English"]].mean())

        st.write("Class Wise Performance")
        st.write(df.groupby("Class")["Percentage"].mean())


# -----------------------------
# GRAPH
# -----------------------------
elif menu == "Graph":
    st.subheader("Subject Wise Average Graph")

    if len(df) > 0:
        df = performance(df)

        avg = {
            "Math": df["Math"].mean(),
            "Science": df["Science"].mean(),
            "English": df["English"].mean()
        }

        fig, ax = plt.subplots()
        ax.bar(avg.keys(), avg.values())

        ax.set_ylabel("Marks")
        ax.set_title("Subject Wise Average")

        st.pyplot(fig)