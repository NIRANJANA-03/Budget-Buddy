# Budget Buddy: Expense Tracker

## Project Video

You can watch the project demo video here: [Budget Buddy Demo](https://youtu.be/i9dByGY2vwY?si=jNMf_adWc5BkgPCq).

---

## Overview

I recently started using various budgeting tools, but I noticed that they lacked features for managing group activities like trips or events, which inspired me to design a user-friendly platform with these capabilities integrated. Budget Buddy simplifies personal financial management by offering a seamless way to track expenses, plan trips, and manage group events.

The primary components of Budget Buddy include:

- **Home Page**: Serves as the central hub for accessing key features.
- **Login/Logout/Register**: Secure user authentication and account management.
- **Expense Tracker**: Allows users to categorize and track their spending with detailed analytics.
- **Tour Planner**: Enables users to budget for trips, allocating funds across various categories like transportation and lodging.
- **Event Planner**: Facilitates group expense management with transparent sharing and reporting.
- **Dynamic Analytics**: Interactive visualizations powered by Chart.js to monitor and optimize spending patterns.

One standout feature is how remaining money at the end of each month is divided into two parts: half is allocated to savings, and the other half is reserved for the emergency fund. This ensures a balanced approach to financial stability and readiness for unforeseen expenses.

Budget Buddy aims to provide users with a comprehensive toolset for managing their finances, helping them track expenses, plan activities, and improve their financial health. It goes beyond traditional budgeting tools by integrating advanced planning features tailored to modern users' needs.

---

## Distinctiveness and Complexity

### Distinctiveness
Budget Buddy stands out due to its unique combination of features:

- **Integration of Trip and Event Management**: Unlike conventional budgeting tools, Budget Buddy combines expense tracking with robust modules for travel and event planning, making it a holistic financial management solution.
- **Dynamic and Interactive Design**: Utilizes JavaScript and Chart.js for real-time updates and visually engaging charts, providing users with actionable financial insights.
- **Mobile-Responsive Design**: Designed to ensure accessibility and usability across various devices.

This project is distinct from other CS50 projects as it neither replicates a social media platform nor an e-commerce site, and it incorporates unique financial tools and interactive features.

### Complexity
Budget Buddy demonstrates significant complexity through:

1. **Backend Design**:
   - Utilizes Django ORM to manage multiple models (`User`, `ExpenseDetails`, `TourDetails`, `EventDetails`, etc.).
   - Implements secure user authentication and robust data handling mechanisms.
2. **Frontend Interaction**:
   - JavaScript enables dynamic updates, form validation, and real-time data rendering.
   - Chart.js generates interactive and customizable visualizations.
3. **Database Management**:
   - SQLite efficiently handles complex relationships and queries.
   - Supports features like real-time updates, custom queries, and user-specific data segregation.
4. **Modular Architecture**:
   - Follows clean code separation, ensuring scalability and maintainability.
5. **Event Dynamics**:
   - Events automatically deactivate once their duration ends, ensuring real-time updates and accuracy.
6. **Financial Strategy**:
   - Implements a thoughtful allocation strategy where leftover funds are split between savings and an emergency fund, promoting financial stability.

These elements collectively showcase a high level of technical sophistication and highlight the innovative solutions implemented to enhance user experience.

---

## Files and Directories

### Main Project Directory
- **`.env`**: Contains local environment variables for email credentials and API keys.
- **`.gitignore`**: Specifies files to be ignored by Git.
- **`settings.py`**: Custom configuration for timezone, email settings, and media file storage.
- **`urls.py`**: Defines project-level URLs and settings for media files.

### Application Directory: `expenses`
- **`static`**:
  - **`scripts.js`**:
    - Fetches current and future expenses/events and displays them dynamically.
    - Handles Google Maps API for location autocomplete.
    - Validates input for location fields and manages CSRF tokens.
  - **`styles.css`**: Provides styling for the sports templates, including flexbox and grid layouts.
- **`templates/sports/`**:
  - **`index.html`**: Displays the homepage with current, past, and single event views.
  - **`create_event.html`**: Form for creating a new event with location and budget inputs.
  - **`layout.html`**: Base template for consistent structure.
- **`models.py`**:
  - Defines two primary models:
    - `User`: Extends Django's `AbstractUser`.
    - `Event`: Stores details about each event, including many-to-many and foreign key relationships with `User`.
- **`views.py`**:
  - Handles core logic, such as creating events, enrolling users, and managing group expenses.
  - Includes form handling and backend API integration.

### Database
- **`db.sqlite3`**: SQLite database to store user, event, and financial data securely.

### Other Files
- **`requirements.txt`**: Lists all dependencies required to run the application.
- **`README.md`**: Comprehensive documentation of the project.

---

## How to Run the Application

### Prerequisites
- Python 3.x
- Pip

### Steps
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/me50/NIRANJANA-03/tree/966c41d79cabbb78c363afffd95f2721fdba306d
    cd Budget-Buddy/expense_tracker
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Apply Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Run the Server**:
    ```bash
    python manage.py runserver
    ```

5. **Access the Application**:
    Open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Additional Information

### Features
- **Expense Tracking**: Organize expenses across categories and monitor monthly budgets.
- **Tour Planner**: Budget for travel expenses with detailed category allocations.
- **Event Planner**: Simplify group expense sharing with automated email reports.
- **Interactive Visualizations**: Chart.js provides dynamic charts for spending analysis.
- **Mobile Responsiveness**: Ensures usability across all devices.

### Future Enhancements
- Integration with external APIs for currency conversion and financial recommendations.
- AI-based suggestions for budgeting and spending.
- Advanced reporting with exportable summaries.

---

### Additional Information

#### To see the Visualisation
- **username**: Rain
- **password**: Rain


#### Also add this in settings for sending the emails

- EMAIL_HOST_USER = 
- EMAIL_HOST_PASSWORD =

Then the details of event will be send directly to the two person whose details is given 
