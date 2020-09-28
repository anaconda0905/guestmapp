$(document).ready(function(){

    $(".upload-btn").on("click", function(event){
        $("#modal_form_blueprint input[name='rawImageUrl']").val('');
        $("input[type='text']").val('');
        $("#modal_form_blueprint").modal('show');
        // console.log($(this).parent().parent().find('.oderId').val());
        $("#modal_form_blueprint input[name='orderid']").val($(this).parent().parent().find('.oderId').val());
        // $("#modal_form_photos_list").modal('show');
        $('#modal_form_blueprint #upload_filename').text('');
        $("#modal_form_blueprint input[name='airbnb']").removeAttr("disabled");
        $("#modal_form_blueprint input[name='airbnb']").text('');
        $("#modal_form_blueprint input[name='google_drive']").removeAttr("disabled");
        $("#modal_form_blueprint input[name='google_drive']").text('');
    });

    $("#blueprint-upload-btn").on("click", function(event){
        event.preventDefault();

        var rawImageUrl = $("#modal_form_blueprint input[name='rawImageUrl']").val();
        var orderid = $("#modal_form_blueprint input[name='orderid']").val();
        var airbnb = $("#modal_form_blueprint input[name='airbnb']").val();
        var google_drive = $("#modal_form_blueprint input[name='google_drive']").val();

        $.ajax({
            url: '/uploadscan/',
            method: 'POST',
            data: {
                rawImageUrl: rawImageUrl,
                orderid: orderid,
                airbnb: airbnb,
                google_drive:google_drive,
                csrfmiddlewaretoken:$('#modal_form_blueprint input[name=csrfmiddlewaretoken]').val(),
            },

            success:function(response){
                if(response.success == true){
                    $('#modal_form_blueprint').modal('hide');
                    $('#modal_form_blueprint_submitted').modal('show');
                }
            }
        });
    });

    // uploading detail after being saved scanTitle
    $('#productTitleBtn').on("click", function(){
        var orderid = $("#modal_form_blueprint input[name='orderid']").val();
        var productTitle = $('#modal_form_blueprint_submitted #productTitle').val();
        $('#modal_form_upload_photos .proj-scan-img').attr("src", "");
        if(productTitle){
            $.ajax({
                url: '/uploadtitle/',
                method: 'POST',
                data: {
                    orderid: orderid,
                    productTitle: productTitle,
                    csrfmiddlewaretoken:$('#modal_form_blueprint_submitted input[name=csrfmiddlewaretoken]').val(),
                },
                success:function(response){
                    if(response.success == true){
                        var scanTitle = response.scan.title;
                        $("#modal_form_blueprint_submitted").modal("hide");
                        switch (response.type) {
                            case 2:
                            case 3:
                                $('#modal_form_upload_photos .proj-title').text(response.scan.title);
                                $('#modal_form_upload_photos .proj-scan-img').attr("src", response.scan.scanImageUrl);
                                $("#modal_form_upload_photos input[name='proj-scan-id']").val(response.scan.id);
                                $('#modal_form_upload_photos').modal("show");
                                break;

                            case 1:
                            case 0:
                                $('#modal_form_scan_submitted .proj-title').text(response.scan.title);
                                $('#modal_form_scan_submitted .preview-img').attr("src", "");
                                $('#modal_form_scan_submitted .preview-img').attr("src", response.scan.scanImageUrl);
                                $('#modal_form_scan_submitted').modal('show');
                                setTimeout(() => {
                                    window.location.href = "/guestmapp";
                                }, 3000);
                                break;
                            default:
                                break;
                        }
                        
                    }
                }
            })
        }

    });

    // ajax for get detail list with respect to scan 
    // get : scan_id  ----- put : detail list
    $('#show_photoslist_btn').on('click', function(){
        var scan_id = $("#modal_form_upload_photos input[name='proj-scan-id']").val();
        if(scan_id){
            $.ajax({
                url: '/getDatailbyId/',
                method: 'POST',
                data: {
                    scan_id: scan_id,
                    csrfmiddlewaretoken:$('#modal_form_upload_photos input[name=csrfmiddlewaretoken]').val(),
                },

                success:function(response){
                    if(response.success == true){
                        show_photos_list();
                        console.log(response.details);
                        $("#modal_form_photos_list .photos-wrapper").children().remove();
                        for(var index = 0; index < response.details.length; index++){
                            $("#modal_form_photos_list .photos-wrapper").append('<li class="photo-item col-lg-6 col-md-6 col-sm-6 col-6"><img class="photo" src="'+response.details[index].scanDetailImageUrl+'"><div class="photo-action"><input type="hidden" class="detailId" value="'+response.details[index].id+'"><span class="title">'+response.details[index].title+'</span><img class="btn-remove" src="/static/img/garbage.png"></div></li>');
                        }
                    }
                }
            });
        }
    });

    // upload detail image and description of course title
    // get : scan_id, image url --- response : detial id, success
    $("#uploadDetailBtn").on("click", function(event){
        var rawImageUrl = $("#modal_form_photos_add input[name='rawImageUrl']").val();
        var scanid = $("#modal_form_upload_photos input[name='proj-scan-id']").val();
        var airbnb = $("#modal_form_photos_add input[name='airbnb']").val();
        var google_drive = $("#modal_form_photos_add input[name='google_drive']").val();
        $("#modal_form_photo_description img").attr("src", "");
        $.ajax({
            url: '/uploadscandetail/',
            method: 'POST',
            data: {
                rawImageUrl: rawImageUrl,
                scanid: scanid,
                airbnb: airbnb,
                google_drive:google_drive,
                csrfmiddlewaretoken:$('#modal_form_photos_add input[name=csrfmiddlewaretoken]').val(),
            },

            success:function(response){
                if(response.success == true){
                    $("input[type='file']").val('');
                    $("input[type='text']").val('');
                    $("#modal_form_photo_description img").attr("src", response.scandetail.scanDetailImageUrl);
                    $("#modal_form_photo_description input[name='scanDetailId']").val(response.scandetail.id);
                    $('#modal_form_photo_description').modal('hide');
                    show_form_photo_description();
                }
                else{
                    $('#modal_form_photos_add').modal('hide');
                    $("#modal_form_photos_list").modal('show');
                }

            }
        });
    });

    // upload title to scandetailtable with respect to detail ID
    // get : scanDetailId --- response : success, to modal_form_photos_add
    $("#photoDescBtn").on("click", function(event){

        var scanDetailId = $("#modal_form_photo_description input[name='scanDetailId']").val();
        var productDetailTitle = $("#modal_form_photo_description input[name='productDetailTitle").val();
        if(productDetailTitle){
            $.ajax({
                url: '/uploadDetialTitle/',
                method: 'POST',
                data: {
                    scanDetailId: scanDetailId,
                    productDetailTitle: productDetailTitle,
                    csrfmiddlewaretoken:$('#modal_form_photo_description input[name=csrfmiddlewaretoken]').val(),
                },

                success:function(response){
                    if(response.success == true){
                        $('#modal_form_photo_description').modal('hide');
                        $('#show_photoslist_btn').click();
                    }
                }
            });
        }
    });

    
    // console.log($("#photos-list-form"))
    $("#photos-list-form").on('click', ".btn-remove",function(event){
        event.preventDefault();
        var detailId = $(this).parent().find('.detailId').val();
        var item = $(this).parents('.photo-item');
        item.remove();
        if(detailId){
            $.ajax({
                url: '/removeDetail/',
                method: 'POST',
                data: {
                    detailId: detailId,
                    csrfmiddlewaretoken:$('#photos-list-form input[name=csrfmiddlewaretoken]').val(),
                },

                success:function(response){
                    if(response.success == true){
                        item.remove();
                    }
                }
            });
        }
    });

    // submit order to ready
    $('#ProjectCompletedBtn').on('click', function(){
        var orderid = $("#modal_form_blueprint input[name='orderid']").val();
        
        $.ajax({
            url: '/orderReady/',
            method: 'POST',
            data: {
                orderid: orderid,
                csrfmiddlewaretoken:$('#modal_form_photos_list input[name=csrfmiddlewaretoken]').val(),
            },

            success:function(response){
                console.log(response);
                if(response.success == true){
                    $('#modal_form_photos_list').modal('hide');
                    $('#modal_form_scan_submitted .proj-title').text(response.scan.title);
                    $('#modal_form_scan_submitted .preview-img').attr("src", "");
                    $('#modal_form_scan_submitted .preview-img').attr("src", response.scan.scanImageUrl);
                    $('#modal_form_scan_submitted').modal('show');
                    setTimeout(() => {
                        window.location.href = "/guestmapp";
                    }, 3000);
                }

            }
        });
    });

    // order status changed to confirmed with respect to order id
    $('#orderConfirmed').on("click", function(){
        var orderid = $('#modal_form_project_completed input[name=orderId]').val();
        $.ajax({
            url: '/orderConfirmed/',
            method: 'POST',
            data: {
                orderid: orderid,
                csrfmiddlewaretoken:$('#modal_form_project_completed input[name=csrfmiddlewaretoken]').val(),
            },

            success:function(response){
                if(response.success == true){
                    $('#modal_form_project_completed').modal('hide');
                    setTimeout(() => {
                        window.location.href = "/guestmapp";
                    }, 3000);
                }

            }
        });
    });

    $('.adjustProjBtn').on('click', function(){
        var title = $(this).parent().find(".proj-title").val();
        var orderid = $(this).parent().find(".order-id").val();
        var imgUrl = $(this).parent().parent().find("img").attr("src");
        
        $('#modal_form_project_completed input[name=orderId]').val(orderid);
        $('#modal_form_project_completed .proj-title').text(title);
        $('#modal_form_project_completed .preview-img').attr("src","");
        $('#modal_form_project_completed .preview-img').attr("src",imgUrl);

        showProjectComplete();
    });
    

    var obj = $(".blueprint-drag");
    obj.on('dragenter', function (e) 
    {
        e.stopPropagation();
        e.preventDefault();
        $(this).css('border', '2px solid #0B85A1');
    });
    obj.on('dragover', function (e) 
    {
         e.stopPropagation();
         e.preventDefault();
    });
    obj.on('drop', function (e) 
    {
         $(this).css('border', '2px dotted #0B85A1');
         e.preventDefault();
         var files = e.originalEvent.dataTransfer.files;
         for(var i = 0; i < files.length; i++){
            console.log(files[i]);
         }
         //We need to send dropped files to Server
         //handleFileUpload(files,obj);
    });
    
    $(document).on('dragenter', function (e) 
    {
        e.stopPropagation();
        e.preventDefault();
    });
    
    $(document).on('dragover', function (e) 
    {
      e.stopPropagation();
      e.preventDefault();
      obj.css('border', '2px dotted #0B85A1');
    });

    $(document).on('drop', function (e) 
    {
        e.stopPropagation();
        e.preventDefault();
    });
     
}); 

