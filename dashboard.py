import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
from charts import charts

data = pd.read_excel('Food Allergic.xlsx')


def load_custom_css():
    custom_css = """
    <link rel="stylesheet" type="text/css" href="custom.css">
    """
    st.markdown(custom_css, unsafe_allow_html=True)


load_custom_css()



def main_function():
    selected = option_menu(
        menu_title=None,  
        options=["Dashboard", "About", "Contact"],  
        icons=["house", "book", "envelope"],  
        menu_icon="cast",  
        default_index=0,  
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#262730"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {
                "font-size": "25px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "green"},
        }
    )

    if selected == "Dashboard":
        st.markdown("## 📊 Food Allergy Type Prediction Dashboard")
        st.write("Welcome to the Food Allergy Type Prediction Dashboard!")
    


        radio_states = {
            'Top 10 Allergens by Prevalence of Allergic Reactions': False,
            'Prevalence of Allergic Reactions by Education Level': False,
            'Prevalence of Allergic Reactions Across Age Groups': False,
            'Distribution of Clinical Presentations by Age Group': False,
            'Allergic Reactions by Sex and Marital Status': False,
            'Distribution of Allergic Types by Age Group': False,
            'Distribution of Categorical Variables': False,
            'Distribution of Educational Levels': False,
            'Distribution of Age Groups': False,
            'Distribution of sex': False,
            'Hide All Charts': True, 
        }

        def handle_radio_state(radio_label):
            for label in radio_states.keys():
                if label == radio_label:
                    radio_states[label] = not radio_states[label] 
                else:
                    radio_states[label] = False

        selected_option = st.radio('Select an option', list(radio_states.keys()), index=None)
        if selected_option is not None:
            handle_radio_state(selected_option)
  




        dataset = pd.read_excel('Food Allergic.xlsx')
        food_columns = dataset[['banana', 'barley', 'corns', 'soya', 'dates', 'peanuts', 'onion', 'tomato', 'codfish', 
                        'peach', 'eggplant', 'pumpkin', 'eggwhole', 'garlic', 'wheat', 'shrimp', 'carrot', 'cucumber', 
                        'beef', 'white', 'whole', 'soyabean', 'orange', 'chocolate', 'sesem', 'celery', 'chilipowder', 
                        'spinach', 'watermelon', 'rice', 'apple', 'milk', 'chicken', 'salmon', 'lobster', 'tea', 'mutton', 
                        'inhalation', 'egg', 'potato', 'eggwhite', 'bean', 'pea', 'strawberry', 'coconut', 'grape', 'eggyolk', 
                        'fish', 'mango', 'olive', 'almond', 'rye', 'oyster', 'scallop', 'clam', 'pistachione', 'trout', 
                        'sweetchestnut', 'bluemussel', 'pacificsquid', 'hazelnut', 'kiwi', 'anchovy', 'plaice', 'eel', 
                        'buckwheat', 'cacao', 'walnut', 'lambmeat', 'sunflower', 'pinenut', 'crab', 'pork', 'tuna', 'mackerel', 
                        'mushroom', 'yeastbaker', 'citrusmixs']]
        allergic_reactions = food_columns.sum()
        prevalence = allergic_reactions / len(food_columns) * 100

        def top_10_Allergens():
            top_10_allergens = prevalence.nlargest(10)

            st.markdown('### Top 10 Allergens by Prevalence of Allergic Reactions')

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=top_10_allergens.index, y=top_10_allergens, hue=top_10_allergens.index, palette="mako", ax=ax)
            ax.legend().remove()
            plt.xticks(rotation=45)

            plt.xlabel('Food/Substance')
            plt.ylabel('Percentage of Allergic Reactions (%)')

            ax.set_title('Top 10 Allergens by Prevalence of Allergic Reactions')
            
            st.pyplot(fig)


        if radio_states['Top 10 Allergens by Prevalence of Allergic Reactions']:
            top_10_Allergens()
    

        def prevalence_of_allergic_reactions_by_bducation_level():
            allergic_reaction_by_education = data.groupby('education')['haveeverhadallegic'].mean().sort_values()

            st.markdown("### Prevalence of Allergic Reactions by Education Level")

            fig, ax = plt.subplots(figsize=(8, 4))
            allergic_reaction_by_education.plot(kind='barh', color='lightblue', ax=ax)
            ax.set_title('Prevalence of Allergic Reactions by Education Level')
            ax.set_xlabel('Prevalence of Allergic Reactions')
            ax.set_ylabel('Education Level')

            st.pyplot(fig)

        if radio_states["Prevalence of Allergic Reactions by Education Level"]:
            prevalence_of_allergic_reactions_by_bducation_level()



        def distribution_of_clinical_precentation():
            st.markdown('### Distribution of Clinical Presentations by Age Group')

            fig, ax = plt.subplots(figsize=(8, 5))
            sns.countplot(data=data, y='clinicalpresentation', hue='Age', palette='Set2')
            plt.title('Distribution of Clinical Presentations by Age Group')
            plt.xlabel('Count')
            plt.ylabel('Clinical Presentation')
            plt.legend(title='Age Group', loc='lower right')
            plt.tight_layout()

            st.pyplot(fig)

        if radio_states["Distribution of Clinical Presentations by Age Group"]:
            distribution_of_clinical_precentation()


        
        def allergic_Reactions_by_Sex_and_Marital_Status():
            marital_status_counts = data['maritalstatus'].value_counts()
            marital_status_df = pd.DataFrame({
                'Marital Status': marital_status_counts.index,
                'Prevalence of Allergic Reactions': marital_status_counts.values
            })

            sex_counts = data['Sex'].value_counts()
            sex_df = pd.DataFrame({
                'Sex': sex_counts.index,
                'Prevalence of Allergic Reactions': sex_counts.values
            })

            st.markdown('## Allergic Reactions by Sex and Marital Status')

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

            
            sns.barplot(data=marital_status_df, x='Marital Status', y='Prevalence of Allergic Reactions', ax=ax1, hue='Marital Status', palette='Blues', dodge=False, legend=False)
            ax1.set_title('Allergic Reactions by Marital Status')
            ax1.set_xlabel('Marital Status')
            ax1.set_ylabel('Prevalence of Allergic Reactions')

            sns.barplot(data=sex_df, x='Sex', y='Prevalence of Allergic Reactions', ax=ax2, hue='Sex', palette='Reds', dodge=False, legend=False)
            ax2.set_title('Allergic Reactions by Sex')
            ax2.set_xlabel('Sex')
            ax2.set_ylabel('Prevalence of Allergic Reactions')

            st.pyplot(fig)

        if radio_states["Allergic Reactions by Sex and Marital Status"]:
            allergic_Reactions_by_Sex_and_Marital_Status()

        

        def distribution_of_allergic_types_by_age_group():
            sns.set(style="whitegrid")

            st.markdown('## Distribution of Allergic Types by Age Group')

            fig, ax = plt.subplots(figsize=(12, 6))
            sns.countplot(data=data, x='Age', hue='allergic_type', ax=ax)

            age_group_labels = ["2 - 18", "19 - 29", "30 - 39", "40 - Above"]
            plt.xticks(range(4), age_group_labels)

            plt.xlabel('Age Group')
            plt.ylabel('Count')

            plt.title('Distribution of Allergic Types by Age Group')

            plt.legend(title='Allergic Type')

            st.pyplot(fig)
        
        if radio_states["Distribution of Allergic Types by Age Group"]:
            distribution_of_allergic_types_by_age_group()



        def distribution_of_categorical_variables():
            st.markdown('<h2 style="text-align: center; font-size: 40px;">Distribution of Categorical Variables</h2>', unsafe_allow_html=True)

            categorical_variables = ['Sex', 'maritalstatus', 'education', 'allergic_type', 'clinicalpresentation']

            chart_palettes = sns.color_palette("husl", len(categorical_variables))

            for category, palette in zip(categorical_variables, chart_palettes):
                category_counts = data[category].value_counts().sort_values(ascending=False)

                normalized_counts = (category_counts - category_counts.min()) / (category_counts.max() - category_counts.min())

                colors = [sns.desaturate(palette, value) for value in normalized_counts]

                fig, ax = plt.subplots(figsize=(8, 6))
  
                sns.countplot(x=category, data=data, palette=colors)

                ax.set_title(f'Distribution of {category}')
                ax.set_xlabel(category)
                ax.set_ylabel('Frequency')
                ax.tick_params(axis='x', rotation=45)
                

                title_html = f'<h2 style="text-align: center; font-size: 24px;">Distribution of {category}</h2>'
                st.markdown(title_html, unsafe_allow_html=True)
                st.pyplot(fig)
                    
        if radio_states["Distribution of Categorical Variables"]:
            distribution_of_categorical_variables()



        def distribution_of_educational_levels():
            st.markdown('## Distribution of Educational Levels')

            colors = ['#1f77b4', '#cc6600', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

            fig, ax = plt.subplots(figsize=(8, 4))
            sns.countplot(data=data, y='education', order=data['education'].value_counts().index, palette=colors)

            ax.set_title('Distribution of Educational Levels')
            ax.set_xlabel('Count')
            ax.set_ylabel('Education Level')

            st.pyplot(fig)

        if radio_states["Distribution of Educational Levels"]:
            distribution_of_educational_levels()


        def distribution_of_age_groups():
            trainset = pd.read_excel('Food Allergic.xlsx')
            sns.set(style="whitegrid")

            st.markdown('## Distribution of Age Groups')

            fig, ax = plt.subplots(figsize=(8, 5))
            sns.countplot(data=trainset, x='Age', ax=ax, palette=['cornflowerblue', 'darkorange', 'mediumseagreen', 'lightcoral'])

            ax.set_title('Distribution of Age Groups')
            ax.set_xlabel('Age Group')
            ax.set_ylabel('Count')
            age_group_labels = ["2 - 18", "19 - 29", "30 - 39", "40 - Above"]
            ax.set_xticklabels(age_group_labels, rotation=45)

            st.pyplot(fig)

        if radio_states["Distribution of Age Groups"]:
            distribution_of_age_groups()


        def distribution_of_sex():
            sex_distribution = data['Sex'].value_counts(normalize=True) * 100

            st.markdown("## Distribution of Sex")

            fig, ax = plt.subplots()
            ax.pie(sex_distribution, labels=sex_distribution.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal') 
            plt.title('Distribution of Sex')

            st.pyplot(fig)

        if radio_states["Distribution of sex"]:
            distribution_of_sex()


        def prevalence_of_allergic_reactions():
            sns.set(style="whitegrid")

            st.markdown('### Prevalence of Allergic Reactions Across Age Groups')

            fig, ax = plt.subplots(figsize=(8, 5))
            sns.countplot(data=data, x='Age', hue='haveeverhadallegic', ax=ax, palette=['cornflowerblue', 'darkorange'])

            ax.set_title('Prevalence of Allergic Reactions Across Age Groups')
            ax.set_xlabel('Age Group')
            ax.set_ylabel('Count')
            age_group_labels = ["2 - 18", "19 - 29", "30 - 39", "40 - Above"]
            ax.set_xticklabels(age_group_labels, rotation=45)
            ax.legend(title='Allergic Reaction', labels=['No', 'Yes'])

            st.pyplot(fig)


        if radio_states["Prevalence of Allergic Reactions Across Age Groups"]:
            prevalence_of_allergic_reactions()


        if radio_states['Hide All Charts']:
            charts()
    
        

    elif selected == "About":
        st.title("📚 About")
        st.write("Here are some of the students who contributed for this project.")

    elif selected == "Contact":
        st.title("✉️ Contact")
        st.write("Get in touch with us!")
        st.write("Email: abdulkadir00b@gmail.com")
        st.write("University: Jamhiriya University of Science and Technology")



if __name__ == '__main__':
    main_function()