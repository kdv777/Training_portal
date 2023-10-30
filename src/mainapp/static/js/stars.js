function update_rating(user_id, post_id){
    rate_sum = 0;
    $("#rating").children("label").each(function(){
        rate_sum += Number(getComputedStyle(this, ':before').getPropertyValue("opacity"));
    });
    $.ajax({
        url: "{% url 'mainapp:rating-create' %}",
        type: "POST",
        data: {
            user_id: user_id,
            post_id: post_id,
            value: rate_sum,
        }
    })
}
function get_rating(user_id, post_id){
    rate_value = 0;
    $.ajax({
        url: "{% url 'mainapp:rating-list' %}",
        type: "GET",
        data: {
            post_id: post_id,
        },
        success: function (data) {
            rate_value = data[0].value;
        },
    });
    $("#rating").children("input").each(function(){
        if (rate_value == this.id){
            $(this).attr("checked", true);
        }
    });
}