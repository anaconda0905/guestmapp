$(function () {
  
    
    $("#fileupload").fileupload({
      dataType: 'json',
      sequentialUploads: true,

      start: function (e) {
        $("#modal-progress").modal("show");
      },

      stop: function (e) {
        $("#modal-progress").modal("hide");
      },

      progressall: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        var strProgress = progress + "%";
        $(".progress-bar").css({"width": strProgress});
        $(".progress-bar").text(strProgress);
      },

      done: function (e, data) {
        if (data.result.is_valid) {
          $("#modal_form_blueprint input[name='rawImageUrl']").val(data.result.url);
          var filename = data.result.name.replace(/^.*[\\\/]/, '')
          
          $('#modal_form_blueprint #upload_filename').text(filename);
          $("#modal_form_blueprint input[name='airbnb']").attr("disabled","disabled");
          $("#modal_form_blueprint input[name='google_drive']").attr("disabled","disabled");
        }
      }
  });

  $("#detailfileupload").fileupload({
      dataType: 'json',
      sequentialUploads: true,

      start: function (e) {
        $("#modal-progress").modal("show");
      },

      stop: function (e) {
        $("#modal-progress").modal("hide");
      },

      progressall: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        var strProgress = progress + "%";
        $(".progress-bar").css({"width": strProgress});
        $(".progress-bar").text(strProgress);
      },

      done: function (e, data) {
        if (data.result.is_valid) {
          $("#modal_form_photos_add input[name='rawImageUrl']").val(data.result.url);
          var filename = data.result.name.replace(/^.*[\\\/]/, '')
          $('#modal_form_photos_add #upload_detailfilename').text(filename);
          $("#modal_form_photos_add input[name='airbnb']").attr("disabled","disabled");
          $("#modal_form_photos_add input[name='google_drive']").attr("disabled","disabled");
        }
      }
  });
});
