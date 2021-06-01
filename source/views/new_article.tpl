% rebase('base.tpl', new_footer=True)

% if err_msg:
<div class="alert alert-danger" role="alert">
  {{err_msg}}
</div>
% end

<form method="POST" action="/new">
<div class="row">
    <div class="col">
        <div class="mb-3">
            <label for="title" class="form-label">Article title</label>
            <input type="text" class="form-control" id="title" name="title" placeholder="Enter title">
        </div>
        <div class="mb-3">
            <label for="tags" class="form-label">Article tags</label>
            % if defined('tag_list'):
            %       tag_str = ', '.join(tag_list)
            % else: tag_str = ''
            % end
            <input value="{{tag_str}}" type="text" class="form-control" id="tag_list" name="tag_list" placeholder="Enter list of tags">
        </div>
    </div>
    <div class="col">
    </div>
</div>
<div class="row">
    <div class="col">
        <div class="mb-3">
            <label for="body" class="form-label">Article body</label>
            <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" id="togglePreview" onclick="onTogglePreview(this)">
                <label class="form-check-label" for="togglePreview">toggle preview</label>
            </div>
        </div>
    </div>
    <div class="col">
    </div>
</div>
<div class="row">
    <div class="col">
        <textarea class="form-control" id="body" name="body" rows="32">{{body}}</textarea>
    </div>
    <div class="col d-none" id="previewpane">
        <div class="col" id="preview">
        </div>
    </div>
</div>
<div class="row">
    <div class="mb-3">
        <button type="submit" class="btn btn-primary">
            Save
        </button>
        <a href="/" class="btn btn-secondary">Cancel</a>
    </div>
</div>
</form>