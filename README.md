
# Crime in the UK (data project)

![crime-stoppers](https://github.com/SzymkowskiDev/crime-in-the-uk/blob/master/crime_stoppers.gif)

The project is focused on processing crime in the UK.
The idea is to take data from https://crimestoppers-uk.org/ which is UK charity website, focused on
providing information about crimes, and rewards for providing informations about perpetrators of crimes.

The project's purpose is to harvest information from the website, store its content in MongoDB, and then process it with
data_proc container, in order to find context of each article using NLP libraries. The processed data is then added to Postgres, which serves as source for Power BI and API for data access and further analysis. 

## Contents

Containers explained:

api - data enpoint, where FastAPI and SQLAlchemy are used to access the data.

ingestor - container which loops over articles, after there is new article spotted, it's content is then added 
to mongodb

mongo_raw - mongodb serving the project as raw storage of data

postgres_final - postgres database which is used by Power BI and api to access the final data

data_proc - responsible for processing raw data to find insights about articles, for example:
<br />  • what type of crime was commited?
<br />  • what is the reward for providing information?
<br />  • what was the location of event?


## 🚀 How to run
Open the CMD at the app folder and run the following command:
```python
docker compose up -d --build
```


## 📋 Requirements
Docker Desktop
Power BI Desktop for dashboard

## ⭐ Features
Introductory sentance.

⭐ **Feature 1**

Data analytics report to freely analyze stored content
<!-- *insert images when report is created* -->

⭐ **Feature 2**

Api access to SQL database

## 📝 Examples
**Example 1. Title**

Description of the example.
```javascript
CODE GOES HERE
```
**Example 2. Title**

Description of the example.
```javascript
CODE GOES HERE
```

## 👨‍💻 Contributing
Sth

## 📦 Builds
Sth

## 📂 Directory Structure

    ├───app
    │   ├───api
    │   ├───ingestor
    │   ├───mongo_raw
    │   ├───postgres_final
    │   ├───powerbi
    │   └───data_proc
    └───documentation
        └───diagrams

## 📅 Release schedule / Development schedule / Plans / TODOs
**Version 1.0.0**

- [x] Feature 1
- [x] Feature 2
- [x] Feature 3

**Version 2.0.0**

- [ ] Feature 4
- [ ] Feature 5
- [ ] Feature 6

## 🆕 Changelog
A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project.

## ⚙ Configurations
Sth

## 💡 Tips
💭 **Tip 1**

Description of tip 1.

💭 **Tip 2**

Description of tip 1.

## 🚧 Warnings / Common Errors / Known Issues

⚠️ **Warning 1**

Description of warning 1.

⚠️ **Warning 2**

Description of warning 2.

## 🧰 Troubleshooting
🚩 **Error 1**

Solution to error 1.

``` SOLUTION CODE ```

🚩 **Error 2**

Solution to error 2.


``` SOLUTION CODE ```

## 📖 Documentation
Link to the wiki or external site.

## 🔗 Related Projects / Thanks / References / Acknowledgement 
* Description 1 [Name 1](http://markdown.github.io)
* Description 2 [Name 2](http://markdown.github.io)
* Description 3 [Name 3](http://markdown.github.io)

## 🎓 Learning Materials
* Description 1 [Name 1](http://markdown.github.io)
* Description 2 [Name 2](http://markdown.github.io)
* Description 3 [Name 3](http://markdown.github.io)

## 📧 Contact
[![](https://img.shields.io/twitter/url?label=/SzymkowskiDev&style=social&url=https%3A%2F%2Ftwitter.com%2FSzymkowskiDev)](https://twitter.com/SzymkowskiDev) [![](https://img.shields.io/twitter/url?label=/kamil-szymkowski/&logo=linkedin&logoColor=%230077B5&style=social&url=https%3A%2F%2Fwww.linkedin.com%2Fin%2Fkamil-szymkowski%2F)](https://www.linkedin.com/in/kamil-szymkowski/) [![](https://img.shields.io/twitter/url?label=@szymkowskidev&logo=medium&logoColor=%23292929&style=social&url=https%3A%2F%2Fmedium.com%2F%40szymkowskidev)](https://medium.com/@szymkowskidev) [![](https://img.shields.io/twitter/url?label=/SzymkowskiDev&logo=github&logoColor=%23292929&style=social&url=https%3A%2F%2Fgithub.com%2FSzymkowskiDev)](https://github.com/SzymkowskiDev)

[![](https://img.shields.io/twitter/url?label=/Dawid-Grzeskow/&logo=linkedin&logoColor=%230077B5&style=social&url=https%3A%2F%2Fhttps://www.linkedin.com/in/dawid-grzeskow%2F)](https:///www.linkedin.com/in/dawid-grzeskow/) [![](https://img.shields.io/twitter/url?label=/Dawido090&logo=github&logoColor=%2523292929&style=social&url=https://github.com/Dawido090)](https://github.com/Dawido090)


## 📄 License
[MIT License](https://choosealicense.com/licenses/mit/) ©️ 2019-2020 [Kamil Szymkowski](https://github.com/SzymkowskiDev "Get in touch!")

[![](https://img.shields.io/badge/license-MIT-green?style=plastic)](https://choosealicense.com/licenses/mit/)





