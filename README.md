# Budget Buddy: Expense Tracker

## Project Overview

Budget Buddy is a comprehensive web-based platform designed to streamline personal financial management. It enables users to monitor expenses, set budgets, plan trips, and organize events effectively. Developed using **Django** for the backend and **HTML**, **CSS**, and **JavaScript** for the frontend, the platform delivers a seamless user experience while ensuring robust data security.

### Key Features

- **Expense Tracking**: Organize and track spending across customizable categories.
- **Tour Planner**: Simplify budgeting for travel expenses.
- **Event Planner**: Distribute and manage group expenses transparently.
- **Analytics and Visualization**: Gain insights into spending patterns through detailed charts and reports.
- **Interactive Visualizations**: JavaScript-powered charts (using Chart.js) provide dynamic and engaging representations of expense data.

---

## Distinctiveness and Complexity

### Distinctiveness

Budget Buddy stands apart from traditional expense tracking systems and projects in its integration of advanced planning features tailored for both individual and group financial activities. Unlike standard budgeting tools:

- It offers specialized modules for event and trip management, enabling users to seamlessly allocate budgets and share expenses in real-time.
- The combination of these features is absent in existing course projects such as e-commerce or social networking platforms, making this project unique.

### Complexity

The project demonstrates its complexity through:

- **Multi-faceted Functionality**: The application integrates diverse features (expense tracking, trip planning, and event management) into a cohesive system.
- **Backend Design**: Django's ORM and SQLite handle intricate data relationships for expenses, budgets, trips, and events.
- **Frontend Interaction**:
  - JavaScript enables dynamic updates, form validation, and real-time visualizations without requiring full-page reloads.
  - Charts (e.g., bar charts and pie charts) are implemented using **Chart.js**, providing a clear and interactive visualization of expense data.
- **Security**: Robust measures, including user authentication and data encryption, protect sensitive financial information.
- **Mobile Responsiveness**: A responsive design ensures usability across various devices, meeting modern web application standards.

---

## Project Files

### Key Directories and Files

#### **Frontend**
- `templates/`: Contains HTML templates for different pages, including login, signup, home, and feature-specific pages.
- `static/`: Includes CSS and JavaScript files for styling, interactivity, and charts (e.g., using Chart.js for data visualization).

#### **Backend**
- `views.py`: Implements logic for handling user requests.
- `models.py`: Defines database schema and relationships.
- `urls.py`: Maps URLs to views.
- `forms.py`: Handles form data validation.

#### **Database**
- SQLite database to store user, expense, trip, and event data.

#### **Other Files**
- `requirements.txt`: Lists dependencies for running the project.
- `README.md`: Documentation for the project.

---

## How to Run the Application

### Prerequisites

Ensure **Python** and **pip** are installed on your system.

### Steps

1. **Clone the repository**:

    ```bash
    git clone https://github.com/NIRANJANA-03/Budget-Buddy/
    cd Budget-Buddy/expense_tracker
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Apply migrations**:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

5. **Access the application**:

    Open your web browser and navigate to:  
    [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Additional Information

For representation with existing data 
**Username**: Rain  
**Password**: Rain
