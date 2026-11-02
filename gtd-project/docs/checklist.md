# Checklist

## PHASE 1: DESIGN

1. Choose the data source you want to analyse. This must allow you produce, in the end, the number of dimensions, measures and hierarchies required by the project specifications and a set of interesting analyses
2. If the data source is on csv or excel files, carry out a re-engineering step to compose a database schema (E/R or Relational model) fitting the data. This is important to both well understand the data and give it a structure. Let’s call it the “schema of the reconciled database”
3. Build the schema for the reconciled database on a DBMS of your choice. Let’s call it the “reconciled database”
4. Conceptual design of your Fact schema:
   a. Choose the fact from the reconciled database
   b. Build the attribute tree and follow all the steps to obtain a DFM Schema using the data driven approach studied during the class
5. Logical design:
   a. Translate the DFM Schema in a Star schema
   b. Build the schema of the star schema on the DBMS of your choice. Let’s call it the “data warehouse” for simplicity

## PHASE 2: DATA MANAGEMENT

1. Populate the reconciled database from the csv file or excel (if any)
2. Design and implement your data quality and cleaning tasks. You can use any tool of your choice for this step (e.g. python, colab, etc.). You can carry out this step either on the reconciled database or on the original csv/excel before populating the database (note that different considerations must be carried
   Checklist

out in the two cases), but the optimal choice would be on the reconciled database

3. If you use python, colab or similar tools, please share the repository containing the code (e.g., using a public github)
4. Design the ETL process from the reconciled database to the data warehouse. You can use any tool of your choice for this step (e.g. python, tableau prep, pentaho, etc. )

## PHASE 3: DATA VISUALIZATION

1. Think about the story you want to tell about your data….
2. Build your analysis charts with Tableau (Sheets and Dashboards; Stories are optional), or any other tool of your choice. Remember that if you use Tableau, you should use Tableau public which does not accept database connections, so you should export your datawarehouse back to csv or excel.
3. Remember that you must allow a dynamic analysis (OLAP), so avoid having only static charts (you should allow applying roll-up, drill-down, slice and dice, ecc. when this makes sense)
4. Remember that you should not only tell the “what” is in the data but also the “why”
5. Remember to apply the data visualization principles studied during the course WHAT DO YOU HAVE TO SUBMIT (email to <u>giorgio.terracina@unical.it</u>):
6. One week before the exam, a short report that presents what you have done in Phase 1 and Phase 2
7. The report must contain at least:
   - A brief description of the data source and the preliminary requirement analysis (what would you analyse)
   - The schema of the reconciled database
   - A description of data quality assessment and data cleaning tasks
     Checklist
   - All the steps for the conceptual design (choice of the fact, attribute tree construction and editing, DFM fact schema design). All the steps must be motivated.
   - The logical star schema, along with the glossary of the measures.
   - No need to include the Analysis sheets or dashboards into the report.
8. The day before the exam a 5 minutes pitch (a ppt, a video, or whatever you prefer) presenting your story. This will be projected during the exam.
9. Bring with you your laptop with all project files (report, code, penthao, tableau, etc.). If needed I will ask you to show me something in more detail.
   Checklist