function show_form_photo_description(){
    $('#modal_form_photos_add').modal('hide');
    $('#modal_form_photo_description').modal('show');
}

function show_blueprint_submitted()
{
    $("#modal_form_blueprint").modal('hide');
    $("#modal_form_blueprint_submitted").modal('show');
}

function show_photos_list()
{
    $("#modal_form_upload_photos").modal('hide');
    $("#modal_form_photos_list").modal('show');
}

function show_upload_photos(){
    $("#modal_form_blueprint_submitted").modal('hide');
    $("#modal_form_upload_photos").modal('show');
}

function show_photos_add()
{
    // reset
    $("#modal_form_photos_add input[name='rawImageUrl']").val('');
    $("#modal_form_photos_add input[name='airbnb']").removeAttr("disabled");
    $("#modal_form_photos_add input[name='airbnb']").text('');
    $("#modal_form_photos_add input[name='google_drive']").removeAttr("disabled");
    $("#modal_form_photos_add input[name='google_drive']").text('');
    $("#detailfileupload").val('');
    $("#modal_form_photos_list").modal('hide');
    $("#modal_form_photos_add").modal('show');
}

function sendFileToServer(formData,status)
{
    var uploadURL ="http://localhost:8000/uploadingScan"; //Upload URL
    var extraData ={}; //Extra Data.
    var jqXHR=$.ajax({
            xhr: function() {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                    xhrobj.upload.addEventListener('progress', function(event) {
                        var percent = 0;
                        var position = event.loaded || event.position;
                        var total = event.total;
                        if (event.lengthComputable) {
                            percent = Math.ceil(position / total * 100);
                        }
                        //Set progress
                        status.setProgress(percent);
                    }, false);
                }
            return xhrobj;
        },
    url: uploadURL,
    type: "POST",
    contentType:false,
    processData: false,
        cache: false,
        data: formData,
        success: function(data){
            status.setProgress(100);
 
            $("#status1").append("File upload Done<br>");         
        }
    }); 
 
    status.setAbort(jqXHR);
}
 
