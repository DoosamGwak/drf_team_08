# articles

<details>
    <summary><b>article_list</b></summary>
    <div markdown="1">

   - endpoint : api/v1/articles/
   - method : GET
   - response
     - title,content(max length=50),
       reporter,created_at,updated_at,image,
       hits,hate(count),comment(count)

   </div>
  </details>

  <details>
    <summary><b>article_create</b></summary>
    <div markdown="1">

   - endpoint : api/v1/articles/
   - method : POST
   - request header
     - Authorization,Content-type
   - request
     - title,content,created_at,
        updated_at,image
       
   </div>
  </details>

<details>
    <summary><b>article_detail</b></summary>
    <div markdown="1">

   - endpoint : api/v1/articles/&#60;int:pk>/
   - method : GET
   - response
     - title,content,reporter,created_at,
       updated_at,image,hits,hate(count),
       comment(count)
       
   </div>
  </details>

<details>
    <summary><b>article_update</b></summary>
    <div markdown="1">

   - endpoint : api/v1/articles/&#60;int:pk>/
   - method : PUT
   - request header
     - Authorization,Content-type
   - request
     - title,content,updated_at,image
       
   </div>
  </details>

<details>
    <summary><b>article_delete</b></summary>
    <div markdown="1">

   - endpoint : api/v1/articles/&#60;int:pk>/
   - method : DELETE
   - request header
     - Authorization
   
       
   </div>
  </details>


