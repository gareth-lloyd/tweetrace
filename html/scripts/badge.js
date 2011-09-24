define(['jquery'],function($){
    /**
     * Attach events
     */
    init = function(){
        $('#badge').click(function(e){
            e.preventDefault;
            badge.toggleForm();
        });
    };
    
    /**
     * All badge actions
     */
    badge = {
        toggleForm : function(){
            $('#just-giving').fadeToggle();
        }
    };
    
    $(function(){
        init();
    });
    
    return badge;
});