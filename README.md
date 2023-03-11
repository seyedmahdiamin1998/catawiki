## Catawiki Crawler
Catawiki Crawler is a project to crawl data from the Catawiki website. In this project, I focus on extracting **car ad** data.

> Catawiki is the most-visited curated marketplace in Europe for special objects, offering over 65,000 objects for auction each week. Their mission is to provide an exciting and seamless experience to their customers for buying and selling special, hard-to-find objects.
website: [https://www.catawiki.com/en/]

![Screenshot](.//assets//img//First_page.JPG)
![Screenshot](.//assets//img//categories.JPG)

___

## Intallation

```
$ pip install -r requirements.txt
```

or if you use pipenv for managing virtual environments you can either install dependencies by code below.

```
$ pipenv install
```
___

## Initiallization 
First of all you need to go to file **pipelines.py** and customize information of your **Postgresql** database.
```
self.USER = 'postgres'
self.PASSWORD = '1234'
```

Or if you want to connect to other databases like **SQLite**, **MySQL** , **oracle**, **Microsoft SQL Server**, or other databases which **sqlalchemy** support them, change the value of **SQLALCHEMY_DATABASE_URL**.

Now you are ready to run the spider which name is **car**.

```
$ cd catawiki
$ scrapy crawl car 
```

___

## Save results as json/csv/xml
If you want to save results as a **json**, **csv** or **xml** file, use below codes.
```
$ scrapy crawl car -o results.json

$ scrapy crawl car -o results.csv

$ scrapy crawl car -o results.xml
```
___

## result example
![Screenshot](.//assets//img//database.JPG)

___
## License
This project is licensed under the terms of the MIT license.