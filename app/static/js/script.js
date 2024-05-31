function setCountCart(item_id, is_buy) {
    var count = prompt("Введите количество", "1");

    if (count == null || count == "") {
        alert("Ошибка ввода");
    } else {
        var item_id = item_id
        var count = count
        var url = '/add_cart?item_id=' + encodeURIComponent(item_id) + '&count=' + encodeURIComponent(count) +
        '&is_buy=' + encodeURIComponent(is_buy);

        window.location.href = url;
    }
}