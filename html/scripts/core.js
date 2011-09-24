define(['jquery'], function($){
    function init(){
        
    }
    
    core = {
        ajax : function(url, params, callback){
            $.get(
                url,
                params,
                core.ajaxSuccess
            );
        },
        
        ajaxSuccess : function(data, textStatus){
            if(textStatus !== 'ok'){
                console.log(textStatus);
            } else if(!calllback){
                return data;
            } else {
                callback(data);
            }
        }
    }
    
    $(function(){
        init();
    });
    
    return core;
});