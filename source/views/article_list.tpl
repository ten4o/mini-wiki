% rebase('base.tpl', new_footer=False)

% for article in article_list:
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">
        <a href="/view/{{article.id}}" class="text-decoration-none">
          <b>{{article.title}}</b>
        </a>
      </h5>
      <h6 class="card-subtitle mb-2 text-muted">
        % tag_list = sorted([tag.name for tag in article.tags])
        % for tag in tag_list:
        <span class="badge bg-info">{{tag}}</span>
        % end
      </h6>
    </div>
  </div>
% end
