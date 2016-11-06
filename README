# CS 575 Project

## Main Functions
For our project, we will be developing a system to aggregate and display varied information about a group of computers, phones, and other computing devices. For example, a sysadmin could use this application to monitor the machines they are responsible for. The user would interact with our service by installing our application on machines to be monitored. The user would label each machine with a unique ID and select different statistics and events for monitoring, such as CPU usage, IP address, disk usage, etc. Our service would then aggregate this data from all of the user’s computers and display it on our web interface. Numeric data such as CPU usage could be displayed as a graph over time, and other data like geolocation could be displayed using a map.


## Distributed Infrastructure
We intend to implement this system via a client-server architecture, wherein an application on monitored computers will push information to a server, which will aggregate the information and provide it to the administrator upon request. The clients and server will communicate over a JSON REST protocol, and the server will also host a website for the user to view their data.


## Programming Languages
We intend to build the data-gathering applications in Java, the server in Python using the flask framework, and the front-end for viewing the data in HTML/CSS/Javascript. 


## Development Environment
We will be using Intellij IDEA for java code and PyCharm for python and HTML/CSS/Javascript.


## Maintainability & Future Extension
We intend to support maintainability by designing our code for extension through software design principles and common design patterns. This idea will be enforced by initially implementing a minimal product and iteratively expanding it throughout the term. We also intend to enforce good coding standards in terms of readability, and maintain thorough documentation for the system. The main areas which we will focus on for future expansion are additional monitoring services (such as GPS location, battery percentage, active SSH connections, etc.), support for other operating systems (such as OSX, Android, IOS, Linux), and APIs for advanced users to allow direct communication with the server over the REST interface, and to allow for custom monitoring. More robust security to prevent users from retrieving or modifying others’ data will also be left for future extensions.


## Repository & Issue Tracking
Version control and issue tracking will be handled via GitHub in a repository created by one of our group members. We will begin our development process by adding all intended features to the issue tracker. Each feature will become it’s own branch, and upon completion of the code and unit tests, the branch will be submitted for review by at least two other group members in a pull request. After successful review, the issue will be closed and the branch will be merged. Any bugs found later or extensions added to the project will be added to the issue tracker and managed in the same way.


## Testing Framework
JUnit will be used as the testing framework for the java app, and the built-in unittest library will be used for Python. Selenium and manual testing of user stories and use cases will be used for testing the website, as well as for functional testing of the app and server. Unit tests will be written and submitted with features as described above under issue tracking, and ensuring adequate unit test coverage will be part of the review process. Functional tests will be written by the QA tester.


## Roles
All members will be responsible for some features and unit testing for their own code, as well as following the review process for other member’s code. Other roles are as follows:
* Karishma Changlani - Database and QA
* Max Mattes - REST API, Server, and Software Architecture
* Patrick Hislop - Java Application and Process Management
* Aditya Patwa - Website and UI Designer


## Timeline
1. Nov 12 - basic components and architecture plans: 
    1. Basic Database - Karishma
    1. Simple Flask server - Max
    1. Post requests to server from Java App - Patrick
    1. Architecture Fleshed out - Max
    1. Receive information from Rest Api to Website - Aditya
    1. Additional Documentation - Everyone
1. Nov 21 - minimal functioning service:
    1. Retrieve IP Address - Patrick
    1. Receive IP Addresses through API - Max
    1. Store IP Addresses - Karishma
    1. Display IP Addresses on Website - Aditya
1. Nov 30 - extension and testing:
    1. Retrieve other data - Patrick
    1. Process & Store other data - Max
    1. Display other data - Aditya
    1. Functional Testing - Karishma
1. Dec 8th - completed service with testing:
    1. User login - Max & Aditya
    1. Completed testing - Karishma
    1. Any additional data to collect and display - Patrick & Aditya
