jQuery_3_6_0(document).ready(function () {
    jQuery_3_6_0(".js-keep-params").click(function () {
        const urlParams = new URLSearchParams(window.location.search);
        const aUrlParams = new URLSearchParams(jQuery_3_6_0(this).attr("href"));

        for (const [key, value] of aUrlParams) {
            urlParams.set(key, value);
        }

        window.location.search = urlParams;
        return false;
    });
});
