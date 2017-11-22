function showOverlay( id ){
	$('#overlay-shadow').show();
	$('.' + id).show();
	$('.' + id).center();

	$('form :input:visible:enabled:first').focus();
}

function closeOverlay(){
	$('#overlay-shadow').hide();
	$('.login-overlay').hide();
	$('.messages-overlay').hide();
	$('.favorites-overlay').hide();
	$('.projects-overlay').hide();
}

jQuery.fn.center = function () {
    this.css('position','absolute');
    var height = Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) + $(window).scrollTop());
    if ( height < 70 ){
    	height = 70;
    }
    this.css('top', height + 'px');
    this.css('left', Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) + $(window).scrollLeft()) + 'px');
    return this;
}

function switchTab( id ){
	$('.tab, ' + id).css( "color", "#333333" );
	$('.tab, ' + id).css( "border-bottom-color", "rgb(221,221,221)" );

	$('.tab').not(id).css( "color", "#b2b2b2" );
	$('.tab').not(id).css( "border-bottom-color", "rgb(200,200,200)" );

	$('.object-list, ' + id).css( "display", "inline-block" );
	$('.object-list').not(id).hide();
}