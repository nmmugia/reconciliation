
$("#unmatchedReportBTN").on("click", function() {
  if ($("#unmatchedReport").hasClass("d-none")) {
    $("#unmatchedReport").removeClass("d-none");
  } else {
    $("#unmatchedReport").addClass("d-none");
  }
})