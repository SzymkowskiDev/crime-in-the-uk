
# Crime in the UK (data project)

Crime Stoppers (crimestoppers-uk.org) is a website that publishes articles on wanted criminals for various offences commited in the UK. Our project harvests this text data and implements Natural Language Processing on it to extract information such as: offender's name, crimes commited, narcotics involved, location, among others. Finally, analtics is performed on the data obtained.

<p align="center">
  <img src="documentation/diagrams/Project%20Diagram.png" width="800" title="hover text">
</p>


## 👨‍💻 Contributing
* [SzymkowskiDev](https://github.com/SzymkowskiDev)
* [Dawido090](https://github.com/Dawido090)

# 🤖 Technology stack
* Docker
* MongoDB
* Postgres
* Python
* pandas
* nltk
* spaCy
* Dash
* PowerBI

## 🚀 How to run
1. Clone the repository to the desired folder
2. Open Docker Desktop and make sure that the downloaded containers appear correctly
3. Open the CMD at the app folder and run the following command:
```cmd
docker compose up -d --build
```

Now, the databases run in the backround and are accessible from Jupyeter notebook or IDE of choice


## 🧱 Containers

* api - data enpoint, where FastAPI and SQLAlchemy are used to access the data.
* ingestor - container which loops over articles, after there is new article spotted, it's content is then added 
to mongodb
* mongo_raw - mongodb serving the project as raw storage of data
* postgres_final - postgres database which is used by Power BI and api to access the final data
* data_proc - responsible for processing raw data to find insights about articles, for example:
<br />  • what type of crime was commited?
<br />  • what is the reward for providing information?
<br />  • what was the location of event?

## ⭐ Features
Overview of technology domains employed in the project:

⭐ **Docker containerisation and orchestration**

⭐ **Natural Language Processing**

⭐ **No-SQL database storage and querying (MongoDB)**

⭐ **SQL database storage and querying (Postgres)**

⭐ **Data Manipulation with Pandas**

⭐ **Data Visualisation with PowerBI and Dash**

⭐ **Web scraping**

## 📅 Development Schedule
**Version 1.0.0**

- [X] Doker orchestration and databases setup
- [X] Web scrapper
- [X] NLP infromation extraction
- [ ] Dashboard

**Version 2.0.0**

- [ ] Computer Vision


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

## 🎓 Learning Materials
* [NLTK](https://github.com/nltk/nltk)

## 📧 Contact
[![](https://img.shields.io/twitter/url?label=/kamil-szymkowski/&logo=linkedin&logoColor=%230077B5&style=social&url=https%3A%2F%2Fwww.linkedin.com%2Fin%2Fkamil-szymkowski%2F)](https://www.linkedin.com/in/kamil-szymkowski/) [![](https://img.shields.io/twitter/url?label=@szymkowskidev&logo=medium&logoColor=%23292929&style=social&url=https%3A%2F%2Fmedium.com%2F%40szymkowskidev)](https://medium.com/@szymkowskidev) [![](https://img.shields.io/twitter/url?label=/SzymkowskiDev&logo=github&logoColor=%23292929&style=social&url=https%3A%2F%2Fgithub.com%2FSzymkowskiDev)](https://github.com/SzymkowskiDev)

[![](https://img.shields.io/twitter/url?label=/Dawid-Grzeskow/&logo=linkedin&logoColor=%230077B5&style=social&url=https%3A%2F%2Fhttps://www.linkedin.com/in/dawid-grzeskow%2F)](https:///www.linkedin.com/in/dawid-grzeskow/) [![](https://img.shields.io/twitter/url?label=/Dawido090&logo=github&logoColor=%2523292929&style=social&url=https://github.com/Dawido090)](https://github.com/Dawido090)


## 📄 License
[MIT License](https://choosealicense.com/licenses/mit/) ©️ 2019-2020 [Kamil Szymkowski](https://github.com/SzymkowskiDev "Get in touch!")

[![](https://img.shields.io/badge/license-MIT-green?style=plastic)](https://choosealicense.com/licenses/mit/)





