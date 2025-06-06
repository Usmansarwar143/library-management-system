<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library Management System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            max-width: 800px;
        }
        h1, h2, h3 {
            color: #333;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        code {
            font-family: 'Courier New', Courier, monospace;
        }
        ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .toc {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Library Management System</h1>
    <p>A database-driven <strong>Library Management System</strong> built with <strong>Python</strong>, <strong>Tkinter</strong>, and <strong>MySQL</strong> to manage library operations efficiently. This project was developed as part of a Database Management Systems (DBMS) course by <strong>[Your Name]</strong>, <strong>Asma Channa</strong>, and <strong>Soyam Kapoor</strong>, under the supervision of <strong>Ma'am Zainab Umair</strong>.</p>

    <h2>Table of Contents</h2>
    <div class="toc">
        <ul>
            <li><a href="#project-overview">Project Overview</a></li>
            <li><a href="#features">Features</a></li>
            <li><a href="#database-schema">Database Schema</a></li>
            <li><a href="#technologies-used">Technologies Used</a></li>
            <li><a href="#installation">Installation</a></li>
            <li><a href="#usage">Usage</a></li>
            <li><a href="#screenshots">Screenshots</a></li>
            <li><a href="#contributing">Contributing</a></li>
            <li><a href="#credits">Credits</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </div>

    <h2 id="project-overview">Project Overview</h2>
    <p>The Library Management System automates library operations, including user authentication, book and member management, transaction tracking, and report generation. It supports two user roles:</p>
    <ul>
        <li><strong>Admin</strong>: Manages books, members, transactions, and reports.</li>
        <li><strong>User</strong>: Searches/views books and tracks borrowed books.</li>
    </ul>
    <p>The system integrates a MySQL database with a Tkinter GUI styled using <code>ttkbootstrap</code> (flatly theme) for a user-friendly experience.</p>

    <h2 id="features">Features</h2>
    <ul>
        <li>Secure user authentication with role-based access.</li>
        <li>Book management: add, search, and view books.</li>
        <li>Member management: add and view library patrons.</li>
        <li>Transaction management: issue/return books, view issued/overdue books.</li>
        <li>Reports: overdue books, fine summaries, CSV export.</li>
        <li>GUI enhancements: scrollable tables, quick-action buttons, input validation.</li>
        <li>Database integrity via constraints (primary keys, foreign keys, unique, check).</li>
    </ul>

    <h2 id="database-schema">Database Schema</h2>
    <p>The MySQL database (<code>library_system</code>) consists of four tables:</p>

    <h3>1. USERS</h3>
    <pre><code class="language-sql">CREATE TABLE USERS (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL
);</code></pre>
    <p>Stores user credentials; default admin: <code>username: admin, password: admin123</code>.</p>

    <h3>2. BOOKS</h3>
    <pre><code class="language-sql">CREATE TABLE BOOKS (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0)
);</code></pre>
    <p>Manages book inventory.</p>

    <h3>3. MEMBERS</h3>
    <pre><code class="language-sql">CREATE TABLE MEMBERS (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15)
);</code></pre>
    <p>Stores patron details.</p>

    <h3>4. TRANSACTIONS</h3>
    <pre><code class="language-sql">CREATE TABLE TRANSACTIONS (
    txn_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    issue_date DATE NOT NULL,
    return_date DATE NOT NULL,
    actual_return_date DATE,
    fine DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES MEMBERS(member_id) ON DELETE CASCADE
);</code></pre>
    <p>Tracks book borrowing/returning.</p>

    <h2 id="technologies-used">Technologies Used</h2>
    <ul>
        <li><strong>Backend</strong>: MySQL, Python 3.x</li>
        <li><strong>Frontend</strong>: Tkinter, <code>ttkbootstrap</code> (flatly theme)</li>
        <li><strong>Libraries</strong>:
            <ul>
                <li><code>mysql-connector-python</code>: Database connectivity</li>
                <li><code>bcrypt</code>: Password hashing</li>
                <li><code>pandas</code>: CSV export</li>
            </ul>
        </li>
        <li><strong>Tools</strong>: MySQL Workbench, VS Code</li>
    </ul>

    <h2 id="installation">Installation</h2>
    <ol>
        <li><strong>Clone the Repository</strong>:
            <pre><code class="language-bash">git clone https://github.com/[your-username]/library-management-system.git
cd library-management-system</code></pre>
        </li>
        <li><strong>Set Up MySQL Database</strong>:
            <p>Install MySQL and MySQL Workbench. Create the database and tables:</p>
            <pre><code class="language-sql">CREATE DATABASE library_system;
USE library_system;
CREATE TABLE USERS (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL
);
CREATE TABLE BOOKS (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0)
);
CREATE TABLE MEMBERS (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15)
);
CREATE TABLE TRANSACTIONS (
    txn_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    issue_date DATE NOT NULL,
    return_date DATE NOT NULL,
    actual_return_date DATE,
    fine DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES MEMBERS(member_id) ON DELETE CASCADE
);
INSERT INTO USERS (username, password, role) 
VALUES ('admin', '$2b$12$7z5Qz7n3gX9j4q2mW9t6S.qX6o3z8q9z4v3mW9t6S.qX6o3z8q9z4', 'admin');
</code></pre>
        </li>
        <li><strong>Install Dependencies</strong>:
            <pre><code class="language-bash">pip install ttkbootstrap mysql-connector-python bcrypt pandas</code></pre>
        </li>
        <li><strong>Configure Database Connection</strong>:
            <p>Update <code>database/db_config.py</code> with your MySQL credentials (host, user, password).</p>
        </li>
        <li><strong>Run the Application</strong>:
            <pre><code class="language-bash">python login_window.py</code></pre>
        </li>
    </ol>

    <h2 id="usage">Usage</h2>
    <ol>
        <li><strong>Login</strong>:
            <p>Use <code>username: admin, password: admin123</code> to access the Admin Dashboard. Register a new user (role: user) to access the User Dashboard.</p>
        </li>
        <li><strong>Admin Dashboard</strong>:
            <p>Add books/members, issue/return books, view transactions, and generate reports.</p>
        </li>
        <li><strong>User Dashboard</strong>:
            <p>Search/view books and check borrowed books.</p>
        </li>
        <li><strong>Database Interaction</strong>:
            <p>Use MySQL Workbench to query tables (e.g., <code>SELECT * FROM BOOKS;</code>).</p>
        </li>
    </ol>

    <h2 id="screenshots">Screenshots</h2>
    <p><em>Coming soon!</em></p>
    <ul>
        <li>Login Window</li>
        <li>Admin Dashboard</li>
        <li>Add Book Form</li>
        <li>Transaction Table</li>
    </ul>

    <h2 id="contributing">Contributing</h2>
    <p>Contributions are welcome! Please fork the repository, create a branch, and submit a pull request with your changes. Ensure code follows PEP 8 guidelines and includes relevant tests.</p>

    <h2 id="credits">Credits</h2>
    <ul>
        <li><strong>Developers</strong>: [Your Name], Asma Channa, Soyam Kapoor</li>
        <li><strong>Supervisor</strong>: Ma'am Zainab Umair</li>
        <li><strong>Course</strong>: Database Management Systems</li>
    </ul>

    <h2 id="contact">Contact</h2>
    <p>For questions or feedback, reach out to [Your Name] at <a href="mailto:[your-email@example.com]">[your-email@example.com]</a> or connect on <a href="#">LinkedIn</a>.</p>
</body>
</html>
