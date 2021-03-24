<body>
<h1>NFT-CLI</h1>
<p>Command-line interface for visualizing NFTs</p>
<br/>
<h3>Requirements</h3>
<ul>
<li><b>Python 3.8:</b> click here to see setup tutorial</li>
<li><b>Mainnet URL:</b> If you don't already have an Http Provider, <a href="https://blog.infura.io/getting-started-with-infura-28e41844cc89/">create an Infura project</a></li>
</ul>
<br/>
<h3>Setup</h3>
<ol>
<li>
<li><p>Install python requirements</p></li>
<code>pip install -r requirements.txt</code>
<code>python config.py #copy/paste your Infura project's mainnet https endpoint when prompted for mainnet_url</code>
<br/>
<h3>How to Use</h3> 
<code>python show.py *contract name* *template filename* *list of token ids (separated by comma) or "all"*</code>
<br/>
<h3>Examples</h3> 
<code>python show.py cryptopunks sales 4152,4153</code>
<hr>
<div style="background-color: white;">
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
</div>
<hr>
</body>