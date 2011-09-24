define(['jquery', 'fundraiser_id:sdi_data'],function($, fundraiserData){
    init = function(){
        $('#badge').click(function(e){
            e.preventDefault;
            badge.toggle_form();
        });
        
        $('#just-give').submit(function(e){
            e.preventDefault();
            badge.submit();
        });
    };
    
    badge = {
        toggle_form : function(){
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