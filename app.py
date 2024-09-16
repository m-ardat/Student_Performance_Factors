# Импорт библиотек
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Загружаем данные из CSV-файла
df_top_10 = pd.read_csv('Топ_10_учащихся.csv')
df = pd.read_csv("ИТОГ.csv")

# Название
st.title("Дашборд оценочный")

# Добавляем боковую панель слева
st.sidebar.title("Выберите ученика")
st.sidebar.write("Здесь вы можете выбрать ученика и просмотреть его оценки и статистику.")
list_button_name = [x for x in df_top_10['id'].unique()]
selected_student = st.sidebar.selectbox(label="Учащийся №:", options=list_button_name)

# Кнопка для отображения общей информации
show_general_info = st.sidebar.button("Общая информация")
st.sidebar.markdown("**Ключевые метрики:**  \n"
                    "1. Результат за текущий экзамен;  \n"
                    "2. Результат за предыдущий экзамен с коэффициентом 0.5;  \n"
                    "3. Участие во внеклассных мероприятиях (+ 10 баллов);  \n"
                    "4. Баллы за мотивацию учащегося (от -10 до + 20 баллов);  \n"
                    "5. Баллы за посещаемость (от 0 до 20 баллов).")
# Визуализируем графики, если кнопка нажата
if show_general_info:
    # Гистограмма распределения баллов
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Exam_Score'], bins=18, kde=True, color='green')
    plt.title('Гистограмма распределения баллов')
    plt.xlabel('Балл')
    plt.ylabel('Количество')
    st.pyplot(plt)  # Отображаем график в Streamlit
    plt.clf()  # Очищаем фигуру

    # Функция для получения коэффициента асимметрии нормального распределения
    def df_skew(data_column):
        return {
            'Среднее': data_column.mean().round(2),
            'Медиана': int(data_column.median()),
            'Мода': data_column.mode()[0],
            'Асимметрия': data_column.skew().round(2)
        }

    dict_rings_skew = df_skew(df['Exam_Score'])
    # Отображаем коэффициенты асимметрии в Streamlit
    for k, v in dict_rings_skew.items():
        st.write(f'{k}: {v}')

    # Диаграмма рассеивания
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df,
                    x='Hours_Studied',
                    y='Exam_Score',
                    hue='Gender',
                    palette='inferno',
                    size='Access_to_Resources',
                    legend='brief')
    plt.title('Диаграмма рассеивания баллов от количества затраченных часов в неделю')
    plt.xlabel('Количество часов в неделю')
    plt.ylabel('Балл')
    st.pyplot(plt)
    plt.clf()

    # Корреляционная матрица
    numeric_data = df.select_dtypes('number')
    corr_pearson = numeric_data.corr()

    # Визуализируем корреляционную матрицу
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_pearson, annot=True, fmt=".2f", cmap='coolwarm', square=True)
    plt.title('Корреляционная матрица')
    st.pyplot(plt)  # Отображаем график в Streamlit

    # Визуализация
    plt.figure(figsize=(10, 8))
    sns.countplot(data=df,
                  x='Distance_from_Home',
                  hue='Distance_from_Home',
                  palette='autumn')
    plt.title('Распределение учащихся по удаленности от школы')
    plt.xlabel('Расстояние')
    plt.ylabel('Количество')
    st.pyplot(plt)

    # Визуализация
    plt.figure(figsize=(10, 8))
    sns.boxplot(x='Parental_Involvement', y='Exam_Score', data=df, hue='Parental_Involvement', palette='autumn')
    plt.title('Связь участия родителей в образовании ученика и сдачи экзамена')
    plt.xlabel('Уровень участия родителя в образовании')
    plt.ylabel('Балл')
    st.pyplot(plt)  # Отображаем график в Streamlit

    # Визуализация
    plt.figure(figsize=(10, 8))
    sns.countplot(x=df['Peer_Influence'], hue=df['Motivation_Level'], palette='Set2')
    plt.title('Влияние сверстников на успеваемость - уровень мотивации')
    plt.xlabel('Уровень влияния сверстинков')
    plt.ylabel('Количество')
    st.pyplot(plt)  # Отображаем график в Streamlit

    # Визуализация
    plt.figure(figsize=(10, 8))
    sns.boxplot(x='Access_to_Resources', y='Exam_Score', data=df, hue='Access_to_Resources', palette='autumn')
    plt.title('Связь между наличием образовательных ресурсов и сдачей экзамена')
    plt.xlabel('Уровень наличия образовательных ресурсов')
    plt.ylabel('Балл')
    st.pyplot(plt)

    # Визуализация
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    sns.countplot(data=df, x='Extracurricular_Activities', hue='Gender', palette='inferno')
    plt.tight_layout()
    plt.subplot(1, 2, 2)
    sns.scatterplot(x=df['Extracurricular_Activities'], y=df['Exam_Score'])
    st.pyplot(plt)

    # Визуализация
    plt.figure(figsize=(10, 8))
    sns.countplot(x=df['School_Type'], hue=df['Teacher_Quality'], palette='Set2')
    plt.title('Гистограмма по виду школ и уровню преподавателей')
    plt.xlabel('Тип школы')
    plt.ylabel('Количество')
    st.pyplot(plt)
else:
    # Фильтруем DataFrame по выбранному студенту
    student_data = df_top_10[df_top_10['id'] == selected_student].copy()

    # Преобразуем данные для круговой диаграммы
    metrics = ['Exam_Score', 'point_attendance', 'point_motivation', 'point_extracurricular_activities',
               'point_previous_scores']
    metric_values = student_data[metrics].values.flatten()
    metric_names = ['Exam Score', 'Attendance', 'Motivation', 'Extracurricular Activities', 'Previous Scores']

    # Создаем DataFrame для круговой диаграммы
    pie_data = pd.DataFrame({
        'Metric': metric_names,
        'Value': metric_values,
    })

    # Создаем круговую диаграмму
    fig_pie = px.pie(pie_data,
                     names='Metric',
                     values='Value',
                     title=f"Вклад метрик в итоговый результат для студента {selected_student}",
                     template='plotly_white')

    # Создаем DataFrame для столбчатой диаграммы
    total_points = student_data['total_point'].values[0]
    df_top_10['rank'] = df_top_10['total_point'].rank(method='min', ascending=False)
    student_rank = df_top_10.loc[df_top_10['id'] == selected_student, 'rank'].values[0]

    bar_data = pd.DataFrame({
        'Metric': metric_names,
        'Value': metric_values,
    })

    # Создаем столбчатую диаграмму
    fig_bar = px.bar(bar_data,
                     x='Metric',
                     y='Value',
                     color='Value',
                     color_continuous_scale=px.colors.sequential.Viridis,
                     title=f"Вклад метрик в итоговый результат для студента {selected_student}",
                     labels={'Value': 'Баллы'},
                     template='plotly_white')

    # Отображаем диаграммы и информацию о суммарном балле и месте
    st.plotly_chart(fig_pie)
    st.plotly_chart(fig_bar)

    st.write(f"Суммарный балл: {total_points}")
    st.write(f"Место среди всех учеников: {int(student_rank)}")


