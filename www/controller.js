$(document).ready(function () {

// Expose function for Python -> JS
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {  
        $(".siri-message").text(message);      // update text
        $(".siri-message").attr("hidden", false); // make sure it's visible
        console.log("DisplayMessage called:", message); // debug
    }

    eel.expose(ShowHood);
    function ShowHood() {
        console.log("ShowHood called - returning to main screen");
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
        $(".siri-message").attr("hidden", true); 
    }
    eel.expose(senderText)
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        }

    eel.expose(receiverText)
    function receiverText(message) {

        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
    }

     

});

