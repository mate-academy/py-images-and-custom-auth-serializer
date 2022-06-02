# Images and custom auth token serializer

- Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before start
- Download [ModHeader](https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en)

### In this task you will work with images and add auth token serializer

1. Add ImageField `image` to the `Movie` model.
   - Upload images should be only available with `/upload-image/` endpoint.
Image field should not be available on POST `api/cinema/movies/`.
   - Image url should be shown on:
     - Movie list and detail pages
     - Movie session detail page
2. Replace username field with email field in User model.
3. Write custom AuthTokenSerializer, so you can obtain token with
email and password

     
