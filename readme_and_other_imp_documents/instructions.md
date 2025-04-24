```

**How to Run This Sample:**

1.  **Save Backend:** Save the Python code as `chatbot_app.py`.
2.  **Install Dependencies:** Open your terminal/command prompt, navigate to the directory where you saved the file, and install Flask and Flask-CORS:
    ```bash
    pip install Flask Flask-Cors
    ```
3.  **Run Backend:** Start the Flask server:
    ```bash
    python chatbot_app.py
    ```
    You should see output indicating the server is running, likely on `http://127.0.0.1:5001/` or `http://0.0.0.0:5001/`. Note the port number (5001 in this case).
4.  **Save Frontend:** Save the HTML code as an HTML file (e.g., `chatbot.html`).
5.  **Open Frontend:** Open the `chatbot.html` file directly in your web browser (usually by double-clicking it).
6.  **Interact:**
    * The login screen should appear.
    * Use the sample credentials (e.g., `alice@example.com` / `password123` or `admin@example.com` / `adminpassword`) to log in.
    * If you log in as an employee, the chat interface will appear. Ask questions like "how much vacation leave do I have?".
    * If you log in as admin, the admin panel will appear. You can select an employee from the dropdown and click "View Details".
    * Use the logout button when finished.

This provides a basic, runnable demonstration of the core concepts discussed in the architecture overvi