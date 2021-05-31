% rebase('base.tpl', new_footer=False)

% for article in article_list:
  <div class="card">
    <div class="card-body">
      <a href="/view/{{article.id}}"><b>"{{article.title}}"</b></a>
    </div>
  </div>
% end
