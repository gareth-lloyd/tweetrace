define(['jquery', 'core', 'mustache', 'twitter:data'], function($, core, mustache, data){
    init = function(){
        console.log(data);
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
                
            }
        }
    };
    
    $(function(){
        init();
    });
    
    return twitter;
});