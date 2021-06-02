% rebase('base.tpl', new_footer=False)
<div class="row">
  <div class="col">
  <h1>{{title}}</h1>
  <div>
    % for tag in tag_list:
    <span class="badge bg-info">{{tag}}</span>
    % end
  </div>
  <hr>
  {{!body}}
  </div>
  <div class="col-3">
  <h3>Related articles</h3>
  <hr>
  % if related_list:
  % for article in related_list:
    <div>
      <h6><a href="/view/{{article.id}}">{{article.title}}</a></h6>
      <span>
        % tag_list = sorted([tag.name for tag in article.tags])
        % for tag in tag_list:
        <small class="badge bg-info">{{tag}}</small>
        % end
      </span>
      <hr>
    </div>
  % end
  % else:
    Nothing appropriate found.
  % end
  </div>
</div>
