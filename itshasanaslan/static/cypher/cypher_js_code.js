         
            var obj;
            var _key;
            var txtText;
            const csrftoken = getCookie('csrftoken');
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            function __download(filename, text) {
                var element = document.createElement('a');
                element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
                element.setAttribute('download', filename);
              
                element.style.display = 'none';
                document.body.appendChild(element);
              
                element.click();
              
                document.body.removeChild(element);
              }
            
            function download(){
                if (txtText.value.length == 0 || document.querySelector("#txt_area_key").value.length == 0){
                    alertBox("Key or text is null", "red", 6000);
                    return;
                }

                var dataToDownload = {
                    "key" : document.querySelector("#txt_area_key").value,
                    "text" :document.querySelector("#txt_area_text").value,
                    "website": "http://www.itshasanaslan.com/cypher"
                }
                __download("encrypted_text.json", JSON.stringify(dataToDownload, null, 4));
            }

            async function getTokenKey(url = 'http://www.itshasanaslan.com/cypher/generate_key/', 
            data = {"csrfmiddlewaretoken": csrftoken}) {
     
        const response = await fetch(url, {
            method: 'POST',
            mode: 'cors', 
            cache: 'no-cache', 
            credentials: 'same-origin',
            headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
      
            },
            redirect: 'follow', 
            referrerPolicy: 'no-referrer', 
            body: JSON.stringify(data)
        });
        return response.json(); 
        }.catch(alert(1));

            async function encrypt(data){
                if (txtText.value.length == 0){
                    alertBox("Write something to encrypt!", "red", 6000);
                    return;
                }
                var url = 'http://www.itshasanaslan.com/cypher/encrypt_message/';
                const response = await fetch(url, {
                method: 'POST', 
                mode: 'cors', 
                cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                credentials: 'same-origin', // include, *same-origin, omit
                headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
                // 'Content-Type': 'application/x-www-form-urlencoded',
                },
                redirect: 'follow', // manual, *follow, error
                referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
                body: JSON.stringify(data) // body data type must match "Content-Type" header
                }).catch(error => {
                    alertBox("Server Error...", "red", 6000);

                });
              
                return response.json();
            }
            
            async function decrypt(data){
                if (txtText.value.length == 0){
                    alertBox("Write something to decrypt", "red", 6000);
                    return;
                }
                var url = 'http://www.itshasanaslan.com/cypher/decrypt_message/';
                const response = await fetch(url, {
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                mode: 'cors', // no-cors, *cors, same-origin
                cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                credentials: 'same-origin', // include, *same-origin, omit
                headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
                // 'Content-Type': 'application/x-www-form-urlencoded',
                },
                redirect: 'follow', // manual, *follow, error
                referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
                body: JSON.stringify(data) // body data type must match "Content-Type" header
                });
                return response.json();
            }

            async function updateKey(){
                var txtArea = document.querySelector("#txt_area_key")
                obj = await getTokenKey().then((data) => {_key = data.cypherKey});
                txtArea.value = _key;

        }
            window.addEventListener('DOMContentLoaded', (event) => {
                        txtText = document.querySelector("#txt_area_text");
                        var btn = document.querySelector("#btn_generate_key");
                        btn.type = "button";
                        btn.onclick = function(){
                            updateKey();
                            alertBox("Generated new key!", "green", 6000);
                        }
                        var btnEnc = document.querySelector("#btn_encrypt");
                        var btnDec = document.querySelector("#btn_decrypt");

                        btnEnc.onclick = function(){
                            var dataToSend = {
                                "key" : document.querySelector("#txt_area_key").value,
                                "text" :document.querySelector("#txt_area_text").value,
                                "csrfmiddlewaretoken" : csrftoken
                            }
                            encrypt(dataToSend).then((data)  => {
                                document.querySelector("#txt_area_text").value = data.encryptedText;
                                //encrypted
                               alertBox("Encrypted your text. Save the key to decrypt later.", "green", 6000);

                            });
                        }


                        btnDec.onclick = function(){
                            var dataToSend = {
                                "key" : document.querySelector("#txt_area_key").value,
                                "text" :document.querySelector("#txt_area_text").value
                            }
                            decrypt(dataToSend).then((data)  => {
                                document.querySelector("#txt_area_text").value = data.decryptedText;
                                alertBox("Decrypted your text.", "green", 6000);

                            });
                        }
                        var btn_save = document.querySelector("#btn_download");
                        btn_save.onclick = function(){
                            download();
                        }
                        updateKey();     
                        
                        ////////////////////
                        window.addEventListener('load', function() {
                            var upload = document.getElementById('fileInput');
                            
                            // Make sure the DOM element exists
                            if (upload) 
                            {
                              upload.addEventListener('change', function() {
                                // Make sure a file was selected
                                if (upload.files.length > 0) 
                                {
                                  var reader = new FileReader(); // File reader to read the file 
                                  
                                  // This event listener will happen when the reader has read the file
                                  reader.addEventListener('load', function() {
                                    var result = JSON.parse(reader.result); // Parse the result into an object 
                                    
                                 
                                    if (!result.key || !result.text){
                                        alertBox("File error!", "red", 6000);
                                        return;
                                    }

                                    
                                    //console.log(result.key);
                                    //console.log(result.text);
                                    //console.log(result.website);
                                    txtText.value = result.text;
                                    document.querySelector("#txt_area_key").value = result.key;
                                    alertBox("Success!", "green", 3000);

                                  });
                                  
                                  reader.readAsText(upload.files[0]); // Read the uploaded file
                                }
                              });
                            }
                          });
                          /////////
            });

        alertBox("Generated new key!", "green", 3000);
        function alertBox(message, color, timeout){
                var s =document.querySelector(".alert");
                s.style.backgroundColor = color;
                s.style.visibility = "visible";
                s.innerText = message;
                setTimeout(function(){ s.style.visibility = "hidden"; }, timeout);
            };


     