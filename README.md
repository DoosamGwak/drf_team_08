# blame_news

## Introduction
- Projectname : spartamarket drf
- Build shoping mall back-end with using django-DRF
 
## Contributors
- Seungju Yi
- Dongin Seo

## Duration
- 2024.09.11 ~ Now

## TechStack
- Back-End
  - <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 3.10.11
- framework
  - <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> 4.2
- database
  - <img src="https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">


## Installation
1. Clone the repo
```
git clone https://github.com/github_username/repo_name.git
```
2. Install pip packages
```
pip install -r requirements.txt
```
3. check settings.py
```
SECRET_KEY = "enter SECRET_KEY"
DEBUG = env("DEBUG")
```

## Architecture
- erd


- project architecture



## How to use

### accounts
  
### articles
<details>
    <summary>comment create</summary>
    <div markdown="1">

   - endpoint : api/v1/articles/&#60;int:pk>/comment/
   - method : POST
   - input in header
     - Required: No need
   - input in body
     - Required: content

   </div>
  </details>
<details>
    <summary>comment list</summary>
    <div markdown="1">

   - endpoint : api/v1/articles/&#60;int:pk>/comment/
   - method : GET
   - input in header
     - Required: access_token
   - input in body
     - Required: No need

   </div>
  </details>

  <details>
    <summary>comment edit</summary>
    <div markdown="1">

   - endpoint : api/v1/articles/comment/&#60;int:comment_pk>/
   - method : PUT
   - input in header
     - Required: access_token
   - input in body
     - Required: changed content

   </div>
  </details>
    <details>
    <summary>comment delete</summary>
    <div markdown="1">

   - endpoint : api/v1/articles/comment/&#60;int:comment_pk>/
   - method : DELETE
   - input in header
     - Required: access_token
   - input in body
     - Required: No need

   </div>
  </details>