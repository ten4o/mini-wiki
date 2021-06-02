## Wiki Application

### How to use

from the root directory run:
```
docker-compose up
```

The web application will be accessable on http://localhost:8081

### Features

1. As a user I want to be able to create wiki pages with a title and content in Markdown format
2. As a user I want to be able to add tags to a wiki page so that users can more easily find related pages
3. As a user I want to be able to view all wiki pages tagged with any given tag(s)
4. As a user I want to be able to easily go to pages that are related to the one I'm currently viewing
5. As a user I want to be able to search for a given keyword in all wiki pages. I want to be able to search in the page title, the page content or both.

### TODO/Areas of improvment

- pagination - when the number of articles becomes too large
- use tsquery for text search in secure way
- cliens side and server side markdown compilers are different - that might lead to poorly formated HTML
- more strict rules for tag names