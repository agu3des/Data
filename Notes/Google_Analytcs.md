# Gemini for Data Scientists and Analysts
### Transcription:
This is a data professional.
They might be a data analyst, data engineer, or data scientist.
We'll refer to them as the **data pro**.
Let's learn how you can use **BigQuery, Gemini, and Vertex AI** to analyze your data to categorize new customers or gain insights like predicted product sales.
Later, you'll use Gemini, Vertex AI, and BigQuery to generate useful next steps for a marketing campaign.
They've recently joined a new company, and part of their role requires them to turn their team's manufacturing plant dashboard from a reactive one into a **proactive one** so that their team can anticipate issues with equipment.
The data pro is here to help ensure that the equipment is functioning properly.
They do that by using data to create reporting mechanisms that **predict when maintenance should occur**.
And **Gemini** is here to help the data pro.
The first step is to open the manufacturing plant dashboard powered by **Looker**.
All of the plant's real-time structured and unstructured data is loaded into **Google Cloud**, analyzed and presented here.
They can identify that one of the plants is having some issues, so they click into it to explore.
Immediately, they notice that throughput has been below target for a number of hours, starting at 2 PM.
The data pro decides to use **Gemini in Looker** to learn why throughput is down.
In the chat window, they prompt Gemini, "why did the throughput drop at 2 PM?"
Gemini responds with the production line that throughput dropped for.
And because it knows the context of the situation, Gemini has gone one step further and suggested additional questions to ask, like this one, "which metrics correlate with the dip?"
From the response, the data pro realizes that there are some equipment issues.
Gemini has gathered from routine diagnostics some machine statistics that our pro will use to start communicating the physical fix to technicians.
This is really helpful for our data pro.
Now, our data pro can understand why they were tasked with making this dashboard proactive instead of reactive.
They need to build a **preventative maintenance model** to predict future downtime and avoid it.
To build and ship a data model, they start in **BigQuery Studio**, a simple, unified environment where they can build anything they want, including in Python.
First, they determine what data already exists so they don't have to start from the beginning.
There are two data sets, one in Google Cloud and another in a different cloud.
They notice a **throughput table** that might be a promising starting point.
They open it to validate the usefulness and quality of the data.
When they open the table, they use the **data profile tool** to perform some light exploratory data analysis.
They also note that there are automated quality checks in place, which is a good sign, so they know this data is actively maintained.
There is even an **insights tab** where Gemini has already analyzed the data and how it's being used, and proactively suggests insights for business questions that our data pro might want to answer.
They decide to open and run one of the queries in BigQuery to further explore the insights.
They appreciate how helpful these insights are to build their understanding of this data quickly.
It seems that another data set also has some reference data, so they'll pull that into the model, too.
Because they're building multiple ML projects, they decide to do this in a **Python Notebook** so collaboration is easier.
**Gemini supports SQL generation and completion**, so they ask it to use the multicloud data to help build a model that can predict throughput based on the attributes currently available.
In the Python Notebook itself, they prompt Gemini by clicking **+ Code** and typing in a prompt to create a logistics regression model.
And just like that, the SQL is ready, that saved our data pro a lot of time.
It also interconnected the data across multiple clouds by using a simple **SQL join in real time** without the need for complex operations or processes here.
Gemini helps our data pro code faster, discover the data, answer business questions, and generate insights.
Amazing, our data pro wants to ensure that the model will actually run on real-time data because it was trained on a table, not a data stream.
First, they use a few lines to verify that the model is actively running against the production data and with predictions, so the model is ready.
Predictions are a good start, but the data pro wants to go further and actually help the plant operators by giving them **recommendations** for how they can keep the plant working optimally.
Luckily, there is some more data available this time **unstructured inspector reports** that may help.
They use **retrieval augmented generation**, which means that they will use their own data and an **LLM**, a large language model, to build an **agent** using tools to connect to their data.
These tools will help improve the reliability of responses from the LLM and reduce **hallucinations**, which happen when the LLM produces inaccurate responses.
Sounds like a lot of work, but they're going to do it in a few lines of code.
First, they'll bring AI to the data in BigQuery.
They use **LLMs powered by Vertex AI and BigQuery's new ML inference engine** to connect to all these amazing models.
Summarize the reports and create **vectors** or numeric representations of their text to help with searches and groupings.
Next, they pass a question or prompt into the LLM to get the vectors and summary.
Then they use the summaries to ask the LLM for recommendations to get the predictive actions and the results are displayed.
This would have taken our data pro a lot of time and effort to do if they used traditional data science methods.
Here they did it with a few functions and in a couple of minutes by using the power of **generative AI** and all in BigQuery where their data remains secure.
Now the pipeline is deployed.
Here are the pipeline results back in the plant dashboard where the predictive results are now displayed.
Our data pro can even set actions by using **Looker** so that the right people are notified to take action on the new recommendations.
Our data pro has succeeded in helping the equipment monitoring dashboard move from **reactive to proactive**.
And with all that time saved, they can now finally get around to playing the ukulele.