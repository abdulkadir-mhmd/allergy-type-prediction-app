import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import base64
from io import BytesIO


data = pd.read_excel('Food Allergic.xlsx')

def charts():
    food_columns = data[['banana', 'barley', 'corns', 'soya', 'dates', 'peanuts', 'onion', 'tomato', 'codfish', 
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

    allergic_reaction_by_education = data.groupby('education')['haveeverhadallegic'].mean().sort_values()

    fig1, ax1 = plt.subplots(figsize=(10, 8))
    sns.barplot(x=prevalence.nlargest(10).index, y=prevalence.nlargest(10), hue=prevalence.nlargest(10).index, palette="mako", ax=ax1)
    ax1.legend().remove()
    plt.xticks(rotation=45)
    plt.xlabel('Food/Substance')
    plt.ylabel('Percentage of Allergic Reactions (%)')
    ax1.set_title('Top 10 Allergens by Prevalence of Allergic Reactions')

    fig2, ax2 = plt.subplots(figsize=(10, 8))
    allergic_reaction_by_education.plot(kind='barh', color='lightblue', ax=ax2)
    ax2.set_title('Prevalence of Allergic Reactions by Education Level')
    ax2.set_xlabel('Prevalence of Allergic Reactions')
    ax2.set_ylabel('Education Level')

    def fig_to_base64(fig):
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()

    fig1_base64 = fig_to_base64(fig1)
    fig2_base64 = fig_to_base64(fig2)

    st.markdown(
        f"""
        <div style="display: flex">
            <div style="flex: 50%; padding: 5px;">
                <h3 style="font-size: 15px">Top 10 Allergens by Prevalence of Allergic Reactions</h3>
                <img src="data:image/png;base64,{fig1_base64}" style="width:100%">
            </div>
            <div style="flex: 50%; padding: 5px;">
                <h3 style="font-size: 15px">Prevalence of Allergic Reactions by Education Level</h3>
                <img src="data:image/png;base64,{fig2_base64}" style="width:100%">
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )





    fig1, ax1 = plt.subplots(figsize=(10, 8))
    sns.countplot(data=data, y='clinicalpresentation', hue='Age', palette='Set2')
    plt.title('Distribution of Clinical Presentations by Age Group')
    plt.xlabel('Count')
    plt.ylabel('Clinical Presentation')
    plt.legend(title='Age Group', loc='lower right')
    plt.tight_layout()

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



    fig2, (ax2_1, ax2_2) = plt.subplots(1, 2, figsize=(10, 8))

    sns.barplot(data=marital_status_df, x='Marital Status', y='Prevalence of Allergic Reactions', ax=ax2_1, hue='Marital Status', palette='Blues', dodge=False, legend=False)
    ax2_1.set_title('Allergic Reactions by Marital Status')
    ax2_1.set_xlabel('Marital Status')
    ax2_1.set_ylabel('Prevalence of Allergic Reactions')

    sns.barplot(data=sex_df, x='Sex', y='Prevalence of Allergic Reactions', ax=ax2_2, hue='Sex', palette='Reds', dodge=False, legend=False)
    ax2_2.set_title('Allergic Reactions by Sex')
    ax2_2.set_xlabel('Sex')
    ax2_2.set_ylabel('Prevalence of Allergic Reactions')

    def fig_to_base64(fig):
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()

    fig1_base64 = fig_to_base64(fig1)
    fig2_base64 = fig_to_base64(fig2)

    st.markdown(
        f"""
        <div style="display: flex">
            <div style="flex: 50%; padding: 5px;">
                <h3 style="font-size: 13px">Distribution of Clinical Presentations by Age Group</h3>
                <img src="data:image/png;base64,{fig1_base64}" style="width:100%">
            </div>
            <div style="flex: 50%; padding: 5px;">
                <h3 style="font-size: 13px">Allergic Reactions by Sex and Marital Status</h3>
                <img src="data:image/png;base64,{fig2_base64}" style="width:100%">
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



    sns.set(style="whitegrid")
    st.markdown('## Distribution of Allergic Types by Age Group')
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.countplot(data=data, x='Age', hue='allergic_type', ax=ax1)
    age_group_labels = ["2 - 18", "19 - 29", "30 - 39", "40 - Above"]
    plt.xticks(range(4), age_group_labels)
    plt.xlabel('Age Group')
    plt.ylabel('Count')
    plt.title('Distribution of Allergic Types by Age Group')
    plt.legend(title='Allergic Type')
    st.pyplot(fig1)

    st.markdown('<h2 style="text-align: center; font-size: 40px;">Distribution of Categorical Variables</h2>', unsafe_allow_html=True)

    categorical_variables = ['Sex', 'maritalstatus', 'education', 'allergic_type', 'clinicalpresentation']
    chart_palettes = sns.color_palette("husl", len(categorical_variables))

    fig2, axes = plt.subplots(1, len(categorical_variables), figsize=(20, 6))

    for ax, category, palette in zip(axes, categorical_variables, chart_palettes):
        category_counts = data[category].value_counts().sort_values(ascending=False)
        normalized_counts = (category_counts - category_counts.min()) / (category_counts.max() - category_counts.min())
        colors = [sns.desaturate(palette, value) for value in normalized_counts]
        sns.countplot(x=category, data=data, hue=category, palette=colors, ax=ax, legend=False)
        ax.set_title(f'Distribution of {category}')
        ax.set_xlabel(category)
        ax.set_ylabel('Frequency')
        ax.tick_params(axis='x', rotation=45)
        
    plt.tight_layout()
    st.pyplot(fig2)


    unique_education_levels = data['education'].nunique()
    colors = ['#1f77b4', '#cc6600', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'][:unique_education_levels]

    fig1, ax1 = plt.subplots(figsize=(10, 8))
    sns.countplot(
        data=data,
        y='education',
        hue='education',
        order=data['education'].value_counts().index,
        palette=colors,
        ax=ax1,
        legend=False
    )
    ax1.set_title('Distribution of Educational Levels')
    ax1.set_xlabel('Count')
    ax1.set_ylabel('Education Level')

    sns.set(style="whitegrid")
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    sns.countplot(data=data, x='Age', hue='Age', palette=['cornflowerblue', 'darkorange', 'mediumseagreen', 'lightcoral'], legend=False)
    ax2.set_title('Distribution of Age Groups')
    ax2.set_xlabel('Age Group')
    ax2.set_ylabel('Count')
    age_group_labels = ["2 - 18", "19 - 29", "30 - 39", "40 - Above"]

    ax2.set_xticks(range(len(age_group_labels)))
    ax2.set_xticklabels(age_group_labels, rotation=45)

    def fig_to_base64(fig):
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()

    fig1_base64 = fig_to_base64(fig1)
    fig2_base64 = fig_to_base64(fig2)

    st.markdown(
        f"""
        <div style="display: flex">
            <div style="flex: 50%; padding: 5px;">
                <h3 style="font-size: 13px">Distribution of Educational Levels</h3>
                <img src="data:image/png;base64,{fig1_base64}" style="width:100%">
            </div>
            <div style="flex: 50%; padding: 5px;">
                <h3 style="font-size: 13px">Distribution of Age Groups</h3>
                <img src="data:image/png;base64,{fig2_base64}" style="width:100%">
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )





    plt.figure(figsize=(8, 4))
    sns.countplot(x='Age', hue='haveeverhadallegic', data=data)
    plt.title('Prevalence of Allergic Reactions Across Age Groups')
    plt.xlabel('Age Group')
    plt.ylabel('Count')

    age_group_labels = ["2 - 18", "20 - 28", "30 - 38", "40 - 48"]

    plt.xticks(range(4), age_group_labels)
    plt.legend(title='Allergic Reaction', labels=['No', 'Yes'])

    plt.tight_layout()


    fig3 = BytesIO()
    plt.savefig(fig3, format='png')
    fig3_base64 = base64.b64encode(fig3.getvalue()).decode()


    sex_distribution = data['Sex'].value_counts(normalize=True) * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))


    ax1.pie(sex_distribution, labels=sex_distribution.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    ax1.set_title('Distribution of Sex')


    fig4 = BytesIO()
    plt.savefig(fig4, format='png')
    fig4_base64 = base64.b64encode(fig4.getvalue()).decode()


    st.markdown(
        f"""
        <div style="display: flex;">
            <div style="padding: 5px;">
                <h3 style="font-size: 13px">Distribution of Sex</h3>
                <img src="data:image/png;base64,{fig4_base64}" style="width:100%">
            </div>
            <div style="padding: 5px;">
                <h3 style="font-size: 10px">Prevalence of Allergic Reactions Across Age Groups</h3>
                <img src="data:image/png;base64,{fig3_base64}" style="width:100%">
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == '__main__':
    charts()