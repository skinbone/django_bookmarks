function bookmark_edit() {
  var item = $(this).parent();
  var url = item.find(".title").attr("href");
  item.load(
    "/save/?ajax&url=" + encodeURIComponent(url),
    null,
    function () {
      $("#save-form").submit(bookmark_save);
    }
  );
  console.log('load an edit')
    //TODO: using jquery to debug firefox为何出现重复的请求, chrome下似乎没有
  return false;
}

function bookmark_save() {
  var item = $(this).parent();
  var data = {
    url: item.find("#id_url").val(),
    title: item.find("#id_title").val(),
    tags: item.find("#id_tags").val()
  };
  $.post("/save/?ajax", data, function (result) {
    if (result != "failure") {
      item.before($("li", result).get(0));
      item.remove();
      $("ul.bookmarks .edit").click(bookmark_edit);
    }
    else {
      alert("Failed to validate bookmark before saving.");
    }
  });
  return false;
}

$(document).ready(function () {
    $("li .edit").click(bookmark_edit);
});