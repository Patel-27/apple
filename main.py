import streamlit as st
import re
import pickle
import bz2
import sqlite3
import pandas as pd
st.set_page_config(page_title="Apple Quality", page_icon="fevicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.

    Returns
    -------
    None.
    The background

    '''
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:url("https://media.istockphoto.com/id/1331302804/photo/red-apples-on-a-green-pastel-paper-background-top-view-flat-lay-copy-space.jpg?s=612x612&w=0&k=20&c=xk7VRqC4JxqE6ft-PJKdq4cyYpoU98MYPKdTIii_yT8=");
            background-size: cover
            }}
         </style>
         """,
         unsafe_allow_html=True
        )
set_bg_hack_url()

conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit() 

menu = ["Home","Login","SignUp","ContactUs"]
choice = st.sidebar.selectbox("Menu",menu)

if choice=="Home":
    st.title("Welcome to the System")
if choice=="SignUp":
        Fname = st.text_input("First Name")
        Lname = st.text_input("Last Name")
        Mname = st.text_input("Mobile Number")
        Email = st.text_input("Email")
        City = st.text_input("City")
        Password = st.text_input("Password",type="password")
        CPassword = st.text_input("Confirm Password",type="password")
        b2=st.button("SignUp")
        if b2:
            pattern=re.compile("(0|91)?[7-9][0-9]{9}")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if Password==CPassword:
                if (pattern.match(Mname)):
                    if re.fullmatch(regex, Email):
                        create_usertable()
                        add_userdata(Fname,Lname,Mname,City,Email,Password,CPassword)
                        st.success("SignUp Success")
                        st.info("Go to Logic Section for Login")
                    else:
            
                        st.warning("Not Valid Email")         
                else:
                    st.warning("Not Valid Mobile Number")
            else:
                st.warning("Pass Does Not Match")
    
            
if choice=="Login":
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password",type="password")

    b1=st.sidebar.checkbox("Login")
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            result = login_user(Email,Password)
            if result:
                if Email=="a@a.com":
                    st.success("Logged In as {}".format(Email))
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                    st.dataframe(clean_db)
                else:
                    st.success("Logged In as {}".format(Email))
                    menu2 = ["SVM","K-Nearest Neighbors", 
                             "Naive Bayes","Decision Tree", "Random Forest",
                             "ExtraTreesClassifier"]
                    choice2 = st.selectbox("Select ML",menu2)

                    size=float(st.slider('size',-7.0,6.5))
                    weight=float(st.slider('weight',-7.0,5.8))
                    sweetness=float(st.slider('sweetness',-6.9,6.4))
                    crunchiness=float(st.slider('crunchiness',-6.0,7.6))
                    juiciness=float(st.slider('juiciness',-5.9,7.3))
                    ripeness=float(st.slider('ripeness',-5.8,7.3))
                    acidity=float(st.slider('acidity',-7.0,7.4))
                    
                    my_array=[size,weight,sweetness,crunchiness,juiciness,ripeness,acidity] 
                    
                    b2=st.button("Predict")
                    model=pickle.load(open("model.pkl",'rb'))
                                           
                    if b2:                        
                        tdata=[my_array]
                        if choice2=="K-Nearest Neighbors":
                            test_prediction = model[0].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="SVM":
                            test_prediction = model[1].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)                 
                        if choice2=="Decision Tree":
                            test_prediction = model[2].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="Random Forest":
                            test_prediction = model[3].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="Naive Bayes":
                            test_prediction = model[4].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="ExtraTreesClassifier":
                            test_prediction = model[5].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)

                                     
            else:
                st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
                       
                            
                            
             
                
                   
           
    