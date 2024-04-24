# memo

## axios

基本的な使い方は以下の通りです。

```js
import axios from "axios";

axios({
    method: "GET",
    url: img_requet_url
}).then(response => {
    console.log(response.data);
}).then(error => {
    console.log(error);
});
```
