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
</div>
