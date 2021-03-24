# NFT-CLI

Command-line interface for visualizing NFTs

## Requirements
Python 3.6 <=
Http Provider (e.g. Infura)

## Setup 
        pip install -r requirements.txt
        python config.py

## How to use
        python show.py <contract name> <template filename> <list of token ids (separated by comma) or "all">

## Examples 
        python show.py cryptopunks sales 4152,4153,4154,4155

        ```html
<body>
<center><h4>NFT Sales</h4></center>
<div class="nft-container">
<center><figure><img src="https://lh3.googleusercontent.com/zRiOmqtsV1xBlKB5QT7_yS82BnCECxhlxeyOYT342gEMRIwrqhdRGMY2vvQ_v8A11edjThkEI9n5vd5dVTNpvuoFIzrmI4wGF-8kzs8" width="100" height="100"><figcaption><a href="https://opensea.io/assets/0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb/4152">#4152</a></figcaption></figure></center><br><br>
<center><table border="2" class="dataframe Table">
  <thead>
    <tr style="text-align: left;">
      <th>Txn</th>
      <th>Date</th>
      <th>Ether</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://etherscan.io/tx/0xfea952369a5f95748f48d4f7550d1ed7797c9a902233b8f2a62900ea8f4b9d0f">0xfea952369a5f95748f...</a></td>
      <td><a href="https://etherscan.io/block/10130160">05/24/20</a></td>
      <td>1.30</td>
    </tr>
    <tr>
      <td><a href="https://etherscan.io/tx/0xfd93fc996365ad9ab48373e5c8f69cb8685fe66b13e9ec1139e54c26084654ce">0xfd93fc996365ad9ab4...</a></td>
      <td><a href="https://etherscan.io/block/11501736">12/22/20</a></td>
      <td>4.25</td>
    </tr>
    <tr>
      <td><a href="https://etherscan.io/tx/0x7667f015d1160840a5516268d9c125cab8638e9f0c0f37730408b6637bae6dba">0x7667f015d1160840a5...</a></td>
      <td><a href="https://etherscan.io/block/11897863">02/20/21</a></td>
      <td>16.48</td>
    </tr>
    <tr>
      <td><a href="https://etherscan.io/tx/0x48e87a58ba1714dbdcc09d2ca1aab85fb30bae650fe2383c470f86d440c36e41">0x48e87a58ba1714dbdc...</a></td>
      <td><a href="https://etherscan.io/block/11963496">03/02/21</a></td>
      <td>0.00</td>
    </tr>
  </tbody>
</table></center>
</div>
<hr>



<div class="nft-container">
<center><figure><img src="https://lh3.googleusercontent.com/sSovmKeih9KFQvg9IZbIDt8KQBnZSRk7rFnhDT091ry6pW8S6A13b42K5pmod4hgF9iwTlvcVpM7CsNxszBoq_oabXxP3KDZV5LhcA" width="100" height="100"><figcaption><a href="https://opensea.io/assets/0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb/4153">#4153</a></figcaption></figure></center><br><br>
<center><table border="2" class="dataframe Table">
  <thead>
    <tr style="text-align: left;">
      <th>Txn</th>
      <th>Date</th>
      <th>Ether</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://etherscan.io/tx/0x1c7cc12827f12addf92b09de32f28d2c9a93b4945a24b9fdd0883d8a210b1acf">0x1c7cc12827f12addf9...</a></td>
      <td><a href="https://etherscan.io/block/11878943">02/17/21</a></td>
      <td>23.0</td>
    </tr>
  </tbody>
</table></center>
</div>
<hr>



<div class="nft-container">
<center><figure><img src="https://lh3.googleusercontent.com/vr7gOgtRBnS3j2RdnycfpSPp-OUk2BQamwfxyaBGucqpWWVCItwIrKU12H88Go1O0xMiAKnDJT4Ym4impj6neFNr82fe68w5UGQ1pQ" width="100" height="100"><figcaption><a href="https://opensea.io/assets/0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb/4154">#4154</a></figcaption></figure></center><br><br>
<center><table border="2" class="dataframe Table">
  <thead>
    <tr style="text-align: left;">
      <th>Txn</th>
      <th>Date</th>
      <th>Ether</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://etherscan.io/tx/0x51520a117fdf886c3088b25d228cdf78ff1490891b62710ea4d1b7ba9adcd623">0x51520a117fdf886c30...</a></td>
      <td><a href="https://etherscan.io/block/4100831">07/31/17</a></td>
      <td>0.45</td>
    </tr>
  </tbody>
</table></center>
</div>
<hr>



<div class="nft-container">
<center><figure><img src="https://lh3.googleusercontent.com/4H79IvUWlXHN0qhOi-Q7fZWvE9tgkG98OTFkCdF4p8cD58W1Lfk3AXDfZtXIHkdQXaxuKQ1f1465LMawdJ0kue8" width="100" height="100"><figcaption><a href="https://opensea.io/assets/0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb/4155">#4155</a></figcaption></figure></center><br><br>
<center><table border="2" class="dataframe Table">
  <thead>
    <tr style="text-align: left;">
      <th>Txn</th>
      <th>Date</th>
      <th>Ether</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://etherscan.io/tx/0x01dad54e3ae63c4bb6f9f09f2e8011f4ddc44214846000a6a898139cbfc1bf22">0x01dad54e3ae63c4bb6...</a></td>
      <td><a href="https://etherscan.io/block/10713219">08/22/20</a></td>
      <td>0.85</td>
    </tr>
  </tbody>
</table></center>
</div>
<hr>
</body>
        ```