const URLSafeBase64 = {
    encode: function (str) {
        str = Base64.encode(str);
        return str.replace(/\+/g, '-').replace(/\//g, '_');
    },
    decode: function (str) {
        str = Base64.decode(str);
        // str = (str + '===').slice(0, str.length + (str.length % 4));
        return str.replace(/-/g, '+').replace(/_/g, '/');
    }
};