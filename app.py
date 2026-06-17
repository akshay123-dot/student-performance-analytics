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
            "Student_ID",
            "Name",
            "Class",
            "Math",
            "Science",
            "English"
        ])


# -----------------------------
# SAVE DATA
# -----------------------------
def save_data(df):
    df.to_csv(FILE_NAME, index=False)


# -----------------------------
# GRADE
# -----------------------------
def grade(percent):
    if percent >= 80:
        return "A"
    elif percent >= 60:
        return "B"
    elif percent >= 40:
        return "C"
    else:
        return "Fail"


# -----------------------------
# PERFORMANCE
# -----------------------------
def calculate_performance(df):

    subjects = ["Math", "Science", "English"]

    df["Total"] = df[subjects].sum(axis=1)

    df["Average"] = df[subjects].mean(axis=1)

    df["Percentage"] = (df["Total"] / 300) * 100

    df["Grade"] = df["Percentage"].apply(grade)

    return df


# -----------------------------
# TITLE
# -----------------------------
st.title("🎓 Student Performance Analytics System")

df = load_data()

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "View Students",
        "Add Student",
        "Update Student",
        "Delete Student",
        "Analytics",
        "Graphs",
        "Export Report"
    ]
)

# -----------------------------
# VIEW
# -----------------------------
if menu == "View Students":

    st.subheader("Student Records")

    st.dataframe(df)

# -----------------------------
# ADD
# -----------------------------
elif menu == "Add Student":

    st.subheader("Add New Student")

    sid = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    name = st.text_input("Name")

    cls = st.text_input("Class")

    math = st.number_input(
        "Math",
        min_value=0,
        max_value=100
    )

    science = st.number_input(
        "Science",
        min_value=0,
        max_value=100
    )

    english = st.number_input(
        "English",
        min_value=0,
        max_value=100
    )

    if st.button("Add Student"):

        if not name or not cls:
            st.error("All fields required")

        elif sid in df["Student_ID"].values:
            st.error("Student ID already exists")

        else:

            new_student = pd.DataFrame([{
                "Student_ID": sid,
                "Name": name,
                "Class": cls,
                "Math": math,
                "Science": science,
                "English": english
            }])

            df = pd.concat(
                [df, new_student],
                ignore_index=True
            )

            save_data(df)

            st.success("Student Added Successfully")

# -----------------------------
# UPDATE
# -----------------------------
elif menu == "Update Student":

    st.subheader("Update Student Marks")

    sid = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    math = st.number_input(
        "New Math Marks",
        min_value=0,
        max_value=100
    )

    science = st.number_input(
        "New Science Marks",
        min_value=0,
        max_value=100
    )

    english = st.number_input(
        "New English Marks",
        min_value=0,
        max_value=100
    )

    if st.button("Update"):

        if sid in df["Student_ID"].values:

            df.loc[
                df["Student_ID"] == sid,
                ["Math", "Science", "English"]
            ] = [math, science, english]

            save_data(df)

            st.success("Updated Successfully")

        else:
            st.error("Student Not Found")

# -----------------------------
# DELETE
# -----------------------------
elif menu == "Delete Student":

    st.subheader("Delete Student")

    sid = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    if st.button("Delete"):

        if sid in df["Student_ID"].values:

            df = df[
                df["Student_ID"] != sid
            ]

            save_data(df)

            st.success("Deleted Successfully")

        else:
            st.error("Student Not Found")

# -----------------------------
# ANALYTICS
# -----------------------------
elif menu == "Analytics":

    st.subheader("Performance Analytics")

    if len(df) > 0:

        df = calculate_performance(df)

        st.dataframe(df)

        st.write("### Top 5 Students")

        st.dataframe(
            df.sort_values(
                "Percentage",
                ascending=False
            ).head(5)
        )

        st.write("### Weak Students")

        st.dataframe(
            df[df["Percentage"] < 40]
        )

        st.write("### Subject Average")

        st.write(
            df[
                ["Math", "Science", "English"]
            ].mean()
        )

        st.write("### Class Wise Performance")

        st.write(
            df.groupby("Class")[
                "Percentage"
            ].mean()
        )

# -----------------------------
# GRAPHS
# -----------------------------
elif menu == "Graphs":

    st.subheader("Visual Analytics")

    if len(df) > 0:

        df = calculate_performance(df)

        avg = df[
            ["Math", "Science", "English"]
        ].mean()

        fig, ax = plt.subplots()

        ax.bar(
            avg.index,
            avg.values
        )

        ax.set_title(
            "Subject Wise Average"
        )

        ax.set_ylabel("Marks")

        st.pyplot(fig)

# -----------------------------
# EXPORT REPORT
# -----------------------------
elif menu == "Export Report":

    st.subheader("Generate Report")

    if len(df) > 0:

        report = calculate_performance(df)

        report.to_csv(
            "performance_report.csv",
            index=False
        )

        st.success(
            "Report Generated"
        )

        with open(
            "performance_report.csv",
            "rb"
        ) as file:

            st.download_button(
                "Download Report",
                file,
                "performance_report.csv",
                "text/csv"
            )