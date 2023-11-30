import streamlit as st
from PIL import Image
from tabs.home import set_bg

def app():
    set_bg("tabs/images/background.jpg")
    st.title('About Me')
    image = Image.open("tabs/images/aboutme.png")
    col1, col2, col3, col4 = st.columns(4)
    with col2:
        st.image(image, width=400)
        
    # Introduction
    st.markdown("""
    Hello! My name is Rong Yi and I am currently a final year student at University of Portsmouth, majoring in BsC (Hons) Data Science and Analytics.
    This is a simplified version of my portfolio, which includes my work experience, education and skills.
    Please feel free to use the contact form or visit my full portfolio at [Vercel](https://rongyi-portfolio.dev/).
                """)
    
    # Drop down menu
    choices = ["Work Experience", "Education", "Projects"]
    option = st.selectbox('Select an option', choices)
    
    # render the page
    if option == "Work Experience":
        logo_ibf = Image.open("tabs/images/ibf.png")
        st.markdown("""
        ## Work Experience
        """)
        #==================== IBF ==================== #
        st.image(logo_ibf, width = 300)      
        # work duration
        st.markdown("""
        ##### Data Analyst Trainee at Institute of Banking and Finance Singapore           
        ##### :orange[Jan '23 - Present]
        """)
        
        st.write("--")

        # OJT description
        st.markdown("""
        *Jul '23 - Present* \n 
        DBS Bank - Regional & Wealth Analytics, Consumer Banking Group
        * Drive business insights using big data technologies
        * Optimise data pipeline scripts using Python and Spark
        * Perform data analytics in Superset
        * Flag transactional anomalies using SQL & Excel \n        
        """)
           
        
        # Training description
        st.markdown("""
        *Jan '23 - Jul '23* \n
        6 months training @ Digipen Institute of Technology Singapore \n
        :blue[Skills acquired:]
        * Basic/ Advanced Python - (*Functional & Object Oriented Programming*)
        * Relational & Non-relational Database Modelling - (*SQL & NoSQL*)
        * Data Visualization - (*PowerBI, Tableau, Matplotlib, Seaborn, Plotly*)
        * Data Structures & Algorithms 
        * Applied Mathematics - (*Statistics, Probability, Linear Algebra & Calculus*)), 
        * Machine Learning Algorithms
        * Data Engineering - (*Hadoop, Spark, Kafka, Hive, PySpark, Google Cloud Platform*)
        
                    """)

        
        st.write("---")

        #==================== E2i ==================== #
        logo_e2i = Image.open("tabs/images/e2i.jpg")
        st.image(logo_e2i, width = 200)
        # work duration
        st.markdown("""
        ##### Career Centre Specialist at Employment and Employability Institute Singapore
        ##### :orange[Jun '20 - Nov '22]
        """)

        st.write("--")

        # Work description
        st.markdown("""
        *Aug '21 - Nov '22* \n
        Summary:
        * Responsible for managing day-to-day career centre operations and curated multiple standard operational processes within the office. Organize, prioritize and delegate tasks effectively to ensure all administrative work is done competently and within deadlines.

        * Enhanced colleague's productivity by curating new tools to overcome system limitation, cutting administrative bloat by returning results in seconds instead of hours.

        * Volunteered to take on additional responsibilities and supported another department in training of new staff and analyzing workforce data.
        """)

        st.markdown("""
        *Jun '20 - Aug '21* \n
        Summary:
        * Rendered support to Self-Employed Person (SEPs) during the pandemic of validating & analyzing over 15,000 records for disbursement of training allowance (NTUC Training Fund).
        * Took on additional responsibilites of managing general inbox and as well as training of new staff. """)

        st.markdown("""
        :blue[Skills acquired:]
        * Data Analysis - (*Excel & PowerBI*)
        * Communication - (*Written & Verbal*)
        * Stakeholder Management
        * Project Management
        * Process Improvement
        * Training & Development
        """)   
    
    elif option == "Education":
        st.markdown("""
        ## Education
        """)
        
        #==================== UOP ==================== #
        # Portsmouth University
        uop_logo = Image.open("tabs/images/uop.png")
        st.image(uop_logo)
        
        st.markdown("""
        #### BsC (Hons) Data Science and Analytics
        ##### :orange[Jun '22 - Dec '23]
        """)

        st.write("--")
        
        st.markdown("""
        *Pending final grade*
        """)
        
        # Summary
        st.markdown("""
                    
        """)
        
        # Uop modules
        st.markdown("""
        Curriculum:
        * Applied Machine Learning and Data Mining
        * Big Data
        * Data Structures and Algorithms
        * Database Principles
        * Software Engineering Theory and Practice
        * Ethical Hacking
        * Business Analytics
        * Open Innovations in Data Science
        * Malware Forensics
        * Internet of Things
        * Individual Project (Engineering) :orange[*(This is my FYP!)*]
        """)
        
        st.write("---")
        
        #==================== Digipen ==================== #
        # Digipen Institute of Technology Singapore
        digipen_logo = Image.open("tabs/images/digipen.png")
        st.image(digipen_logo)
        
        st.markdown("""
        #### Specialist Diploma in Data Analytics & Engineering
        ##### :orange[Jan '23 - Jul '23]
        """)

        st.write("--")

        st.markdown("""
        *Pending final grade*
        """)
        
        st.markdown("""
        Curriculum:
        * Programming Methodologies: Python
        * Programming Paradigms: Advanced Python
        * Data Structures and Algorithms with Python
        * Databases and Data Modeling
        * Applied Mathematics and Statistics for Data Analytics
        * Data Visualization
        * Data Engineering: Big Data Technologies
        * Introduction to Machine Learning
        """)

    elif option == "Projects":
        st.markdown("""
        ## Projects
        """)

        st.markdown("""
        Please visit my full portfolio at [Vercel](https://rongyi-portfolio.dev/projects/).
                    """)        
    