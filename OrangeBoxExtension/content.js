function getStars(rating, total_ratings) {
    return "<div class='news-detective'><div class='star-ratings'><div class='fill-ratings' style='width: "+rating+"%;'><span>★★★★★</span></div><div class='empty-ratings'><span>★★★★★</span></div></div><span class='ratings-count'>"+total_ratings+"</span></div>";
}

function callAttentionToX(jNode) {
    var uCW = jNode.closest("[role='article']");
//    var uCW = jNode.closest("div._q7o");
//       uCW.css("border", "2px solid red");
    var button = document.createElement("a");
//    button.innerHTML = "🔍";
    button.style.fontWeight = "600"
//    button.style.fontSize = "17px";
//    button.style.color = "white";
    //       button.setAttribute('href', '#me');
//    button.style.border = "10px solid white";
    button.style.padding = "10px";
    button.style.margins = "10px";
//    button.style.backgroundColor = "#ffdf99";
    button.style.color = "rgba(255,255,255,0.101)";
    button.style.display = "block";
    button.style.height = 35;
//    button.textShadow = "white 0px 0px 0px";


//TODO: make button change color based on publication rating

    try {

// gets image that starts with "https://external"

        var image = $(uCW).find('[src^="https://external"]').attr("src");
        console.log(image);

        console.log("here comes the test code");
        var cat = $("image").closest('a').href;
        console.log("cat", cat)


// gets URL that starts with "https://l.facebook"
        var firsturl = $(uCW).find('[href^="https://l.facebook"]').attr("href");
        console.log("here comes the first fb url")
        console.log(firsturl);

        if(typeof image !== "undefined"){
            if (firsturl.includes("addthis")){
                console.log("addthisspotted");
                var url = $(uCW).find('[href^="https://l.facebook"]').eq(1).attr("href");
                }
            else{
                var url = firsturl;
                }
                console.log("url", url)
        }
//        var turl = $(uCW).find('[href^="https://t.co"]').attr("href");
//        console.log("here comes the twitter url")
//        console.log(turl);

// gets title
//
        if ($((uCW).find('.mbs')).length)
            {var title = $(uCW).find('.mbs').text();}
        else
            {var title = $(uCW).find('[style*="display: -webkit-box; -webkit-box-orient: vertical;"]').text();}
        console.log(title);

//works for new facebook
//        var title = $(uCW).find('[style*="display: -webkit-box; -webkit-box-orient: vertical;"]').text();
//works for old facebook
//        var title = $(uCW).find('.mbs').text();
//also works for old facebook
//        var title = $(uCW).find('[href^="https://l.facebook"]:has(".accessible_elem")').attr("aria-label");

// sending url to background script
//        chrome.runtime.sendMessage({ "articleUrl": articleUrl }, function (response) {
//            console.log("sending url");
//            console.log(response);
//        });



//getting rating



//adding button
        var image_div = $(uCW).find('[src^="https://external"]');
//        var likes = $(uCW).find('[src^="data"]');
        var likes = $(uCW).find('[aria-label="Send this to friends or post it on your timeline."]');
        var more = $(uCW).find('[aria-label="More"]')[0];
        console.log("more coming")
        console.log(more)
        var oldmore = $(uCW).find('[data-tooltip-content="Show more information about this link"]')[0];
//        var oldimage = $(uCW).find('[class="scaledImageFitWidth"]')[0];
//        var clearfix = $(uCW).find('[class="clearfix"]');
//            clearfix.css("border", "2px solid red");
        var dnh = $(uCW).find('[class="_1dnh"]');

        var stringcheese = String(image);
        console.log(stringcheese);
        window.bar2 = stringcheese;

// finding the old fb div
        var _qo = $(uCW).find('._q7o');
        console.log("found it", _qo);
//        _qo.css("border", "2px solid blue");
        var qimage = $(_qo).find('[src^="https://external"]');
        console.log("there's an image here", qimage);

        if (bar2.startsWith("https://external")
        ) {



//            // send URL to background script so it can get the publication score
//            chrome.runtime.sendMessage({ "type": "articleUrl", "url": url });
//            // recieving pubscore from background
//            chrome.runtime.onMessage.addListener((message) => {
//                console.log('sent from background', message.score);
//            });

            chrome.runtime.sendMessage({ "type": "articleUrl", "url": url }, function (response) {
                console.log("here's the response for sending the URL");
                console.log(response);
                var article_total = response[2];
                var article_rating = response[3];
                var rating = response[1];
                //            rating = .4
                var total = response[0];
                    if (total > 1){
                        if (rating >= 70){
                         button.style.backgroundColor = "#39ac73";
                         button.innerHTML = "PScore: " + getStars(rating, total) + "<div>AScore: " + getStars(article_rating, article_total) + "</div>";
                         button.style.color = "white";
                         }
                        if (rating < 70 && rating > 30){
                        button.style.backgroundColor = "gold";
                        button.innerHTML = "PScore: " + getStars(rating, total) + "<div>AScore: " + getStars(article_rating, article_total) + "</div>";
                        button.style.color = "black";
                        }
                        if (rating <= 30){
                        button.style.backgroundColor = "red";
                        button.innerHTML = "PScore: " + getStars(rating, total) + "<div>AScore: " + getStars(article_rating, article_total) + "</div>";
                        button.style.color = "white";
                        }
                    }
                    else {button.style.backgroundColor = "#3366ff";
                          button.innerHTML = "🔍 Investigate Me!";
                          button.style.color = "white";

                    }
            });



            if (qimage.length){
//                button.style.border = "10px solid white";
                button.style.fontSize = "14px";
//                button.style.margins = "10px";
//                oldimage.after(button);}
//                qimage.after(button);}
                dnh.prepend(button);}
//                  clearfix.after(button);}
//                _qo.after(button);}
            else {
                button.style.border = "3px solid white";
                button.style.fontSize = "17px";
                more.before(button);
            //             if it appears in a article box in new facebook
            }

        }
    } catch(error) {
        console.log("Error occurred when adding button.", error)
    }

    button.addEventListener("click", function () {
        if (stringcheese.startsWith("https"));
        console.log("content 1");
        if (bar2.startsWith("https"));
        chrome.runtime.sendMessage({ "type": "articleData", "title": title, "image_url": image, "url": url, "snippet": "test" }
//        , function (response) {
//            console.log("here's the response for sending articleData");
//            console.log(response);
//        }
        );
    });



}

waitForKeyElements("[role='article']", callAttentionToX);
