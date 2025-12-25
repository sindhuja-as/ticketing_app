**GAME-ON – Automatic Ticket Categorization System**
This application automatically categorizes and routes customer complaints for the GAME-ON gaming app using Machine Learning. It helps support teams handle tickets faster and more accurately.

1. Problem Statement
As the number of users grows, manually reading and routing complaints becomes inefficient. This system classifies complaints into predefined categories and routes them to the correct team.
2. Complaint Categories with Examples
Billing
    • - I was charged twice for my GAME-ON premium subscription
    • - Refund for my in-game purchase is still not credited
    • - Money deducted but gems were not added to my account
Technical
    • - GAME-ON crashes when I start a multiplayer match
    • - Game freezes on the loading screen
    • - Unable to connect to the GAME-ON servers
Product
    • - Matchmaking is unfair and unbalanced
    • - Rewards system is not working as expected
    • - New update removed important game features
Account
    • - Unable to login to my GAME-ON account
    • - Password reset link is not working
    • - My account got locked without explanation
Other
    • - Customer support is not responding
    • - Overall experience with GAME-ON is disappointing
    • - I have a general feedback about the game
3. System Architecture
• Streamlit UI for complaint submission and dashboard
• Text preprocessing using NLP techniques
• Machine Learning model for classification
• Confidence-based routing logic
• SQLite database for ticket storage

4. Workflow / Order of Execution
1. User enters complaint in Streamlit UI
2. Text is preprocessed (cleaning, lemmatization)
3. Model predicts category and confidence
4. Low-confidence complaints go to Pending Review
5. Valid tickets are saved to SQLite database
6. Dashboard displays tickets with filters

5. How to Run the App
1. Create virtual environment and activate it
2. Install dependencies using requirements.txt
3. Run: streamlit run app.py
4. Open browser and start submitting complaints
6. Database
SQLite database (tickets.db) is used.
Tickets are stored with ID, complaint text, category, routing, confidence and status.
7. Key Features
• Automatic ticket categorization
• Confidence-based validation
• Daily-reset ticket ID generation
• Interactive dashboard with filters
• Easy deployment on AWS EC2
