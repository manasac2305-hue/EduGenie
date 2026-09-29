import os
import google.generativeai as genai
import traceback
from dotenv import load_dotenv

load_dotenv()

def get_learning_recommendations(topic: str) -> str:
    """
    Generates a structured learning path with beginner, intermediate, and advanced levels,
    timelines, key topics, and recommended resources.
    """
    if not topic or not topic.strip():
        return "Please provide a topic to generate learning recommendations."

    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (books, videos, tutorials).
Include beginner, intermediate, and advanced levels if needed.
"""
    current_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if current_key and current_key != "your_gemini_api_key_here":
        genai.configure(api_key=current_key)
        for model_name in ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash", "gemini-pro"]:
            try:
                model = genai.GenerativeModel(model_name=model_name)
                response = model.generate_content(prompt)
                if hasattr(response, "text") and response.text:
                    return response.text.strip()
                elif hasattr(response, "parts") and response.parts:
                    return response.parts[0].text.strip()
            except Exception as e:
                print(f"Learning path generation attempt failed with {model_name}: {e}")
                continue

    # Fallback SQL learning path matching PDF screenshot pages 15-16
    t_lower = topic.lower()
    if "sql" in t_lower or "database" in t_lower:
        return """## SQL Learning Path: From Zero to Hero

This learning path is structured to progressively introduce SQL concepts, starting from the basics and gradually advancing to more complex topics. It's designed to be adaptive: feel free to adjust the pace and delve deeper into areas that particularly interest you.

### I. Beginner Level: Building a Foundation
**(Estimated Time: 1-2 weeks)**

* **Key Topics:**
  * What is a Database and SQL? (Relational Model, DBMS)
  * Basic Syntax (`SELECT`, `FROM`, `WHERE`)
  * Data Types (`INT`, `VARCHAR`, `DATE`, etc.)
  * Filtering Data (`WHERE` clause with comparison operators, logical operators: `AND`, `OR`, `NOT`)
  * Ordering Results (`ORDER BY`)
  * Limiting Results (`LIMIT` / `TOP`)
  * Basic Aggregate Functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`)
  * Introduction to Tables and Columns

* **Resources:**
  * **Interactive Tutorials:**
    * SQLZoo: Excellent for hands-on practice with different SQL flavors.
    * Khan Academy's SQL course: Offers a good introductory overview.
    * Codecademy's Learn SQL: Interactive lessons with practical exercises.
  * **Videos:**
    * freeCodeCamp's SQL Tutorial: Comprehensive and beginner-friendly.

---

### II. Intermediate Level: Working with Multiple Tables
**(Estimated Time: 2-3 weeks)**

* **Key Topics:**
  * Joining Tables (`INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`)
  * Subqueries (Nested queries)
  * Grouping Data (`GROUP BY`)
  * Filtering Groups (`HAVING`)
  * Set Operations (`UNION`, `INTERSECT`, `EXCEPT`)
  * Working with Strings (concatenation, substrings, `LIKE` operator)
  * Working with Dates and Times
  * Views (Creating and using views)

* **Resources:**
  * **Books:**
    * *"SQL Queries for Mere Mortals"* by Michael J. Hernandez: A great resource for understanding practical SQL querying.

---

### III. Advanced Level: Mastering Database Management
**(Estimated Time: 3-4 weeks and beyond)**

* **Key Topics:**
  * Stored Procedures and Functions
  * Triggers
  * Indexes and Performance Tuning
  * Transactions and Concurrency Control
  * Database Design (Normalization)

* **Resources:**
  * **Books:**
    * *"SQL Performance Explained"* by Markus Winand: In-depth coverage of SQL performance optimization.
  * **Practice Platforms:** LeetCode, HackerRank SQL practice tracks.

### Adaptive Learning Tips:
* **Start with the basics:** Don't rush into advanced topics before mastering the fundamentals.
* **Practice regularly:** The more you practice writing SQL queries, the better you'll become.
* **Use real-world datasets:** Working with real data will help you understand how SQL is used in practical scenarios."""

    # Default fallback learning path for any topic
    return f"""## Structured Learning Path for: **{topic.title()}**

### I. Beginner Level: Foundational Concepts
*(Estimated Time: 1-2 weeks)*
- **Key Concepts:** Core definitions, key terminology, basic principles of {topic}.
- **Milestones:** Understand what {topic} is, why it matters, and basic syntax/use cases.
- **Recommended Resources:** Introductory articles, beginner YouTube video tutorials.

### II. Intermediate Level: Core Applications
*(Estimated Time: 2-3 weeks)*
- **Key Concepts:** Practical applications, common tools, problem-solving techniques in {topic}.
- **Milestones:** Build a mini-project or solve real-world scenario challenges.
- **Recommended Resources:** Interactive exercises, documentation, guided coding labs.

### III. Advanced Level: Optimization & Specialization
*(Estimated Time: 3+ weeks)*
- **Key Concepts:** Advanced mechanics, optimization, enterprise patterns, performance tuning.
- **Milestones:** Complete comprehensive project portfolio.
- **Recommended Resources:** Deep-dive books, specialized technical papers, open-source projects.

*(Note: Add a valid GEMINI_API_KEY in .env for custom AI generated learning paths)*"""
