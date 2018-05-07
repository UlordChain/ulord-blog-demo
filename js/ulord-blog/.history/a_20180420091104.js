function getUserId() {
    return new Promise(function(reslove) {
        http.get(url, function(results) {
            resolve(results.id)
        })
    })
}

get