# Images and custom auth token serializer

Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before starting.
- Download [ModHeader](https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en)
- Use the following command to load prepared data from fixture to test and debug your code:
  `python manage.py loaddata cinema_service_db_data.json`.
- After loading data from fixture you can use following superuser (or create another one by yourself):
  - Login: `admin.user`
  - Password: `1qazcde3`
  - email: admin.user@cinema.com

### In this task you will work with images and add auth token serializer

1. Add ImageField `image` to the `Movie` model.
   - Upload images should be only available with `/upload-image/` endpoint.
   - Image format of saving must be next:  `f"{slugify(movie.title)}-{uuid}{ext}"`
   - Image field should not be available on POST `api/cinema/movies/`.
   - Image url should be shown on:
     - Movie: `list` and `detail` pages
     - Movie session: on `list` page with `movie_image` key; on
`detail` page inside `movie` -> `image`.

Movie list example:
```python
GET http://127.0.0.1:8000/api/cinema/movies/

[
    {
        "id": 1,
        ...
        "image": "http://127.0.0.1:8000/media/uploads/movies/liar-93733032-c097-4a38-9b2b-20404e7186e6.jpeg",
        ...
    }
]
```

Movie session list example:
```python
GET http://127.0.0.1:8000/api/cinema/movie_sessions/

[
    {
        "id": 1,
        ...
        "movie_image": "http://127.0.0.1:8000/media/uploads/movies/liar-93733032-c097-4a38-9b2b-20404e7186e6.jpeg",
        ...
    }
]
```
2. Replace username field with email field in User model.
3. Write custom AuthTokenSerializer, so you can obtain token with
email and password

   
### Note: Check your code using this [checklist](checklist.md) before pushing your solution.
