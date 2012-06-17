(function($)
{   
    $.fn.maxChars = function(max_chars, target)
    {
        return this.each(function()
        {
            var $target = null;
            
            if(target === undefined || target === false)
            {
                var _target = $("#" + $(this).attr('id') + "_counter");
                if(_target.length > 0) $target = _target;
            }
            else if(target === true)
            {
                $target = 
                $('<div style="position:absolute;bottom:2px;right:15px;color:#BABABA;"></div>');
                
                $(this)
                .wrap('<div style="position:relative;display:inline-block;"></div>')
                .parent().append($target);
            }
            else $target = target;
            
            var mc = new MaxChars($(this), $target, max_chars);
            
            mc.count();
            
            $(this).keyup(function(){ mc.count(); });
        });
    };  
    
    function MaxChars($this, $target, max)
    {
        this.content = $this;
        this.target = $target;
        this.max = max;
        this.current = null;
        this.left = null;

        return this;
    }
    
    MaxChars.prototype =
    {
        count: function()
        {
            this.current = this.content.val().length;
            this.left = this.max - this.current;
                
            if(this.target && this.target.length > 0) 
                this.target.html(this.left < 0 ? 0 : this.left);
            
            if(this.current > this.max) 
                this.content.val(this.content.val().substring(0, this.max));
        }
    }
})(jQuery);