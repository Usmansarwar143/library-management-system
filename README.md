# Library Management System

The **Library Management System** is a database-driven application designed to streamline library operations, developed as part of a Database Management Systems (DBMS) course. This project was collaboratively built by **Muhammad Usman**, **Asma Channa**, and **Soyam Kapoor**, under the supervision of **Ma'am Zainab Umair**. It leverages a MySQL database and a Python Tkinter GUI to provide an efficient, user-friendly platform for managing library resources.

The system supports two user roles: **Admin** (for managing books, members, transactions, and reports) and **User** (for searching/viewing books and tracking borrowed items). It emphasizes robust database design and intuitive interface to meet library management needs.

## Key Features

The Library Management System offers the following core functionalities:

- **User Authentication**: Secure login and registration with role-based access for admins and users.
- **Book Management**: Add, search, and view books in the library inventory.
- **Member Management**: Register and view library patrons’ details.
- **Transaction Management**: Issue and return books, and track borrowed or overdue items.
- **Reporting**: Generate reports on overdue books, transaction summaries, and export data for further analysis.
- **User Interface**: Intuitive navigation through a graphical interface with interactive tables and quick-access buttons.


## System Requirements

To run the Library Management System, ensure your environment meets the following requirements:

- **Operating System**: Windows, macOS, or Linux
- **Software**:
  - Python 3.8 or higher
  - MySQL 8.0 or higher
  - MySQL Workbench (recommended for database management)
- **Python Libraries**:
  - `ttkbootstrap`
  - `mysql-connector-python`
  - `bcrypt`
  - `pandas`
- **Hardware**:
  - Minimum 4 GB RAM
  - 500 MB free disk space for installation and database
- **Additional Tools**:
  - Git for cloning the repository
  - Code editor (e.g., VS Code) for configuration



    <h2>Installation and Running Instructions</h2>
    <p>To set up and run the Library Management System, follow these steps:</p>
    <ol>
        <li><strong>Clone the Repository</strong>:
            <p>Clone the project using Git:</p>
            <pre><code>git clone https://github.com/[your-username]/library-management-system.git
cd library-management-system</code></pre>
        </li>
        <li><strong>Set Up the MySQL Database</strong>:
            <p>Install MySQL and MySQL Workbench. Use the SQL schema in the project’s <code>docs/</code> folder to create the database and tables. Configure the default admin user with <code>username: admin</code> and <code>password: admin123</code>.</p>
        </li>
        <li><strong>Install Python Dependencies</strong>:
            <p>Ensure Python 3.8 or higher is installed. Install required libraries using pip:</p>
            <pre><code>pip install ttkbootstrap mysql-connector-python bcrypt pandas</code></pre>
        </li>
        <li><strong>Configure Database Connection</strong>:
            <p>Update <code>database/db_config.py</code> with your MySQL credentials (host, user, password).</p>
        </li>
        <li><strong>Launch the Application</strong>:
            <p>Run the application from the project directory:</p>
            <pre><code>python login_window.py</code></pre>
            <p>The login window will open.</p>
        </li>
        <li><strong>Use the System</strong>:
            <p>Log in as an admin using <code>username: admin</code> and <code>password: admin123</code> for the Admin Dashboard. Register a new user for the User Dashboard.</p>
        </li>
    </ol>
## Contribution and Contact

**Contributing**  
We welcome contributions to enhance the Library Management System! To contribute:
- Fork the repository on GitHub.
- Create a new branch for your changes.
- Submit a pull request with a clear description of your improvements.
- Ensure your contributions align with the project’s goals and follow standard coding practices.

## 📞 Contact

If you have any questions, suggestions, or would like to connect with the project contributors, feel free to reach out through the following platforms:

### 👨‍💻 Muhammad Usman  
- [LinkedIn](https://www.linkedin.com/in/muhammad-usman-018535253)  
- 📧 Email: muhammadusman.becsef22@iba-suk.edu.pk 

### 👩‍💻 Asma Channa  
- [LinkedIn](https://www.linkedin.com/in/iasmachanna/)
- 📧 Email: asmachanna.becsef22@iba-suk.edu.pk

### 👨‍💻 Soyam Kapoor  
- [LinkedIn](https://www.linkedin.com/in/soyamkapoor/)  
- 📧 Email: soyamkapoor.becsef22@iba-suk.edu.pk 

