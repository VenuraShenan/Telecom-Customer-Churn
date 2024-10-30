import streamlit as st
import pandas as pd
import plotly.express as px

# Load your dataset
df = pd.read_csv('Data\Cleaned_Data.csv')  # Replace with the actual path to your data

# Apply Power BI-inspired dark theme styling
st.set_page_config(layout="wide", page_title="Customer Churn Dashboard")
st.markdown(
    """
    <style>
    /* Background Image with Opacity and Blur */
    .main .block-container {
        background: url('https://www.pwc.com/gx/en/industries/tmt/assets/telco-banner-v2.jpeg') no-repeat center center fixed; /* Replace with your image URL */
        background-size: cover; /* Cover the entire background */
        position: relative; /* Position for overlay */
        z-index: 0; /* Send background behind other content */
    }

    /* Overlay for Background Image */
    .main .block-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.9); /* Semi-transparent black overlay */
        z-index: 1; /* Ensure overlay is above the background */
    }

    /* Blur effect */
    .main .block-container img {
        filter: blur(25px); /* Apply blur effect to the image */
        -webkit-filter: blur(25px);
        position: absolute; /* Position it absolutely */
        top: 0; /* Align to the top */
        left: 0; /* Align to the left */
        width: 100%; /* Full width */
        height: 100%; /* Full height */
        z-index: -1; /* Send it behind other content */
    }

    .main .block-container > * {
        position: relative; /* Bring content above overlay */
        z-index: 2; /* Ensure content is above overlay */
    }

    .sidebar .sidebar-content {
        background-color: rgba(40, 42, 54, 0.8); /* Semi-transparent sidebar background */
        color: #e0e0e0;
    }
    
    /* Title Styling */
    h1 {
        font-size: 3.5rem;  /* Increase the font size */
        font-weight: 900;   /* Make it bolder */
        color: rgba(255, 255, 255, 0.9); /* White color with some transparency */
        text-shadow: 4px 4px 10px rgba(0, 0, 0, 0.8);  /* Shadow effect for depth */
        text-align: center; /* Center the title */
        margin-bottom: 2rem; /* Space below the title */
        background-color: #007bff; /* Solid background color */
        padding: 1rem; /* Padding around the title */
        border-radius: 10px; /* Rounded corners for the title */
    }
    
    h2, h3, .metric {
        font-family: 'Arial', sans-serif;
        color: #007bff; /* Change to main blue */
        font-weight: 600;
        text-align: center; /* Center section titles */
        margin-top: 1rem; /* Add spacing above sections */
    }
    
    /* Card style */
    .card {
        background-color: rgba(44, 46, 51, 0.9); /* Slightly transparent card background */
        border-radius: 15px; /* More rounded corners */
        padding: 1.5rem;  
        margin: 1rem;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.5); /* Deeper shadow */
        color: #e0e0e0;
        transition: transform 0.3s; /* Smooth transform effect */
    }

    /* Card hover effect */
    .card:hover {
        transform: scale(1.05); /* Slightly enlarge on hover */
        box-shadow: 0px 6px 30px rgba(0,0,0,0.7); /* More prominent shadow */
    }

    /* Custom text colors */
    .highlight {
        color: #007bff; /* Change to main blue */
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True
)

# Add a JavaScript alert for a welcome message
st.markdown(
    """
    <script>
        window.onload = function() {
            alert("Welcome to the Customer Churn Performance Dashboard!");
        }
    </script>
    """, unsafe_allow_html=True
)



# Title
st.title("Customer Analysis Dashboard")


# Sidebar filters
st.sidebar.header("Filters")

# Customer Status Dropdown
status_options = ['All', 'Churned', 'Not Churned']
selected_status = st.sidebar.selectbox("Customer Status", status_options)

min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))

gender_options = df['Gender'].unique()
selected_gender = st.sidebar.selectbox("Gender", ["All"] + list(gender_options))

# Phone Service Filter
phone_service_options = df['Phone Service'].unique()
selected_phone_service = st.sidebar.multiselect("Phone Service", list(phone_service_options), default=list(phone_service_options))

# Internet Service Filter
internet_service_options = df['Internet Service'].unique()
selected_internet_service = st.sidebar.multiselect("Internet Service", list(internet_service_options), default=list(internet_service_options))

# Internet Type Filter
internet_type_options = df['Internet Type'].unique()
selected_internet_type = st.sidebar.multiselect("Internet Type", list(internet_type_options), default=list(internet_type_options))

# Reset Filters Button
if st.sidebar.button("Reset Filters"):
    selected_status = 'All'  # Reset to 'All'
    age_range = (min_age, max_age)  # Reset age range to the full range
    selected_gender = "All"  # Reset gender selection to 'All'
    selected_phone_service = list(phone_service_options)  # Reset phone service selection to all
    selected_internet_service = list(internet_service_options)  # Reset internet service selection to all
    selected_internet_type = list(internet_type_options)  # Reset internet type selection to all

# Filter the data based on selections
filtered_df = df.copy()

if selected_status == 'Churned':
    filtered_df = filtered_df[filtered_df['Customer Status'] == 'Churned']
elif selected_status == 'Not Churned':
    filtered_df = filtered_df[filtered_df['Customer Status'] == 'Not Churned']

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

if selected_phone_service:
    filtered_df = filtered_df[filtered_df['Phone Service'].isin(selected_phone_service)]

if selected_internet_service:
    filtered_df = filtered_df[filtered_df['Internet Service'].isin(selected_internet_service)]

if selected_internet_type:
    filtered_df = filtered_df[filtered_df['Internet Type'].isin(selected_internet_type)]

filtered_df = filtered_df[filtered_df['Age'].between(*age_range)]


# Customer Status
# Customer Status Metric (Centered)
status_counts = filtered_df['Customer Status'].value_counts()
churned_count = status_counts.get("Churned", 0)
not_churned_count = status_counts.get("Not Churned", 0)

# Display the metric at the beginning
st.markdown(
    f"""
    <div class='card' style='text-align: center;'>
        <h3 style='margin-bottom: 0; color: #007bff;'>Customer Status</h3>
        <h1 style='color: white;'>Churned: {churned_count:,} | Not Churned: {not_churned_count:,}</h1>
    </div>
    """, 
    unsafe_allow_html=True
)


#Demographics Section in a Grid
st.markdown("<div class='card'><h2>Demographics</h2></div>", unsafe_allow_html=True)

# Create a grid layout for demographics
col1, col2 = st.columns(2)

with col1:
    # Gender Distribution (Pie Chart)
    st.markdown("<h3>Gender Distribution</h3>", unsafe_allow_html=True)
    gender_count = filtered_df['Gender'].value_counts()
    fig_gender = px.pie(gender_count, values=gender_count.values, names=gender_count.index,
                        template='plotly_dark', color_discrete_sequence=["#ff007b", "#00ff7b"])  # Pink and Green palette
    st.plotly_chart(fig_gender)

with col2:
    # Marital Status Distribution (Bar Chart)
    st.markdown("<h3>Marital Status Distribution</h3>", unsafe_allow_html=True)
    marital_status_count = filtered_df['Married'].value_counts()
    fig_marital = px.bar(marital_status_count, x=marital_status_count.index, y=marital_status_count.values,
                          color=marital_status_count.index,
                          color_discrete_sequence=["#ff0000", "#007bff"], template='plotly_dark')  # Red and Blue palette
    st.plotly_chart(fig_marital)
    

with col1:
    # Age Histogram
    st.markdown("<h3>Age Histogram</h3>", unsafe_allow_html=True)
    fig_age_histogram = px.histogram(filtered_df, x='Age', nbins=30,
                                      color_discrete_sequence=["#007bff"],  # Blue color
                                      template='plotly_dark')
    st.plotly_chart(fig_age_histogram)

with col2:
    # Region Distribution (Bar Chart)
    st.markdown("<h3>Region Distribution</h3>", unsafe_allow_html=True)
    region_count = filtered_df['Region'].value_counts()
    fig_region = px.bar(region_count, x=region_count.index, y=region_count.values,
                         color=region_count.index,
                         color_discrete_sequence=px.colors.qualitative.Plotly, template='plotly_dark')
    st.plotly_chart(fig_region)

# Internet Services Section in a Grid
st.markdown("<div class='card'><h2>Telecom Services</h2></div>", unsafe_allow_html=True)

# Create a grid layout for internet services
col1, col2 = st.columns(2)

with col1:
    # Internet Service Distribution (Bar Chart)
    st.markdown("<h3>Internet Service Distribution</h3>", unsafe_allow_html=True)
    internet_service_count = filtered_df['Internet Service'].value_counts()
    fig_internet_service = px.bar(internet_service_count, x=internet_service_count.index, y=internet_service_count.values,
                                   color=internet_service_count.index,
                                   color_discrete_sequence=["#ff0000", "#007bff"], template='plotly_dark')  # Red and Blue palette
    st.plotly_chart(fig_internet_service)

with col2:
    # Phone Service Distribution (Bar Chart)
    st.markdown("<h3>Phone Service Distribution</h3>", unsafe_allow_html=True)
    phone_service_count = filtered_df['Phone Service'].value_counts()
    fig_phone_service = px.bar(phone_service_count, x=phone_service_count.index, y=phone_service_count.values,
                                color=phone_service_count.index,
                                color_discrete_sequence=["#ff0000", "#007bff"], template='plotly_dark')  # Red and Blue palette
    st.plotly_chart(fig_phone_service)

# Revenue Section in a Grid
st.markdown("<div class='card'><h2>Revenue Metrics</h2></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Card - Total Revenue Metric
    st.markdown(
    f"""
    <div class='card' style='text-align: center;'>
        <h3 style='margin-bottom: 0; color: #007bff;'>Total Revenue</h3>
        <h1 style='color: white;'>${filtered_df['Total Revenue'].sum():,.0f}</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

    # Monthly Charges Distribution (Histogram)
    st.markdown("<div class='card'><h3>Monthly Charges Distribution</h3>", unsafe_allow_html=True)
    fig_monthly_charges = px.histogram(filtered_df, x='Monthly Charge', 
                                        nbins=30, 
                                        color_discrete_sequence=["#007bff"],  # Blue color
                                        template='plotly_dark')
    st.plotly_chart(fig_monthly_charges)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Average Monthly GB Download Metric
    st.markdown(
    f"""
    <div class='card' style='text-align: center;'>
        <h3 style='margin-bottom: 0; color: #007bff;'>Average Monthly GB Download</h3>
        <h1 style='color: white;'>{filtered_df['Avg Monthly GB Download'].mean():.1f} GB</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

    # Avg Monthly GB Download Distribution (Histogram)
    st.markdown("<div class='card'><h3>Avg Monthly GB Download </h3>", unsafe_allow_html=True)
    fig_avg_gb_download = px.histogram(filtered_df, x='Avg Monthly GB Download',  
                                        nbins=30, 
                                        color_discrete_sequence=["#007bff"],  # Blue color
                                        template='plotly_dark')
    st.plotly_chart(fig_avg_gb_download)
    st.markdown("</div>", unsafe_allow_html=True)



# Interactive Bivariate Plots Section
st.markdown("<div class='card'><h2>Interactive Bivariate Plots</h2></div>", unsafe_allow_html=True)

# User-selected features for bivariate plot
x_feature = st.selectbox("Select X Feature", df.select_dtypes(include=['int64','float64']).columns.tolist())
y_feature = st.selectbox("Select Y Feature", df.select_dtypes(include=['int64','float64']).columns.tolist())
if x_feature and y_feature:
    fig_bivariate = px.scatter(filtered_df, x=x_feature, y=y_feature,
                                color='Customer Status', 
                                title='Bivariate Plot',
                                color_discrete_sequence=["#ff007b", "#00ff7b"],  # Churned and Not Churned colors
                                template='plotly_dark')
    st.plotly_chart(fig_bivariate)

