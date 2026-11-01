# Crononote

#### Video Demo: <https://youtu.be/BX2lTrWVz-o>

#### Description:
Crononote is a clean and lightweight web-based daily study journal designed to help students track their learning progress visually. Rather than using complex dashboards, it presents a minimalist calendar grid where users can click on any day, log the topic studied, and take quick notes for future review. 

This project was developed as the final project for CS50x 2026.

### Features
- **Anonymous Workspace Sessions**: Users are assigned an automatic UUID session on their first visit, allowing immediate personal data storage without requiring a registration or login barrier.
- **Dynamic Calendar**: Interactive calendar generated via JavaScript, allowing forward and backward month navigation with real-time day calculation.
- **Full CRUD Operations**: Users can Create, Read, Update, and Delete notes directly through an intuitive modal window.
- **Visual Status Badges**: Days with logged study sessions highlight automatically with a preview badge showing the topic.
- **Input Validation & Security**: Server-side validation for character limits, SQL injection protection via parameterized queries, and sanitized inputs.

### Project Architecture & File Structure
- `app.py`: The main Flask backend controller containing HTTP routes (`/`, `/logs`, `/save`), session workspace management, and database query executions using the `cs50.SQL` library.
- `schema.sql`: Contains the database schema definition creating the `logs` table and performance index.
- `study.db`: The SQLite database file storing persistent workspace logs.
- `templates/index.html`: The Jinja template rendering the base calendar layout, controls, and the study entry modal.
- `static/style.css`: Modern, clean CSS styles defining responsive grids, layout spacing, and modal overlays.
- `static/script.js`: Vanilla JavaScript handling calendar date calculations, DOM updates, and asynchronous `fetch` requests to the Flask API.
- `requirements.txt`: Python dependencies required to run the project (`Flask`, `cs50`).

### Design Decisions
During the development of Crononote, several design choices were made to keep the application lightweight and user-friendly. Instead of forcing users to create an account with a username and password, I opted for an anonymous session-based approach using Python's `uuid` library. This allows users to start logging their studies immediately. 

For the database, SQLite was chosen as it integrates perfectly with Flask and the `cs50.SQL` module taught in the course, providing a simple yet robust way to store text data. Security was also a priority; therefore, backend validations restrict the length of inputs (100 characters for topics and 5000 for notes) to prevent database overload, while parameterized SQL queries protect against SQL injection attacks.

### How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
