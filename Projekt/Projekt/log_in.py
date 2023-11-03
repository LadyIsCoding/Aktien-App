import streamlit as st
import csv, json

def login():
    with st.expander("LogIn"):
        with st.form("LogIn"):
            username = st.text_input("Username")
            password = st.text_input("Passwort", type="password")

            if st.form_submit_button("LogIn"):

                with open("user_data.csv", "r", encoding="utf-8") as file:
                    login_successful = False 
                    for line in csv.reader(file):
                        if line[0] == username:
                            if line[1] == password:
                                login_successful = True
                                return line[0]
                                #st.session_state["current_user"] = line[0]
                                #st.write("Erfolgreich eingeloggt!")
                                #st.experimental_rerun()
                            


def signup():
    with st.expander("SignUp"):
        with st.form("SignUp"):
            username = st.text_input("Username")
            password = st.text_input("Passwort", type="password")

            if st.form_submit_button("SignUp"):
                with open("user_data.csv", "r", encoding="utf-8") as file:
                    for line in csv.reader(file):
                        if username in line:
                            return st.warning("Username already exist")
                    
                with open("user_data.csv", "a", encoding="utf-8", newline="") as file:
                    writerobj = csv.writer(file)
                    writerobj.writerow([username, password])

                with open(f"portfolios/{username}_portfolio.json", "w", encoding="utf=8") as file:
                    json.dump({}, file, indent=4)
                