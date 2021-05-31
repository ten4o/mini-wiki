<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">

    <title>Mini Wiki</title>
  </head>
  <body>
    <div class="container">
        <div class="row">
            <div class="col-1 d-flex position-relative">
                <h2>Mini Wiki</h2>
                <a href="/" class="stretched-link"></a>
            </div>
            <div class="col align-items-center d-flex">
                <form method="GET" action="/search">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="search1">Search</span>
                        <input type="text" name="title" class="form-control" placeholder="search text in title" aria-label="title" aria-describedby="search1"
                            data-bs-custom-class="bg-info" data-bs-toggle="tooltip" data-bs-placement="bottom" title="search text in title"
                        >
                        <span class="input-group-text">/</span>
                        <input type="text" name="body" class="form-control" placeholder="search text in body" aria-label="body" aria-describedby="search1"
                            data-bs-custom-class="bg-info" data-bs-toggle="tooltip" data-bs-placement="bottom" title="search text in body"
                        >
                        <button type="submit" class="btn btn-primary">
                            <svg aria-hidden="true" class="s-input-icon s-input-icon__search svg-icon iconSearch" width="18" height="18" viewBox="0 0 18 18"><path d="M18 16.5l-5.14-5.18h-.35a7 7 0 10-1.19 1.19v.35L16.5 18l1.5-1.5zM12 7A5 5 0 112 7a5 5 0 0110 0z"></path></svg>
                        </button>
                    </div>
                </form>
            </div>
        </div>
        <div class="row"><hr></div>
        {{!base}}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-gtEjrD/SeCtmISkJkNUaaKMoLD0//ElJ19smozuHV6z3Iehds+3Ulb9Bn9Plx0x4" crossorigin="anonymous"></script>

    % if defined('new_footer'):
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="/static/js/new.js"></script>
    % end
  </body>
</html>