define(['jquery', 'core', 'mustache', 'twitter:data'], function($, core, mustache, data){
    init = function(){
        setInterval(twitter.controller.getFeed, 60000);
    };
    
    twitter = {
        controller : {
            getFeed : function(feedname){
                feed = core.ajax(data.url, data.getData, twitter.view.updateFeed);
                twitter.view.updateFeed(feed);
            }
        },
        
        view : {
            updateFeed : function(feed){
                // console.log(feed);
            }
        }
    };
    
    $(function(){
        init();
    });
    
    return twitter;
});