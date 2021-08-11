let url = "https://news-detective.herokuapp.com";
//let url = "https://0.0.0.0:5000";

// when installed, opens factcheckclass
//chrome.runtime.onInstalled.addListener(function() {
//      console.log("The color is green.");
//      window.open(`${url}/factcheckclass`, "MsgWindow", "width=800,height=800");
//      console.log("background 1");
//      // receives test info?
//    fetch(`${url}/factcheckclass`)
////    console.log("background 2. responce:")
////    console.log(response)
//    .then(function (response) {
//        return response.text();
//    })
//
//});



chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.type == "articleUrl") {
        console.log("background heard articleUrl")
        console.log(request);
        var articleUrl = request;
        $.ajax({
        type: 'POST',
        url: `${url}/buttoncolor`,
        data: articleUrl,
        success(data){
            console.log("incoming data");
            console.log(data);
            sendResponse(data);
            console.log("sent data");
            },
        });
        return true;
    }
    else if (request.type == "articleData") {
        console.log("background heard articleData")
        console.log(request);
        var articleData = request
        $.ajax({
            type: 'POST',
            url: `${url}/bootstrap`,
            data: articleData,
            success: function myFunction(data) {
            integer = data;
            var myInput = integer
            var websitelink = `${url}/results/` + myInput;
//            window.open(websitelink, 'MsgWindow', location=yes, "width=400,height=800");
            window.open(websitelink, "MsgWindow", "location=yes,width=600,height=800");
            console.log("background seven");
            }
         })
    }
    else if (request.type == "domainCheck") {
        var articleUrl = request;
        console.log(articleUrl);
        $.ajax({
            type: 'POST',
            url: `${url}/domain_check`,
            data: articleUrl,
            success(data){
            console.log("incoming data");
            console.log(data);
            sendResponse(data);
            console.log("sent data");
            },
        });
        return true;
    }
});




//    sendResponse({ message: "Background has received that message 🔥" });
//});




