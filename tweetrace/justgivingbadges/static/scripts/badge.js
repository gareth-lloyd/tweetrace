define(['jquery'],function($){
    init = function(){
        $('#badge').click(function(e){
            e.preventDefault;
            badge.toggleForm();
        });
        
        $('#just-give').submit(function(e){
            e.preventDefault();
            badge.submit();
        });
    };
    
    badge = {
        toggleForm : function(){
            $('#just-giving').fadeToggle();
        },
        submit : function(){
            
            alert('submit your moneys');
        }
    };
    
    $(function(){
        init();
    });
    
    return badge;
});