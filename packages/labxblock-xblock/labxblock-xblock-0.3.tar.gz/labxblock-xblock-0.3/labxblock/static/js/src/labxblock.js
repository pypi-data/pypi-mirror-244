function LabXBlock(runtime, element) {

    const  usageId =element.getAttribute('data-usage-id')
    const notify = $("#lab-notification", element) 

   
    $.ajax({
        type: "GET",
        url: runtime.handlerUrl(element, 'lab'),
        success: function(data) {
               if (data.block_id == usageId){
                const labElement = $(element).find('#lab');
                if (data.type === 'text'){
                    if ( !data.result_student){
                        const btnLabText = $(element).find('#btn-lab-text');
                        const btnSubmit = $(element).find('#btn-lab-submit')
                        btnLabText.removeClass('none')
                        
                        $('#btn-lab-text', element).click(function (event){
                            btnSubmit.removeClass('none')
                            let newDiv = `
                            <div id='editor'></div>`
                            labElement.append(newDiv);
                             ClassicEditor
                            .create( element.querySelector( '#editor' ) ).then(editor =>{
                                btnLabText.addClass('none')
                                btnSubmit.click(function (event){
                                    const editorData = editor.getData();
                                    const formData = new FormData();
                                    formData.append("text", editorData);
                                    formData.append('type', 'lab');
                                    $.ajax({
                                        type: "POST",
                                        url: runtime.handlerUrl(element, 'lab_text'),
                                        contentType: false,
                                        processData: false,
                                        data: formData,
                                        success: (data)=>{
                                            viewResultText(data)
                                        }
                                    });
                                }).catch( error => {
                                            console.error( error );
                             } );
                            })})
                    }else {
                        viewResultText(data)
                       

                        
                    }
        
                }else if (data.type == 'file'){
                    // console.log('data', data)
                    if (data.url.length == 0){
                        const inputHtml = ` 
                        <div class='notify-upload'>
                            <span>Tải file Zip lên</span>
                            <span> Nén (các) tệp dự án của bạn thành mọt tệp zip duy nhất trên máy tính của bạn, giới hạn 500 MB (không nén) </span>
                        </div>
                        <div>
                        <input type="file" name="file" id="file" class="inputfile"  />      
                        <label for="file">Chọn file</label>
                        </div>
                            <div id='file-info'></div>
                        `;
                        labElement.append(inputHtml);
                        $(element).on('change', '.inputfile', function() {
                            const selectedFile = this.files[0];
                            const fileInfoContainer = $('#file-info');
                            if (selectedFile) {
                                fileInfoContainer.html(`
                                   <div class='info-file-content'>
                                    <span><i class="fa fa-file-text" aria-hidden="true"></i> ${selectedFile.name}</span>
                                    <span><i class="fa fa-times" aria-hidden="true"></i></span>
                                   </div>
                                `);
                                $('.inputfile').css('display', 'none');
                                $('label[for="file"]').css('display', 'none');
                                $(element).find('#btn-lab-submit').removeClass('none')
                                $(element).find('.lab-btn').css('text-align' , 'start')

                                $('.fa-times' , element).click(function (){
                                    $('#file')[0].value = '';
                                    $('.info-file-content', element).remove()
    
                                    $('.inputfile').css('display', 'inline-block');
                                    $('label[for="file"]').css('display', 'inline-block');
                                    $(element).find('#btn-lab-submit').addClass('none')
                                })
                                $(element).find('#btn-lab-submit').click(function (){
                                    const selectedFile = $('#file')[0].files[0];
                                    if (selectedFile) {
                                        const formData = new FormData();
                                        formData.append("file", selectedFile);
                                        formData.append('type', 'lab');
                                        $.ajax({
                                            type: "POST",
                                            url: runtime.handlerUrl(element, 'upload'),
                                            contentType: false,
                                            processData: false,
                                            data: formData,
                                            success: (data)=>{
                                                console.log(data)
                                                viewUpload(data)
                                            }
                                        });
                                       
                                    } else {
                                        console.log('No file selected');
                                    }
                                })
    
                            } else {
                                fileInfoContainer.html('<p>Không có file được chọn.</p>');
    
                            }
                        });
                
                    }else {
                        viewUpload(data)
                    }


                }
             

               }   
        }
    });



    function viewDateSuccess(date){
        let dateObject = new Date(date);
        let year = dateObject.getFullYear();
        let month = dateObject.getMonth() + 1; 
        let day = dateObject.getDate();
        let formattedDate = day + '/' + month + '/' + year;
        let text = `Ngày nộp : ${formattedDate}`
        $('.lab-date-success', element).html(text)
    }

    function viewResultText(data){
        viewDateSuccess(data.date)
       const text = `
            <div>
                <div class='student-lab'>
                    <div class='student-lab-title'>
                        <span>Nội dung bài lab</span>
                        <span  id='student-lab-edit'>Edit</span>
                    </div>
                    <div  class='student-lab-content'>
                        <span id='content-student-lab'> ${data.result_student}</span>
                    </div>
                </div>
                <div class='result-lab'>
                    <span class='result-lab-title'>Đáp án tham khảo</span>
                    <div class='result-container'> 
                    <span> Xem đáp án tham khảo bài Lab</span>
                    <details class="detail-lab-result">
                        <summary class='result-summary'>
                            <span>Đáp án tham khảo</span>
                            <span style='color:black'><i class="fa fa-chevron-right" aria-hidden="true"></i></span>
                        </summary>
                        <div >
                            <span style='padding-bottom:10px; padding-top:5px'>${data.result}</span>
                        </div>
                    </details>
                        
                    </div>
                </div>
            </div>
        `
        $(".lab-content", element).html(text);
        $('#lab-notification').removeClass('none');
        $(element).find('.detail-lab-result').on('toggle', function() {
            var $iconSpan = $(element).find('.fa-chevron-right');
            if ($(this).prop('open')) {
                $iconSpan.hide(); 
            } else {
                $iconSpan.show(); 
            }
        });

        $("#student-lab-edit" , element).click(function(){
            // $("#content-student-lab" , element).addClass('none')
            const labElement = $(element).find('.student-lab-content');
            let newDiv = `
            <div id='lab-edit'>
                <div id='editor'>
                    <span>${data.result_student}</span>
                    <div>
                        <span id='lab-huy'>Huy</span>
                        <span>chinh sua</span>
                    </div>
                </div>
                
            </div>
            `
            labElement.append(newDiv);
             ClassicEditor
            .create( element.querySelector( '#editor' ) ).then(editor =>{
                $('#lab-huy', element).click(function(){
                    // $("#content-student-lab" , element).removeClass('none')
                    editor.destroy().then(() => {
                        // $('#lab-edit').parent().remove();
                    }).catch(error => {
                        console.error('Lỗi khi hủy trình soạn thảo:', error);
                    });
                })
            })
        })
    }

    function viewUpload (data){
        viewDateSuccess(data.date)
        $('.inputfile').css('display', 'none');
        $('label[for="file"]').css('display', 'none');
        $('.notify-upload').css('display', 'none');
        const text = `
        <div>
            <div class='student-lab'>
                <div >
                    <a class='student-file'  href=${data.url} target='_blank' > 
                        <span>Tải xuống bài đã nộp </span>
                    </a>
                </div>
            </div>
            <div class='result-lab'>
                <span class='result-lab-title'>Đáp án tham khảo</span>
                <div class='result-container'> 
                <span> Xem đáp án tham khảo bài Lab</span>
                <details class="detail-lab-result">
                    <summary class='result-summary'>
                        <span>Đáp án tham khảo</span>
                        <span style='color:black'><i class="fa fa-chevron-right" aria-hidden="true"></i></span>
                    </summary>
                    <div >
                        <span style='padding-bottom:10px; padding-top:5px'>${data.result}</span>
                    </div>
                </details>
                    
                </div>
            </div>
        </div>
    `
    $(".lab-content", element).html(text);
    $('#lab-notification').removeClass('none');
    }



}