var rowCount=0;
function createStatusbar(obj)
{
     rowCount++;
     var row="odd";
     if(rowCount %2 ==0) row ="even";
     this.statusbar = $("<div class='statusbar "+row+"'></div>");
     this.filename = $("<div class='filename'></div>").appendTo(this.statusbar);
     this.size = $("<div class='filesize'></div>").appendTo(this.statusbar);
     this.progressBar = $("<div class='progressBar'><div></div></div>").appendTo(this.statusbar);
     this.abort = $("<div class='abort'>Abort</div>").appendTo(this.statusbar);
     obj.after(this.statusbar);
 
    this.setFileNameSize = function(name,size)
    {
        var sizeStr="";
        var sizeKB = size/1024;
        if(parseInt(sizeKB) > 1024)
        {
            var sizeMB = sizeKB/1024;
            sizeStr = sizeMB.toFixed(2)+" MB";
        }
        else
        {
            sizeStr = sizeKB.toFixed(2)+" KB";
        }
 
        this.filename.html(name);
        this.size.html(sizeStr);
    }
    this.setProgress = function(progress)
    {       
        var progressBarWidth =progress*this.progressBar.width()/ 100;  
        this.progressBar.find('div').animate({ width: progressBarWidth }, 10).html(progress + "% ");
        if(parseInt(progress) >= 100)
        {
            this.abort.hide();
        }
    }
    this.setAbort = function(jqxhr)
    {
        var sb = this.statusbar;
        this.abort.click(function()
        {
            jqxhr.abort();
            sb.hide();
        });
    }
}

function handleFileUpload(files,obj)
{
   for (var i = 0; i < files.length; i++) 
   {
        var fd = new FormData();
        fd.append('file', files[i]);
 
        var status = new createStatusbar(obj); //Using this we can set progress.
        status.setFileNameSize(files[i].name,files[i].size);
        // sendFileToServer(fd,status);
 
   }
}

function show_photo_description()
{
    $('#modal_form_photo_description').modal('show');
}

function showDetailComplete()
{
    $('#modal_form_scan_submitted').modal('show');
}

function showProjectComplete()
{
    $('#modal_form_photos_list').modal('hide');
    $('#modal_form_project_completed').modal('show');
}