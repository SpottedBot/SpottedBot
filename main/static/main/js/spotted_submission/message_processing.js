function parse_text() {
    // Takes the message input and parses it into a list of dicts containing the search results
    var results = new Set();
    var words = $("#id_message").val().replace(/['!"#$%&\\'()\*+,\-\.\/:;<=>?@\[\\\]\^_`{|}~']/g,"").replace(/\s{2,}/g," ").replace(/(?:\r\n|\r|\n)/g, ' ').split(" ");
    for (word in words) {
        var result = manual_search(words[word]);
        if (result.length > 0) {
            if (words.length > word) {
                var proximo = parseInt(word) + 1;
                new_result = manual_search(words[word] + " " + words[proximo]);
                if (new_result.length > 0) {
                    var value = {};
                    value[words[word] + " " + words[proximo]] = new_result;
                    results.add(value);
                    continue;
                }
            }
            var value = {};
            value[words[word]] = result;
            results.add(value);
        }
    }
    return results;
};

function process_message() {
    // returns a name if it was found within the message. Null otherwise
    var resp = parse_text();
    function compare(a, b) {
        function get_length(val) {
            for (key in val)
                return val[key];
        }
        if (get_length(a) < get_length(b))
            return -1;
        if (get_length(a) > get_length(b))
            return 1;
        return 0;
    }
    var sorted_users = [...resp].sort(compare);
    for (user in sorted_users) {
        for (p in sorted_users[user]) {
            name = p;
            break;
        }
        if (name.length > 4) {
            return name;
        }
    }
    return null;
}
