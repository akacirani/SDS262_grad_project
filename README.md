# SDS262_grad_project
Graduate project by Kimia S. and Arlind K.

Proposal:
One of the issues that we have noticed on campus has been the lack of a centralized system for events that occur in Engineering and Applied Science. There is an Events tab in Yale SEAS website, however, events from Applied Physics and Computer Science departments (which are part of SEAS) are featured only on their own department websites. Additionally the events from West Campus Institutes are usually not featured on main campus. Hence what we had in mind was to have Llama 2 retrieve the calendars from these 4 APIs (SEAS, AP, CS, West Campus) and build a search engine or directory that displays all the events (like seminars, talks, invited lectures, etc.) with dates and other details in one central location.

Instructor Feedback:
It might be useful to crawl all the calendars and put together something unified. It might not be super difficult if they give this in some a standard feed format. You can look at standard formats that are used to follow blog posts or calendar events (should be RSS I think). Not sure that they have this.
If they don't have something standard, one part of your team might want to look at libraries that help you crawl normal websites.
I'm not sure what an LLM would do with it though. Maybe it can be used to decide for each upcoming event if it fits ones interests based on some prompt sentence you would give it, or using a list of talks you liked or didn't like. One can imagine some kind of bot like this that you interact with to get updates.
Actually making a fancy bot might be a little too much, but some offline demonstration that would allow us to ask for talks on certain subjects would be a good project.


Plan:
1. Create a Jupyter Notebook to manage the entire project.
2. Use Python library BeautifulSoup to crawl the 4 websites' Events pages (SEAS, AP, CS, West Campus)
3. Use Llama 2 (by Meta) to create a chatbot that feeds from the search engine produced by crawling the websites.
4. Check on performance with a few examples.
5. Future Direction: Propose the feature for the new Yale Engineering website (provide code to Dean's Office).

Detailed Steps:

1. Getting a Replicate API token
  1. Go to https://replicate.com/signin/
  2. Sign in with GitHub account (username: akacirani, not Yale GutHub)
  3. Proceed to the API tokens page and copy the API token
2. Check for Python version (3.7.4 nd up)
  python --version
  Python 3.10.9
4. Upload Llama2_chatbot.py code on GitHub (modified from By Chanin Nantasenamat version)
3. Set up an API token:
  1. Setting up Streamlit Community Cloud account (arlind.kacirani@yale.edu GitHub)


## 1. Installation
1. To install Beautiful Soup 4 using pip, we ran the following command:
*pip install beautifulsoup4* 
About Beautiful Soup package that was used in this project: Beautiful Soup is a Python library used for web scraping, which is the process of extracting data from websites. It allowed us to parse HTML and XML documents, navigate the parse tree, and extract the information we needed from Yale events websites.

2. To install the lxml library using pip, we ran the following command:
*pip install lxml*
About lxml library: This library is often used as a parser with Beautiful Soup for more efficient and robust parsing of HTML and XML documents. 
## 3. Scraping Data - SEAS
Explaination of the code is scraping event information from the Yale School of Engineering & Applied Science (SEAS) website for the specified next three months and organizing it into a list of dictionaries containing details about each event. The html format for SEAS was different from other websites for other departments. The url for each month's events in different so we wrote a for loop for months. This is the explaination of the scaping for SEAS step by step:
 - *url_seas* is the base URL for SEAS events.
 - *months* is a list of strings representing the months for which events will be scraped. Here as there were events for the next three months, we scraped the     events for the next three months.
  
    1. The code iterates over each *month* in the *months* list which consists of months in spring.
    2. For each month, it constructs the url by appending the month to the base url.
    3. It sends a get request to the constructed url and retrieves the html content.
    4. Using *BeautifulSoup*, it parses the html content.
    5. It finds all the div elements (divisions) with the class *"item-list"*, which typically contain event information. This specific keyword for division was understood from the source page for the calender.
    6. Inside the loop for each month, it extracts event titles and times by finding div elements with specific classes *("views-field-title" and "views-field-field-event-time-value" respectively)*. This was also understood from the source page about what are these names for the classes and what keywords for divisions to use for these division to be able to extract the target information.
    7. It constructs the event link by finding the href attribute of the anchor tag within the *"views-field-title"* div.
    8. It stores the event information (title, time, link) in a dictionary named *events_for_month*.
    9. For each event found in a month, it appends a dictionary containing event details (title, link, date, department) to the *final_list*.
    10. The department information is hardcoded based on the SEAS departments.
    11. The events for each month are stored in the *list_of_event_seas* dictionary with the month as the key and the events dictionary *events_for_month* as the value.
    12. After scraping all months, the code prints the *final_list,* which contains all the scraped event information in a structured format.



## 4. Scraping Data - Computer Science
In this code, events from the Computer Science(CS) department at Yale are being scraped from their calendar webpage - the procedure for this code is similar to the one for SEAS but the format for CS was easier to scrap as months did not need to be specified and there was one url link for all the events.
- *list_of_event_cs* is initialized as an empty dictionary to store event titles as keys and event times as values.

    1. A request is sent to the URL of the CS department's calendar page, and the HTML content of the page is retrieved.
    2. BeautifulSoup parses the html content.
    3. The code finds all the table <td> elements with classes *"views-field views-field-title"* and *"views-field views-field-field-event-time"*, which contains event titles and times respectively. This was understood by looking at the source page for the calender.
    4. Inside the loop for each event and time, it extracts the event title and time by stripping any leading or trailing whitespace from the text content of the elements. It also extracts the event link by finding the href attribute of the anchor tag within the event element.
    5. For each event found, a dictionary containing event details (title, link, date, department) is appended to the final_list.
    6. The event title and time are also stored in the *list_of_event_cs* dictionary.

  
Finally, the code iterates over the items in the final_list and prints each item, displaying the event details.

## 5. Scraping Data - West Campus
The code  for West Campus is similar to the previous ones, but it targets the West Campus department's calendar page to scrape event information. For west campus, the code finds all the table <td> elements with classes *"views-field views-field-title"* and *"h3"*, which contain event titles and times respectively. *h3* is a font size for header and it was practical in the case of west campus to extract the information with *h3* font for the time, otherwise, when I extracted the class for time, it only extracted the time and not the date of the event.

 ## 6. Scraping Data - Applied Physics
Applied Physics' code follows a similar structure to the previous ones but adapts it to scrape event information specifically from the Applied Physics department's calendar page.

## 7. Convert Date Function
The convert_date function converts a date string into a desired format for all the datas to be unified for the sake of upgrading the quality of the list handed to the bot in the next steps. This function handles two different date formats:
- Full Date with Weekday: Format like "Monday, May 20, 2024 - 2:30pm - 4:00pm" ==> date format for the SEAS and Applied Physics events
- Date Only: Format like "April 19, 2024"  ==> date format for the West Campus, Computer Science events

1. Handling Full Date with Weekday: we first split the date string using the dash character to remove any additional time information. Then attempt to parse the date string using the %A, %B %d, %Y format specifier, which represents the full weekday name, full month name, day of the month, and year. If successful, it formats the parsed date object to the desired format %Y-%m-%d year-month-day.
2. Handling Date Only: If the first attempt fails (due to a ValueError) meaning it was not in the first format, ww tried parsing the date string using the %B %d, %Y format specifier, which represents the full month name, day of the month, and year. If successful, it formats the parsed date object to the desired format %Y-%m-%d year-month-day.
3. If both attempts fail (both ValueError exceptions are raised), it returns None. This  is not possible in this case unless the html and the date format on these were the different formats for dates. In case of the change, this function should be updated to be adapted with the new format.
