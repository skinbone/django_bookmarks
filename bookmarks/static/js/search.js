function search_submit() {
  var query = $("#id_query").val();
  $("#search-results").load(
    "/search/?ajax&query=" + encodeURIComponent(query)
  );
  return false;
  //return false to tell the browser not to submit the
  //form after calling our handler.
}

$(document).ready(function () {
  $("#search-form").submit(search_submit);
});
